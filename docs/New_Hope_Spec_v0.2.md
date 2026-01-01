# New Hope Specification v0.2

## 2.2 Carrier wire format (canonical representation)

We standardize one canonical representation for hashing/signing, regardless of transport:

```json
{
  "carrier_version": "1",
  "protocol_ref": "hash://blake3/<protocol-hash>",
  "signal": {
    "type": "MessagePosted|ClaimAsserted|CitationAdded|ModerationAction|...",
    "ts": "2025-12-26T22:14:00Z",
    "id": "hash://blake3/<signal-hash>",
    "parents": ["hash://..."],
    "thread_root": "hash://...",
    "derived_from": ["hash://..."]
  },
  "payload": { "...": "..." },
  "provenance": {
    "emitter": {
      "kind": "human|agent|service",
      "id": "did:key:...",
      "device_attestation": "optional"
    },
    "signatures": [
      {
        "alg": "ed25519",
        "sig": "base64...",
        "covers": "hash://blake3/<canonical-carrier-hash>"
      }
    ],
    "inputs": ["hash://..."],
    "transforms": [
      {"receptor_id": "did:key:...", "ts": "...", "notes": "optional"}
    ]
  },
  "policy_context": {
    "tenant": "commons|org:<id>|team:<id>",
    "community": "news:<id>|topic:<id>",
    "ruleset_ref": "hash://blake3/<policy-hash>",
    "labels": ["public", "needs_review", "contains_pii:false"]
  }
}
```

**Key rule:** hash/sign the canonical form (stable key order + stable serialization).
