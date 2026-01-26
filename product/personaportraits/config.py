# ARCANACORE/product/personaportraits/config.py

PERSONA_PORTRAITS_V1 = {
    "max_seeds": 1,
    "min_outputs": 4,
    "max_outputs": 8,
    "allow_retry": True,

    # UX contract
    "review_mode": "binary",
    "expose_trinary": False,

    # Engine behavior constraints
    "allow_multi_seed": False,
    "allow_user_grading": False,
}
