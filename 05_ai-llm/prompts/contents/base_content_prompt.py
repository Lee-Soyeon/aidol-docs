"""Common base prompt for all content image generation.

This module provides shared context (Identity Lock, Constraint Lock,
PromptCombination type, build_prompt function) that applies to all
content types: daily, finger heart, school.
"""

from typing import TypedDict

# ── Fixed Option: Identity Lock ──
IDENTITY_LOCK = """Keep the person's facial features exactly the same as the reference image.
This is the same person, not a look-alike or approximation.
Preserve the same skin tone and facial structure. Skin should look natural and smooth."""

# ── Fixed Option: Constraint Lock ──
CONSTRAINT_LOCK = """Maintain natural, anatomically correct body proportions.
The head must not appear oversized relative to the shoulders and torso.
Frame the shot so the upper body including chest and shoulders is visible.
Prioritize natural human scale over stylized or exaggerated proportions.
Both eyes must be anatomically correct and natural-looking — symmetrical eye shape, proper iris placement, natural eyelid coverage, and consistent pupil size. Both eyes must have the exact same iris color as the reference image. No crossed eyes, misaligned irises, distorted eye shapes, or heterochromia.
Both arms must be fully visible and anatomically complete — no missing, truncated, or merged limbs. Each arm should have a natural, clearly separated form from shoulder to hand.
Each hand must have exactly five fingers with correct hand anatomy — proper thumb placement, natural finger joints, and proportional hand size relative to the body. No extra digits, no fused fingers, no duplicate hands.
Do not place shelves, furniture, or any objects immediately next to the subject that obstruct or clutter the frame edges."""


class PromptCombination(TypedDict):
    scene: str
    gaze: str
    expression: str
    outfit: str
    camera: str
    atmosphere: str


def build_prompt(
    combo: PromptCombination,
    *,
    scene_options: dict,
    gaze_options: dict,
    expression_options: dict,
    outfit_options: dict,
    camera_options: dict,
    atmosphere_options: dict,
) -> str:
    """
    최종 프롬프트를 조립한다.
    combo의 각 값은 해당 OPTIONS dict의 키워드 키이다.
    """

    prompt_parts = [
        # [Identity]
        IDENTITY_LOCK,
        # [Scene]
        scene_options[combo["scene"]],
        # [Gaze]
        gaze_options[combo["gaze"]],
        # [Expression]
        expression_options[combo["expression"]],
        # [Outfit]
        outfit_options[combo["outfit"]],
        # [Composition]
        camera_options[combo["camera"]],
        # [Style]
        atmosphere_options[combo["atmosphere"]],
        # [Controls]
        CONSTRAINT_LOCK,
    ]

    return "\n\n".join(prompt_parts)
