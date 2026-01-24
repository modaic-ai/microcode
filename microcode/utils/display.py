import os
import re
import shutil
from .constants import RESET, BOLD, DIM, BLUE, BANNER_ART, GREEN
import click


def separator() -> str:
    """
    Return a horizontal separator line that fits the terminal width.
    """
    size = shutil.get_terminal_size() or 800
    return f"{DIM}{'─' * size.columns}{RESET}"


def render_markdown(text: str) -> str:
    """
    Convert basic markdown bold syntax to ANSI bold.
    """
    assert isinstance(text, str), "text must be a str"
    return re.sub(r"\*\*(.+?)\*\*", f"{BOLD}\\1{RESET}", text)


def format_auth_error(err: Exception) -> str | None:
    """
    Format authentication errors for display.

    Args:
        err: The exception object

    Returns:
        A formatted error message or None if not an auth error
    """
    message = str(err)
    if (
        "OpenrouterException" in message
        and "No cookie auth credentials found" in message
    ):
        return (
            "OpenRouter authentication failed: no credentials found. "
            "Set `OPENROUTER_API_KEY` or run `/key` to cache it."
        )
    if "AuthenticationError" in message and "OpenrouterException" in message:
        return (
            "OpenRouter authentication failed. "
            "Set `OPENROUTER_API_KEY` or run `/key` to cache it."
        )
    return None


def short_cwd(path: str) -> str:
    """
    Shorten a file path to show only the last two directory levels.

    Args:
        path: The full file path

    Returns:
        The shortened path
    """
    assert path is not None, "path must not be None"
    assert isinstance(path, str), "path must be a str"

    parts = path.split(os.sep)
    if len(parts) <= 2:
        return path
    return os.sep.join(parts[-2:])


def read_int_env(var_name: str) -> int | None:
    """
    Read an integer environment variable.

    Args:
        var_name: The name of the environment variable

    Returns:
        The integer value or None if not set or invalid
    """
    assert var_name is not None, "var_name must not be None"
    assert isinstance(var_name, str), "var_name must be a str"

    value = os.getenv(var_name)
    if value is None:
        return None
    try:
        return int(value)
    except ValueError:
        return None


def print_banner(
    model: str,
    sub_lm: str,
    cwd: str,
    history_limit: int,
    max_iterations: int | None,
    max_tokens: int | None,
    max_output_chars: int | None,
    verbose: bool | None,
) -> None:
    """
    Print the startup banner with current configuration.

    Args:
        model: The primary model ID
        sub_lm: The sub model ID
        cwd: The current working directory
        history_limit: Maximum number of messages to keep in history
        max_iterations: Maximum number of iterations
        max_tokens: Maximum number of tokens
        max_output_chars: Maximum number of output characters
        verbose: Enable verbose logging
    """
    art_lines = BANNER_ART.splitlines()
    while art_lines and not art_lines[0].strip():
        art_lines.pop(0)
    while art_lines and not art_lines[-1].strip():
        art_lines.pop()

    def format_setting(value: object) -> str:
        if value is None:
            return "unset"
        if isinstance(value, bool):
            return "true" if value else "false"
        return str(value)

    def gradient_color(line_index: int, total_lines: int) -> str:
        if total_lines <= 1:
            t = 0.0
        else:
            t = line_index / (total_lines - 1)
        start = (150, 190, 230)
        end = (40, 120, 200)
        r = int(start[0] + (end[0] - start[0]) * t)
        g = int(start[1] + (end[1] - start[1]) * t)
        b = int(start[2] + (end[2] - start[2]) * t)
        return f"\033[38;2;{r};{g};{b}m"

    right_lines = [
        f"{BOLD}{BLUE}MICROCODE -{RESET} {DIM}An Efficient RLM Terminal Agent{RESET}",
        "",
        f"{DIM}Configuration:{RESET}",
        f"  {DIM}model:{RESET} {DIM}RLM({RESET}{model.removeprefix('openrouter/')}{DIM}){RESET}",
        f"  {DIM}sub_model:{RESET} {sub_lm.removeprefix('openrouter/')}",
        f"  {DIM}max_turns:{RESET} {history_limit}",
        f"  {DIM}max_tokens:{RESET} {format_setting(max_tokens)}",
        "",
        f"{DIM}Settings:{RESET}",
        f"  {DIM}verbose:{RESET} {format_setting(verbose)}",
        f"  {DIM}cwd:{RESET} {cwd}",
        "",
        f"{DIM}Quick commands:{RESET}",
        f"  {BLUE}/help - help{RESET}",
        f"  {BLUE}/model - switch RLM model and sub model{RESET}",
        f"  {BLUE}/key - set API key{RESET}",
        f"  {BLUE}/c - clear conversation{RESET}",
        f"  {BLUE}/q - quit{RESET}",
    ]

    total_lines = max(len(art_lines), len(right_lines))
    art_width = max((len(line) for line in art_lines), default=0)

    banner_lines = []
    for idx in range(total_lines):
        left_raw = art_lines[idx] if idx < len(art_lines) else ""
        left_padded = left_raw.ljust(art_width)
        if left_raw:
            left = f"{gradient_color(idx, len(art_lines))}{left_padded}{RESET}"
        else:
            left = left_padded
        right = right_lines[idx] if idx < len(right_lines) else ""
        banner_lines.append(f"{left}  {right}")

    click.echo("\n".join(banner_lines))


def print_help() -> None:
    """
    Print the help message with available commands.
    """
    click.echo(f"\n{BOLD}Microcode commands{RESET}")
    click.echo(f"  {BLUE}/help{RESET}            Show this help")
    click.echo(f"  {BLUE}/model{RESET}           Change model and sub_lm")
    click.echo(f"  {BLUE}/key{RESET}             Set or clear openrouter key")
    click.echo(f"  {BLUE}/clear{RESET}           Clear the screen")
    click.echo(f"  {BLUE}/c{RESET}               Clear conversation history")
    click.echo(f"  {BLUE}/q{RESET}               Quit")
    click.echo(f"  {BLUE}/mcp{RESET}             Manage MCP servers")
    click.echo(f"  {BLUE}/reset{RESET}           Reset to default configuration")


def print_status_line(
    model: str, sub_lm: str, cwd: str, mcp_servers: dict | None = None
) -> None:
    """
    Print the status line with current configuration.

    Args:
        model: The primary model ID
        sub_lm: The sub model ID
        cwd: The current working directory
        mcp_servers: Dictionary of MCP servers
    """
    assert isinstance(model, str), "model must be a str"
    assert isinstance(sub_lm, str), "sub_lm must be a str"
    assert isinstance(cwd, str), "cwd must be a str"
    assert isinstance(mcp_servers, dict | None), "mcp_servers must be a dict or None"

    mcp_label = f"{len(mcp_servers)}" if mcp_servers else "0"
    click.echo(
        f"{DIM}cwd:{RESET} {GREEN}{cwd}{RESET}  {DIM}RLM(model):{RESET} {GREEN}{model.removeprefix('openrouter/')}{RESET}  "
        f"{DIM}sub_model:{RESET} {GREEN}{sub_lm.removeprefix('openrouter/')}{RESET}  {DIM}mcp_tools:{RESET} {GREEN}{mcp_label}{RESET}"
        "\n"
    )
