# Lattice Studio Workspace New Hope Handoff

New Hope consumes Lattice Studio workspace outputs as semantic carriers for membrane governance.

## Fixture

The initial carrier fixture lives at:

```text
fixtures/lattice-studio/workspace-synthesis-carrier.v0.json
```

It maps a Lattice Studio `WorkspaceSynthesisArtifact` / `PlatformAssetRecordEnrichment` into:

```text
Carrier
Entity
Claim
Citation
Lens
Membrane decision context
```

## Canonical mapping

```text
PlatformAssetRecord.assetId -> Carrier.entityId
PlatformAssetRecord.producerRepo -> Citation.source
PlatformAssetRecord.policyRef -> Claim.policyRef / membrane input
PlatformAssetRecord.evidenceCorrelationId -> Evidence link
PlatformAssetRecord.compatibilitySurfaces -> Lens candidates
PlatformAssetRecordEnrichment.slashTopics -> topic context
```

## Membrane questions

New Hope must be able to decide:

- Is this workspace synthesis discoverable?
- Are all source objects visible under active policy?
- Are source claims properly cited?
- Does the publication receipt preserve output digest and evidence correlation?
- Can the artifact be replayed from the notebook session and runtime asset?

## Doctrine

Workspace synthesis is a semantic carrier, not just a generated office document. It must participate in claim, citation, lens, and membrane governance before broad search or publication exposure.
