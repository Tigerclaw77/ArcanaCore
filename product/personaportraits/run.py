# ARCANACORE/product/personaportraits/run.py

from intake.run_intake import run_intake, IntakeError
from output.select_final import select_final_images
from product.personaportraits.config import PERSONA_PORTRAITS_V1

from runs.execute_run import execute_identity_run  # ← existing or stub


def run_persona_portraits(seed_image_path: str) -> dict:
    """
    PersonaPortraits v1 execution.
    Thin wrapper over ArcanaCore.
    """

    try:
        intake_result = run_intake(seed_image_path)
    except IntakeError as e:
        return {
            "status": "rejected",
            "reason": str(e)
        }

    run = execute_identity_run(
        intake_result["normalized_image"],
        mode="persona_portraits"
    )

    approved_dir = run["approved_dir"]

    finals = select_final_images(
        approved_dir=approved_dir,
        min_outputs=PERSONA_PORTRAITS_V1["min_outputs"],
        max_outputs=PERSONA_PORTRAITS_V1["max_outputs"]
    )

    return {
        "status": "success",
        "final_images": finals,
        "run_id": run["run_id"]
    }
