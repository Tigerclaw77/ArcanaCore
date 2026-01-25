"""
face_detect.py

MediaPipe Face Mesh extraction for ArcanaCore intake v1.

Responsibilities:
- detect exactly one dominant face
- extract pixel-space landmarks
- reject multi-face or low-confidence cases

Note:
- 468 landmarks (standard)
- 478 landmarks when refine_landmarks=True (includes iris)
"""

from typing import Dict, Tuple
import cv2
import numpy as np
import mediapipe as mp


# =========================
# MediaPipe setup
# =========================

_mp_face_mesh = mp.solutions.face_mesh

FACE_MESH = _mp_face_mesh.FaceMesh(
    static_image_mode=True,
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.6,
    min_tracking_confidence=0.6,
)


# =========================
# Core detection logic
# =========================

def extract_landmarks(
    image_bgr: np.ndarray,
) -> Dict[int, Tuple[float, float]]:
    """
    Extract face landmarks in pixel coordinates.

    Args:
        image_bgr: OpenCV image (BGR)

    Returns:
        dict: { landmark_index: (x_px, y_px) }

    Raises:
        ValueError if no face or multiple faces detected
    """

    if image_bgr is None or image_bgr.size == 0:
        raise ValueError("Invalid image")

    h, w = image_bgr.shape[:2]

    # MediaPipe expects RGB
    image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)

    result = FACE_MESH.process(image_rgb)

    if not result.multi_face_landmarks:
        raise ValueError("No face detected")

    if len(result.multi_face_landmarks) != 1:
        raise ValueError("Multiple faces detected")

    face_landmarks = result.multi_face_landmarks[0]

    landmarks_xy: Dict[int, Tuple[float, float]] = {}

    for idx, lm in enumerate(face_landmarks.landmark):
        x_px = lm.x * w
        y_px = lm.y * h
        landmarks_xy[idx] = (x_px, y_px)

    if len(landmarks_xy) not in (468, 478):
        raise ValueError(f"Unexpected landmark count: {len(landmarks_xy)}")

    # Record landmark mode for downstream logic
    landmark_count = len(landmarks_xy)


    return landmarks_xy
