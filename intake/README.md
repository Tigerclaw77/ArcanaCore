# Face Intake & Normalization

This module handles the **first irreversible step** in the ArcanaCore pipeline:
converting arbitrary user-uploaded photos into standardized, identity-safe
face images suitable for downstream generation and evaluation.

This step is **deterministic** and **non-creative**.

---

## Purpose

The intake process ensures that all subsequent stages (generation, scoring,
filtering, refinement) operate on **consistent facial representations**.

If intake is incorrect, identity stability cannot be recovered later.

---

## Guarantees

This module guarantees that output images:

- Contain exactly **one primary face**
- Are **centered** with eyes horizontally aligned
- Use a **consistent scale** (inter-eye distance normalized)
- Maintain **original facial identity** without stylistic changes
- Are reproducible (same input → same output)

---

## Non-Goals

This module does **not**:

- Beautify or modify facial features
- Alter skin texture, age, or expression
- Enforce symmetry or correct asymmetries
- Perform identity scoring or quality ranking
- Generate new images or variations

---

## Input

- One or more user-uploaded image files
- Any resolution, orientation, lighting, or background
- Common formats: JPG, PNG, WEBP

---

## Processing Steps

1. Detect face bounding box and landmarks
2. Correct rotation so eyes are horizontally aligned
3. Normalize scale using inter-eye distance
4. Center face within fixed frame
5. Apply minimal padding if needed
6. Export normalized image

All steps are **algorithmic** and **non-probabilistic**.

---

## Output

- One or more normalized face images
- Fixed resolution (e.g. 512×512 or 768×768)
- Neutral framing suitable for reuse as anchors

Example output path:

---

## Failure Conditions

An input image is rejected if:

- No face is detected
- Multiple dominant faces are detected
- Face is too occluded for reliable landmark detection
- Extreme pose prevents reliable alignment

Rejected images should be logged but not modified.

---

## Design Notes

- This module is intentionally conservative
- False negatives are preferred over false positives
- Later stages may discard images, but intake must not introduce drift

---

## Downstream Dependencies

All later pipeline stages assume intake outputs are:

- Geometrically normalized
- Identity-faithful
- Free of stylistic bias

No downstream step may attempt to “fix” intake errors.

---

## Status

- Version: v1 (initial)
- Scope: local, offline, CPU-safe
- Intended to be replaced or extended only with extreme caution
