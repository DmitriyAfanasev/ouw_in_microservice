import re

from pydantic import ValidationError


def validate_phone(v: str) -> str:
    cleaned = re.sub(r"[^\d+]", "", v)
    if not cleaned.startswith("+"):
        raise ValidationError("Phone number must start with '+' and country code")
    digits = re.sub(r"\D", "", cleaned)
    if not 8 <= len(digits) <= 15:
        raise ValidationError("Phone number must contain between 8 and 15 digits")

    return cleaned
