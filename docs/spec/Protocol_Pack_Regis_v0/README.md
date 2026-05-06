# Protocol Pack Regis v0

This pack defines New Hope carrier envelopes for HolographMe and Regis artifacts.

## Objects

- TwinProjectionFeatureCarrier
- FeatureAssertionCarrier
- EmbeddingCardCarrier
- PromotionDecisionCarrier
- RevocationPropagationCarrier
- NeedAssessmentCarrier
- WantPreferenceCarrier

## Rule

The carrier transports typed semantic payloads. It does not own or canonicalize the human digital twin, the Regis graph, or the GAIA ontology.

## Required carrier sections

Each carrier includes:

- carrier_version
- protocol_ref
- signal
- payload
- provenance
- policy_context

## Required policy behavior

Membranes must be able to allow, deny, quarantine, redact, downgrade fidelity, require additional signatures, block egress, and propagate revocation.
