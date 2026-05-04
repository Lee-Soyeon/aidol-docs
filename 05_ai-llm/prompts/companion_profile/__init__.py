"""Companion profile prompt templates."""

from aidol.prompts.companion_profile.base import (
    COMPANION_IMAGE_GENRE_PROMPT,
    COMPANION_IMAGE_QUALITY_PROMPT,
)
from aidol.prompts.companion_profile.profile import (
    CompanionProfilePromptContext,
    build_companion_profile_prompt,
)

__all__ = [
    "COMPANION_IMAGE_GENRE_PROMPT",
    "COMPANION_IMAGE_QUALITY_PROMPT",
    "CompanionProfilePromptContext",
    "build_companion_profile_prompt",
]
