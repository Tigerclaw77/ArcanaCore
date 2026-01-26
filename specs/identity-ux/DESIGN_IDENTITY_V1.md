# Identity UX Spec (v1)

This repository defines the UX scaffold and design contract
for the identity convergence system.

Principles:
- One → many → one identity loop
- System explores, scout filters, user decides
- Convergence based on facet coverage, not image count
- v1 deliverable: 4–8 identity-consistent images
- Output doubles as PersonaPortraits product and future toji seeds

This repo is a UX/specification shell and will be integrated
into the production identity engine later.

## V1 User Interaction Timing (Authoritative)

User input is intentionally delayed.

The system explores identity space first.
The user only evaluates system-generated candidates.

Rationale:
- Avoids judging user-supplied images
- Preserves premium, confidence-first UX
- Aligns with luxury creative tools (Apple, pro photography)

## Intake Screen (V1)

User provides:
- Exactly one photo (identity seed)

The system does NOT:
- Grade the photo visibly
- Expose pass/fail or borderline labels
- Request batches upfront

Messaging focuses on exploration, not evaluation.

Example copy:
"We’ll explore identity-consistent variations from your photo."

### Intake Validation (System-Only)

The system may reject an upload only for structural reasons:
- No single clear human face detected
- Multiple faces present
- Non-human subject
- Image too small or corrupted
- Extreme occlusion or alignment failure

These are category errors, not quality judgments.
Rejection messaging must remain neutral and non-judgmental.


## Review Screen (V1)

The user is shown:
- Only system-filtered, high-quality candidates
- No obviously failed images

User actions:
- Approve
- Reject

Binary choice only.
No trinary labels exposed.

Internal systems may use trinary grading,
but the user interface remains binary.

## V1 Deliverable (PersonaPortraits)

The paid product is:
- A curated set of 4–8 identity-consistent images

Pricing is based on:
- Final output quality
- Curation
- Identity consistency

Pricing is NOT based on:
- Number of uploads
- Pass/fail counts
- Exploration volume

## Deferred (Post-V1)

- Exposing trinary grading to users
- Multi-seed intake
- Explicit toji readiness indicators
- User-visible facet coverage metrics

These may appear in v2+ but are excluded from v1
to preserve UX clarity and premium positioning.
