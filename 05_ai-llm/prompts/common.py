"""Shared prompt-building helpers across image prompt modules."""

from collections.abc import Mapping
from typing import Final, TypeVar

OptionKey = TypeVar("OptionKey", bound=str)

IDENTITY_LOCK: Final[
    str
] = """Keep the person's facial features exactly the same as the reference image.
This is the same person, not a look-alike or approximation.
Preserve the same skin tone and facial structure. Skin should look natural and smooth."""

COMMON_CONSTRAINT_LOCK: Final[
    str
] = """Maintain natural, anatomically correct body proportions.
The head must not appear oversized relative to the shoulders and torso.
Prioritize natural human scale over stylized or exaggerated proportions.
Both eyes must be anatomically correct and natural-looking -- symmetrical eye shape, proper iris placement, natural eyelid coverage, and consistent pupil size. Both eyes must have the exact same iris color as the reference image. No crossed eyes, misaligned irises, distorted eye shapes, or heterochromia.
Both arms must be fully visible and anatomically complete -- no missing, truncated, or merged limbs. Each arm should have a natural, clearly separated form from shoulder to hand.
Each hand must have exactly five fingers with correct hand anatomy -- proper thumb placement, natural finger joints, and proportional hand size relative to the body. No extra digits, no fused fingers, no duplicate hands.
Do not place shelves, furniture, or any objects immediately next to the subject that obstruct or clutter the frame edges."""


def compose_prompt(*parts: str | None) -> str:
    """Join prompt sections while ignoring blank values."""
    return "\n\n".join(part.strip() for part in parts if part and part.strip())


def resolve_option_text(
    options: Mapping[OptionKey, str],
    key: OptionKey,
    option_name: str,
) -> str:
    """Resolve option text with a stable error for invalid keys."""
    try:
        return options[key]
    except KeyError as exc:
        raise ValueError(f"Unknown {option_name}: {key}") from exc


def build_constraint_lock(*extra_sections: str) -> str:
    """Append module-specific constraints to the shared constraint block."""
    return compose_prompt(COMMON_CONSTRAINT_LOCK, *extra_sections)
