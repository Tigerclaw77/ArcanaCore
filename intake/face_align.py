"""
face_align.py

ArcanaCore intake v1
Face alignment and normalization using MediaPipe Face Mesh.

This module:
- aligns faces by eye centers
- normalizes scale via inter-eye distance
- outputs a 768x768 deterministic face crop

No beautification. No identity alteration.
"""

from pathlib import Path
import math
import cv2
import numpy as np


# =========================
# Constants (LOCKED v1)
# =========================

OUTPUT_SIZE = 768
EYE_Y_RATIO = 0.40          # eyes at 40% height
IED_RATIO = 0.32            # inter-eye distance = 32% of width
IED_TARGET = int(OUTPUT_SIZE * IED_RATIO)

# MediaPipe landmark indices
LEFT_EYE_LANDMARKS = [33, 133, 159, 145]
RIGHT_EYE_LANDMARKS = [362, 263, 386, 374]
NOSE_BRIDGE_LANDMARK = 168


# =========================
# Utility functions
# =========================

def mean_landmark(points):
    pts = np.array(points, dtype=np.float32)
    return pts.mean(axis=0)


def rotate_image(image, mat):
    h, w = image.shape[:2]
    return cv2.warpAffine(
        image,
        mat,
        (w, h),
        flags=cv2.INTER_LINEAR,
        borderMode=cv2.BORDER_REFLECT_101,
    )


def scale_image(image, scale):
    h, w = image.shape[:2]
    return cv2.resize(
        image,
        (int(w * scale), int(h * scale)),
        interpolation=cv2.INTER_LINEAR,
    )


def transform_landmarks(landmarks_xy, mat, scale=1.0):
    """
    Apply affine transform + scale to landmarks.
    """
    transformed = {}
    for idx, (x, y) in landmarks_xy.items():
        vec = np.array([x, y, 1.0], dtype=np.float32)
        x_t, y_t = mat @ vec
        transformed[idx] = (x_t * scale, y_t * scale)
    return transformed


# =========================
# Core alignment logic
# =========================

def align_face(
    image_bgr: np.ndarray,
    landmarks_xy: dict,
) -> np.ndarray:
    """
    Align and normalize a single face image.

    Args:
        image_bgr: input image (BGR)
        landmarks_xy: dict[int, (x, y)] in pixel coordinates

    Returns:
        aligned face image (768x768 BGR)

    Raises:
        ValueError if alignment fails
    """

    # --- Eye centers (original space) ---
    left_eye = mean_landmark([landmarks_xy[i] for i in LEFT_EYE_LANDMARKS])
    right_eye = mean_landmark([landmarks_xy[i] for i in RIGHT_EYE_LANDMARKS])

    # --- Roll correction ---
    dx = right_eye[0] - left_eye[0]
    dy = right_eye[1] - left_eye[1]
    angle_rad = math.atan2(dy, dx)
    angle_deg = math.degrees(angle_rad)

    eye_center = tuple(((left_eye + right_eye) / 2).astype(np.float32))

    rot_mat = cv2.getRotationMatrix2D(eye_center, angle_deg, 1.0)

    rotated_img = rotate_image(image_bgr, rot_mat)

    rotated_landmarks = transform_landmarks(landmarks_xy, rot_mat)

    # --- Inter-eye distance after rotation ---
    left_eye_r = mean_landmark([rotated_landmarks[i] for i in LEFT_EYE_LANDMARKS])
    right_eye_r = mean_landmark([rotated_landmarks[i] for i in RIGHT_EYE_LANDMARKS])

    inter_eye_dist = np.linalg.norm(right_eye_r - left_eye_r)
    if inter_eye_dist <= 0:
        raise ValueError("Invalid inter-eye distance")

    # --- Scale normalization ---
    scale = IED_TARGET / inter_eye_dist

    scaled_img = scale_image(rotated_img, scale)
    scaled_landmarks = {
        k: (v[0] * scale, v[1] * scale)
        for k, v in rotated_landmarks.items()
    }

    # --- Translation (eye-anchored) ---
    eye_mid = (left_eye_r + right_eye_r) / 2
    eye_mid = eye_mid * scale

    target_x = OUTPUT_SIZE // 2
    target_y = int(OUTPUT_SIZE * EYE_Y_RATIO)

    tx = target_x - eye_mid[0]
    ty = target_y - eye_mid[1]

    trans_mat = np.array([
        [1, 0, tx],
        [0, 1, ty],
    ], dtype=np.float32)

    translated = cv2.warpAffine(
        scaled_img,
        trans_mat,
        (scaled_img.shape[1], scaled_img.shape[0]),
        flags=cv2.INTER_LINEAR,
        borderMode=cv2.BORDER_REFLECT_101,
    )

    # --- Final crop ---
    h, w = translated.shape[:2]
    cx, cy = target_x, target_y

    x0 = int(cx - OUTPUT_SIZE // 2)
    y0 = int(cy - OUTPUT_SIZE // 2)
    x1 = x0 + OUTPUT_SIZE
    y1 = y0 + OUTPUT_SIZE

    if x0 < 0 or y0 < 0 or x1 > w or y1 > h:
        raise ValueError("Aligned image out of bounds")

    aligned = translated[y0:y1, x0:x1]

    if aligned.shape[:2] != (OUTPUT_SIZE, OUTPUT_SIZE):
        raise ValueError("Final image incorrect size")

    return aligned


# =========================
# I/O wrapper (CLI-safe)
# =========================

def process_image(
    image_path: Path,
    landmarks_xy: dict,
    out_path: Path,
):
    image = cv2.imread(str(image_path))
    if image is None:
        raise ValueError(f"Failed to read image: {image_path}")

    aligned = align_face(image, landmarks_xy)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(out_path), aligned)
