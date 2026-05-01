#!/usr/bin/env python3
"""Validate New Hope runtime-profile membrane fixture."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "fixtures" / "lattice" / "lattice-runtime-profile-membrane" / "membrane-fixture.v0.1.json"
NOTEBOOK = "runtime-asset:prophet-python-ml:0.1.0"
RAY = "runtime-asset:prophet-ray-ml:0.1.0"
BEAM = "runtime-asset:prophet-beam-dataops:0.1.0"
BINDING = "runtime-profile-binding:lattice-data-governai:0.1.0"
REQUIRED_INPUTS = {NOTEBOOK, RAY, BEAM, BINDING}
REQUIRED_DECISIONS = {"allow", "require-review"}
REQUIRED_SEQUENCE = [
    "slash-topic-scope",
    "slash-topics-runtime-alias",
    "runtime-profile-binding",
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
    require(isinstance(value, str) and bool(value), f"{key} must be non-empty string")
    return value


def require_list(mapping: dict[str, Any], key: str) -> list[Any]:
    value = mapping.get(key)
    require(isinstance(value, list) and bool(value), f"{key} must be non-empty list")
    return value


def main() -> int:
    if not FIXTURE.exists():
        return fail(f"missing {FIXTURE}")
    try:
        data = json.loads(FIXTURE.read_text(encoding="utf-8"))
        require(data.get("apiVersion") == "newhope.socioprophet.dev/v0", "apiVersion mismatch")
        require(data.get("kind") == "LatticeRuntimeProfileMembraneFixture", "kind mismatch")
        refs = data.get("refs")
        require(isinstance(refs, dict), "refs must be object")
        for key in ["slashTopicScopeRef", "runtimeProfileTopicPackRef", "compatibilityRef", "sherlockRuntimeFixtureRef", "slashRuntimeTopicRef", "platformRuntimeCatalogRef", "agentplaneRuntimeRefsRef", "topologyRuntimeRef"]:
            require_str(refs, key)
        require(refs["slashTopicScopeRef"] == "slash-topic://lattice/data-governai/runtime-profiles", "slashTopicScopeRef mismatch")
        require(refs["compatibilityRef"].startswith("newhope://"), "compatibilityRef must be newhope ref")

        surface = data.get("surfaceModel")
        require(isinstance(surface, dict), "surfaceModel must be object")
        require(surface.get("publicSurface") == "slash-topics", "publicSurface mismatch")
        require(surface.get("runtimeSubstrate") == "new-hope", "runtimeSubstrate mismatch")
        require(surface.get("mustNotRedefineRuntimeAsset") is True, "mustNotRedefineRuntimeAsset must be true")
        require(surface.get("mustNotBypassPolicyFabric") is True, "mustNotBypassPolicyFabric must be true")

        inputs = require_list(data, "runtimeInputs")
        input_ids = {require_str(item, "assetId") for item in inputs if isinstance(item, dict)}
        require(input_ids == REQUIRED_INPUTS, f"runtimeInputs mismatch: {sorted(input_ids)}")
        for item in inputs:
            require(require_str(item, "topic").startswith("/lattice/runtime/"), "runtime topic mismatch")
            require_str(item, "policyRef")
            require_str(item, "evidenceCorrelationId")
            require_list(item, "roles")

        decisions = require_list(data, "membraneDecisions")
        decision_results = set()
        decision_assets = set()
        for decision in decisions:
            asset_ref = require_str(decision, "assetRef")
            require(asset_ref in REQUIRED_INPUTS, f"decision assetRef {asset_ref} not in runtimeInputs")
            result = require_str(decision, "decision")
            require(result in REQUIRED_DECISIONS, f"unexpected decision {result}")
            decision_results.add(result)
            decision_assets.add(asset_ref)
            require(require_str(decision, "topicRef") == "slash-topic://lattice/data-governai/runtime-profiles", "decision topicRef mismatch")
            require_str(decision, "policyRef")
            require_list(decision, "evidenceRefs")
            require_list(decision, "egressControls")
        require(decision_assets == REQUIRED_INPUTS, "not every runtime input has a decision")
        require(decision_results == REQUIRED_DECISIONS, f"decision result coverage mismatch: {sorted(decision_results)}")

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
