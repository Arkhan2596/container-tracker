def clean_input(value):
    """
    Sətirdəki BL/Container və ya Shipping line inputundakı boşluqları təmizləyir.
    """
    if not value:
        return ""
    return str(value).strip().replace(" ", "").upper()
