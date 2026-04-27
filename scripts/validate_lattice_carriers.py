#!/usr/bin/env python3
"""Validate New Hope Lattice carrier fixtures."""

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
    require(doc.get("kind") == "CarrierFixture", "kind mismatch")
    carrier = doc.get("carrier")
    require(isinstance(carrier, dict), "carrier must be an object")
    require(carrier.get("carrierKind") == "PlatformAssetRecordCarrier", "carrierKind mismatch")
    require(carrier.get("sourceRecordKind") == "PlatformAssetRecord", "sourceRecordKind mismatch")
    require(isinstance(carrier.get("claims"), list) and carrier["claims"], "claims must be non-empty")
    membrane = doc.get("membrane")
    require(isinstance(membrane, dict), "membrane must be an object")
    require(isinstance(membrane.get("requiredEvidence"), list) and membrane["requiredEvidence"], "requiredEvidence must be non-empty")


def main(argv: list[str] | None = None) -> int:
    paths = [Path(arg) for arg in (argv if argv is not None else sys.argv[1:])]
    if not paths:
        paths = sorted(Path("fixtures/lattice").glob("*.json"))
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
