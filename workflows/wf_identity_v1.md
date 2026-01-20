# wf_identity_v1

Purpose:  
Preserve character identity across controlled generations.

This workflow prioritizes recognizability over novelty.

---

## Identity Rules

- Anchor images MUST be provided
- Anchors define identity, not prompts
- No averaging across large image sets

---

## Allowed Variations

- Pose
- Expression
- Minor lighting changes

Only one dimension may change per run.

---

## Disallowed Variations

- Face structure
- Age
- Stylization
- Camera distortion
- Heavy lighting shifts

If identity drifts, constraints must be tightened — prompts must not be expanded.

---

## Reproducibility

- Seeds must be recorded
- Parameters must be logged
- Outputs are immutable once generated

This workflow is locked.  
Changes require a new workflow ID.
