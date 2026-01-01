# History

## Origins: HOPE as a lineage, not a myth

We went looking for the original **HOPE (Higher Order Programming Environment)** work—both the implementation and the closest thing to a specification. What we found was not a single RFC-style document, but a *distributed spec* spread across:

- Marc Clifton’s blog posts (motivation + conceptual framing)
- the CodeProject article series (architecture published in a spec-like format)
- the HOPE GitHub repository (the executable spec: interfaces, routing logic, examples)

Together, those sources capture HOPE’s core claim: computation should move through a **semantic runtime** as meaning-bearing structures, not as raw values threaded through ad-hoc glue.

## What HOPE contributed (atoms worth preserving)

HOPE’s primitives still map cleanly to modern agentic composition:

- **Semantic Types** — meaning-bearing structures, not just schemas.
- **Carriers** — typed envelopes moving through a routed runtime.
- **Receptors** — composable behaviors (proto-agent modules).
- **Membranes** — boundaries between behaviors (routing in HOPE; enforcement in New Hope).
- **Finite Automata** — workflows as formal state machines (replay + testability).
- **Semantic Database** — storage as a participant receptor, not a separate kingdom.

## Why this becomes New Hope (the missing bones)

HOPE’s atoms are correct, but a 2025+ knowledge commons cannot survive on routing elegance alone. The environment must make these properties **mandatory**:

- **Provenance is mandatory**: content-addressing + signatures as the precondition for attribution, audit, replay, appeals, and federation.
- **Membranes are enforcement points**: minimization/redaction, quotas, capability gating, tenant isolation, and controlled egress.
- **Nondeterminism is explicit**: stochastic components must declare themselves and emit traceable metadata.
- **News + messaging are protocol-native**: threads, claims, citations, stances, lenses, moderation, and appeals are first-class objects.
- **Replay is a conformance requirement**: deterministic components must replay; nondeterministic components must be bounded and explainable.

## TritRPC as the wire lineage we align to

New Hope’s “Carrier” is a logical envelope concept. Where we need canonical bytes for hashing/signing/transport, we align to **TritRPC**’s envelope framing model:

- routing metadata (SERVICE + METHOD)
- optional AUX structures (Trace, signatures placeholders, proofs)
- authenticated encryption lane (AEAD) and canonical encoding discipline

That alignment is documented in `docs/Carrier_Wire_Format_TritRPC.md`, with New Hope’s semantic carrier mapped onto TritRPC’s envelope regions.

## Repository map (what this repo asserts)

- `docs/New_Hope_Spec_v0.2.md` — normative objects and minimum requirements
- `docs/Carrier_Wire_Format.md` — New Hope logical carrier example
- `docs/Carrier_Wire_Format_TritRPC.md` — TritRPC-aligned envelope mapping
- `docs/Protocol_Pack_v0.md` + `docs/spec/Protocol_Pack_v0/*.json` — protocol objects as files
- `docs/Conformance_Tests.md` + `docs/spec/conformance/*.json` — test definitions as files
- `docs/Mapping_HOPE_to_NewHope.md` — lineage-preserving mapping
- `docs/Roadmap.md` — hardening steps (canonicalization RFC, membrane decision model, harness)
