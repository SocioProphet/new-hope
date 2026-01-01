# History

## Where this started

We went looking for the original **HOPE (Higher Order Programming Environment)** work—both the implementation and the closest thing to a “spec.” What we found wasn’t a single RFC-style document, but a *distributed specification* spread across:

- Marc Clifton’s explanatory blog posts (motivation + conceptual framing)
- the CodeProject article series (architecture published in a spec-like format)
- the HOPE GitHub repository (the executable spec: interfaces, routing logic, examples)

Together, those sources capture HOPE’s core claim: that we can build systems where computation is not just “values through functions,” but **meaning-bearing structures moving through a semantic runtime**.

## What HOPE is (in plain terms)

HOPE presents a semantic computation environment with a small set of primitives:

- **Semantic Types**  
  Data structures that carry explicit meaning, not just shape—so the runtime can reason about *what* something is, not just how it’s encoded.

- **Receptors**  
  Plug-in computational modules that accept semantic input and emit semantic output. Receptors are the unit of composition: you build systems as networks of behaviors.

- **Carriers**  
  The typed envelopes that move between receptors—carrying semantic payloads plus the contextual metadata needed for routing and processing.

- **Membranes**  
  Boundaries between receptors (or groups of receptors) that control how carriers move. HOPE used membranes primarily as routing boundaries; the idea generalizes naturally to enforcement boundaries.

- **Semantic Database**  
  A persistence/query layer intended to store semantic structures as first-class objects, rather than forcing everything into a single relational/graph/document mold.

From a modern perspective, HOPE got something rare and important right: it made “agentic composition” feel like a runtime design problem, not an application-specific pile of glue code.

## The primary source trail (the “distributed spec”)

HOPE doesn’t appear to have a single formal specification document. Instead, we treat the following as the canonical lineage:

- **CodeProject: HOPE — Higher Order Programming Environment**  
  The closest thing to an architectural spec: concepts, runtime semantics, receptors/carriers/membranes, semantic type declarations, and the shape of the IDE.  
  https://www.codeproject.com/Articles/777843/HOPE-Higher-Order-Programming-Environment  
  Repository referenced by the article: https://github.com/cliftonm/HOPE

- **Blog: Semantic Database — Concept, Architecture and Implementation**  
  The rationale and design intent behind a semantic persistence layer that participates in the runtime rather than sitting “under” it.  
  https://marcclifton.wordpress.com/2014/10/25/semantic-database-concept-architecture-and-implementation/

- **CodeProject: The Semantic Database in Action**  
  Practical demonstrations that show how the receptor model and semantic persistence behave in real workflows.  
  https://www.codeproject.com/Articles/837878/The-Semantic-Database-In-Action

- **Blog: Higher Order Programming on the Web is Alive**  
  An evolutionary note: HOPE’s ideas pushed toward web-era deployment and interaction models.  
  https://marcclifton.wordpress.com/2017/12/09/higher-order-programming-on-the-web-is-alive/

In practice: the CodeProject articles provide the narrative “spec,” while the GitHub code provides the normative truth of interfaces and behaviors.

## Timeline (compressed)

- **2014** — HOPE and the semantic database concepts are articulated in a spec-like public form (blog + CodeProject series).
- **2015–2017** — Continued refinement and web-facing viability notes; HOPE demonstrates a runtime worldview that still maps well to agentic composition.
- **2025+** — The world requires commons-grade properties HOPE didn’t need to specify: cryptographic provenance, enforcement boundaries, explicit nondeterminism, multi-tenant governance, and ranking transparency. This is the pressure that produces **New Hope**.

## Why this becomes **New Hope**

HOPE’s primitives are the right atoms for a system we still want—but the world changed. A 2025+ knowledge commons and agentic runtime can’t survive on routing elegance alone. It needs *enforcement-grade trust and governance* as first-class semantics.

So “New Hope” is not a rebrand. It’s a continuation with missing bones added:

- **Provenance is mandatory**  
  Content-addressing and signatures aren’t optional features; they are the precondition for attribution, audit, replay, appeals, and federation.

- **Membranes become enforcement points**  
  Not just “where messages pass,” but where policy is evaluated: minimization/redaction, rate limits, capability gating, tenant isolation, and controlled egress.

- **Nondeterminism is modeled explicitly**  
  Modern systems include stochastic components (LLMs, retrieval, tool calls). If nondeterminism is not first-class, replay becomes theater.

- **News + messaging primitives are native objects**  
  Threads, claims, citations, stances, moderation actions, and ranking transparency are not “app features”—they are protocol-level entities.

- **Replay is a conformance requirement**  
  Deterministic components must be replayable; nondeterministic components must be traceable and bounded.

In short: HOPE gave us a compositional semantic runtime. **New Hope** keeps those atoms, but upgrades the system into a commons-grade substrate where trust, governance, and auditability are part of the runtime contract—not bolted on afterward.

## What’s different in this repo (concrete mapping)

This repository encodes the “added bones” explicitly:

- `docs/New_Hope_Spec_v0.2.md`
  Normative objects (Protocol/Signal/Carrier/Receptor/Membrane/System) and minimum membrane expressivity.

- `docs/Carrier_Wire_Format.md`
  Canonical carrier example used for hashing/signing discussions and tooling.

- `docs/Protocol_Pack_v0.md`
  First-class objects for news + messaging (Message/Thread/Claim/Citation/Entity/Lens/ModerationEvent).

- `docs/Conformance_Tests.md`
  Non-negotiable tests: replay, nondeterminism declaration, provenance, membrane enforcement, and ranking explainability.

- `docs/Mapping_HOPE_to_NewHope.md`
  Lineage mapping that preserves the HOPE mental model while making enforcement and trust mandatory.

- `docs/Roadmap.md`
  Immediate hardening steps (canonicalization RFC, membrane decision outputs, registry packaging, harness spec).

## Non-goals (to keep this honest)

- **Not** a monolithic “everything platform.” New Hope is a runtime + protocol spine, designed to compose.
- **Not** “trust by vibes.” Trust is expressed as signed lineage, enforceable membranes, and conformance tests.
- **Not** a promise that nondeterminism disappears. We model and constrain it; we do not pretend it isn’t there.
- **Not** dependent on proprietary services. The design assumes open, inspectable implementations and federated deployment.
