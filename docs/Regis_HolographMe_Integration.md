# Regis / HolographMe Integration

## Purpose

This document defines how New Hope transports HolographMe and Regis artifacts as signed, provenance-preserving, membrane-governed semantic carriers.

HolographMe owns the self-owned human digital twin and consent-scoped projection runtime. Regis owns governed feature assertions, embedding cards, promotion decisions, and graph-computable projection surfaces. GAIA owns ontology semantics. New Hope owns carrierized semantic movement through receptors and membranes.

## Architecture

HolographMe projection -> Regis feature artifact -> New Hope carrier -> membrane decision -> downstream receptor.

New Hope does not own the twin, graph, or ontology. It moves typed semantic payloads with provenance and policy context.

## Carrier requirements

Every Regis/HolographMe carrier must include:

- carrier_version
- protocol_ref
- signal.type
- signal.id
- signal.parents
- signal.thread_root
- signal.derived_from
- payload
- provenance.emitter
- provenance.inputs
- provenance.transforms
- policy_context.tenant
- policy_context.community
- policy_context.ruleset_ref
- policy_context.labels

## Membrane responsibilities

Membranes must decide whether a carrier is allowed, denied, quarantined, redacted, downgraded, or routed for review.

Required checks:

1. Consent scope compatibility.
2. Purpose compatibility.
3. Recipient and community compatibility.
4. Revocation status.
5. Retention status.
6. Egress permission.
7. High-impact use review.
8. Denied-field leakage protection.
9. Fidelity downgrade when raw details are not allowed.
10. Additional signature or human review requirements.

## Regis protocol pack

The Regis protocol pack lives under `docs/spec/Protocol_Pack_Regis_v0/` and defines carrier envelopes for:

- TwinProjectionFeatureCarrier
- FeatureAssertionCarrier
- EmbeddingCardCarrier
- PromotionDecisionCarrier
- RevocationPropagationCarrier
- NeedAssessmentCarrier
- WantPreferenceCarrier

## Invariant

A carrier can transport a projection-derived feature. A carrier must not transform that feature into identity truth. Downstream use remains bounded by provenance, policy context, consent scope, and membrane decisions.
