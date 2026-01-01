# Carrier Wire Format (TritRPC-Aligned)

This document maps **New Hope’s logical Carrier** onto **TritRPC v1** envelope framing, so we have a canonical, signed, transport-stable byte representation.

## Why TritRPC

TritRPC defines a disciplined envelope that separates:

- routing metadata (**SERVICE + METHOD**)
- optional AUX structures (e.g., **Trace**, signature placeholders, Proof-of-Execution)
- payload encoding lane
- authenticated integrity/confidentiality lane (AEAD), with canonical encoding rules

New Hope needs this because a commons-grade runtime requires stable hashing/signing and trace correlation across hops.

## Mapping: New Hope Carrier → TritRPC Envelope regions

### Envelope routing
- `SERVICE`  := receptor-system service name (or protocol family)
- `METHOD`   := protocol operation (e.g., `Message.Post`, `Claim.Assert`, `Moderation.Apply`)

### AUX structures
- `Trace` carries correlation IDs:
  - `signal.id`           → trace_id (or span correlation root)
  - `signal.parents[*]`   → parent span pointers
  - hop-level span IDs are assigned per membrane crossing

Optional AUX payloads:
- signature bundles (if TritRPC lane uses detached signatures)
- Proof-of-Execution (PoE) receipts for deterministic replay checkpoints

### Payload
The New Hope Carrier fields are encoded as the payload object (codec-dependent), with these invariants:

- `protocol_ref` MUST be present
- `signal` MUST be present
- `payload` MUST validate against the resolved protocol schema
- `provenance` + `policy_context` MUST be present for publishable carriers

### AEAD and canonical bytes
- The envelope’s AAD (associated data) binds routing + AUX layout.
- Any change to envelope or payload must invalidate the AEAD tag.
- Hashing/signing in New Hope MUST be performed over the canonical bytes of the full TritRPC frame (envelope + payload [+ AEAD tag where applicable]).

## Pointers
- TritRPC repository: https://github.com/SocioProphet/tritrpc
- In that repo, look for: envelope framing, AUX Trace, AEAD lane, canonical encoding notes, and the SALAD YAML defining `Trace`.
