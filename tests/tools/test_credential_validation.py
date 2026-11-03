"""Opt-in API-key validation for preflight, using mocked HTTP responses.

No network: every probe goes through a fake ``http_get``, and the default
transport is replaced with one that fails the test if anything reaches it
unexpectedly.

Run: pytest tests/tools/test_credential_validation.py -v
"""

from __future__ import annotations

import json
import os
from typing import Any

import pytest

from tools import credential_validation as cv
from tools.base_tool import BaseTool, ToolResult, ToolStatus
from tools.tool_registry import ToolRegistry

PLACEHOLDER_GEMINI = "abc123"
PLACEHOLDER_PEXELS = "xyz789"
REAL_GEMINI = "AIzaSy-real-looking-gemini-key-0001"
REAL_PEXELS = "real-looking-pexels-key-0002"

GEMINI_INVALID_BODY = json.dumps(
    {
        "error": {
            "code": 400,
            "message": "API key not valid. Please pass a valid API key.",
            "status": "INVALID_ARGUMENT",
            "details": [{"reason": "API_KEY_INVALID", "domain": "googleapis.com"}],
        }
    }
)
PEXELS_INVALID_BODY = json.dumps(
    {"status": 401, "code": "Unauthorized", "message": "Invalid API key"}
)


class FakeResponse:
    def __init__(self, status_code: int, text: str = "") -> None:
        self.status_code = status_code
        self.text = text


class FakeHttp:
    """Answers by (url, key) and records every call."""

    def __init__(self, valid_keys: set[str] | None = None) -> None:
        self.valid_keys = valid_keys or set()
        self.calls: list[dict[str, Any]] = []
        self.overrides: dict[str, Any] = {}

    def _key_from(self, headers: dict, params: dict) -> str:
        auth = headers.get("x-goog-api-key") or headers.get("Authorization") or ""
        for prefix in ("Bearer ", "Key "):
            if auth.startswith(prefix):
                auth = auth[len(prefix):]
        return auth or params.get("key", "")

    def __call__(self, url: str, *, headers=None, params=None, timeout=None):
        headers, params = headers or {}, params or {}
        self.calls.append({"url": url, "headers": headers, "params": params, "timeout": timeout})
        if url in self.overrides:
            result = self.overrides[url]
            if isinstance(result, Exception):
                raise result
            return result
        key = self._key_from(headers, params)
        if key in self.valid_keys:
            return FakeResponse(200, "{}")
        if "generativelanguage" in url:
            return FakeResponse(400, GEMINI_INVALID_BODY)
        return FakeResponse(401, PEXELS_INVALID_BODY)


@pytest.fixture(autouse=True)
def isolated_env(monkeypatch):
    """No real keys, no .env, empty cache, and no real transport."""
    for name in cv.supported_env_vars() + ["GOOGLE_APPLICATION_CREDENTIALS"]:
        monkeypatch.delenv(name, raising=False)
    monkeypatch.setattr(ToolRegistry, "_load_dotenv", staticmethod(lambda: None))

    def _no_real_http(*_a, **_k):
        raise AssertionError("credential validation reached the real transport")

    monkeypatch.setattr(cv, "_default_http_get", _no_real_http)
    cv.clear_cache()
    yield
    cv.clear_cache()


# ---- module-level probes ----------------------------------------------------


def test_placeholder_gemini_key_is_invalid_and_never_echoed(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", PLACEHOLDER_GEMINI)
    http = FakeHttp()

    result = cv.validate_credentials(http_get=http)

    check = result["GEMINI_API_KEY"]
    assert check["status"] == cv.INVALID
    assert check["family"] == "gemini"
    assert check["http_status"] == 400
    assert "API_KEY_INVALID" in check["detail"]
    assert PLACEHOLDER_GEMINI not in json.dumps(result)
    # Read-only list-models call with the key in a header, not the URL.
    (call,) = http.calls
    assert call["url"].endswith("/v1beta/models")
    assert call["headers"] == {"x-goog-api-key": PLACEHOLDER_GEMINI}
    assert call["params"] == {"pageSize": 1}


def test_placeholder_pexels_key_is_invalid(monkeypatch):
    monkeypatch.setenv("PEXELS_API_KEY", PLACEHOLDER_PEXELS)
    http = FakeHttp()

    check = cv.validate_credentials(http_get=http)["PEXELS_API_KEY"]

    assert check["status"] == cv.INVALID
    assert check["http_status"] == 401
    (call,) = http.calls
    assert call["params"]["per_page"] == 1


def test_valid_keys_are_valid(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", REAL_GEMINI)
    monkeypatch.setenv("PEXELS_API_KEY", REAL_PEXELS)
    http = FakeHttp(valid_keys={REAL_GEMINI, REAL_PEXELS})

    result = cv.validate_credentials(http_get=http)

    assert {k: v["status"] for k, v in result.items()} == {
        "GEMINI_API_KEY": cv.VALID,
        "PEXELS_API_KEY": cv.VALID,
    }


def test_unset_vars_are_skipped_without_any_request():
    http = FakeHttp()
    assert cv.validate_credentials(http_get=http) == {}
    assert http.calls == []


def test_results_are_cached_per_process_and_keyed_by_value(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", PLACEHOLDER_GEMINI)
    http = FakeHttp(valid_keys={REAL_GEMINI})

    cv.validate_credentials(http_get=http)
    cv.validate_credentials(http_get=http)
    assert len(http.calls) == 1  # second call served from cache

    cv.validate_credentials(http_get=http, force=True)
    assert len(http.calls) == 2  # force bypasses the cache

    monkeypatch.setenv("GEMINI_API_KEY", REAL_GEMINI)  # key edited in .env
    assert cv.validate_credentials(http_get=http)["GEMINI_API_KEY"]["status"] == cv.VALID
    assert len(http.calls) == 3

    # The cache never holds the key itself.
    cached = repr(cv._cache)
    assert PLACEHOLDER_GEMINI not in cached and REAL_GEMINI not in cached


def test_network_failure_is_unverified_uncached_and_does_not_leak(monkeypatch):
    monkeypatch.setenv("PIXABAY_API_KEY", "pixabay-secret-123")
    http = FakeHttp()
    # requests puts the full URL, including ?key=..., in exception messages.
    http.overrides["https://pixabay.com/api/"] = ConnectionError(
        "Max retries exceeded with url: /api/?key=pixabay-secret-123&q=nature"
    )

    check = cv.validate_credentials(http_get=http)["PIXABAY_API_KEY"]

    assert check["status"] == cv.UNVERIFIED
    assert check["http_status"] is None
    assert "ConnectionError" in check["detail"]
    assert "pixabay-secret-123" not in json.dumps(check)

    cv.validate_credentials(http_get=http)
    assert len(http.calls) == 2  # transport failures are retried, not cached


@pytest.mark.parametrize(
    "env_var, status_code, body, expected",
    [
        # Gemini: real key restricted to other Google APIs -> don't call it invalid.
        ("GEMINI_API_KEY", 403, '{"error": {"status": "PERMISSION_DENIED"}}', cv.UNVERIFIED),
        ("GEMINI_API_KEY", 400, '{"error": {"status": "INVALID_ARGUMENT"}}', cv.UNVERIFIED),
        ("GEMINI_API_KEY", 503, "", cv.UNVERIFIED),
        ("PEXELS_API_KEY", 429, "", cv.UNVERIFIED),
        ("PIXABAY_API_KEY", 400, "[ERROR 400] Invalid or missing API key", cv.INVALID),
        ("FAL_KEY", 401, '{"detail": "Unauthorized"}', cv.INVALID),
        ("FAL_KEY", 200, '{"models": []}', cv.VALID),
        ("OPENAI_API_KEY", 401, '{"error": {"code": "invalid_api_key"}}', cv.INVALID),
        # Valid project key without the model-read scope -> not "invalid".
        ("OPENAI_API_KEY", 401, '{"error": {"message": "Missing scopes"}}', cv.UNVERIFIED),
        ("REPLICATE_API_TOKEN", 401, '{"detail": "Invalid token."}', cv.INVALID),
    ],
)
def test_classification_is_conservative(monkeypatch, env_var, status_code, body, expected):
    monkeypatch.setenv(env_var, "some-key-value")
    http = FakeHttp()
    http.overrides[cv.PROBES_BY_ENV[env_var].url] = FakeResponse(status_code, body)

    assert cv.validate_credentials(http_get=http)[env_var]["status"] == expected


# ---- registry integration -------------------------------------------------


class _EnvTool(BaseTool):
    """Mimics provider tools that override get_status with an env check."""

    env_vars: tuple[str, ...] = ()

    def get_status(self) -> ToolStatus:
        if any(os.environ.get(v) for v in self.env_vars):
            return ToolStatus.AVAILABLE
        return ToolStatus.UNAVAILABLE

    def execute(self, inputs: dict[str, Any]) -> ToolResult:  # pragma: no cover
        return ToolResult(success=True)


class FakeImagen(_EnvTool):
    name = "fake_imagen"
    capability = "image_generation"
    provider = "google_imagen"
    env_vars = ("GOOGLE_API_KEY", "GEMINI_API_KEY")
    install_instructions = "Set GEMINI_API_KEY in .env"


class FakeGeminiTTS(_EnvTool):
    name = "fake_gemini_tts"
    capability = "tts"
    provider = "gemini"
    env_vars = ("GEMINI_API_KEY",)


class FakePexelsVideo(_EnvTool):
    name = "fake_pexels_video"
    capability = "video_generation"
    provider = "pexels"
    env_vars = ("PEXELS_API_KEY",)
    install_instructions = "Set PEXELS_API_KEY in .env"


class FakeLocal(BaseTool):
    name = "fake_local"
    capability = "image_generation"
    provider = "local"

    def execute(self, inputs: dict[str, Any]) -> ToolResult:  # pragma: no cover
        return ToolResult(success=True)


@pytest.fixture
def reg() -> ToolRegistry:
    registry = ToolRegistry()
    registry._discovered_packages.add("tools")  # skip real discovery
    for cls in (FakeImagen, FakeGeminiTTS, FakePexelsVideo, FakeLocal):
        registry.register(cls())
    return registry


def _cap(summary: dict, name: str) -> dict:
    return next(c for c in summary["capabilities"] if c["capability"] == name)


def test_default_summary_stays_offline(monkeypatch, reg):
    monkeypatch.setenv("GEMINI_API_KEY", PLACEHOLDER_GEMINI)
    monkeypatch.setenv("PEXELS_API_KEY", PLACEHOLDER_PEXELS)

    summary = reg.provider_menu_summary()  # _default_http_get would raise

    assert "credential_checks" not in summary
    assert _cap(summary, "image_generation")["configured"] == 2
    assert _cap(summary, "tts")["configured"] == 1


def test_placeholder_keys_surface_as_warnings_and_unavailable(monkeypatch, reg):
    monkeypatch.setenv("GEMINI_API_KEY", PLACEHOLDER_GEMINI)
    monkeypatch.setenv("PEXELS_API_KEY", PLACEHOLDER_PEXELS)
    http = FakeHttp()
    monkeypatch.setattr(cv, "_default_http_get", http)

    summary = reg.provider_menu_summary(validate_keys=True)

    warnings = summary["runtime_warnings"]
    gemini_warning = next(w for w in warnings if w.startswith("GEMINI_API_KEY:"))
    pexels_warning = next(w for w in warnings if w.startswith("PEXELS_API_KEY:"))
    assert "fake_imagen" in gemini_warning and "fake_gemini_tts" in gemini_warning
    assert "fake_pexels_video" in pexels_warning
    # Env var names only, never values.
    dumped = json.dumps(summary)
    assert PLACEHOLDER_GEMINI not in dumped and PLACEHOLDER_PEXELS not in dumped

    image = _cap(summary, "image_generation")
    assert image["configured"] == 1  # only the local tool is left
    assert "google_imagen" in image["unavailable_providers"]
    assert _cap(summary, "tts")["configured"] == 0
    assert _cap(summary, "video_generation")["configured"] == 0

    offers = {o["tool"]: o for o in summary["setup_offers"]}
    assert offers["fake_imagen"]["kind"] == "invalid_credential"
    assert offers["fake_imagen"]["env_vars"] == ["GEMINI_API_KEY"]
    assert offers["fake_pexels_video"]["env_vars"] == ["PEXELS_API_KEY"]

    assert summary["credential_checks"]["GEMINI_API_KEY"]["status"] == cv.INVALID

    # Environment restored after the availability re-check.
    assert os.environ["GEMINI_API_KEY"] == PLACEHOLDER_GEMINI
    assert os.environ["PEXELS_API_KEY"] == PLACEHOLDER_PEXELS


def test_provider_menu_marks_credential_issue(monkeypatch, reg):
    monkeypatch.setenv("PEXELS_API_KEY", PLACEHOLDER_PEXELS)
    monkeypatch.setattr(cv, "_default_http_get", FakeHttp())

    menu = reg.provider_menu(validate_keys=True)

    (entry,) = menu["video_generation"]["unavailable"]
    assert entry["status"] == "unavailable"
    assert entry["credential_issue"]["kind"] == "invalid_api_key"
    assert entry["credential_issue"]["env_vars"] == ["PEXELS_API_KEY"]
    assert menu["video_generation"]["configured"] == 0


def test_valid_keys_are_unaffected(monkeypatch, reg):
    monkeypatch.setenv("GEMINI_API_KEY", REAL_GEMINI)
    monkeypatch.setenv("PEXELS_API_KEY", REAL_PEXELS)
    monkeypatch.setattr(
        cv, "_default_http_get", FakeHttp(valid_keys={REAL_GEMINI, REAL_PEXELS})
    )

    baseline = reg.provider_menu_summary()
    validated = reg.provider_menu_summary(validate_keys=True)

    assert validated["capabilities"] == baseline["capabilities"]
    assert validated["setup_offers"] == baseline["setup_offers"]
    assert validated["runtime_warnings"] == baseline["runtime_warnings"]
    assert {v["status"] for v in validated["credential_checks"].values()} == {cv.VALID}


def test_tool_with_another_valid_credential_stays_available(monkeypatch, reg):
    monkeypatch.setenv("GEMINI_API_KEY", PLACEHOLDER_GEMINI)  # invalid
    monkeypatch.setenv("GOOGLE_API_KEY", REAL_GEMINI)  # valid
    monkeypatch.setattr(cv, "_default_http_get", FakeHttp(valid_keys={REAL_GEMINI}))

    menu = reg.provider_menu(validate_keys=True)

    assert {e["name"] for e in menu["image_generation"]["available"]} == {
        "fake_imagen",
        "fake_local",
    }
    (tts,) = menu["tts"]["unavailable"]  # GEMINI_API_KEY was its only path
    assert tts["name"] == "fake_gemini_tts"


def test_unverified_key_warns_but_keeps_tools_available(monkeypatch, reg):
    monkeypatch.setenv("PEXELS_API_KEY", REAL_PEXELS)
    http = FakeHttp()
    http.overrides[cv.PROBES_BY_ENV["PEXELS_API_KEY"].url] = TimeoutError("timed out")
    monkeypatch.setattr(cv, "_default_http_get", http)

    summary = reg.provider_menu_summary(validate_keys=True)

    assert _cap(summary, "video_generation")["configured"] == 1
    assert any(
        w.startswith("PEXELS_API_KEY: could not verify") for w in summary["runtime_warnings"]
    )
