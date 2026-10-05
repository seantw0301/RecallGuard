import httpx
import pytest

from backend.nebius.client import NebiusClient
from backend.nebius.models import NebiusError


def _client(handler):
    return NebiusClient("k", "m", "http://x/v1", transport=httpx.MockTransport(handler), backoff_s=0)


def _ok():
    return httpx.Response(200, json={"model": "m", "choices": [{"message": {"content": "{}"}}]})


def test_retries_transient_then_succeeds():
    seq = iter([httpx.Response(429), httpx.Response(503), _ok()])
    r = _client(lambda req: next(seq)).chat_json([{"role": "user", "content": "hi"}])
    assert r.attempts == 3 and r.text == "{}"


def test_auth_error_not_retried():
    n = []
    def h(req):
        n.append(1)
        return httpx.Response(401)
    with pytest.raises(NebiusError) as e:
        _client(h).chat_json([])
    assert e.value.kind == "AUTH" and len(n) == 1


def test_gives_up_after_three():
    with pytest.raises(NebiusError) as e:
        _client(lambda req: httpx.Response(500)).chat_json([])
    assert e.value.kind == "SERVER"
