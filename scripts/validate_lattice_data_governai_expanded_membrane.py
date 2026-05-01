#!/usr/bin/env python3
"""Validate expanded Lattice Data/GovernAI New Hope membrane fixtures."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "fixtures" / "lattice" / "lattice-data-governai-membrane" / "expanded-membrane-fixture.v0.1.json"

REQUIRED_ASSET_KINDS = {
    "model-zoo-entry",
    "rag-pipeline",
    "training-dataset",
    "research-package",
    "trust-posture-summary",
}
REQUIRED_DECISIONS = {"allow", "require-review", "deny"}
REQUIRED_SEQUENCE = [
    "slash-topic-scope",
    "slash-topics-runtime-alias",
    "newhope-compatibility-membrane",
    "memory-mesh-profile",
    "policy-fabric-decision",
    "semantic-membrane-decision",
]


def fail(message: str) -> int:
    print(f"ERR: {message}", file=sys.stderr)
    return 1


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def require_str(mapping: dict[str, Any], key: str) -> str:
    value = mapping.get(key)
    require(isinstance(value, str) and bool(value), f"{key} must be a non-empty string")
    return value


def require_list(mapping: dict[str, Any], key: str) -> list[Any]:
    value = mapping.get(key)
    require(isinstance(value, list) and value, f"{key} must be a non-empty list")
    return value


def validate_asset(asset: dict[str, Any]) -> str:
    asset_id = require_str(asset, "assetId")
    kind = require_str(asset, "assetKind")
    require(kind in REQUIRED_ASSET_KINDS, f"unexpected assetKind {kind}")
    require(require_str(asset, "topic").startswith("/lattice/"), "topic must be /lattice/*")
    require_str(asset, "policyRef")
    require_str(asset, "evidenceCorrelationId")
    require(require_str(asset, "runtimeRef") == "runtime-asset:prophet-python-ml:0.1.0", "runtimeRef mismatch")
    lineage = require_list(asset, "dataLineageRefs")
    require(
        "urn:srcos:data-product:community_truth_demo" in lineage or kind == "rag-pipeline",
        f"{kind} must preserve DataProduct lineage or retrieval lineage",
    )
    if kind == "rag-pipeline":
        require("urn:srcos:retrieval-corpus:community_truth_demo" in lineage, "rag-pipeline must preserve retrieval corpus lineage")
    require(asset_id, "assetId must be present")
    return kind


def validate_decision(decision: dict[str, Any], asset_refs: set[str]) -> str:
    require_str(decision, "decisionId")
    asset_ref = require_str(decision, "assetRef")
    require(asset_ref in asset_refs, f"decision assetRef {asset_ref} not found in assetInputs")
    result = require_str(decision, "decision")
    require(result in REQUIRED_DECISIONS, f"unexpected decision {result}")
    require(require_str(decision, "topicRef") == "slash-topic://lattice/data-governai", "topicRef mismatch")
    require_str(decision, "policyRef")
    require_list(decision, "evidenceRefs")
    require_list(decision, "egressControls")
    redacted = decision.get("redactedFields")
    require(isinstance(redacted, list), "redactedFields must be list")
    return result


def main() -> int:
    if not FIXTURE.exists():
        return fail(f"missing {FIXTURE}")
    try:
        data = json.loads(FIXTURE.read_text(encoding="utf-8"))
        require(isinstance(data, dict), "fixture root must be object")
        require(data.get("apiVersion") == "newhope.socioprophet.dev/v0", "apiVersion mismatch")
        require(data.get("kind") == "LatticeDataGovernAIExpandedMembraneFixture", "kind mismatch")
        metadata = data.get("metadata")
        require(isinstance(metadata, dict), "metadata must be object")
        require(metadata.get("name") == "lattice-data-governai-expanded-membrane", "metadata.name mismatch")

        refs = data.get("refs")
        require(isinstance(refs, dict), "refs must be object")
        require(require_str(refs, "slashTopicScopeRef") == "slash-topic://lattice/data-governai", "slashTopicScopeRef mismatch")
        require(require_str(refs, "topicPackRef") == "slash-topics://packs/lattice-data-governai@0.1.0", "topicPackRef mismatch")
        require(require_str(refs, "runtimeAliasRef").startswith("slash-topics://runtime/"), "runtimeAliasRef must be Slash Topics runtime alias")
        require(require_str(refs, "compatibilityRef").startswith("newhope://"), "compatibilityRef must be New Hope ref")
        require(require_str(refs, "memoryProfileRef").startswith("memory-mesh://"), "memoryProfileRef must be Memory Mesh ref")
        for key in ["expandedSherlockFixtureRef", "expandedSlashTopicsRef", "policyFixtureRef", "topologyFixtureRef"]:
            require_str(refs, key)

        surface = data.get("surfaceModel")
        require(isinstance(surface, dict), "surfaceModel must be object")
        require(surface.get("publicSurface") == "slash-topics", "publicSurface must be slash-topics")
        require(surface.get("runtimeSubstrate") == "new-hope", "runtimeSubstrate must be new-hope")
        require(surface.get("mustNotReplacePublicSurface") is True, "mustNotReplacePublicSurface must be true")
        require(surface.get("mustNotRedefinePlatformAssetRecord") is True, "mustNotRedefinePlatformAssetRecord must be true")
        require(surface.get("mustNotBypassPolicyFabric") is True, "mustNotBypassPolicyFabric must be true")

        assets = require_list(data, "assetInputs")
        asset_kinds = set()
        asset_refs = set()
        for asset in assets:
            require(isinstance(asset, dict), "assetInputs entries must be objects")
            asset_kinds.add(validate_asset(asset))
            asset_refs.add(asset["assetId"])
        missing_assets = sorted(REQUIRED_ASSET_KINDS - asset_kinds)
        require(not missing_assets, f"missing asset kinds: {missing_assets}")

        decisions = require_list(data, "membraneDecisions")
        decision_results = set()
        for decision in decisions:
            require(isinstance(decision, dict), "membraneDecisions entries must be objects")
            decision_results.add(validate_decision(decision, asset_refs))
        missing_decisions = sorted(REQUIRED_DECISIONS - decision_results)
        require(not missing_decisions, f"missing decision outcomes: {missing_decisions}")

        require(data.get("requiredSequence") == REQUIRED_SEQUENCE, "requiredSequence mismatch")
        safety = data.get("safety")
        require(isinstance(safety, dict), "safety must be object")
        require(safety.get("dryRunOnly") is True, "dryRunOnly must be true")
        require(safety.get("hostMutation") is False, "hostMutation must be false")
        require(safety.get("network") == "none", "network must be none")
        require(safety.get("secrets") == "none", "secrets must be none")
    except Exception as exc:  # noqa: BLE001
        return fail(str(exc))
    print(f"PASS {FIXTURE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
