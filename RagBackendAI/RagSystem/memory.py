# memory.py — Aquaculture Memory Management
# Two-layer extraction:
#   Layer 1 — LLM-based (accurate, may fail silently)
#   Layer 2 — Regex fallback (always works, zero API calls)
# Both run on every message and results are merged.

import re
import json
from datetime import datetime
# Use relative import to avoid conflict with 'config' package in site-packages
from .config import EMERGENCY_KEYWORDS, EXTRACTION_MODEL, EXTRACT_MAX_TOKENS


# ── Default Memory ─────────────────────────────────────────────
def default_memory() -> dict:
    return {
        "species"              : [],
        "symptoms"             : [],
        "duration"             : "",
        "water_parameters"     : {},
        "pond_type"            : "",
        "treatments_applied"   : [],
        "history"              : [],
        "location"             : "",
        "consultation_date"    : datetime.now().strftime("%Y-%m-%d %H:%M"),
    }


# ══════════════════════════════════════════════════
# LAYER 1 — LLM Extraction
# ══════════════════════════════════════════════════
def _llm_extract(text: str, client) -> dict:
    """Tries LLM-based extraction. Returns {} on any failure."""
    if not client:
        return {}
    try:
        resp = client.chat.completions.create(
            model=EXTRACTION_MODEL,
            max_tokens=EXTRACT_MAX_TOKENS,
            temperature=0.0,
            messages=[{
                "role": "user",
                "content": (
                    "Extract aquaculture data from this text. "
                    "Return ONLY a JSON object. No markdown, no explanation.\n\n"
                    f'Text: "{text}"\n\n'
                    'JSON: {"species":[], "symptoms":[], "duration":"", "water_parameters":{}, '
                    '"pond_type":"", "treatments_applied":[], "history":[], "location":""}'
                )
            }]
        )
        raw = resp.choices[0].message.content.strip()
        raw = re.sub(r"```(?:json)?", "", raw).strip().rstrip("`").strip()
        match = re.search(r'\{.*\}', raw, re.DOTALL)
        if match:
            raw = match.group(0)
        data = json.loads(raw)
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


# ══════════════════════════════════════════════════
# LAYER 2 — Regex Fallback
# ══════════════════════════════════════════════════

_SPECIES_KEYWORDS = [
    "tilapia", "catfish", "carp", "rohu", "mrigal", "catla", "prawn", "shrimp",
    "salmon", "trout", "bass", "pangasius", "clarias", "anabas", "tuna"
]

_SYMPTOM_KEYWORDS = [
    "gasping", "surface breathing", "loss of appetite", "not eating",
    "lesions", "spots", "ulcers", "fin rot", "tail rot", "swollen belly",
    "clamped fins", "flashing", "rubbing", "lethargy", "sluggish",
    "unusual swimming", "whirling", "white spots", "cotton wool", "fungus",
    "cloudy eyes", "pop eye", "mortality", "fish dying"
]

_WATER_PARAM_PATTERNS = {
    "ph": [r'ph\s*(?:is\s+)?(\d+(?:\.\d+)?)'],
    "do": [r'(?:do|oxygen|dissolved\s+oxygen)\s*(?:is\s+)?(\d+(?:\.\d+)?)'],
    "temp": [r'(?:temp|temperature)\s*(?:is\s+)?(\d+(?:\.\d+)?)'],
    "ammonia": [r'ammonia\s*(?:is\s+)?(\d+(?:\.\d+)?)'],
    "nitrate": [r'nitrate\s*(?:is\s+)?(\d+(?:\.\d+)?)'],
}

_POND_TYPE_KEYWORDS = [
    "earthen pond", "concrete tank", "raceway", "biofloc", "ras", "cage", "pen"
]

_TREATMENT_KEYWORDS = [
    "lime", "salt", "potassium permanganate", "kmno4", "formalin", "oxytetracycline",
    "probiotics", "zeolite", "bkc", "iodine"
]


def _regex_extract(text: str) -> dict:
    t = text.lower()
    result = default_memory()
    result.pop("consultation_date") # not needed for extraction

    # Species
    for sp in _SPECIES_KEYWORDS:
        if re.search(r'\b' + re.escape(sp) + r'\b', t):
            result["species"].append(sp)

    # Symptoms
    for sym in _SYMPTOM_KEYWORDS:
        if sym in t:
            result["symptoms"].append(sym)

    # Water Params
    for param, patterns in _WATER_PARAM_PATTERNS.items():
        for pattern in patterns:
            m = re.search(pattern, t)
            if m:
                result["water_parameters"][param] = m.group(1)
                break

    # Pond Type
    for pt in _POND_TYPE_KEYWORDS:
        if pt in t:
            result["pond_type"] = pt
            break

    # Treatments
    for tr in _TREATMENT_KEYWORDS:
        if tr in t:
            result["treatments_applied"].append(tr)

    return result


def extract_entities(text: str, client) -> dict:
    regex_data = _regex_extract(text)
    llm_data   = _llm_extract(text, client)

    merged      = {}
    list_fields = ["species", "symptoms", "treatments_applied", "history"]
    str_fields  = ["duration", "pond_type", "location"]

    for field in list_fields:
        llm_val   = llm_data.get(field, []) or []
        regex_val = regex_data.get(field, []) or []
        merged[field] = list(set(llm_val) | set(regex_val))

    for field in str_fields:
        llm_val   = (llm_data.get(field, "") or "").strip()
        regex_val = (regex_data.get(field, "") or "").strip()
        merged[field] = llm_val if llm_val else regex_val

    regex_params = regex_data.get("water_parameters", {}) or {}
    llm_params   = llm_data.get("water_parameters", {}) or {}
    merged["water_parameters"] = {**regex_params, **llm_params}

    return merged


def update_memory(memory: dict, new_data: dict) -> dict:
    list_fields = ["species", "symptoms", "treatments_applied", "history"]
    str_fields  = ["duration", "pond_type", "location"]

    for field in list_fields:
        if new_data.get(field):
            existing = set(memory.get(field, []))
            existing.update(new_data[field])
            memory[field] = list(existing)

    for field in str_fields:
        if new_data.get(field):
            memory[field] = new_data[field]

    if new_data.get("water_parameters"):
        memory["water_parameters"].update(new_data["water_parameters"])
    return memory


def is_emergency(text: str) -> bool:
    # Use config keywords, or just basic ones here
    emergency_kws = ["mass mortality", "dying", "floating", "gasping", "poisoning"]
    return any(kw in text.lower() for kw in emergency_kws)


def memory_has_data(memory: dict) -> bool:
    return any([
        memory.get("species"),
        memory.get("symptoms"),
        memory.get("water_parameters"),
        memory.get("pond_type"),
    ])
