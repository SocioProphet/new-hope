# Carrier Wire Format (Canonical Representation)

Membranes MUST enforce:
- data minimization + redaction
- cross-tenant constraints
- signing requirements
- egress controls (especially for external calls)

## Receptor System (graph runtime)
A **Receptor System** is a graph of receptors connected by membranes.

MUST:
- produce a trace graph for every carrier hop
- support replay from any checkpoint
- support federation (controlled cross-system relays)

---

## Carrier wire format (canonical representation)

We standardize one canonical representation for hashing/signing, regardless of transport.

NOTE: full JSON example lives in docs/New_Hope_Spec_v0.2.md §2.2.
