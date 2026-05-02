#!/usr/bin/env python3
"""Validate New Hope replay evidence membrane fixture."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "fixtures" / "lattice" / "lattice-replay-evidence-membrane" / "membrane-fixture.v0.1.json"
BUNDLE = "urn:srcos:evidence-bundle:lattice-governed-execution-0001"
RAY = "runtime-asset:prophet-ray-ml:0.1.0"
BEAM = "runtime-asset:prophet-beam-dataops:0.1.0"
REQUIRED_DECISIONS = {"allow", "require-review"}
REQUIRED_SEQUENCE = [
    "slash-topic-scope",
    "replay-evidence-topic-pack",
    "sherlock-replay-evidence-index",
    "newhope-compatibility-membrane",
    "policy-fabric-decision",
    "semantic-membrane-decision",
]
REQUIRED_ARTIFACTS = {
    "urn:srcos:artifact:community_truth_demo_ray_metrics",
    "urn:srcos:artifact:community_truth_demo_beam_quality",
    "urn:srcos:model:community_truth_demo_candidate",
}
REQUIRED_RECEIPTS = {
    "urn:srcos:lineage-receipt:ray-community-truth-demo-0001",
    "urn:srcos:lineage-receipt:beam-community-truth-demo-0001",
}
REQUIRED_COMMANDS = {
    "/lattice mlops ray run community_truth_demo --runtime prophet-ray-ml --dry-run",
    "/lattice dataops beam run community_truth_demo --runtime prophet-beam-dataops --dry-run",
}


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
    require(isinstance(value, list) and value, f"{key} must be non-empty list")
    return value


def main() -> int:
    if not FIXTURE.exists():
        return fail(f"missing {FIXTURE}")
    try:
        data = json.loads(FIXTURE.read_text(encoding="utf-8"))
        require(data.get("apiVersion") == "newhope.socioprophet.dev/v0", "apiVersion mismatch")
        require(data.get("kind") == "LatticeReplayEvidenceMembraneFixture", "kind mismatch")
        refs = data.get("refs")
        require(isinstance(refs, dict), "refs must be object")
        for key in ["slashTopicScopeRef", "topicPackRef", "compatibilityRef", "sherlockReplayEvidenceRef", "slashReplayEvidenceRef", "mlopsReplayEvidenceRef", "demoReadinessTopologyRef"]:
            require_str(refs, key)
        require(refs["slashTopicScopeRef"] == "slash-topic://lattice/data-governai/replay-evidence", "slashTopicScopeRef mismatch")
        require(refs["sherlockReplayEvidenceRef"] == "SocioProphet/sherlock-search#33", "Sherlock ref mismatch")
        require(refs["slashReplayEvidenceRef"] == "SocioProphet/slash-topics#26", "Slash ref mismatch")
        require(refs["mlopsReplayEvidenceRef"] == "SocioProphet/prophet-platform-fabric-mlops-ts-suite#35", "MLOps ref mismatch")

        surface = data.get("surfaceModel")
        require(isinstance(surface, dict), "surfaceModel must be object")
        require(surface.get("publicSurface") == "slash-topics", "publicSurface mismatch")
        require(surface.get("runtimeSubstrate") == "new-hope", "runtimeSubstrate mismatch")
        require(surface.get("mustNotBypassPolicyFabric") is True, "mustNotBypassPolicyFabric must be true")
        require(surface.get("mustPreserveReplayEvidenceRefs") is True, "mustPreserveReplayEvidenceRefs must be true")

        inputs = require_list(data, "replayInputs")
        require(len(inputs) == 1, "must contain one replay input")
        replay = inputs[0]
        require(replay.get("assetRef") == BUNDLE, "assetRef mismatch")
        require(replay.get("assetKind") == "replay-evidence-bundle", "assetKind mismatch")
        require(set(require_list(replay, "runtimeRefs")) == {RAY, BEAM}, "runtimeRefs mismatch")
        require(REQUIRED_ARTIFACTS <= set(require_list(replay, "artifactRefs")), "artifactRefs incomplete")
        require(REQUIRED_RECEIPTS <= set(require_list(replay, "lineageReceiptRefs")), "lineageReceiptRefs incomplete")
        require(REQUIRED_COMMANDS <= set(require_list(replay, "replayCommandRefs")), "replayCommandRefs incomplete")
        safety = replay.get("safety")
        require(isinstance(safety, dict), "input safety must be object")
        require(safety.get("network") == "none", "network must be none")
        require(safety.get("secrets") == "none", "secrets must be none")
        require(safety.get("hostMutation") is False, "hostMutation must be false")

        decisions = require_list(data, "membraneDecisions")
        results = set()
        actions = set()
        for decision in decisions:
            require(isinstance(decision, dict), "decision must be object")
            require(require_str(decision, "assetRef") == BUNDLE, "decision assetRef mismatch")
            result = require_str(decision, "decision")
            require(result in REQUIRED_DECISIONS, f"unexpected decision result {result}")
            results.add(result)
            actions.add(require_str(decision, "action"))
            require(require_str(decision, "topicRef") == "slash-topic://lattice/data-governai/replay-evidence", "decision topicRef mismatch")
            require_str(decision, "policyRef")
            require_list(decision, "evidenceRefs")
            require_list(decision, "egressControls")
        require(results == REQUIRED_DECISIONS, f"decision result coverage mismatch {results}")
        require("use-replay-evidence-for-demo-review" in actions, "missing demo review action")
        require("use-replay-evidence-for-promotion" in actions, "missing promotion action")

        require(data.get("requiredSequence") == REQUIRED_SEQUENCE, "requiredSequence mismatch")
        top_safety = data.get("safety")
        require(isinstance(top_safety, dict), "top-level safety must be object")
        require(top_safety.get("dryRunOnly") is True, "dryRunOnly must be true")
        require(top_safety.get("hostMutation") is False, "hostMutation must be false")
        require(top_safety.get("network") == "none", "network must be none")
        require(top_safety.get("secrets") == "none", "secrets must be none")
    except Exception as exc:  # noqa: BLE001
        return fail(str(exc))
    print(f"PASS {FIXTURE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
