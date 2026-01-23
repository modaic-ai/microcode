import json
import os
import tempfile
from .constants import (
    OPENROUTER_KEY_PATH,
    CACHE_DIR,
    MODEL_CONFIG_PATH,
    SETTINGS_CONFIG_PATH,
)


def load_openrouter_key() -> str | None:
    """
    Load the OpenRouter API key from the cache file or environment variable.
    """
    assert isinstance(OPENROUTER_KEY_PATH, str), "cache path must be a str"

    if os.getenv("OPENROUTER_API_KEY"):
        return os.getenv("OPENROUTER_API_KEY")

    if not os.path.exists(OPENROUTER_KEY_PATH):
        return None

    try:
        with open(OPENROUTER_KEY_PATH, "r", encoding="utf-8") as handle:
            data = json.load(handle)

        key = data.get("openrouter_api_key")
        return key if key else None

    except (OSError, json.JSONDecodeError):
        return None


def save_openrouter_key(key: str) -> None:
    """
    Save the OpenRouter API key to the cache file.
    """
    assert isinstance(key, str), "key must be a str"

    os.makedirs(CACHE_DIR, exist_ok=True)
    tmp_path = None
    try:
        fd, tmp_path = tempfile.mkstemp(
            prefix="microcode_key_", suffix=".json", dir=CACHE_DIR
        )
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump({"openrouter_api_key": key}, handle)
        os.replace(tmp_path, OPENROUTER_KEY_PATH)
        try:
            os.chmod(OPENROUTER_KEY_PATH, 0o600)
        except OSError:
            pass
    finally:
        if tmp_path and os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
            except OSError:
                pass


def clear_openrouter_key() -> None:
    """
    Clear the OpenRouter API key from the cache file.
    """
    assert isinstance(OPENROUTER_KEY_PATH, str), "cache path must be a str"

    try:
        os.remove(OPENROUTER_KEY_PATH)
    except OSError:
        pass


def load_model_config() -> tuple[str | None, str | None]:
    """
    Load the model configuration from the cache file.
    """
    assert isinstance(MODEL_CONFIG_PATH, str), "model config path must be a str"

    if not os.path.exists(MODEL_CONFIG_PATH):
        return None, None

    try:
        with open(MODEL_CONFIG_PATH, "r", encoding="utf-8") as handle:
            data = json.load(handle)

        model = data.get("model")
        sub_lm = data.get("sub_lm")
        model = model if isinstance(model, str) and model else None
        sub_lm = sub_lm if isinstance(sub_lm, str) and sub_lm else None
        return model, sub_lm

    except (OSError, json.JSONDecodeError):
        return None, None


def save_model_config(model: str, sub_lm: str) -> None:
    """
    Save the model configuration to the cache file.
    """
    assert isinstance(model, str), "model must be a str"
    assert isinstance(sub_lm, str), "sub_lm must be a str"

    os.makedirs(CACHE_DIR, exist_ok=True)
    tmp_path = None
    try:
        fd, tmp_path = tempfile.mkstemp(
            prefix="microcode_model_", suffix=".json", dir=CACHE_DIR
        )
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump({"model": model, "sub_lm": sub_lm}, handle)
        os.replace(tmp_path, MODEL_CONFIG_PATH)
        try:
            os.chmod(MODEL_CONFIG_PATH, 0o600)
        except OSError:
            pass
    finally:
        if tmp_path and os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
            except OSError:
                pass


def load_settings_config() -> dict[str, object]:
    """
    Load the settings configuration from the cache file.
    """
    assert isinstance(SETTINGS_CONFIG_PATH, str), "settings config path must be a str"

    if not os.path.exists(SETTINGS_CONFIG_PATH):
        return {}

    try:
        with open(SETTINGS_CONFIG_PATH, "r", encoding="utf-8") as handle:
            data = json.load(handle)

        if not isinstance(data, dict):
            return {}

        settings: dict[str, object] = {}
        max_iters = data.get("max_iters")
        max_tokens = data.get("max_tokens")
        max_output_chars = data.get("max_output_chars")
        api_base = data.get("api_base")
        verbose = data.get("verbose")

        if isinstance(max_iters, int):
            settings["max_iters"] = max_iters
        if isinstance(max_tokens, int):
            settings["max_tokens"] = max_tokens
        if isinstance(max_output_chars, int):
            settings["max_output_chars"] = max_output_chars
        if isinstance(api_base, str) and api_base:
            settings["api_base"] = api_base
        if isinstance(verbose, bool):
            settings["verbose"] = verbose

        return settings

    except (OSError, json.JSONDecodeError):
        return {}


def save_settings_config(
    max_iters: int | None,
    max_tokens: int | None,
    max_output_chars: int | None,
    api_base: str | None,
    verbose: bool | None,
) -> None:
    """
    Save the settings configuration to the cache file.
    """
    os.makedirs(CACHE_DIR, exist_ok=True)
    payload: dict[str, object] = {}
    if max_iters is not None:
        payload["max_iters"] = max_iters
    if max_tokens is not None:
        payload["max_tokens"] = max_tokens
    if max_output_chars is not None:
        payload["max_output_chars"] = max_output_chars
    if api_base is not None:
        payload["api_base"] = api_base
    if verbose is not None:
        payload["verbose"] = verbose

    tmp_path = None
    try:
        fd, tmp_path = tempfile.mkstemp(
            prefix="microcode_settings_", suffix=".json", dir=CACHE_DIR
        )
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(payload, handle)
        os.replace(tmp_path, SETTINGS_CONFIG_PATH)
        try:
            os.chmod(SETTINGS_CONFIG_PATH, 0o600)
        except OSError:
            pass
    finally:
        if tmp_path and os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
            except OSError:
                pass
