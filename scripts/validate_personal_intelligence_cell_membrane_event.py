#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas/personal-intelligence-cell-membrane-event.schema.json"
EXAMPLE = ROOT / "examples/personal-intelligence-cell/membrane-event.example.json"

EXPECTED_OUTCOMES = {
    "allow": "admit",
    "deny": "reject",
    "quarantine": "quarantine",
    "review_required": "hold",
    "redact": "hold",
}


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def fail(message: str) -> int:
    print(f"Personal Intelligence Cell membrane event failed validation: {message}")
    return 1


def main() -> int:
    schema = load_json(SCHEMA)
    example = load_json(EXAMPLE)
    if schema.get("title") != "PersonalIntelligenceCellMembraneEvent":
        return fail("schema title mismatch")
    missing = sorted(set(schema.get("required", [])) - set(example))
    if missing:
        return fail(f"example missing required fields: {', '.join(missing)}")
    if example["schemaVersion"] != "new-hope-cell-membrane.v0.1":
        return fail("schemaVersion mismatch")
    policy = example.get("policyDecision", {})
    decision = policy.get("decision")
    if decision not in EXPECTED_OUTCOMES:
        return fail("invalid policy decision")
    if example.get("membraneOutcome") != EXPECTED_OUTCOMES[decision]:
        return fail("membrane outcome does not match policy decision")
    message = example.get("message", {})
    if not message.get("citationRefs"):
        return fail("message citationRefs required")
    lineage = example.get("lineage", {})
    for key in ["cellRef", "sourceRef", "signalRef", "feedItemRef", "evidenceRefs"]:
        if not lineage.get(key):
            return fail(f"lineage.{key} required")
    if message.get("messageRef") != lineage.get("feedItemRef"):
        return fail("messageRef must match lineage.feedItemRef")
    if message.get("citationRefs") != lineage.get("evidenceRefs"):
        return fail("citationRefs must match lineage.evidenceRefs")
    print("Personal Intelligence Cell membrane event validates.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
