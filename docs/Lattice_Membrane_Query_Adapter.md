# Lattice Membrane Query Adapter Contract

**Lattice identifier:** `newhope-membrane-query`
**Contract version:** `0.1.0`
**Status:** Draft
**Aligned to:** New Hope Spec v0.2, Protocol Pack v0

---

## 1. Purpose

This document defines the **query adapter contract** that allows Lattice's federated
query plane to route and evaluate queries against a New Hope backend without
violating membrane boundaries.

New Hope is modelled as a first-class Lattice backend identified by the string
`newhope-membrane-query`.  The adapter contract governs:

- which concept types may be queried and through which operations
- what policy and provenance metadata MUST accompany every request
- how **dry-run** routing works (route + evidence, no side-effects, no data
  returned at runtime)
- how conformance is validated

---

## 2. Concept-Type Query Matrix

Every operation maps to exactly one New Hope Protocol Pack v0 object.

| Concept | Signal type | Adapter operation |
|---|---|---|
| `Message` | `MessagePosted` | `query.message` |
| `Thread` | `ThreadCreated` | `query.thread` |
| `Claim` | `ClaimAsserted` | `query.claim` |
| `Citation` | `CitationAdded` | `query.citation` |
| `Entity` | `EntityResolved` | `query.entity` |
| `Lens` | `LensApplied` | `query.lens` |
| `ModerationEvent` | `ModerationAction` | `query.moderation_event` |
| `MembraneDecision` | `MembraneDecisionRecorded` | `query.membrane_decision` |

---

## 3. Query Request Shape

Every query issued by Lattice MUST conform to the following structure.

```json
{
  "adapter":        "newhope-membrane-query",
  "adapter_version": "0.1.0",
  "operation":      "<adapter operation from §2>",
  "query_id":       "<uuid-v4 or content-addressed id>",
  "dry_run":        true,
  "filter": {
    "concept":      "<Message|Thread|Claim|Citation|Entity|Lens|ModerationEvent|MembraneDecision>",
    "predicates":   [],
    "limit":        50,
    "cursor":       null
  },
  "policy_context": {
    "tenant":       "commons|org:<id>|team:<id>",
    "community":    "news:<id>|topic:<id>",
    "ruleset_ref":  "hash://blake3/<policy-hash>"
  },
  "provenance": {
    "requester_id":     "did:key:...",
    "requester_kind":   "human|agent|service",
    "request_ts":       "<ISO-8601>",
    "purpose_code":     "search|ranking|audit|moderation|federation",
    "session_ref":      "optional"
  }
}
```

### 3.1 Required fields

| Field | Constraint |
|---|---|
| `adapter` | MUST equal `"newhope-membrane-query"` |
| `operation` | MUST be one of the values in §2 |
| `dry_run` | MUST be present; when `true` no records are returned |
| `filter.concept` | MUST match the concept implied by `operation` |
| `policy_context.tenant` | MUST be present |
| `policy_context.ruleset_ref` | MUST be a content-addressed reference (`hash://`) |
| `provenance.requester_id` | MUST be a DID |
| `provenance.purpose_code` | MUST be one of the enumerated values |

---

## 4. Dry-Run Behavior

When `dry_run: true` the adapter MUST:

1. **Resolve the route** – determine which New Hope receptors would handle the query.
2. **Evaluate membrane eligibility** – run the membrane policy check against
   `policy_context` and `provenance` without touching live data.
3. **Return a `DryRunRoute`** – see §5.
4. **Emit no side-effects** – no reads from live data stores, no writes, no
   downstream signals.
5. **Record the dry-run event** – append a `MembraneDecision` carrier with
   `decision: "dry-run"` to the audit log.

Dry-run results are non-binding but MUST be stable: identical inputs produce
identical route and evidence outputs (deterministic evaluation).

---

## 5. Dry-Run Route Response Shape

```json
{
  "adapter":        "newhope-membrane-query",
  "query_id":       "<mirrors request query_id>",
  "dry_run":        true,
  "route": {
    "eligible":     true,
    "receptors": [
      {
        "receptor_id":    "did:key:...",
        "receptor_kind":  "MessageQueryReceptor|...",
        "membrane_gate":  "did:key:...",
        "policy_match":   true
      }
    ],
    "denial_reasons": []
  },
  "evidence": {
    "policy_ref":     "hash://blake3/<policy-hash>",
    "ruleset_ref":    "hash://blake3/<ruleset-hash>",
    "matching_labels": ["public"],
    "provenance_chain": ["hash://..."]
  },
  "membrane_decision": {
    "decision":     "allow|deny|quarantine|redact|require-signature",
    "rationale":    "Free-text or structured reason.",
    "redacted_fields": [],
    "required_signatures": []
  },
  "ts": "<ISO-8601>"
}
```

### 5.1 Route eligibility rules

| `eligible` | Condition |
|---|---|
| `true` | At least one receptor matches and membrane policy allows |
| `false` | No receptor matches **or** membrane denies / quarantines |

When `eligible: false` the `denial_reasons` array MUST contain at least one
entry explaining which membrane check failed.

---

## 6. Policy and Provenance Requirements

### 6.1 Policy

- Every query MUST reference a `ruleset_ref` that is content-addressed
  (`hash://blake3/…`).
- The adapter MUST NOT evaluate queries whose `ruleset_ref` cannot be resolved.
- `policy_context.tenant` and `policy_context.community` constrain which
  receptors are in scope; cross-tenant queries are rejected unless an explicit
  federation agreement exists.

### 6.2 Provenance

- `provenance.requester_id` MUST be a valid DID.
- `provenance.purpose_code` is required to prevent purpose-creep (a query for
  `"ranking"` MUST NOT silently execute `"audit"` reads).
- The adapter appends a `MembraneDecision` carrier to the audit trail for every
  request (dry-run or live), signed by the adapter receptor's DID key.

### 6.3 Data minimisation

The membrane MAY:
- Redact fields listed in `membrane_decision.redacted_fields`.
- Downgrade fidelity (e.g., strip `text`, retain embedding reference only).
- Gate access behind `require-signature` for sensitive concept types
  (`ModerationEvent`, `MembraneDecision`).

---

## 7. Per-Concept Query Semantics

### 7.1 `query.message`
Filter predicates: `thread_root`, `author_did`, `language`, `visibility`,
`ts_range`, `label`.

Membrane gate checks: visibility policy, cross-tenant read, PII labels.

### 7.2 `query.thread`
Filter predicates: `root_message`, `participant_did`, `fork_depth`, `ts_range`.

Membrane gate checks: thread-level visibility, participant membership.

### 7.3 `query.claim`
Filter predicates: `stance`, `scope`, `confidence_min`, `evidence_ref`,
`calibration_ref`.

Membrane gate checks: source community policy, citation completeness.

### 7.4 `query.citation`
Filter predicates: `url_hash`, `content_hash`, `archive_ptr`, `ts_range`.

Membrane gate checks: egress domain allowlist, archive availability.

### 7.5 `query.entity`
Filter predicates: `canonical_name`, `aliases`, `type`, `resolution_proof_ref`.

Membrane gate checks: entity disambiguation policy, cross-tenant identity.

### 7.6 `query.lens`
Filter predicates: `pipeline_id`, `input_ref`, `output_ref`.

Membrane gate checks: lens explainability requirement (every result MUST have
an explanation carrier available).

### 7.7 `query.moderation_event`
Filter predicates: `action`, `reason_code`, `policy_ref`, `appeal_state`,
`ts_range`.

Membrane gate checks: moderator-role required; `require-signature` gate for
appeal-state changes.

### 7.8 `query.membrane_decision`
Filter predicates: `decision`, `query_ref`, `policy_ref`, `ts_range`.

Membrane gate checks: audit-role required; result is always read-only.

---

## 8. Lattice FederatedQueryPlane Integration

Lattice identifies this backend in its `FederatedQueryPlane` config as:

```yaml
backends:
  - id: newhope-membrane-query
    kind: NewHopeAdapter
    contract_ref: "hash://blake3/<contract-hash>"
    dry_run_endpoint: "/newhope/query/dry-run"
    live_endpoint: null          # not activated in this tranche
    policy_context:
      tenant: "commons"
      ruleset_ref: "hash://blake3/<default-ruleset-hash>"
```

`live_endpoint: null` signals that only dry-run routing is active in this
tranche; no runtime execution is performed.

---

## 9. Conformance

A Lattice ↔ New Hope adapter implementation is conformant when it passes all
fixtures defined in:

```
docs/spec/conformance/MembraneQueryConformance_v0.example.json
fixtures/lattice/newhope-membrane-query/
```

Minimum conformance checks (mirrors `docs/Conformance_Tests.md`):

| # | Check | Requirement |
|---|---|---|
| CQ-01 | Dry-run is side-effect-free | Identical inputs → identical `DryRunRoute` |
| CQ-02 | Policy ref is content-addressed | `ruleset_ref` must parse as `hash://` |
| CQ-03 | Provenance requester is a DID | `requester_id` must match `did:` prefix |
| CQ-04 | Cross-tenant denial | Query crossing tenant boundary without federation agreement → `eligible: false` |
| CQ-05 | Audit trail appended | Every request produces a `MembraneDecision` carrier in the audit log |
| CQ-06 | Sensitive concept gate | `query.moderation_event` and `query.membrane_decision` require audit/moderator role |
| CQ-07 | Concept/operation alignment | `filter.concept` must match `operation` or request is rejected |

---

## 10. Out of Scope (This Tranche)

- Live data queries (runtime execution against actual New Hope stores)
- Write / mutation operations
- Cross-system relay authentication key exchange
- Real-time streaming subscriptions
