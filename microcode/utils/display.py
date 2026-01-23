import os
import re

RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
BLUE = "\033[34m"
CYAN = "\033[36m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
RED = "\033[31m"
MAGENTA = "\033[35m"


def separator() -> str:
    """Return a horizontal separator line that fits the terminal width."""
    size = os.get_terminal_size()
    assert size.columns > 0, "terminal columns must be positive"
    return f"{DIM}{'─' * min(size.columns, 80)}{RESET}"


def render_markdown(text: str) -> str:
    """Convert basic markdown bold syntax to ANSI bold."""
    assert isinstance(text, str), "text must be a str"
    return re.sub(r"\*\*(.+?)\*\*", f"{BOLD}\\1{RESET}", text)
