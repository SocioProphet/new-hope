# Conformance Tests (Non-Negotiable)

A New Hope implementation is “real” only if it passes the tests below. These tests are designed to make replay, provenance, membrane enforcement, and ranking explainability enforceable rather than aspirational.

## 1) Replay test
- Deterministic receptors MUST reproduce exact outputs from the same inputs.
- Replay MUST be supported from any checkpoint in the receptor graph.

## 2) Nondeterminism declaration test
- Receptors that are stochastic MUST declare: `bounded_nondeterministic` or `nondeterministic`.
- Outputs MUST include input references + model/tool metadata sufficient to explain provenance (even if not to reproduce exact bytes).

## 3) Provenance test
- Every published carrier MUST be content-addressed and signed.
- Signature coverage MUST reference the canonical carrier hash.

## 4) Membrane enforcement test
- Forbidden cross-tenant flows MUST be blocked and logged.
- Redactions/quarantines MUST be recorded as first-class events with policy refs.

## 5) Ranking explainability test
- Every lens pipeline MUST be able to emit an Explanation carrier.
- Explanation MUST enumerate the boosts/blocks/filters that produced the ranking.

---

## Implementation notes
- We should define a standard “conformance harness” runner that replays recorded traces and validates expected invariants.
- The harness MUST fail closed: missing provenance or missing membrane decisions are test failures.
