"""
quality_gates.py

Acceptance gates for ArcanaCore intake v1.

Goal:
- conservative rejection to prevent identity drift and bad anchors
- deterministic, non-creative checks only

Checks:
- landmark geometry sanity
- face size minimum (via inter-eye distance)
- blur detection (variance of Laplacian)
- approximate yaw/pitch via landmark symmetry heuristics
"""

from dataclasses import dataclass
import numpy as np
import cv2


# -------------------------
# Landmark indices (locked)
# -------------------------

LEFT_EYE_LANDMARKS = [33, 133, 159, 145]
RIGHT_EYE_LANDMARKS = [362, 263, 386, 374]
NOSE_BRIDGE_LANDMARK = 168

# Nose tip region (helps yaw/pitch heuristics)
NOSE_TIP_LANDMARK = 1

# Mouth center-ish (helps pitch heuristic)
UPPER_LIP_LANDMARK = 13
LOWER_LIP_LANDMARK = 14

# Face sides (cheek-ish) for yaw heuristic
LEFT_CHEEK_LANDMARK = 234
RIGHT_CHEEK_LANDMARK = 454


@dataclass(frozen=True)
class GateConfig:
    # Minimum face size in the source image (pixels)
    min_inter_eye_px: float = 120.0

    # Blur threshold: variance of Laplacian
    # Typical: 80–150; higher = stricter
    min_laplacian_var: float = 90.0

    # Approximate pose limits (degrees)
    # These are heuristic; conservative defaults
    max_abs_yaw_deg: float = 30.0
    max_abs_pitch_deg: float = 25.0

    # Safety margin: landmarks must be within frame bounds (slightly tolerant)
    bounds_margin_px: float = 2.0


def _mean_point(landmarks_xy: dict, idxs: list) -> np.ndarray:
    pts = np.array([landmarks_xy[i] for i in idxs], dtype=np.float32)
    return pts.mean(axis=0)


def _laplacian_var(image_bgr: np.ndarray) -> float:
    gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
    return float(cv2.Laplacian(gray, cv2.CV_64F).var())


def _ensure_landmarks_present(landmarks_xy: dict, required: list):
    missing = [i for i in required if i not in landmarks_xy]
    if missing:
        raise ValueError(f"Missing required landmarks: {missing}")


def _bounds_check(landmarks_xy: dict, width: int, height: int, margin: float):
    for idx, (x, y) in landmarks_xy.items():
        if x < -margin or y < -margin or x > (width - 1 + margin) or y > (height - 1 + margin):
            raise ValueError(f"Landmark {idx} out of bounds: ({x:.1f},{y:.1f})")


def _estimate_yaw_pitch_deg(landmarks_xy: dict) -> tuple[float, float]:
    """
    Heuristic yaw/pitch estimate using landmark symmetry.

    Yaw heuristic:
      Compare distances from nose tip to left/right cheek landmarks.
      Larger imbalance => more yaw.

    Pitch heuristic:
      Compare vertical distances between nose bridge, nose tip, and mouth center.
      Large shifts indicate pitch.

    Returns:
      (yaw_deg, pitch_deg) approximately
    """

    nose_tip = np.array(landmarks_xy[NOSE_TIP_LANDMARK], dtype=np.float32)
    left_cheek = np.array(landmarks_xy[LEFT_CHEEK_LANDMARK], dtype=np.float32)
    right_cheek = np.array(landmarks_xy[RIGHT_CHEEK_LANDMARK], dtype=np.float32)

    # yaw proxy: cheek distance imbalance relative to total
    dl = np.linalg.norm(nose_tip - left_cheek)
    dr = np.linalg.norm(nose_tip - right_cheek)
    if (dl + dr) <= 1e-6:
        yaw = 0.0
    else:
        imbalance = (dr - dl) / (dr + dl)  # [-1, 1]
        # Map imbalance to degrees (empirical scaling)
        yaw = float(imbalance * 45.0)

    nose_bridge = np.array(landmarks_xy[NOSE_BRIDGE_LANDMARK], dtype=np.float32)
    upper_lip = np.array(landmarks_xy[UPPER_LIP_LANDMARK], dtype=np.float32)
    lower_lip = np.array(landmarks_xy[LOWER_LIP_LANDMARK], dtype=np.float32)
    mouth_center = (upper_lip + lower_lip) / 2.0

    # pitch proxy: relative vertical ratios
    nb_to_tip = nose_tip[1] - nose_bridge[1]
    tip_to_mouth = mouth_center[1] - nose_tip[1]

    denom = abs(nb_to_tip) + abs(tip_to_mouth)
    if denom <= 1e-6:
        pitch = 0.0
    else:
        ratio = (tip_to_mouth - nb_to_tip) / denom  # [-1,1] proxy
        # Map ratio to degrees (empirical scaling)
        pitch = float(ratio * 35.0)

    return yaw, pitch


def run_acceptance_gates(
    image_bgr: np.ndarray,
    landmarks_xy: dict,
    config: GateConfig = GateConfig(),
) -> dict:
    """
    Run all acceptance gates.

    Returns:
      dict with metrics useful for logging:
        {
          "inter_eye_px": float,
          "laplacian_var": float,
          "yaw_deg": float,
          "pitch_deg": float
        }

    Raises:
      ValueError on failure (conservative rejection)
    """
    if image_bgr is None or image_bgr.size == 0:
        raise ValueError("Invalid image input")

    h, w = image_bgr.shape[:2]

    required = (
        LEFT_EYE_LANDMARKS
        + RIGHT_EYE_LANDMARKS
        + [NOSE_BRIDGE_LANDMARK, NOSE_TIP_LANDMARK, UPPER_LIP_LANDMARK, LOWER_LIP_LANDMARK, LEFT_CHEEK_LANDMARK, RIGHT_CHEEK_LANDMARK]
    )
    _ensure_landmarks_present(landmarks_xy, required)
    _bounds_check(landmarks_xy, w, h, config.bounds_margin_px)

    # Face size: inter-eye distance
    left_eye = _mean_point(landmarks_xy, LEFT_EYE_LANDMARKS)
    right_eye = _mean_point(landmarks_xy, RIGHT_EYE_LANDMARKS)
    inter_eye = float(np.linalg.norm(right_eye - left_eye))
    if inter_eye < config.min_inter_eye_px:
        raise ValueError(f"Face too small (inter-eye {inter_eye:.1f}px < {config.min_inter_eye_px:.1f}px)")

    # Blur gate
    lv = _laplacian_var(image_bgr)
    if lv < config.min_laplacian_var:
        raise ValueError(f"Image too blurry (Laplacian var {lv:.1f} < {config.min_laplacian_var:.1f})")

    # Pose gate (heuristic)
    yaw, pitch = _estimate_yaw_pitch_deg(landmarks_xy)
    if abs(yaw) > config.max_abs_yaw_deg:
        raise ValueError(f"Yaw too large ({yaw:.1f}° > {config.max_abs_yaw_deg:.1f}°)")
    if abs(pitch) > config.max_abs_pitch_deg:
        raise ValueError(f"Pitch too large ({pitch:.1f}° > {config.max_abs_pitch_deg:.1f}°)")

    return {
        "inter_eye_px": inter_eye,
        "laplacian_var": lv,
        "yaw_deg": float(yaw),
        "pitch_deg": float(pitch),
    }
