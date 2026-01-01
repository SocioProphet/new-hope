# Protocol Pack v0 (News + Messaging)

This file defines the first-class protocol objects New Hope implementations MUST support. These are the native semantics needed for a news+messaging commons: claims, citations, threads, moderation, and transparent ranking.

## Message
Fields:
- `text`, `media[]`, `mentions[]`, `links[]`
- `thread_root`, `reply_to`
- `language`, `client_hints` (optional)
- `visibility`: public | community | limited

## Thread
Fields:
- `root_message`
- `participants[]`
- `forked_from` (for branching narratives)
- `merge_of[]` (for reconciled threads)

## Claim
Fields:
- `claim_text` (atomic)
- `stance`: assert | deny | uncertain
- `scope`: time/place/topic
- `confidence` + `calibration_ref`
- `evidence[]` (citations + extracted support spans)
- `counterclaims[]`

## Citation
Fields:
- `url`
- `retrieved_at`
- `content_hash` (snapshot)
- `excerpt_hash` (quoted fragment)
- `archive_ptr` (local store pointer)
- `source_quality_signals` (optional, transparent)

## Entity
Fields:
- `canonical_name`
- `aliases[]`
- `type` (person/org/place/thing)
- `evidence_edges[]`
- `resolution_proof` (how we matched)

## Lens
A Lens is a reusable filter/ranking pipeline. This is where slashtag mechanics slot in cleanly.

Fields:
- `pipeline[]` operators: filter, boost, demote, join, cluster, timeline
- `inputs`: protocols allowed
- `outputs`: ranking + explanation carrier requirements

## ModerationEvent
Fields:
- `action`: remove | label | limit | ban | quarantine
- `reason_code` + `policy_ref`
- `appeal_state`
- `review_signatures[]` (humans)

---

## Agentic loop (how receptors become “agents” safely)
An “agent” is just a receptor (or receptor bundle) with:
- a planning receptor (FA/workflow)
- tool receptors (search, summarize, entity-resolve)
- a memory/index receptor (hybrid retrieval)
- strict membranes around tool use and egress

Critical safety requirement: tool receptors do not get raw authority — membranes do.
