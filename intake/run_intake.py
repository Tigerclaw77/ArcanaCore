# ARCANACORE/intake/run_intake.py

from intake.face_detect import detect_faces
from intake.face_align import align_face
from intake.quality_gates import evaluate_quality
from intake.normalize import normalize_image


class IntakeError(Exception):
    pass


def run_intake(image_path: str) -> dict:
    """
    Structural intake only.
    No aesthetic judgment.
    """

    faces = detect_faces(image_path)

    if faces is None or len(faces) == 0:
        raise IntakeError("No face detected")

    if len(faces) > 1:
        raise IntakeError("Multiple faces detected")

    aligned = align_face(image_path, faces[0])
    normalized = normalize_image(aligned)

    quality = evaluate_quality(normalized)

    if not quality["passes_structural"]:
        raise IntakeError("Structural intake failure")

    return {
        "normalized_image": normalized,
        "quality": quality,
    }
