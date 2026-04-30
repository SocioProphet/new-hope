#!/usr/bin/env python3
"""Validate New Hope Lattice newhope-membrane-query dry-run fixtures.

Checks CQ-01 through CQ-07 structural requirements from
docs/Lattice_Membrane_Query_Adapter.md §9.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ADAPTER = "newhope-membrane-query"
VALID_OPERATIONS = {
    "query.message",
    "query.thread",
    "query.claim",
    "query.citation",
    "query.entity",
    "query.lens",
    "query.moderation_event",
    "query.membrane_decision",
}
OPERATION_TO_CONCEPT = {
    "query.message": "Message",
    "query.thread": "Thread",
    "query.claim": "Claim",
    "query.citation": "Citation",
    "query.entity": "Entity",
    "query.lens": "Lens",
    "query.moderation_event": "ModerationEvent",
    "query.membrane_decision": "MembraneDecision",
}
VALID_PURPOSE_CODES = {"search", "ranking", "audit", "moderation", "federation"}
CONTENT_HASH_PATTERN = re.compile(r"^hash://blake3/[0-9a-f]{64}$")
DID_PATTERN = re.compile(r"^did:[a-z]+:.+")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def validate_request(req: dict, fixture_path: Path) -> None:
    """Validate the request block of a DryRunQueryFixture."""
    require(req.get("adapter") == ADAPTER, f"request.adapter must be '{ADAPTER}'")
    require(req.get("dry_run") is True, "request.dry_run must be true (CQ-01)")

    operation = req.get("operation")
    require(operation in VALID_OPERATIONS, f"request.operation '{operation}' not in allowed set")

    flt = req.get("filter", {})
    concept = flt.get("concept")
    expected_concept = OPERATION_TO_CONCEPT.get(operation)
    require(
        concept == expected_concept,
        f"filter.concept '{concept}' does not match operation '{operation}' "
        f"(expected '{expected_concept}') (CQ-07)",
    )

    policy = req.get("policy_context", {})
    require(bool(policy.get("tenant")), "policy_context.tenant must be present")
    ruleset_ref = policy.get("ruleset_ref", "")
    require(
        bool(CONTENT_HASH_PATTERN.match(ruleset_ref)),
        f"policy_context.ruleset_ref '{ruleset_ref}' must match hash://blake3/<64-hex-chars> (CQ-02)",
    )

    prov = req.get("provenance", {})
    requester_id = prov.get("requester_id", "")
    require(
        bool(DID_PATTERN.match(requester_id)),
        f"provenance.requester_id '{requester_id}' must be a DID (CQ-03)",
    )
    require(
        prov.get("purpose_code") in VALID_PURPOSE_CODES,
        f"provenance.purpose_code '{prov.get('purpose_code')}' not in {VALID_PURPOSE_CODES}",
    )


def validate_expected_route(route: dict) -> None:
    """Validate the expected_route block."""
    eligible = route.get("eligible")
    require(isinstance(eligible, bool), "expected_route.eligible must be a boolean")
    require(isinstance(route.get("receptors"), list), "expected_route.receptors must be a list")
    denial_reasons = route.get("denial_reasons", [])
    if not eligible:
        require(
            isinstance(denial_reasons, list) and len(denial_reasons) > 0,
            "expected_route.denial_reasons must be non-empty when eligible is false (CQ-04/CQ-06)",
        )


def validate_expected_membrane_decision(decision_block: dict) -> None:
    """Validate the expected_membrane_decision block."""
    valid_decisions = {"allow", "deny", "quarantine", "redact", "require-signature", "dry-run"}
    decision = decision_block.get("decision")
    require(decision in valid_decisions, f"membrane_decision.decision '{decision}' not in {valid_decisions}")


def validate(path: Path) -> None:
    doc = json.loads(path.read_text(encoding="utf-8"))
    require(doc.get("kind") == "DryRunQueryFixture", "kind must be 'DryRunQueryFixture'")

    request = doc.get("request")
    require(isinstance(request, dict), "request must be an object")
    validate_request(request, path)

    route = doc.get("expected_route")
    require(isinstance(route, dict), "expected_route must be an object")
    validate_expected_route(route)

    decision = doc.get("expected_membrane_decision")
    require(isinstance(decision, dict), "expected_membrane_decision must be an object")
    validate_expected_membrane_decision(decision)


def main(argv: list[str] | None = None) -> int:
    paths = [Path(arg) for arg in (argv if argv is not None else sys.argv[1:])]
    if not paths:
        paths = sorted(Path("fixtures/lattice/newhope-membrane-query").glob("*.json"))
    failed = False
    for path in paths:
        try:
            validate(path)
            print(f"PASS {path}")
        except Exception as exc:  # noqa: BLE001
            failed = True
            print(f"FAIL {path}: {exc}", file=sys.stderr)
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
