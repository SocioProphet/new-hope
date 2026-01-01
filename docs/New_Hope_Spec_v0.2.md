# New Hope Specification v0.2

## 2.2 Carrier wire format (canonical representation)

We standardize one canonical representation for hashing/signing, regardless of transport:

```json
{
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
    "emitter": {
      "kind": "human|agent|service",
      "id": "did:key:...",
      "device_attestation": "optional"
    },
    "signatures": [
      {
        "alg": "ed25519",
        "sig": "base64...",
        "covers": "hash://blake3/<canonical-carrier-hash>"
      }
    ],
    "inputs": ["hash://..."],
    "transforms": [
      {"receptor_id": "did:key:...", "ts": "...", "notes": "optional"}
    ]
  },
  "policy_context": {
    "tenant": "commons|org:<id>|team:<id>",
    "community": "news:<id>|topic:<id>",
    "ruleset_ref": "hash://blake3/<policy-hash>",
    "labels": ["public", "needs_review", "contains_pii:false"]
  }
}
```

**Key rule:** hash/sign the canonical form (stable key order + stable serialization).

## 2.1 Normative core objects

### Protocol (semantic schema)
A **Protocol** is a versioned schema describing payload structure + semantic meaning + validation rules.

**MUST**
- be content-addressed (hash of canonical form)
- define compatibility rules (backward/forward)
- include safety classifications per field (public/private/sensitive)

### Signal (event)
A **Signal** is an event occurrence with causality and intent.

**MUST**
- be append-only
- include causal pointers: `parents[]`, `thread_root`, `derived_from[]`

### Carrier (typed envelope)
A **Carrier** is the message between receptors.

**MUST include**
- `protocol_ref` (content hash)
- `signal` (event metadata)
- `payload` (validated by protocol)
- `provenance` (signatures + lineage)
- `policy_context` (tenant/community + ruleset refs)

### Receptor (behavior / agent module)
A **Receptor** consumes carriers and emits carriers.

**MUST declare**
- accepted/emitted protocols
- capability needs (network, model calls, filesystem)
- determinism class: `deterministic | bounded_nondeterministic | nondeterministic`
- sandbox profile (required)

### Membrane (policy enforcement)
A **Membrane** is an enforcement point between receptors.

**MUST enforce**
- authn/authz
- quotas/rate limits
- data minimization + redaction
- cross-tenant constraints
- signing requirements
- egress controls (especially for external calls)

### Receptor System (graph runtime)
A **Receptor System** is a graph of receptors connected by membranes.

**MUST**
- produce a trace graph for every carrier hop
- support replay from any checkpoint
- support federation (controlled cross-system relays)

## 2.3 Membrane policy minimum (MUST be expressible)
Membranes must be able to decide on each carrier:
- allow / deny / quarantine
- redact fields
- downgrade fidelity (e.g., remove raw text, keep embeddings only)
- require additional signatures (human review gates)
- rate limit by identity + community + protocol type
- block egress to external networks unless explicitly allowed

Implementation note: we can evaluate policy via an open policy engine (OPA/Rego-style or equivalent). What matters is the minimum expressivity above.
