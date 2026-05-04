"""Shared prompt building primitives for companion profile generation.

Prompt style follows the official Google Gemini Image Generation guidance:
https://ai.google.dev/gemini-api/docs/image-generation
- Narrative paragraphs over keyword lists or labeled blocks.
- Plain declarative descriptions instead of "do NOT" / instructive negatives.
"""

from typing import Final

from aidol.prompts import common as prompt_common

compose_prompt = prompt_common.compose_prompt
resolve_option_text = prompt_common.resolve_option_text


COMPANION_IMAGE_GENRE_PROMPT: Final[str] = (
    "Photorealistic K-pop idol casting headshot in professional ID photo style."
)


COMPANION_IMAGE_QUALITY_PROMPT: Final[
    str
] = """A tight professional headshot composition with the face filling the frame, centered in the upper two-thirds, front-facing with eyes at camera, wearing a plain white crew-neck t-shirt against a seamless single-color white paper studio backdrop free of gradient, objects, walls, windows, or environment. Soft butterfly lighting with gentle fill in pure white provides symmetrical even illumination and a soft shadow only under the chin. Shot on a Canon EOS R5 with an 85mm f/1.4 portrait lens, ultra-sharp focus on the eyes, 4K resolution.

The subject is extremely photogenic with perfect facial symmetry, harmonious golden-ratio proportions, smooth dewy youthful skin showing subtle fine pores and authentic natural texture, and a fresh-faced softness that reads unmistakably as a teenage idol trainee aged 17-19 rather than an adult. The iris stays natural with subtle striations, a soft limbal ring, and realistic depth, never colored-contact, oversaturated, glowing, glassy, or CGI-like. Hair color and length match the description exactly and the specified gender is preserved. The skin is clear of facial hair, forehead wrinkles, eye wrinkles, nasolabial folds, neck lines, and sagging. A single subject occupies the frame, free of additional faces, text, or watermark."""
