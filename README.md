# Character Identity Engine

## Purpose

This project exists to solve **character identity persistence**, not image generation.

Modern image tools optimize for novelty and visual quality, but fail at:
- Maintaining recognizability across generations
- Allowing controlled modification of a character
- Preserving identity across outputs
- Supporting professional, iterative character development

This engine treats a **character as a first-class object**, not as a side effect of prompts.

---

## Core Idea

An image can be **promoted** into a persistent character identity.

Once promoted, a character should be:
- Recognizable across outputs
- Stable when constrained
- Flexible when constraints are loosened
- Modifiable along specific dimensions (pose, expression, age, clothing, style)

Identity is defined explicitly, not discovered accidentally.

---

## What This Project Is Not

- Not an image generator
- Not a prompt marketplace
- Not a one-click “consistency” tool
- Not a public SaaS

This is an **internal character production engine**.

---

## Canon Tooling

### Generation
- Local diffusion engine (e.g. ComfyUI)
- One or two locked workflows only
- Emphasis on repeatability and control

### Exploration
- Fast third-party tools may be used for ideation only
- Outputs are sketches, never final assets

### Review
- Simple local web UI
- Human approval and tagging only
- No generation occurs here

### Persistence
- MongoDB (local or free tier)
- Lightweight, flexible schema
- Low cost, low cognitive overhead

---

## Canon Data Objects

Only the following objects exist:
- Character
- Generation Run
- Image
- Tags / Feedback

Anything beyond this is out of scope.

---

## Identity Definition

### Anchor Images
- Identity is defined by a small set of anchor images
- Typical range: 5–7
- Chosen for clarity, neutrality, and recognizability
- Used directly in generation

### Approved Images
- Larger sets (20–60+) define boundaries
- Used for validation and drift detection
- Not fed back into generation simultaneously

**Key rule:**  
Identity is defined by boundaries and extremes, not averages.

---

## Feedback Loop

Human judgment is essential.

The system relies on:
- Explicit approval / rejection
- Short, human-meaningful tags
- Gradual refinement of constraints

There is no automated learning at the start.

---

## Training Policy

No training (e.g. LoRA) initially.

Training is considered only when:
- Identity is already stable
- Drift is minimal
- The goal is compression or portability

Training is treated as compression, not discovery.

---

## Development Philosophy

- Build small, ugly, internal spikes
- Validate assumptions with real outputs
- Avoid theory paralysis
- Avoid premature automation
- Avoid premature productization

---

## Success Criterion

This project succeeds only if the following question can be answered **yes**:

> Can a promoted image remain recognizably the same character across controlled generations?

Everything else is secondary.

---

## Status

**Canonized and locked**
- Problem framing
- Identity-first approach
- Tooling stack
- Data model
- Anchor strategy
- Feedback loop philosophy

**Not decided**
- Public access
- Pricing
- Automation
- Branding
- Scaling

Anything not written here is intentionally undecided.
