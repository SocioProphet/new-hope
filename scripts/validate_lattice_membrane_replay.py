#!/usr/bin/env python3
"""Validate New Hope Lattice membrane replay reports."""

from __future__ import annotations

import json
import sys
from pathlib import Path


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def validate(path: Path) -> None:
    doc = json.loads(path.read_text(encoding="utf-8"))
    require(doc.get("apiVersion") == "newhope.socioprophet.dev/v1", "apiVersion mismatch")
    require(doc.get("kind") == "MembraneReplayReport", "kind mismatch")
    require(doc.get("carrierKind") == "PlatformAssetRecordCarrier", "carrierKind mismatch")
    require(doc.get("sourceRecordKind") == "PlatformAssetRecord", "sourceRecordKind mismatch")
    require(doc.get("status") in {"candidate-pass", "candidate-incomplete"}, "invalid status")
    checks = doc.get("checks")
    require(isinstance(checks, dict), "checks must be an object")
    require(checks.get("evidenceComplete") is True, "evidence must be complete")
    require(checks.get("claimsComplete") is True, "claims must be complete")
    require(checks.get("questionsComplete") is True, "questions must be complete")


def main(argv: list[str] | None = None) -> int:
    paths = [Path(arg) for arg in (argv if argv is not None else sys.argv[1:])]
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
