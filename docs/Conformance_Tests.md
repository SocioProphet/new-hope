# Conformance Tests

A New Hope implementation is conformant only if it can demonstrate:

1) Replay: deterministic receptors replay exactly from the same inputs.
2) Nondeterminism declaration: nondeterministic outputs include input refs + tool/model metadata.
3) Provenance integrity: every publishable carrier is signed and content-addressed.
4) Membrane enforcement: forbidden cross-tenant flows are blocked and logged.
5) Ranking explainability: every lens pipeline can emit an explanation carrier.

Test fixture examples live in: `docs/spec/conformance/`
