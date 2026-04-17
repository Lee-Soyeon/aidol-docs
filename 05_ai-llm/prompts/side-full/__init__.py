"""Side-full prompt templates (side profile + full body)."""

from aidol_docs.prompts.side_full.base import (
    CONSTRAINT_LOCK,
    IDENTITY_LOCK,
    SideFullConceptKey,
)
from aidol_docs.prompts.side_full.side_prompt import (
    SideProfilePromptContext,
    build_side_profile_prompt,
)
from aidol_docs.prompts.side_full.fullbody_prompt import (
    FullBodyPromptContext,
    build_full_body_prompt,
)

__all__ = [
    "CONSTRAINT_LOCK",
    "IDENTITY_LOCK",
    "SideFullConceptKey",
    "SideProfilePromptContext",
    "FullBodyPromptContext",
    "build_side_profile_prompt",
    "build_full_body_prompt",
]
