"""Opt-in, read-only API-key validation for preflight.

Tool availability (``BaseTool.get_status``) only checks that an env var is
*set*. A placeholder such as ``GEMINI_API_KEY=abc123`` therefore reports the
Gemini tools as available, and the failure surfaces mid-production as
``400 API_KEY_INVALID``. This module asks each provider whether the key is
real, using one free, read-only request per provider family:

    Gemini / Google AI Studio   GET /v1beta/models?pageSize=1   (list models)
    Pexels                      GET /v1/search?per_page=1       (1-result search)
    Pixabay                     GET /api/?per_page=3            (3 is its minimum)
    fal.ai                      GET /v1/models?limit=1          (platform API)
    OpenAI                      GET /v1/models                  (list models)
    Replicate                   GET /v1/account                 (whoami)

None of these generate anything or spend credits.

Guarantees:

* **Opt-in.** Nothing here runs unless a caller asks for it
  (``registry.validate_credentials()`` or
  ``registry.provider_menu_summary(validate_keys=True)``), so the default
  preflight path, and the test suite, stays offline.
* **Never leaks a key.** Results carry the env var *name* only. Exception
  messages, which can echo a URL with a key in its query string, are reduced
  to the exception class name.
* **Cached per process.** The result is cached under the env var name plus a
  SHA-256 digest of the value. The value itself is never stored, and editing
  the key in ``.env`` triggers a fresh check. Transport failures, where no
  HTTP answer came back, are not cached, so a retry after the network
  recovers gets a real verdict.
* **Conservative.** Only an answer that clearly rejects the key, such as
  401 or Gemini's ``API_KEY_INVALID``, marks it ``invalid``. A network error,
  a blocked proxy, a 403, a 429 or a 5xx is reported as ``unverified``, so a
  flaky network never hides a working key.
"""

from __future__ import annotations

import hashlib
import os
import threading
from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict, dataclass
from typing import Any, Callable, Iterable, Optional

VALID = "valid"
INVALID = "invalid"
UNVERIFIED = "unverified"

DEFAULT_TIMEOUT_SECONDS = 5.0

# (status, detail) produced by a probe's classifier from (http_status, body).
Classification = tuple[str, str]


@dataclass(frozen=True)
class CredentialProbe:
    """How to ask one provider whether a key is real, without spending credits."""

    env_var: str
    family: str
    url: str
    build_headers: Callable[[str], dict[str, str]]
    build_params: Callable[[str], dict[str, Any]]
    classify: Callable[[int, str], Classification]


@dataclass(frozen=True)
class CredentialCheck:
    """Outcome of validating one env var. Never contains the key itself."""

    env_var: str
    family: str
    status: str  # VALID | INVALID | UNVERIFIED
    http_status: Optional[int]
    detail: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


# ---- classifiers ----------------------------------------------------------


def _classify_common(code: int, body: str) -> Classification:
    if 200 <= code < 300:
        return VALID, "key accepted"
    if code == 401:
        return INVALID, "HTTP 401 unauthenticated"
    if code == 403:
        return UNVERIFIED, (
            "key recognised but refused for the check endpoint (HTTP 403); "
            "it may be restricted or lack permissions"
        )
    if code == 429:
        return UNVERIFIED, "rate limited during the check (HTTP 429)"
    return UNVERIFIED, f"unexpected HTTP {code} from the check endpoint"


def _classify_gemini(code: int, body: str) -> Classification:
    # A key that doesn't exist gets 400 INVALID_ARGUMENT with reason
    # API_KEY_INVALID, not 401.
    if code == 400 and ("API_KEY_INVALID" in body or "API key not valid" in body):
        return INVALID, "HTTP 400 API_KEY_INVALID"
    if code == 403:
        # Real key, but the Generative Language API is disabled or the key is
        # restricted to other Google APIs (e.g. a Cloud TTS-only key).
        return UNVERIFIED, (
            "key exists but the Gemini API refused it (HTTP 403); it may be "
            "restricted to other Google APIs or the API is not enabled"
        )
    return _classify_common(code, body)


def _classify_pixabay(code: int, body: str) -> Classification:
    if code == 400 and "api key" in body.lower():
        return INVALID, "HTTP 400 invalid API key"
    return _classify_common(code, body)


def _classify_openai(code: int, body: str) -> Classification:
    # OpenAI also answers 401 for valid project keys that lack the
    # model-read scope. Only the explicit code means "this key is not real".
    if code == 401:
        if "invalid_api_key" in body or "Incorrect API key" in body:
            return INVALID, "HTTP 401 invalid_api_key"
        return UNVERIFIED, (
            "key refused for the model-list endpoint (HTTP 401) without "
            "invalid_api_key; it may be a restricted project key"
        )
    return _classify_common(code, body)


# ---- probe table ----------------------------------------------------------

_GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models"


def _no_params(_key: str) -> dict[str, Any]:
    return {}


PROBES: tuple[CredentialProbe, ...] = (
    CredentialProbe(
        env_var="GEMINI_API_KEY",
        family="gemini",
        url=_GEMINI_URL,
        build_headers=lambda key: {"x-goog-api-key": key},
        build_params=lambda _key: {"pageSize": 1},
        classify=_classify_gemini,
    ),
    CredentialProbe(
        env_var="GOOGLE_API_KEY",
        family="gemini",
        url=_GEMINI_URL,
        build_headers=lambda key: {"x-goog-api-key": key},
        build_params=lambda _key: {"pageSize": 1},
        classify=_classify_gemini,
    ),
    CredentialProbe(
        env_var="PEXELS_API_KEY",
        family="pexels",
        url="https://api.pexels.com/v1/search",
        build_headers=lambda key: {"Authorization": key},
        build_params=lambda _key: {"query": "nature", "per_page": 1},
        classify=_classify_common,
    ),
    CredentialProbe(
        env_var="PIXABAY_API_KEY",
        family="pixabay",
        url="https://pixabay.com/api/",
        build_headers=lambda _key: {},
        build_params=lambda key: {"key": key, "q": "nature", "per_page": 3},
        classify=_classify_pixabay,
    ),
    CredentialProbe(
        env_var="FAL_KEY",
        family="fal",
        url="https://api.fal.ai/v1/models",
        build_headers=lambda key: {"Authorization": f"Key {key}"},
        build_params=lambda _key: {"limit": 1},
        classify=_classify_common,
    ),
    CredentialProbe(
        env_var="OPENAI_API_KEY",
        family="openai",
        url="https://api.openai.com/v1/models",
        build_headers=lambda key: {"Authorization": f"Bearer {key}"},
        build_params=_no_params,
        classify=_classify_openai,
    ),
    CredentialProbe(
        env_var="REPLICATE_API_TOKEN",
        family="replicate",
        url="https://api.replicate.com/v1/account",
        build_headers=lambda key: {"Authorization": f"Bearer {key}"},
        build_params=_no_params,
        classify=_classify_common,
    ),
)

PROBES_BY_ENV: dict[str, CredentialProbe] = {p.env_var: p for p in PROBES}


def supported_env_vars() -> list[str]:
    """Env vars this module knows how to validate."""
    return [p.env_var for p in PROBES]


# ---- transport + cache ----------------------------------------------------

HttpGet = Callable[..., Any]

_cache: dict[tuple[str, str], CredentialCheck] = {}
_cache_lock = threading.Lock()


def clear_cache() -> None:
    """Forget every cached result (tests, or after rotating keys)."""
    with _cache_lock:
        _cache.clear()


def _digest(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _default_http_get(url: str, **kwargs: Any) -> Any:
    import requests  # lazy: keep import-time cost off the registry

    return requests.get(url, **kwargs)


def _run_probe(
    probe: CredentialProbe, key: str, timeout: float, http_get: HttpGet
) -> CredentialCheck:
    try:
        response = http_get(
            probe.url,
            headers=probe.build_headers(key),
            params=probe.build_params(key),
            timeout=timeout,
        )
    except Exception as exc:  # noqa: BLE001 - any transport failure is "unverified"
        # Do not interpolate str(exc): requests embeds the full URL, which for
        # query-string auth (Pixabay) contains the key.
        return CredentialCheck(
            env_var=probe.env_var,
            family=probe.family,
            status=UNVERIFIED,
            http_status=None,
            detail=f"could not reach the {probe.family} check endpoint ({type(exc).__name__})",
        )

    code = int(getattr(response, "status_code", 0) or 0)
    try:
        body = str(getattr(response, "text", "") or "")
    except Exception:  # noqa: BLE001
        body = ""
    status, detail = probe.classify(code, body)
    return CredentialCheck(
        env_var=probe.env_var,
        family=probe.family,
        status=status,
        http_status=code or None,
        detail=detail,
    )


def validate_credentials(
    env_vars: Optional[Iterable[str]] = None,
    *,
    force: bool = False,
    timeout: float = DEFAULT_TIMEOUT_SECONDS,
    http_get: Optional[HttpGet] = None,
) -> dict[str, dict[str, Any]]:
    """Validate configured API keys with free, read-only provider calls.

    Args:
        env_vars: Restrict to these env var names. Defaults to every
            supported env var. Unset or empty vars are skipped (there is
            nothing to validate), as are names without a probe.
        force: Ignore the per-process cache and re-check.
        timeout: Per-request timeout in seconds.
        http_get: Injectable ``requests.get``-compatible callable (tests).

    Returns:
        ``{env_var: {"env_var", "family", "status", "http_status", "detail"}}``
        where ``status`` is ``"valid"``, ``"invalid"`` or ``"unverified"``.
        Key values are never included.
    """
    names = list(env_vars) if env_vars is not None else supported_env_vars()
    getter = http_get or _default_http_get

    results: dict[str, CredentialCheck] = {}
    pending: list[tuple[CredentialProbe, str, tuple[str, str]]] = []
    for name in names:
        probe = PROBES_BY_ENV.get(name)
        value = (os.environ.get(name) or "").strip()
        if probe is None or not value:
            continue
        cache_key = (name, _digest(value))
        with _cache_lock:
            cached = None if force else _cache.get(cache_key)
        if cached is not None:
            results[name] = cached
        else:
            pending.append((probe, value, cache_key))

    if pending:
        with ThreadPoolExecutor(max_workers=min(8, len(pending))) as pool:
            futures = [
                (cache_key, pool.submit(_run_probe, probe, value, timeout, getter))
                for probe, value, cache_key in pending
            ]
            for cache_key, future in futures:
                check = future.result()
                results[check.env_var] = check
                # Network failures are not cached: a retry after the
                # network recovers should get a real answer.
                if check.http_status is not None:
                    with _cache_lock:
                        _cache[cache_key] = check

    return {name: results[name].to_dict() for name in names if name in results}
