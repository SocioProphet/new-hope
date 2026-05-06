# New Hope

New Hope is a Higher-Order Semantic Runtime for agentic commons (news + messaging).

## Docs

- docs/HOPE_Evaluation.md — what HOPE got right and what breaks in 2025+
- docs/New_Hope_Spec_v0.2.md — normative v0.2 spec (carrier, receptor, membrane, runtime)
- docs/Protocol_Pack_v0.md — first-class objects: Message/Thread/Claim/Citation/Entity/Lens/ModerationEvent
- docs/Conformance_Tests.md — replay/provenance/membrane/ranking tests
- docs/Mapping_HOPE_to_NewHope.md — lineage mapping and deltas
- docs/Roadmap.md — canonicalization RFC, membrane decision model, harness

## Personal Intelligence Cell membrane event

The Personal Intelligence Cell membrane event is now represented as a first cell-specific New Hope bridge:

- `schemas/personal-intelligence-cell-membrane-event.schema.json`
- `examples/personal-intelligence-cell/membrane-event.example.json`
- `scripts/validate_personal_intelligence_cell_membrane_event.py`

Validate locally:

```bash
python3 scripts/validate_personal_intelligence_cell_membrane_event.py
```

The event maps `prophet-platform` cell feed publication into New Hope carrier/receptor/membrane semantics:

```text
Cell -> Signal -> FeedItem -> NewHopeMembraneEvent
```

Policy decision mapping:

- `allow` -> `admit`
- `deny` -> `reject`
- `quarantine` -> `quarantine`
- `review_required` / `redact` -> `hold`

## Status

Spec is being reconstructed into repo-native docs in paste-safe chunks.
