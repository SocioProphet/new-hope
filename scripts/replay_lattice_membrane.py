#!/usr/bin/env python3
"""Replay New Hope membrane checks for Lattice PlatformAssetRecord carriers."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"expected JSON object in {path}")
    return data


def replay(fixture: dict[str, Any]) -> dict[str, Any]:
    if fixture.get("kind") != "CarrierFixture":
        raise ValueError("fixture kind must be CarrierFixture")
    carrier = fixture.get("carrier")
    membrane = fixture.get("membrane")
    if not isinstance(carrier, dict):
        raise ValueError("carrier must be an object")
    if not isinstance(membrane, dict):
        raise ValueError("membrane must be an object")

    required_evidence = membrane.get("requiredEvidence", [])
    claims = carrier.get("claims", [])
    questions = membrane.get("questions", [])
    evidence_complete = isinstance(required_evidence, list) and "PlatformAssetRecord" in required_evidence and "PlatformAssetRecordEnrichment" in required_evidence
    claims_complete = isinstance(claims, list) and len(claims) >= 1
    questions_complete = isinstance(questions, list) and len(questions) >= 1

    status = "candidate-pass" if evidence_complete and claims_complete and questions_complete else "candidate-incomplete"
    return {
        "apiVersion": "newhope.socioprophet.dev/v1",
        "kind": "MembraneReplayReport",
        "carrierEntityId": carrier.get("entityId"),
        "carrierKind": carrier.get("carrierKind"),
        "sourceRecordKind": carrier.get("sourceRecordKind"),
        "status": status,
        "checks": {
            "evidenceComplete": evidence_complete,
            "claimsComplete": claims_complete,
            "questionsComplete": questions_complete
        },
        "requiredEvidence": required_evidence,
        "questions": questions
    }


def emit(report: dict[str, Any], output: Path | None) -> None:
    rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if output is None:
        print(rendered, end="")
        return
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(rendered, encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Replay New Hope membrane checks for a Lattice carrier fixture")
    parser.add_argument("fixture", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    try:
        emit(replay(load_json(args.fixture)), args.output)
        return 0
    except Exception as exc:  # noqa: BLE001
        print(f"replay_lattice_membrane: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
