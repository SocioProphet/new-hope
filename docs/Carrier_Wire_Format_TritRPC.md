# Carrier Wire Format (TritRPC-aligned)

This document aligns **New Hope**’s Carrier with the **TritRPC v1** envelope model found in `../tritrpc/TritRPC-v1-full/`.

## What TritRPC v1 actually is (per repo)

TritRPC v1 is a **canonical, byte-level envelope** that separates:

- **Routing keys:** `SERVICE` + `METHOD`
- **AUX structures:** optional trace/signature/PoE lanes
- **Payload bytes:** application message bytes (e.g., Avro/JSON-LD/etc.)
- **Integrity lane:** AEAD tag computed over AAD (envelope) + payload

Where this lives in the TritRPC repo:
- Spec overview: `tritrpc/TritRPC-v1-full/README.md`
- Envelope theory: `tritrpc/TritRPC-v1-full/docs/THEORY.md` (see “Envelope model”)
- Reference implementation: `tritrpc/TritRPC-v1-full/reference/tritrpc_v1.py`
- Go envelope builder: `tritrpc/TritRPC-v1-full/go/tritrpcv1/envelope.go`
- Schema-ish definitions (Trace, etc.): `tritrpc/TritRPC-v1-full/spec/salad/tritrpc_salad.yml`

## The alignment rule (non-negotiable)

**TritRPC envelope = transport/authenticated framing.**  
**New Hope Carrier = semantic envelope (protocol_ref, signal, provenance, policy_context, payload).**

In TritRPC terms, the New Hope Carrier is the *payload bytes* (or a payload object encoded to bytes) whose integrity is protected by TritRPC’s AEAD lane.

## Canonical bytes, not “pretty JSON”

TritRPC’s security property depends on canonical encoding:

- Canonical envelope bytes are built from SERVICE + METHOD + AUX + flags + payload length framing
- AEAD tag is computed over **AAD = envelope routing/aux/flags** and the payload
- Any mutation of envelope or payload breaks verification

So: **hash/sign TritRPC canonical bytes** (or at minimum hash/sign the canonical New Hope Carrier bytes inside the TritRPC payload). Prefer signing the whole TritRPC frame bytes when feasible, since it binds routing keys too.

## Envelope: logical model (conceptual)

A TritRPC frame is logically:

- `SERVICE` (routing key)
- `METHOD` (routing key)
- `AUX` (optional)
  - `Trace` (trace_id, span_id, parent_span_id) exists today
  - `Sig` / `PoE` appear as planned/placeholder lanes in docs
- `PAYLOAD` (opaque bytes to TritRPC)
- `AEAD_TAG` (when AEAD enabled)

The concrete byte layout is defined by TritRPC v1’s canonical encoding rules (TLEB3/TritPack243) and the envelope builder/parser code.

## How New Hope Carrier rides inside TritRPC

### Option A (recommended): Carrier bytes as payload

- Payload bytes = canonical serialization of the New Hope Carrier object
- TritRPC `SERVICE/METHOD` identify the receptor interface (routing)
- TritRPC `AUX.Trace` provides hop-level correlation
- New Hope Carrier provides: protocol_ref + provenance + policy_context + semantic signal graph

### Option B: Carrier hash in AUX + carrier bytes as payload

- AUX includes a `carrier_hash` (or `schema_id` / `context_id` depending on profile)
- Payload carries the full carrier bytes
- Useful if routers want to enforce policy based on hashes without parsing full payload

## Minimum membrane enforcement (New Hope requirement)

Regardless of transport, membranes MUST be able to enforce per-carrier:

- data minimization + redaction
- cross-tenant constraints
- signing requirements
- egress controls (especially external calls)
- quotas / rate limits
- allow / deny / quarantine / require-human-signature decisions with audit logging

TritRPC helps by making routing keys + trace data part of the authenticated envelope. New Hope completes it by making semantic provenance + policy_context first-class.

## Replay + trace (two ledgers, different jobs)

- TritRPC `Trace` = hop correlation (runtime causality)
- New Hope `provenance.transforms` + `signal.parents/derived_from` = semantic causality and audit proof

**Both are needed** for real replay: TritRPC proves envelope/payload integrity across transport; New Hope proves semantic lineage and policy context across the knowledge commons.

