import re
import shutil
from .constants import RESET, BOLD, DIM


def separator() -> str:
    """
    Return a horizontal separator line that fits the terminal width.
    """
    size = shutil.get_terminal_size() or 800
    assert size.columns > 0, "terminal columns must be positive"
    return f"{DIM}{'─' * size.columns}{RESET}"


def render_markdown(text: str) -> str:
    """
    Convert basic markdown bold syntax to ANSI bold.
    """
    assert isinstance(text, str), "text must be a str"
    return re.sub(r"\*\*(.+?)\*\*", f"{BOLD}\\1{RESET}", text)
