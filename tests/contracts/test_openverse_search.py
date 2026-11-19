"""``openverse_search`` contract: auth, attribution, downloads and credits.

The network is replaced by a fake ``urlopen`` so these run offline. What must
hold:

1. Anonymous by default: no token request, no Authorization header.
2. With OPENVERSE_CLIENT_ID/SECRET, a token is fetched with a form-encoded
   client_credentials POST, cached across calls, and refreshed once on a 401.
3. Every result carries url/title/creator/license/license_url/source_url and
   an attribution string; HTML-escaped names are decoded.
4. Downloads land in projects/<id>/assets/audio, use a real extension (Jamendo
   reports "mp32"), and append each attribution to credits.md exactly once.
"""

from __future__ import annotations

import io
import json
import urllib.error
import urllib.parse
from email.message import Message

import pytest

from tools.audio import openverse_search as ov
from tools.audio.openverse_search import OpenverseSearch


def _result(**overrides):
    r = {
        "id": "328cd1a8-2945-44f1-9384-027bf2d0bd9b",
        "title": "Guitar Mix (Rain)",
        "creator": "Freeky Cleen &amp; Dickey",
        "url": "https://files.example.invalid/?trackid=1&format=mp32",
        "foreign_landing_url": "https://www.jamendo.com/track/389520",
        "license": "by",
        "license_version": "3.0",
        "license_url": "https://creativecommons.org/licenses/by/3.0/",
        "source": "jamendo",
        "filetype": "mp32",
        "duration": 113000,
        "attribution": '"Guitar Mix (Rain)" by Freeky Cleen &amp; Dickey is licensed under CC BY 3.0.',
    }
    r.update(overrides)
    return r


class _Resp(io.BytesIO):
    def __init__(self, payload: bytes, content_type: str = "application/json"):
        super().__init__(payload)
        self.headers = Message()
        self.headers["Content-Type"] = content_type

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return None


class _FakeNet:
    def __init__(self, search_payload, token_responses=None, search_errors=None):
        self.search_payload = search_payload
        self.token_responses = list(token_responses or [])
        self.search_errors = list(search_errors or [])
        self.calls = []

    def __call__(self, req, timeout=None):
        url = req.full_url
        self.calls.append(req)
        if url.endswith("/auth_tokens/token/"):
            return _Resp(json.dumps(self.token_responses.pop(0)).encode())
        if "api.openverse.org" in url:
            if self.search_errors:
                code = self.search_errors.pop(0)
                raise urllib.error.HTTPError(url, code, "err", Message(), io.BytesIO(b"{}"))
            return _Resp(json.dumps(self.search_payload).encode())
        return _Resp(b"ID3fake-mp3-bytes", content_type="audio/mpeg")


@pytest.fixture(autouse=True)
def _reset(monkeypatch, tmp_path):
    OpenverseSearch._token_cache.clear()
    monkeypatch.delenv("OPENVERSE_CLIENT_ID", raising=False)
    monkeypatch.delenv("OPENVERSE_CLIENT_SECRET", raising=False)
    monkeypatch.chdir(tmp_path)


def _payload():
    return {"result_count": 1, "page_count": 1, "results": [_result()]}


def test_anonymous_search_shapes_results(monkeypatch):
    net = _FakeNet(_payload())
    monkeypatch.setattr(ov.urllib.request, "urlopen", net)

    res = OpenverseSearch().execute({"q": "rain", "license_type": "commercial", "page_size": 5})

    assert res.success, res.error
    assert res.data["auth_mode"] == "anonymous"
    assert len(net.calls) == 1 and net.calls[0].get_header("Authorization") is None
    query = urllib.parse.parse_qs(urllib.parse.urlparse(net.calls[0].full_url).query)
    assert query == {"q": ["rain"], "page_size": ["5"], "license_type": ["commercial"]}
    item = res.data["results"][0]
    for key in ("url", "title", "creator", "license", "license_url", "source_url", "attribution"):
        assert item[key]
    assert item["creator"] == "Freeky Cleen & Dickey"
    assert item["license"] == "CC BY 3.0"
    assert "&amp;" not in item["attribution"]
    assert item["attribution"].endswith("Source: https://www.jamendo.com/track/389520")


def test_image_media_type_uses_images_endpoint(monkeypatch):
    net = _FakeNet(_payload())
    monkeypatch.setattr(ov.urllib.request, "urlopen", net)
    assert OpenverseSearch().execute({"q": "ruins", "media_type": "image"}).success
    assert "/v1/images/?" in net.calls[0].full_url


def test_token_is_cached_and_refreshed_on_401(monkeypatch):
    monkeypatch.setenv("OPENVERSE_CLIENT_ID", "cid")
    monkeypatch.setenv("OPENVERSE_CLIENT_SECRET", "csecret")
    net = _FakeNet(
        _payload(),
        token_responses=[
            {"access_token": "t1", "expires_in": 36000},
            {"access_token": "t2", "expires_in": 36000},
        ],
    )
    monkeypatch.setattr(ov.urllib.request, "urlopen", net)
    tool = OpenverseSearch()

    assert tool.execute({"q": "rain"}).success
    assert tool.execute({"q": "rain"}).success  # cached: no second token call
    token_calls = [c for c in net.calls if c.full_url.endswith("/auth_tokens/token/")]
    assert len(token_calls) == 1
    body = urllib.parse.parse_qs(token_calls[0].data.decode())
    assert body == {"grant_type": ["client_credentials"], "client_id": ["cid"], "client_secret": ["csecret"]}
    assert token_calls[0].get_header("Content-type") == "application/x-www-form-urlencoded"
    assert net.calls[-1].get_header("Authorization") == "Bearer t1"

    net.search_errors = [401]
    assert tool.execute({"q": "rain"}).success
    assert net.calls[-1].get_header("Authorization") == "Bearer t2"


def test_download_writes_asset_and_credits_once(monkeypatch, tmp_path):
    net = _FakeNet(_payload())
    monkeypatch.setattr(ov.urllib.request, "urlopen", net)
    tool = OpenverseSearch()
    inputs = {"q": "rain", "download": [0], "project_id": "the-last-of-men"}

    first = tool.execute(inputs)
    second = tool.execute(inputs)

    assert first.success and second.success, (first.error, second.error)
    path = tmp_path / first.artifacts[0]
    assert path.parent == tmp_path / "projects/the-last-of-men/assets/audio"
    assert path.suffix == ".mp3"
    credits = (tmp_path / "projects/the-last-of-men/credits.md").read_text()
    assert credits.count("Guitar Mix (Rain)") == 1
    assert path.name in credits


def test_download_requires_destination(monkeypatch):
    monkeypatch.setattr(ov.urllib.request, "urlopen", _FakeNet(_payload()))
    res = OpenverseSearch().execute({"q": "rain", "download": [0]})
    assert not res.success and "project_id" in res.error
