import hashlib
import json

PROMPT_VERSION = "v1"

TEMPLATE = (
    "You are a personal assistant.\n\n"
    "User request:\n{request}\n\n"
    "Available options:\n{options}\n\n"
    "Relevant user memories:\n{memories}\n\n"
    "Select exactly one option. Return JSON only with keys: selected_option_id, "
    "decision_factors (list of strings), memory_ids_used (list of memory ids), "
    "confidence (0-1), summary."
)

SYSTEM_PROMPT_HASH = hashlib.sha256(TEMPLATE.encode()).hexdigest()[:16]


def render_options(options: list[dict]) -> str:
    return json.dumps({o["id"]: o["description"] for o in options}, indent=1)


def render_memories(memories: list[dict]) -> str:
    if not memories:
        return "(none)"
    return json.dumps({m["id"]: m["content"] for m in memories}, indent=1)


def build_messages(user_message: str, options: list[dict], memories: list[dict]) -> list[dict]:
    content = TEMPLATE.format(request=user_message, options=render_options(options),
                              memories=render_memories(memories))
    return [{"role": "user", "content": content}]
