"""Openly-licensed audio and image search via the Openverse API.

Searches Openverse (https://api.openverse.org/v1) for Creative Commons and
public-domain audio or images, returns each result with a ready-to-paste
attribution, and optionally downloads selected results into the project's
asset folder while appending their attributions to the project's credits.md.

Works anonymously. When OPENVERSE_CLIENT_ID and OPENVERSE_CLIENT_SECRET are
set, a bearer token is fetched from POST /v1/auth_tokens/token/
(client_credentials, form-encoded), cached until shortly before it expires,
and refreshed once on a 401.
"""

from __future__ import annotations

import html
import json
import mimetypes
import os
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

from tools.base_tool import (
    BaseTool,
    Determinism,
    ExecutionMode,
    ResourceProfile,
    RetryPolicy,
    ToolResult,
    ToolRuntime,
    ToolStability,
    ToolStatus,
    ToolTier,
)


class OpenverseSearch(BaseTool):
    name = "openverse_search"
    version = "0.1.0"
    tier = ToolTier.SOURCE
    capability = "music_search"
    provider = "openverse"
    stability = ToolStability.BETA
    execution_mode = ExecutionMode.SYNC
    determinism = Determinism.DETERMINISTIC
    runtime = ToolRuntime.API

    dependencies = []  # works anonymously; credentials are optional
    install_instructions = (
        "No setup needed: Openverse works anonymously.\n"
        "Optional, for higher rate limits and larger pages: register at\n"
        "  https://api.openverse.org/v1/#tag/auth (POST /v1/auth_tokens/register/)\n"
        "then set OPENVERSE_CLIENT_ID and OPENVERSE_CLIENT_SECRET in .env."
    )

    agent_skills = []

    capabilities = [
        "search_audio",
        "search_images",
        "download_audio",
        "download_images",
        "attribution",
    ]
    supports = {
        "media_types": ["audio", "image"],
        "license_type_filter": True,
        "attribution_strings": True,
        "credits_file": True,
        "anonymous_access": True,
        "free_creative_commons": True,
    }
    best_for = [
        "Creative Commons / public-domain sound effects and ambiences",
        "openly-licensed reference or texture images",
        "assets that need a correct attribution line in the credits",
    ]
    not_good_for = [
        "commercially licensed stock (every result carries its own CC license)",
        "bulk downloading (Openverse terms forbid scraping)",
        "offline use",
    ]

    fallback_tools = ["freesound_music", "pixabay_music"]

    input_schema = {
        "type": "object",
        "required": ["q"],
        "properties": {
            "q": {
                "type": "string",
                "minLength": 1,
                "maxLength": 200,
                "description": "Search query (Openverse caps it at 200 characters).",
            },
            "media_type": {
                "type": "string",
                "enum": ["audio", "image"],
                "default": "audio",
            },
            "license_type": {
                "type": "string",
                "description": (
                    "Comma-separated license types: all, all-cc, commercial, "
                    "modification. Use 'commercial' for anything you may monetise."
                ),
            },
            "page_size": {
                "type": "integer",
                "minimum": 1,
                "default": 20,
                "description": (
                    "Results per page. The maximum depends on your Openverse "
                    "access level; anonymous callers get a smaller cap."
                ),
            },
            "source": {
                "type": "string",
                "description": (
                    "Optional comma-separated source names (from "
                    "/v1/audio/stats/ or /v1/images/stats/), e.g. "
                    "'wikimedia_audio'. Useful when one source's file host "
                    "refuses downloads."
                ),
            },
            "download": {
                "type": "array",
                "items": {"type": ["integer", "string"]},
                "default": [],
                "description": (
                    "Results to download: 0-based indexes into this search's "
                    "results, or Openverse result ids. Empty = search only."
                ),
            },
            "project_id": {
                "type": "string",
                "description": (
                    "Project under projects/. Downloads go to "
                    "projects/<id>/assets/audio|images and attributions to "
                    "projects/<id>/credits.md."
                ),
            },
            "output_dir": {
                "type": "string",
                "description": "Overrides the download folder (credits.md still goes to the project root, or here without a project_id).",
            },
        },
    }

    resource_profile = ResourceProfile(
        cpu_cores=1, ram_mb=256, vram_mb=0, disk_mb=200, network_required=True
    )
    retry_policy = RetryPolicy(max_retries=2, retryable_errors=["rate_limit", "timeout"])
    idempotency_key_fields = ["q", "media_type", "license_type", "source", "page_size"]
    side_effects = [
        "calls the Openverse API",
        "writes downloaded media into the project asset folder",
        "appends attribution lines to the project's credits.md",
    ]
    user_visible_verification = [
        "Listen to / view each downloaded asset",
        "Check each license allows your use (NC = non-commercial, ND = no derivatives)",
        "Keep credits.md with the final film",
    ]

    _BASE_URL = "https://api.openverse.org/v1"
    # Descriptive agent with a project URL: some file hosts (e.g. Wikimedia) throttle generic ones.
    _USER_AGENT = "OpenMontage/0.1 (https://github.com/calesthio/OpenMontage; openverse_search tool)"
    _MEDIA_PATHS = {"audio": "audio", "image": "images"}
    _ASSET_DIRS = {"audio": "audio", "image": "images"}
    _TOKEN_SAFETY_MARGIN_S = 60

    # Class-level cache so every instance in this process shares one token.
    _token_lock = threading.Lock()
    _token_cache: dict[str, Any] = {}

    # ------------------------------------------------------------------
    # Contract
    # ------------------------------------------------------------------

    def get_status(self) -> ToolStatus:
        return ToolStatus.AVAILABLE  # anonymous access needs no configuration

    def estimate_cost(self, inputs: dict[str, Any]) -> float:
        return 0.0  # Openverse is free

    def get_info(self) -> dict[str, Any]:
        info = super().get_info()
        info["auth_mode"] = "client_credentials" if self._credentials() else "anonymous"
        return info

    def execute(self, inputs: dict[str, Any]) -> ToolResult:
        start = time.time()
        query = (inputs.get("q") or "").strip()
        if not query:
            return ToolResult(success=False, error="'q' is required.")
        media_type = inputs.get("media_type", "audio")
        if media_type not in self._MEDIA_PATHS:
            return ToolResult(
                success=False,
                error=f"media_type must be 'audio' or 'image', got {media_type!r}.",
            )

        try:
            payload = self._search(inputs, query, media_type)
            results = [self._shape(r) for r in payload.get("results", [])]

            downloads: list[dict[str, Any]] = []
            selections = inputs.get("download") or []
            if selections:
                if not inputs.get("project_id") and not inputs.get("output_dir"):
                    return ToolResult(
                        success=False,
                        error="Downloading needs 'project_id' or 'output_dir'.",
                        data={"results": results},
                    )
                dest_dir, credits_path = self._destinations(inputs, media_type)
                for sel in selections:
                    result = self._select(results, sel)
                    path = self._download(result, dest_dir)
                    self._append_credit(credits_path, result, path)
                    downloads.append({**result, "local_path": str(path)})
        except Exception as e:  # noqa: BLE001 — surface any failure as a ToolResult
            return ToolResult(
                success=False,
                error=f"Openverse request failed: {e}",
                duration_seconds=round(time.time() - start, 2),
            )

        data: dict[str, Any] = {
            "provider": "openverse",
            "auth_mode": "client_credentials" if self._credentials() else "anonymous",
            "query": query,
            "media_type": media_type,
            "result_count": payload.get("result_count"),
            "page_count": payload.get("page_count"),
            "results": results,
            "downloads": downloads,
        }
        if downloads:
            data["credits_file"] = str(credits_path)
        return ToolResult(
            success=True,
            data=data,
            artifacts=[d["local_path"] for d in downloads],
            cost_usd=0.0,
            duration_seconds=round(time.time() - start, 2),
        )

    # ------------------------------------------------------------------
    # Auth
    # ------------------------------------------------------------------

    @staticmethod
    def _credentials() -> tuple[str, str] | None:
        cid = os.environ.get("OPENVERSE_CLIENT_ID", "").strip()
        secret = os.environ.get("OPENVERSE_CLIENT_SECRET", "").strip()
        return (cid, secret) if cid and secret else None

    def _token(self, force_refresh: bool = False) -> str | None:
        creds = self._credentials()
        if not creds:
            return None
        with self._token_lock:
            cached = self._token_cache
            fresh = (
                cached.get("client_id") == creds[0]
                and cached.get("expires_at", 0) > time.time()
            )
            if fresh and not force_refresh:
                return cached["access_token"]

            body = urllib.parse.urlencode({
                "grant_type": "client_credentials",
                "client_id": creds[0],
                "client_secret": creds[1],
            }).encode("ascii")
            req = urllib.request.Request(
                f"{self._BASE_URL}/auth_tokens/token/",
                data=body,
                method="POST",
                headers={
                    "Content-Type": "application/x-www-form-urlencoded",
                    "User-Agent": self._USER_AGENT,
                },
            )
            with urllib.request.urlopen(req, timeout=30) as resp:
                tok = json.loads(resp.read().decode("utf-8"))
            expires_in = int(tok.get("expires_in") or 0)
            self._token_cache.clear()
            self._token_cache.update({
                "client_id": creds[0],
                "access_token": tok["access_token"],
                "expires_at": time.time() + max(0, expires_in - self._TOKEN_SAFETY_MARGIN_S),
            })
            return tok["access_token"]

    def _get_json(self, url: str) -> dict[str, Any]:
        """GET with the bearer token when configured; refresh once on 401."""
        for attempt in range(2):
            headers = {"User-Agent": self._USER_AGENT, "Accept": "application/json"}
            token = self._token(force_refresh=attempt > 0)
            if token:
                headers["Authorization"] = f"Bearer {token}"
            req = urllib.request.Request(url, headers=headers)
            try:
                with urllib.request.urlopen(req, timeout=30) as resp:
                    return json.loads(resp.read().decode("utf-8"))
            except urllib.error.HTTPError as e:
                if e.code == 401 and token and attempt == 0:
                    continue  # token expired or revoked: fetch a new one, retry once
                detail = e.read().decode("utf-8", "replace")[:300]
                raise RuntimeError(f"HTTP {e.code} from Openverse: {detail}") from e
        raise RuntimeError("Openverse rejected the refreshed token (HTTP 401).")

    # ------------------------------------------------------------------
    # Search
    # ------------------------------------------------------------------

    def _search(self, inputs: dict[str, Any], query: str, media_type: str) -> dict[str, Any]:
        params: dict[str, Any] = {"q": query, "page_size": int(inputs.get("page_size", 20))}
        for key in ("license_type", "source"):
            if inputs.get(key):
                params[key] = inputs[key]
        url = f"{self._BASE_URL}/{self._MEDIA_PATHS[media_type]}/?{urllib.parse.urlencode(params)}"
        return self._get_json(url)

    @classmethod
    def _license_label(cls, code: str | None, version: str | None) -> str:
        if not code:
            return "unknown license"
        code = code.lower()
        if code == "cc0":
            return "CC0 1.0"
        if code == "pdm":
            return "Public Domain Mark 1.0"
        label = f"CC {code.upper()}"
        return f"{label} {version}" if version else label

    @classmethod
    def _shape(cls, r: dict[str, Any]) -> dict[str, Any]:
        license_label = cls._license_label(r.get("license"), r.get("license_version"))
        # Some sources (e.g. Jamendo) deliver HTML-escaped names ("A &amp; B").
        title = html.unescape(r.get("title") or "Untitled")
        creator = html.unescape(r.get("creator") or "Unknown creator")
        source_url = r.get("foreign_landing_url")
        attribution = html.unescape(r["attribution"]) if r.get("attribution") else None
        if not attribution:  # API normally supplies one; build the TASL form otherwise
            attribution = f'"{title}" by {creator} is licensed under {license_label}.'
            if r.get("license_url"):
                attribution += f" To view a copy of this license, visit {r['license_url']}."
        if source_url and source_url not in attribution:
            attribution = f"{attribution} Source: {source_url}"
        return {
            "id": r.get("id"),
            "url": r.get("url"),
            "title": title,
            "creator": creator,
            "creator_url": r.get("creator_url"),
            "license": license_label,
            "license_code": r.get("license"),
            "license_version": r.get("license_version"),
            "license_url": r.get("license_url"),
            "source_url": source_url,
            "source": r.get("source"),
            "filetype": r.get("filetype"),
            "duration_ms": r.get("duration"),
            "attribution": attribution,
        }

    # ------------------------------------------------------------------
    # Download + credits
    # ------------------------------------------------------------------

    def _destinations(self, inputs: dict[str, Any], media_type: str) -> tuple[Path, Path]:
        project_id = inputs.get("project_id")
        project_root = Path("projects") / project_id if project_id else None
        if inputs.get("output_dir"):
            dest = Path(inputs["output_dir"])
        else:
            dest = project_root / "assets" / self._ASSET_DIRS[media_type]
        credits = (project_root or dest) / "credits.md"
        return dest, credits

    @staticmethod
    def _select(results: list[dict[str, Any]], sel: int | str) -> dict[str, Any]:
        if isinstance(sel, int) or (isinstance(sel, str) and sel.isdigit()):
            idx = int(sel)
            if not 0 <= idx < len(results):
                raise IndexError(f"download index {idx} out of range (0..{len(results) - 1})")
            return results[idx]
        for r in results:
            if r["id"] == sel:
                return r
        raise KeyError(f"result id {sel!r} is not in this page of results")

    def _download(self, result: dict[str, Any], dest_dir: Path) -> Path:
        if not result.get("url"):
            raise RuntimeError(f"result {result['id']} has no file URL")
        dest_dir.mkdir(parents=True, exist_ok=True)
        safe_title = "".join(c if c.isalnum() or c in "-_" else "_" for c in result["title"])[:50].strip("_")
        stem = f"openverse_{(result['id'] or 'x')[:8]}_{safe_title or 'asset'}"
        req = urllib.request.Request(result["url"], headers={"User-Agent": self._USER_AGENT})
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                body = resp.read()
                content_type = resp.headers.get_content_type()
        except urllib.error.HTTPError as e:
            host = urllib.parse.urlparse(result["url"]).netloc
            retry_after = e.headers.get("Retry-After") if e.headers else None
            wait = f" Retry after {retry_after} s." if retry_after else ""
            raise RuntimeError(
                f"{host} refused the download of '{result['title']}' (HTTP {e.code}).{wait} "
                f"Download it by hand from {result.get('source_url')}, or search "
                f"again with a 'source' filter for another source."
            ) from e
        path = dest_dir / f"{stem}.{self._extension(result, content_type)}"
        path.write_bytes(body)
        return path

    # Openverse 'filetype' values that are not real extensions (Jamendo uses "mp32").
    _FILETYPE_ALIASES = {"mp32": "mp3", "ogx": "ogg", "mpeg": "mp3", "jpeg": "jpg"}

    @classmethod
    def _extension(cls, result: dict[str, Any], content_type: str | None) -> str:
        filetype = (result.get("filetype") or "").lower()
        if filetype:
            return cls._FILETYPE_ALIASES.get(filetype, filetype)
        guessed = mimetypes.guess_extension(content_type or "") if content_type else None
        if guessed:
            return cls._FILETYPE_ALIASES.get(guessed.lstrip("."), guessed.lstrip("."))
        suffix = Path(urllib.parse.urlparse(result["url"]).path).suffix.lstrip(".").lower()
        return suffix or "bin"

    @staticmethod
    def _append_credit(credits_path: Path, result: dict[str, Any], local_path: Path) -> None:
        credits_path.parent.mkdir(parents=True, exist_ok=True)
        existing = credits_path.read_text(encoding="utf-8") if credits_path.exists() else ""
        marker = f"<!-- openverse:{result['id']} -->"
        if marker in existing:
            return  # already credited
        lines = []
        if not existing:
            lines.append("# Credits\n")
        lines.append(f"- {result['attribution']} (file: `{local_path.name}`) {marker}")
        with credits_path.open("a", encoding="utf-8") as fh:
            if existing and not existing.endswith("\n"):
                fh.write("\n")
            fh.write("\n".join(lines) + "\n")
