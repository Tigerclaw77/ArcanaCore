# ARCANACORE/output/select_final.py

import os
from typing import List


def select_final_images(
    approved_dir: str,
    min_outputs: int,
    max_outputs: int
) -> List[str]:
    """
    Selects final deliverables from already-approved images.
    Assumes ArcanaCore has already filtered failures.
    """

    if not os.path.exists(approved_dir):
        raise RuntimeError("Approved directory does not exist")

    images = sorted([
        os.path.join(approved_dir, f)
        for f in os.listdir(approved_dir)
        if f.lower().endswith((".png", ".jpg", ".jpeg"))
    ])

    if len(images) < min_outputs:
        raise RuntimeError("Insufficient approved images")

    return images[:max_outputs]
