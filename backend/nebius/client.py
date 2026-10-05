import time

import httpx

from backend.config import settings
from backend.nebius.models import ChatResult, NebiusError


class NebiusClient:
    """OpenAI-compatible chat client for Nebius Token Factory (Nemotron)."""

    def __init__(self, api_key: str, model: str, base_url: str, timeout_s: float = 60.0,
                 transport: httpx.BaseTransport | None = None, backoff_s: float = 1.0):
        if not (api_key and model and base_url):
            raise NebiusError("AUTH", "NEBIUS_API_KEY / NEBIUS_MODEL / NEBIUS_BASE_URL not set")
        self.model = model
        self.backoff_s = backoff_s
        self._http = httpx.Client(
            base_url=base_url.rstrip("/"), timeout=timeout_s, transport=transport,
            headers={"Authorization": f"Bearer {api_key}"},
        )

    def chat_json(self, messages: list[dict]) -> ChatResult:
        body = {"model": self.model, "temperature": 0, "max_tokens": 2000,
                "messages": messages, "response_format": {"type": "json_object"}}
        last: NebiusError | None = None
        t0 = time.time()
        for attempt in range(1, 4):
            try:
                r = self._http.post("/chat/completions", json=body)
            except httpx.TimeoutException:
                last = NebiusError("TIMEOUT", "request timed out")
            except httpx.HTTPError as e:
                last = NebiusError("SERVER", str(e))
            else:
                if r.status_code in (401, 403):
                    raise NebiusError("AUTH", f"HTTP {r.status_code}")
                if r.status_code == 429:
                    last = NebiusError("RATE_LIMIT", "HTTP 429")
                elif r.status_code >= 500:
                    last = NebiusError("SERVER", f"HTTP {r.status_code}")
                elif r.status_code >= 400:
                    raise NebiusError("BAD_RESPONSE", f"HTTP {r.status_code}: {r.text[:200]}")
                else:
                    try:
                        data = r.json()
                        text = data["choices"][0]["message"]["content"] or ""
                    except (ValueError, KeyError, IndexError) as e:
                        raise NebiusError("BAD_RESPONSE", f"malformed body: {e!r}")
                    return ChatResult(text=text, model=data.get("model", self.model),
                                      latency_ms=int((time.time() - t0) * 1000), attempts=attempt)
            if attempt < 3:
                time.sleep(self.backoff_s * 2 ** (attempt - 1))
        raise last  # type: ignore[misc]


def get_llm() -> NebiusClient:
    s = settings()
    return NebiusClient(s.api_key, s.model, s.base_url, s.timeout_s)
