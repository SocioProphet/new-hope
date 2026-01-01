# Carrier Wire Format (TritRPC-aligned)

This document updates New Hope’s carrier envelope so it can be transported via TritRPC without losing commons-grade requirements: provenance, policy context, replay, and trace.

## Minimum membrane enforcement (mandatory)

Membranes MUST enforce:
- data minimization + redaction
- cross-tenant constraints
- signing requirements
- egress controls (especially for external calls)
- quotas / rate limits
- quarantine / require-human-signature gates

## TritRPC envelope (outer) + New Hope carrier (inner)

**Design rule:** TritRPC is the outer envelope (routing/execution/trace). New Hope Carrier is the inner envelope (semantic protocol + provenance + policy context).

### Canonical composite message shape (wire-level JSON example)

```json
{
  "tritrpc": {
    "version": "1",
    "kind": "call|event|reply",
    "method": "receptor.consume|receptor.emit|policy.eval|index.put|index.query|...",
    "call_id": "hash://blake3/<call-hash>",
    "parent_call_id": "hash://blake3/<parent-call-hash>",
    "ts": "2026-01-01T00:00:00Z",
    "from": { "did": "did:key:...", "kind": "human|agent|service" },
    "to":   { "did": "did:key:...", "kind": "agent|service" },
    "routing": {
      "tenant": "commons|org:<id>|team:<id>",
      "community": "news:<id>|topic:<id>",
      "lane": "control|data|audit",
      "qos": "best_effort|at_least_once|exactly_once",
      "ttl_ms": 30000
    },
    "capabilities": {
      "requested": ["model_call","net","fs","hsm"],
      "granted": ["model_call"],
      "egress_allowlist": ["example.com"],
      "hsm_required": false
    },
    "trace": {
      "trace_id": "hash://blake3/<trace-hash>",
      "span_id": "hash://blake3/<span-hash>",
      "hops": [
        { "node": "did:key:...", "ts": "...", "decision": "allow|deny|quarantine", "policy_ref": "hash://..." }
      ]
    }
  },
  "carrier": {
    "carrier_version": "1",
    "protocol_ref": "hash://blake3/<protocol-hash>",
    "signal": {
      "type": "MessagePosted|ClaimAsserted|CitationAdded|ModerationAction|...",
      "ts": "2025-12-26T22:14:00Z",
      "id": "hash://blake3/<signal-hash>",
      "parents": ["hash://..."],
      "thread_root": "hash://...",
      "derived_from": ["hash://..."]
    },
    "payload": { "...": "..." },
    "provenance": {
      "emitter": { "kind": "human|agent|service", "id": "did:key:..." },
      "signatures": [
        { "alg": "ed25519", "sig": "base64...", "covers": "hash://blake3/<canonical-carrier-hash>" }
      ],
      "inputs": ["hash://..."],
      "transforms": [
        { "receptor_id": "did:key:...", "ts": "...", "notes": "optional" }
      ]
    },
    "policy_context": {
      "tenant": "commons|org:<id>|team:<id>",
      "community": "news:<id>|topic:<id>",
      "ruleset_ref": "hash://blake3/<policy-hash>",
      "labels": ["public","needs_review","contains_pii:false"]
    }
  }
}
```

## Normative rules

1) **Canonicalization + hashing**
- The carrier MUST be canonicalized (stable key order + stable serialization) before hashing/signing.
- TritRPC MAY sign its outer envelope, but MUST preserve carrier signatures and carrier hash references.

2) **Traceability**
Each hop MUST be able to log: decision (allow/deny/quarantine), policy_ref, redactions, and capability grants.

3) **Determinism**
Receptors MUST declare determinism class. Nondeterministic work MUST record tool/model IDs, input hashes, and budgets/timeouts.

## Mapping

- tritrpc.routing.tenant/community MUST match carrier.policy_context.tenant/community (or be a strict superset for transport only).
- tritrpc.capabilities are membrane-governed execution authority; MUST NOT be inferred from payload.
- tritrpc.trace is runtime hop ledger; carrier.provenance.transforms is semantic transform chain. Both are required for real replay.
