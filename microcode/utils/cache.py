import json
import os
import tempfile

CACHE_DIR = os.path.join(
    os.getenv("XDG_CACHE_HOME", os.path.expanduser("~/.cache")),
    "nanocode",
)
OPENROUTER_KEY_PATH = os.path.join(CACHE_DIR, "openrouter_key.json")
MODEL_CONFIG_PATH = os.path.join(CACHE_DIR, "model_config.json")


def load_openrouter_key() -> str | None:
    assert isinstance(OPENROUTER_KEY_PATH, str), "cache path must be a str"

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
    assert isinstance(key, str), "key must be a str"

    os.makedirs(CACHE_DIR, exist_ok=True)
    tmp_path = None
    try:
        fd, tmp_path = tempfile.mkstemp(
            prefix="nanocode_key_", suffix=".json", dir=CACHE_DIR
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
    assert isinstance(OPENROUTER_KEY_PATH, str), "cache path must be a str"

    try:
        os.remove(OPENROUTER_KEY_PATH)
    except OSError:
        pass


def load_model_config() -> tuple[str | None, str | None]:
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
    assert isinstance(model, str), "model must be a str"
    assert isinstance(sub_lm, str), "sub_lm must be a str"

    os.makedirs(CACHE_DIR, exist_ok=True)
    tmp_path = None
    try:
        fd, tmp_path = tempfile.mkstemp(
            prefix="nanocode_model_", suffix=".json", dir=CACHE_DIR
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
