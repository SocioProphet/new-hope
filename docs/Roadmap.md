# Roadmap (Immediate Hardening)

This roadmap turns the v0.2 spec into an enforcement-grade implementation spine.

## Next immediate hardening (no fluff)

### 1) Canonicalization + hashing + signing rules (RFC-style)
- Specify canonical serialization (canonical JSON vs CBOR, exact key ordering rules)
- Define what is included/excluded from carrier hash coverage
- Define signature envelope: algorithms, rotation, and verification policy

### 2) Membrane decision model (formal outputs + audit fields)
- Standardize decision outputs: allow | deny | quarantine | redact | require_signature | downgrade
- Require mandatory audit fields: policy_ref, reason_code, timestamps, affected fields, reviewers

### 3) Publish Protocol Pack v0 as a versioned registry bundle
- Message/Thread/Claim/Citation/Entity/Lens/ModerationEvent
- Add versioning + compatibility semantics per Protocol

### 4) FA/workflow conformance harness spec
- Representation of automata + checkpoints
- Trace replay runner + invariant checks
- Golden test fixtures for deterministic and nondeterministic receptors

---

## Known risks (keep honest)
- Overselling: keep Ehrhart/zeta-style talk strictly in “risk bounding / disclosure counting” territory when used elsewhere.
- DSL safety: marketer/query DSL must be capability-limited via membranes, not trusted by convention.
- Drift: docs must be source-of-truth with automated sync where duplication exists.
