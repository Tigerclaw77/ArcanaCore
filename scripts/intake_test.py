"""
intake_test.py

End-to-end intake runner for ArcanaCore intake v1.

Usage:
    python scripts/intake_test.py path/to/image.jpg

What it does:
1. Loads image
2. Extracts landmarks (MediaPipe)
3. Runs acceptance gates
4. Aligns face to canonical 768x768 frame
5. Saves output + prints metrics or rejection reason
"""

import sys
from pathlib import Path
import traceback

import cv2

from intake.face_detect import extract_landmarks
from intake.face_align import align_face
from intake.quality_gates import GateConfig


# =========================
# Config (tweak here only)
# =========================

OUTPUT_DIR = Path("output/intake_test")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

GATE_CONFIG = GateConfig(
    min_inter_eye_px=120.0,
    min_laplacian_var=90.0,
    max_abs_yaw_deg=30.0,
    max_abs_pitch_deg=25.0,
)


# =========================
# Runner
# =========================

def main():
    if len(sys.argv) != 2:
        print("Usage: python scripts/intake_test.py path/to/image.jpg")
        sys.exit(1)

    image_path = Path(sys.argv[1])
    if not image_path.exists():
        print(f"Error: file not found: {image_path}")
        sys.exit(1)

    print(f"\n[INFO] Processing: {image_path}")

    image = cv2.imread(str(image_path))
    if image is None:
        print("[ERROR] Failed to load image")
        sys.exit(1)

    try:
        # 1. Landmark extraction
        landmarks_xy = extract_landmarks(image)
        print("[OK] Landmarks extracted")

        # 2. Alignment + gates
        aligned, metrics = align_face(
            image_bgr=image,
            landmarks_xy=landmarks_xy,
            run_gates=True,
            gate_config=GATE_CONFIG,
        )
        print("[OK] Alignment successful")

        # 3. Save output
        out_path = OUTPUT_DIR / f"{image_path.stem}_aligned.png"
        cv2.imwrite(str(out_path), aligned)

        print(f"[OK] Saved aligned image to: {out_path}")

        # 4. Print metrics
        print("\n--- Intake Metrics ---")
        for k, v in metrics.items():
            if isinstance(v, float):
                print(f"{k:>20}: {v:.3f}")
            else:
                print(f"{k:>20}: {v}")
        print("----------------------\n")

    except Exception as e:
        print("\n[REJECTED]")
        print(str(e))
        print("\n--- Trace (for debugging) ---")
        traceback.print_exc()
        print("----------------------------\n")
        sys.exit(2)


if __name__ == "__main__":
    main()
