import importlib
import os
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def _run_interactive(monkeypatch, tmp_path, env_vars, cache_settings, **overrides):
    captured_config = {}

    def fake_from_precompiled(_repo, _rev=None, config=None, **_kwargs):
        if config is None:
            config = {}
        captured_config.update(config)
        return SimpleNamespace(config=SimpleNamespace(**config))

    def fake_read_user_input(_prompt):
        raise KeyboardInterrupt

    defaults = {
        "history_limit": 1,
        "show_banner": False,
        "model": "openrouter/test-model",
        "sub_lm": "openrouter/test-sub",
        "api_key": None,
        "max_iterations": None,
        "max_tokens": None,
        "max_output_chars": None,
        "api_base": None,
        "verbose": None,
        "env": None,
    }
    defaults.update(overrides)

    for var in (
        "XDG_CACHE_HOME",
        "MICROCODE_MAX_ITERATIONS",
        "MICROCODE_MAX_TOKENS",
        "MICROCODE_MAX_OUTPUT_CHARS",
        "MICROCODE_API_BASE",
        "MICROCODE_VERBOSE",
        "MICROCODE_MODEL",
        "MICROCODE_SUB_LM",
        "MICROCODE_ENV",
        "MODAIC_ENV",
        "OPENROUTER_API_KEY",
    ):
        monkeypatch.delenv(var, raising=False)
    monkeypatch.setenv("XDG_CACHE_HOME", str(tmp_path))
    for key, value in env_vars.items():
        monkeypatch.setenv(key, value)

    constants = importlib.import_module("utils.constants")
    importlib.reload(constants)
    cache = importlib.import_module("utils.cache")
    importlib.reload(cache)
    microcode_main = importlib.import_module("main")
    importlib.reload(microcode_main)

    if cache_settings:
        cache.save_settings_config(
            max_iters=cache_settings.get("max_iters"),
            max_tokens=cache_settings.get("max_tokens"),
            max_output_chars=cache_settings.get("max_output_chars"),
            api_base=cache_settings.get("api_base"),
            verbose=cache_settings.get("verbose"),
        )

    monkeypatch.setattr(
        microcode_main.AutoProgram, "from_precompiled", fake_from_precompiled
    )
    monkeypatch.setattr(microcode_main, "read_user_input", fake_read_user_input)

    microcode_main.run_interactive(**defaults)

    return cache.load_settings_config(), captured_config


def test_cli_flags_override_env_and_cache(monkeypatch, tmp_path):
    env_vars = {
        "MICROCODE_MAX_ITERATIONS": "111",
        "MICROCODE_MAX_TOKENS": "222",
        "MICROCODE_MAX_OUTPUT_CHARS": "333",
        "MICROCODE_API_BASE": "https://env.example/api",
        "MICROCODE_VERBOSE": "0",
    }
    cache_settings = {
        "max_iters": 1,
        "max_tokens": 2,
        "max_output_chars": 3,
        "api_base": "https://cache.example/api",
        "verbose": False,
    }

    saved, captured = _run_interactive(
        monkeypatch,
        tmp_path,
        env_vars,
        cache_settings,
        max_iterations=10,
        max_tokens=20,
        max_output_chars=30,
        api_base="https://cli.example/api",
        verbose=True,
    )

    expected = {
        "max_iters": 10,
        "max_tokens": 20,
        "max_output_chars": 30,
        "api_base": "https://cli.example/api",
        "verbose": True,
    }
    assert saved == expected
    for key, value in expected.items():
        assert captured.get(key) == value


def test_env_overrides_cache_when_cli_missing(monkeypatch, tmp_path):
    env_vars = {
        "MICROCODE_MAX_ITERATIONS": "12",
        "MICROCODE_MAX_TOKENS": "34",
        "MICROCODE_MAX_OUTPUT_CHARS": "56",
        "MICROCODE_API_BASE": "https://env.example/api",
        "MICROCODE_VERBOSE": "1",
    }
    cache_settings = {
        "max_iters": 99,
        "max_tokens": 88,
        "max_output_chars": 77,
        "api_base": "https://cache.example/api",
        "verbose": False,
    }

    saved, captured = _run_interactive(monkeypatch, tmp_path, env_vars, cache_settings)

    expected = {
        "max_iters": 12,
        "max_tokens": 34,
        "max_output_chars": 56,
        "api_base": "https://env.example/api",
        "verbose": True,
    }
    assert saved == expected
    for key, value in expected.items():
        assert captured.get(key) == value


def test_cache_used_when_no_overrides(monkeypatch, tmp_path):
    env_vars = {}
    cache_settings = {
        "max_iters": 7,
        "max_tokens": 8,
        "max_output_chars": 9,
        "api_base": "https://cache.example/api",
        "verbose": True,
    }

    saved, captured = _run_interactive(monkeypatch, tmp_path, env_vars, cache_settings)

    expected = {
        "max_iters": 7,
        "max_tokens": 8,
        "max_output_chars": 9,
        "api_base": "https://cache.example/api",
        "verbose": True,
    }
    assert saved == expected
    for key, value in expected.items():
        assert captured.get(key) == value
