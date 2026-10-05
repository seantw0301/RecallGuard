from dataclasses import dataclass
from typing import Protocol


@dataclass
class ChatResult:
    text: str
    model: str
    latency_ms: int
    attempts: int = 1


class NebiusError(Exception):
    def __init__(self, kind: str, message: str):
        super().__init__(f"{kind}: {message}")
        self.kind = kind  # AUTH | RATE_LIMIT | TIMEOUT | SERVER | BAD_RESPONSE


class LLM(Protocol):
    def chat_json(self, messages: list[dict]) -> ChatResult: ...
