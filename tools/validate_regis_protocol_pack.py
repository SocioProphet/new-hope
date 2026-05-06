#!/usr/bin/env python3
"""Lightweight validator for the New Hope Regis protocol pack."""

from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "docs" / "spec" / "Protocol_Pack_Regis_v0"
EXAMPLES = PACK / "examples"

EXAMPLE_TO_SCHEMA = {
    "twin-projection-feature-carrier.example.json": "TwinProjectionFeatureCarrier.json",
    "embedding-card-carrier.example.json": "EmbeddingCardCarrier.json",
    "revocation-propagation-carrier.example.json": "RevocationPropagationCarrier.json",
}


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def validate_carrier_shape(example: dict) -> None:
    signal = example["signal"]
    provenance = example["provenance"]
    policy_context = example["policy_context"]
    if not signal.get("derived_from"):
        raise AssertionError("carrier signal must include derived_from lineage")
    if not provenance.get("inputs"):
        raise AssertionError("carrier provenance must include inputs")
    if not policy_context.get("labels"):
        raise AssertionError("carrier policy_context must include labels")


def validate_embedding_no_raw_vector(example: dict) -> None:
    payload = example["payload"]
    if payload.get("raw_vector_inline") is not False:
        raise AssertionError("embedding carrier examples must not inline raw vectors")
    if "vector" in payload:
        raise AssertionError("embedding carrier payload must use vector_ref, not raw vector")


def main() -> int:
    for example_name, schema_name in EXAMPLE_TO_SCHEMA.items():
        schema = load_json(PACK / schema_name)
        example = load_json(EXAMPLES / example_name)
        Draft202012Validator.check_schema(schema)
        Draft202012Validator(schema).validate(example)
        validate_carrier_shape(example)
        if example_name == "embedding-card-carrier.example.json":
            validate_embedding_no_raw_vector(example)
        print(f"validated {example_name} against {schema_name}")
    print("Regis protocol pack validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
