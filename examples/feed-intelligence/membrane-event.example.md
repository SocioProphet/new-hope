# Feed Intelligence membrane event example

Status: example-only contract

This example maps normalized Feed Intelligence reader items into New Hope membrane semantics without changing schemas, validators, or runtime behavior.

Canonical reader surface:

```text
SocioProphet/socioprophet/socioprophet-web/client-vue
```

## Purpose

The Feed Intelligence reader may render sources, ticker state, normalized items, and memex side-panel state. New Hope owns the membrane decision for whether a normalized feed item is admitted, held, quarantined, or rejected before downstream memory, graph, or publication behavior can occur.

## Decision meanings

`admit` means the item is eligible for guarded reader display and later governed enrichment.

`hold` means the item requires review before publication, writeback, or graph expansion.

`quarantine` means the item may remain visible as local evidence but cannot propagate.

`reject` means the item fails membrane admission and should only produce audit/receipt state.

## Example event

```yaml
eventId: newhope-feed-intelligence-001
eventType: newhope.feed-intelligence.membrane.evaluated
feedItemRef: item-001
slashTopicRef: /news/global
sourceRef: source-global-news
canonicalUrl: https://socioprophet.news/items/ticker-proof-of-life
decision: admit
reason: source-normalized-and-scope-resolved
evidenceRefs:
  - eventlog://feed.subscribed/001
  - eventlog://item.fetched/001
  - eventlog://item.normalized/001
downstreamEligibility:
  memoryRecall: eligible
  memoryWriteback: review-only
  graphView: eligible
  derivedPublication: policy-required
```

## Boundary rules

- New Hope evaluates membrane admission; it does not fetch feeds.
- SlashTopics supplies governed scope context.
- BearBrowser may supply browser-origin evidence, but capture does not imply admission.
- MemoryMesh cannot write back merely because New Hope admits an item; writeback remains review-only unless later policy allows it.
- MeshRush graph expansion is downstream eligibility, not automatic execution.
- ActivityPub publication requires an explicit derived-publication decision.

## Acceptance posture

This example is acceptable while it remains a membrane contract example. It must not claim live publication, live feed fetching, memory writeback, graph traversal, or federation side effects.
