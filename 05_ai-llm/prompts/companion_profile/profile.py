"""Prompt renderer for companion profile image generation.

Output format follows Google Gemini Image Generation guidance:
narrative paragraphs over keyword lists, declarative descriptions over
"do NOT" instructions. See base.py for the shared genre/quality blocks.
"""

import random
from dataclasses import dataclass

from aidol.prompts.companion_profile.base import (
    COMPANION_IMAGE_GENRE_PROMPT,
    COMPANION_IMAGE_QUALITY_PROMPT,
    compose_prompt,
    resolve_option_text,
)

GENDER_PROMPTS: dict[str, str] = {
    "FEMALE": "Female",
    "MALE": "Male",
}

ETHNICITY_PROMPTS: dict[str, str] = {
    "EAST_ASIAN": "East Asian features — refined facial harmony with balanced almond-shaped double-eyelid eyes, clean straight nose bridge proportional to the face, smooth oval facial structure with elegant Korean/Japanese/Chinese proportions",
    "SOUTHEAST_ASIAN": "Southeast Asian features with K-pop idol refinement — large round expressive double-eyelid eyes with bright vivid gaze, gently rounded facial structure with softer volume, naturally fuller lips, softly defined nose with delicate slim proportions, warm-toned harmonious balance",
    "EUROPEAN": "European Caucasian features — high straight nose bridge with sharply defined ridge, deep-set large open eyes with prominent eyelid crease, sharply sculpted angular jawline and high cheekbones, dimensional facial depth and Western bone structure",
    "SOUTH_AMERICAN": "South American Latin features with youthful K-pop trainee softness — Mediterranean-influenced facial structure with hints of Indigenous American heritage, expressive deep-set double-eyelid eyes with luminous bright youthful gaze, prominent straight nose bridge, softly defined cheekbones, balanced Latin facial structure with warm radiant aura, smooth dewy teen skin",
    "KOR_JPN": "Korean-Japanese mixed heritage, refined East Asian features — straight clean nose bridge, large almond double-eyelid eyes, delicate oval face with elegant bone structure",
    "KOR_RUS": "Korean-Russian mixed heritage with Russian Slavic descent, distinctly visible hybrid identity balancing both ancestries — sharply chiseled high nose bridge with clearly defined ridge typical of Russian Slavic features, deep-set double-eyelid almond eyes with refined upturned outer corners, sharply sculpted high cheekbones with angular jawline, dimensional facial depth and angular bone structure typical of Russian Slavic heritage while retaining unmistakable Korean facial harmony and eye proportions — looks neither purely Korean nor purely Russian",
    "KOR_USA": "Korean-American mixed heritage with Western Caucasian descent — appearing unmistakably mixed-race rather than purely East Asian, with clearly Western-influenced features: high straight nose bridge with prominent dimensional ridge, deep-set double-eyelid eyes blending East Asian almond shape with Western depth, prominently dimensional cheekbones, sculpted Western-style jawline, dimensional facial depth typical of Caucasian bone structure while retaining Korean facial harmony — distinctly hybrid, neither purely Korean nor purely Western",
    "KOR_CAN": "Korean-Canadian mixed heritage with Anglo-Canadian British Isles descent — appearing unmistakably mixed-race rather than purely East Asian, with clearly Western-influenced features: prominent high straight nose bridge with dimensional ridge, large round open double-eyelid eyes with Caucasian-leaning luminous depth and bright clear gaze, sharply dimensional high cheekbones, defined angular jawline, Anglo-Canadian British Isles bone structure while retaining Korean facial harmony — distinctly hybrid, neither purely Korean nor purely Western",
}

MOOD_PROMPTS: dict[str, str] = {
    "CHIC": "chic and charismatic",
    "REFRESHING": "refreshing and youthful",
    "CONFIDENT": "confident",
    "PURE": "innocent and pure",
    "DARK": "dark and mysterious",
    "CUTE": "cute",
    "PLAYFUL": "playful",
    "ETHEREAL": "ethereal, mysterious",
    "REFINED": "polished and refined",
    "AFFECTIONATE": "warm and affectionate",
    "SHY": "shy and demure",
}

EYE_COLOR_PROMPTS: dict[str, str] = {
    "BROWN": "warm natural brown eyes with realistic iris striations and a soft limbal ring",
    "DARK_BROWN": "natural dark brown eyes with a subtle warm undertone and soft realistic iris detail, calmly grounded gaze, distinguishable from pure black yet never glossy, dramatic, or contact-lens-like",
    "HAZEL": "hazel eyes with a natural green-brown gradient and realistic iris detail",
    "AMBER": "subtly amber-tinted dark brown eyes with a warm golden undertone visible only on close inspection, naturalistic and grounded, never yellow, glowing, or contact-lens-like",
    "BLACK": "deep brown eyes (distinguishable from raven black, never void) with clearly visible warm brown iris striations, a soft limbal ring, and a naturally lit pupil",
}

FACE_SHAPE_PROMPTS: dict[str, str] = {
    "SHARP": "sharp features, an intense gaze, and a sculpted jawline",
    "SOFT": "soft features and gentle warm eyes",
    "INTENSE": "intense sharp-angled almond eyes with upturned outer corners, thick defined eyebrows, and a piercing gaze",
    "HEAVY": "softly heavy-lidded eyes with composed refined presence and grounded bone structure carrying a youthful idol aura",
    "DEEP": "deep-set eyes with a thoughtful mysterious presence",
}

HAIR_COLOR_PROMPTS: dict[str, str] = {
    "BLACK": "black",
    "DARK_BROWN": "dark brown",
    "CHESTNUT": "chestnut",
    "AUBURN": "auburn",
    "BROWN": "brown",
    "RED": "red",
    "BLONDE": "blonde",
    "PLATINUM": "platinum",
    "PINK": "cool desaturated muted dusty pink",
    "ASH_GRAY": "naturally desaturated cool-toned dark ash",
}

HAIR_STYLE_MALE_PROMPTS: dict[str, str] = {
    "SHORT": "short textured hair in K-pop idol styling",
    "MUSHROOM": "modern textured mushroom cut with airy bangs in K-pop idol styling",
    "MEDIUM": "medium layered hair in K-pop idol styling",
    "WAVY": "wavy hair in K-pop idol styling",
    "CURLY": "curly hair in K-pop idol styling",
    "BANGS": "voluminous styled hair with airy textured bangs in K-pop idol styling",
    "TWO_BLOCK": "two-block cut with voluminous top and cropped sides in K-pop idol styling",
    "WOLF": "edgy wolf cut with layered texture and a longer back in K-pop idol styling",
    "COMMA": "polished comma-shaped side-swept fringe with glossy soft volume, the signature K-pop boy idol look",
}

HAIR_STYLE_FEMALE_PROMPTS: dict[str, str] = {
    "LONG_STRAIGHT": "long straight hair",
    "SHOULDER_LENGTH": "shoulder-length hair",
    "BOB": "bob with bangs",
    "MEDIUM": "medium layered hair",
    "WAVY": "wavy hair",
    "CURLY": "curly hair",
    "BRAIDED": "braided hair",
    "PONYTAIL": "ponytail",
    "HIGH_PONYTAIL": "high ponytail",
    "BANGS": "hair with bangs",
    "FLOWING": "flowing loose hair",
}

SKIN_DETAIL_PROMPTS: dict[str, str] = {
    "FRECKLES": "clearly visible natural freckles densely scattered across the nose bridge and cheeks with realistic skin texture",
    "MOLE": "one small distinct natural mole on the cheek",
    "DIMPLES": "natural clearly visible deep dimples on both cheeks, gently activated by a soft natural smile to reveal them prominently",
    "SINGLE_DIMPLE": "one natural clearly visible deep dimple on a single cheek, gently activated by a soft natural smile to reveal it prominently",
    "CHEEKBONES": "clearly defined high cheekbones with visible structural prominence",
    "CLEAR_SKIN": "clear unmarked skin",
}

AUTO_VARIABLE_OPTIONS: dict[str, list[str]] = {
    "eye_spacing": ["slightly close-set eyes", "balanced eye spacing", "slightly wide-set eyes"],
    "eye_opening": ["a narrow eye opening", "a medium eye opening", "a slightly round eye opening"],
    "brow_shape": ["a straight brow", "a softly arched brow", "a slightly angled brow"],
    "brow_pos": ["a lower brow position", "a higher brow position"],
    "nose_tip": ["a small rounded nose tip", "a small sharper nose tip", "a small soft nose tip"],
    "lip_shape": ["a soft cupid's bow", "a soft lip line"],
    "mouth_width": ["a slightly wider mouth", "a compact mouth"],
    "chin_length": ["a shorter chin", "a balanced chin"],
    "chin_width": ["a narrow chin", "a slightly broader chin"],
    "midface": ["a shorter midface", "a balanced midface"],
}


@dataclass(frozen=True, slots=True)
class CompanionProfilePromptContext:
    """Serializable prompt context for companion profile generation."""

    gender_key: str
    ethnicity_key: str
    mood_key: str
    eye_color_key: str
    face_shape_key: str
    hair_color_key: str
    hair_style_key: str
    skin_detail_key: str


def _roll_auto_variables() -> dict[str, str]:
    """Randomly sample one option from each AUTO_VARIABLE_OPTIONS slot."""
    return {key: random.choice(options) for key, options in AUTO_VARIABLE_OPTIONS.items()}


def build_companion_profile_prompt(context: CompanionProfilePromptContext) -> str:
    """Build the final companion profile generation prompt as a narrative paragraph."""
    gender_text = resolve_option_text(
        GENDER_PROMPTS, context.gender_key, "companion profile gender"
    )
    ethnicity_text = resolve_option_text(
        ETHNICITY_PROMPTS, context.ethnicity_key, "companion profile ethnicity"
    )
    mood_text = resolve_option_text(
        MOOD_PROMPTS, context.mood_key, "companion profile mood"
    )
    eye_color_text = resolve_option_text(
        EYE_COLOR_PROMPTS, context.eye_color_key, "companion profile eye color"
    )
    face_shape_text = resolve_option_text(
        FACE_SHAPE_PROMPTS, context.face_shape_key, "companion profile face shape"
    )
    skin_detail_text = resolve_option_text(
        SKIN_DETAIL_PROMPTS, context.skin_detail_key, "companion profile skin detail"
    )

    hair_color_text = resolve_option_text(
        HAIR_COLOR_PROMPTS, context.hair_color_key, "companion profile hair color"
    )
    if context.gender_key == "MALE":
        hair_style_text = resolve_option_text(
            HAIR_STYLE_MALE_PROMPTS,
            context.hair_style_key,
            "companion profile hair style (male)",
        )
    else:
        hair_style_text = resolve_option_text(
            HAIR_STYLE_FEMALE_PROMPTS,
            context.hair_style_key,
            "companion profile hair style (female)",
        )
    hairstyle_text = f"{hair_color_text} {hair_style_text}".strip()

    auto = _roll_auto_variables()

    subject_paragraph = (
        f"A stunningly attractive late-teen {gender_text.lower()} K-pop idol trainee "
        f"aged 17-19 with {ethnicity_text}. "
        f"The face shows {face_shape_text}, with {eye_color_text}. "
        f"The expression reads {mood_text}. "
        f"The subject has {hairstyle_text} and {skin_detail_text}. "
        f"Subtle micro features include {auto['eye_spacing']} with {auto['eye_opening']}, "
        f"{auto['brow_shape']} at {auto['brow_pos']}, "
        f"{auto['nose_tip']}, "
        f"{auto['lip_shape']} with {auto['mouth_width']}, "
        f"{auto['chin_length']} with {auto['chin_width']}, "
        f"and {auto['midface']}."
    )

    return compose_prompt(
        COMPANION_IMAGE_GENRE_PROMPT,
        subject_paragraph,
        COMPANION_IMAGE_QUALITY_PROMPT,
    )
