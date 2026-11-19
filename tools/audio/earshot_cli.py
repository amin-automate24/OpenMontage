"""Thin wrapper around the Earshot CLI (https://github.com/Leonxlnx/earshot).

Earshot is installed as its own tool (`uv tool install`) and is not
re-implemented here. This wrapper only shells out to its CLI with `--json` for:

- ``critique``   — `earshot critique FILE [--video V] [--fast]`: a scorecard of a
                   soundtrack / final mix against a profile of professional films,
                   with timestamped fixes. Loads CLAP + AST models (CPU, ~20-40 s).
- ``sfx_search`` — `earshot sfx list [--category C] [--kind K]`: the built-in bank
                   of code-made sound effects, optionally narrowed by a substring
                   over id / notes. No models.
- ``sfx_render`` — `earshot sfx render ID -o OUT.wav [--dur --apex --pitch ...]`:
                   one bank sound rendered to a 24-bit WAV, audited. No models.

For many calls in one session, the Earshot MCP server (`claude mcp add earshot
-- earshot mcp`) keeps the models loaded; this tool is for pipeline steps.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import time
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
    ToolTier,
)


class Earshot(BaseTool):
    name = "earshot"
    version = "0.1.0"
    tier = ToolTier.ANALYZE
    capability = "audio_processing"
    provider = "earshot"
    stability = ToolStability.EXPERIMENTAL
    execution_mode = ExecutionMode.SYNC
    determinism = Determinism.DETERMINISTIC
    runtime = ToolRuntime.LOCAL

    dependencies = ["cmd:earshot", "cmd:ffmpeg"]
    install_instructions = (
        "Install Earshot (needs uv, ffmpeg and ffprobe on PATH; CPU only):\n"
        '  uv tool install "earshot[mcp] @ git+https://github.com/Leonxlnx/earshot"\n'
        "  earshot doctor --fetch   # downloads the two models (~1.1 GB), needed for critique\n"
        "Optional MCP server for Claude Code:\n"
        "  claude mcp add earshot --scope user -e EARSHOT_THREADS=3 -- earshot mcp"
    )

    agent_skills = []

    capabilities = ["critique_mix", "search_sfx_bank", "render_sfx"]
    supports = {
        "operations": ["critique", "sfx_search", "sfx_render"],
        "video_sync_check": True,
        "offline": True,
        "models_required_for": ["critique"],
    }
    best_for = [
        "a measured critique of the final mix (loudness, arc, sync to cuts) with timestamped fixes",
        "deterministic, license-clean UI / motion SFX (whooshes, hits, pops, risers) from a code bank",
        "letting the agent 'hear' a soundtrack it cannot listen to",
    ]
    not_good_for = [
        "realistic foley or ambience recordings (rain, crowds) — the bank is code-synthesized",
        "judging taste, emotion or speech content (see Earshot docs/LIMITS.md)",
        "fast batch critique via CLI (each call reloads models; use the MCP server)",
    ]

    fallback_tools = ["audio_mixer"]

    input_schema = {
        "type": "object",
        "required": ["operation"],
        "properties": {
            "operation": {
                "type": "string",
                "enum": ["critique", "sfx_search", "sfx_render"],
            },
            # critique
            "input_path": {"type": "string", "description": "critique: soundtrack or film to score."},
            "video_path": {"type": "string", "description": "critique: the picture the soundtrack is for."},
            "profile_path": {"type": "string", "description": "critique: profile JSON from `earshot profile` (default: bundled 7 launch films)."},
            "fast": {"type": "boolean", "default": False, "description": "critique: skip the AudioSet and realness passes."},
            # sfx_search
            "category": {"type": "string", "description": "sfx_search: one category (whoosh_fast, pro_impact, ...)."},
            "kind": {"type": "string", "description": "sfx_search: a cue kind or kit role (whoosh, hit, key, bell ...)."},
            "query": {"type": "string", "description": "sfx_search: substring filter over id, category, kinds and notes (applied here)."},
            "limit": {"type": "integer", "default": 25, "minimum": 1},
            # sfx_render
            "sound_id": {"type": "string", "description": "sfx_render: bank id, e.g. whoosh_fast/crisp."},
            "output_path": {"type": "string", "description": "sfx_render: WAV to write (24-bit)."},
            "seed": {"type": "integer"},
            "dur": {"type": "number", "description": "Length in seconds (exact)."},
            "apex": {"type": "number", "description": "Seconds from start to the loudest moment (whoosh family)."},
            "pitch": {"type": "string", "description": "Note name ('E5') or Hz."},
            "peak": {"type": "number", "description": "Sample peak in dBFS, <= 0 (default -1)."},
            "weight": {"type": "number", "description": "Level relative to peak (0.5 = -6 dB)."},
            "sr": {"type": "integer", "enum": [44100, 48000, 88200, 96000]},
            # shared
            "threads": {"type": "integer", "minimum": 1},
            "report_path": {"type": "string", "description": "Also save Earshot's JSON result here (--out)."},
            "timeout_s": {"type": "integer", "default": 900},
        },
    }

    resource_profile = ResourceProfile(
        cpu_cores=4, ram_mb=4096, vram_mb=0, disk_mb=1200, network_required=False
    )
    retry_policy = RetryPolicy(max_retries=0)
    idempotency_key_fields = ["operation", "input_path", "sound_id", "seed", "dur", "apex", "pitch"]
    side_effects = ["sfx_render writes a WAV to output_path", "report_path writes a JSON report"]
    user_visible_verification = [
        "Read the critique's FIX FIRST list and check the timestamps against the cut",
        "Listen to rendered SFX in context before locking the mix",
    ]

    def estimate_cost(self, inputs: dict[str, Any]) -> float:
        return 0.0  # local, open models

    def execute(self, inputs: dict[str, Any]) -> ToolResult:
        start = time.time()
        op = inputs.get("operation")
        try:
            if op == "critique":
                args, artifacts = self._critique_args(inputs)
            elif op == "sfx_search":
                args, artifacts = self._search_args(inputs)
            elif op == "sfx_render":
                args, artifacts = self._render_args(inputs)
            else:
                return ToolResult(success=False, error=f"Unknown operation {op!r}.")
        except ValueError as e:
            return ToolResult(success=False, error=str(e))

        if inputs.get("threads"):
            args += ["--threads", str(inputs["threads"])]
        if inputs.get("report_path"):
            Path(inputs["report_path"]).parent.mkdir(parents=True, exist_ok=True)
            args += ["--out", inputs["report_path"]]
            artifacts.append(inputs["report_path"])

        try:
            result = self._run(args, timeout=int(inputs.get("timeout_s", 900)))
        except RuntimeError as e:
            return ToolResult(success=False, error=str(e), duration_seconds=round(time.time() - start, 2))

        if op == "sfx_search":
            result = self._filter_bank(result, inputs.get("query"), int(inputs.get("limit", 25)))

        return ToolResult(
            success=True,
            data={"provider": "earshot", "operation": op, "command": " ".join(args), "result": result},
            artifacts=artifacts,
            cost_usd=0.0,
            duration_seconds=round(time.time() - start, 2),
        )

    # ------------------------------------------------------------------
    # Argument builders — flags mirror `earshot <cmd> --help` exactly
    # ------------------------------------------------------------------

    @staticmethod
    def _critique_args(inputs: dict[str, Any]) -> tuple[list[str], list[str]]:
        path = inputs.get("input_path")
        if not path or not Path(path).exists():
            raise ValueError(f"critique needs an existing 'input_path' (got {path!r}).")
        args = ["critique", path, "--json"]
        if inputs.get("video_path"):
            args += ["--video", inputs["video_path"]]
        if inputs.get("profile_path"):
            args += ["--profile", inputs["profile_path"]]
        if inputs.get("fast"):
            args.append("--fast")
        return args, []

    @staticmethod
    def _search_args(inputs: dict[str, Any]) -> tuple[list[str], list[str]]:
        args = ["sfx", "list", "--json"]
        if inputs.get("category"):
            args += ["--category", inputs["category"]]
        if inputs.get("kind"):
            args += ["--kind", inputs["kind"]]
        return args, []

    @staticmethod
    def _render_args(inputs: dict[str, Any]) -> tuple[list[str], list[str]]:
        sound_id, out = inputs.get("sound_id"), inputs.get("output_path")
        if not sound_id or not out:
            raise ValueError("sfx_render needs 'sound_id' and 'output_path'.")
        Path(out).parent.mkdir(parents=True, exist_ok=True)
        args = ["sfx", "render", sound_id, "-o", out, "--json"]
        for key in ("seed", "dur", "apex", "pitch", "peak", "weight", "sr"):
            if inputs.get(key) is not None:
                args += [f"--{key}", str(inputs[key])]
        return args, [out]

    # ------------------------------------------------------------------

    @staticmethod
    def _run(args: list[str], timeout: int) -> Any:
        exe = shutil.which("earshot")
        if not exe:
            raise RuntimeError("earshot is not on PATH. " + Earshot.install_instructions)
        try:
            proc = subprocess.run(
                [exe, *args], capture_output=True, text=True, timeout=timeout, check=False
            )
        except subprocess.TimeoutExpired as e:
            raise RuntimeError(f"earshot {args[0]} timed out after {timeout} s") from e
        if proc.returncode != 0:
            # Earshot prints one-line errors on stderr: "earshot <command>: error: ..."
            msg = (proc.stderr.strip().splitlines() or ["(no stderr)"])[-1]
            raise RuntimeError(f"earshot exited {proc.returncode}: {msg}")
        try:
            return json.loads(proc.stdout)
        except json.JSONDecodeError as e:
            raise RuntimeError(f"earshot printed non-JSON output: {proc.stdout[:300]!r}") from e

    @staticmethod
    def _filter_bank(result: dict[str, Any], query: str | None, limit: int) -> dict[str, Any]:
        sounds = result.get("sounds", [])
        if query:
            q = query.lower()
            sounds = [
                s for s in sounds
                if q in " ".join([
                    s.get("id", ""), s.get("category", ""), " ".join(s.get("kinds", [])), s.get("notes", "") or "",
                ]).lower()
            ]
        return {
            "version": result.get("version"),
            "total_matches": len(sounds),
            "sounds": [
                {k: s.get(k) for k in ("id", "category", "kinds", "dur_s", "peak_s", "onset_s", "knobs", "notes", "source")}
                for s in sounds[:limit]
            ],
        }
