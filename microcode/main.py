from datetime import datetime
from pytz import UTC
import os
import shlex
import getpass
from typing import Literal
import click
import typer
from modaic import AutoProgram

from utils.cache import (
    clear_openrouter_key,
    load_openrouter_key,
    load_settings_config,
    save_openrouter_key,
    save_settings_config,
)
from utils.constants import (
    BOLD,
    BLUE,
    CYAN,
    DIM,
    GREEN,
    RED,
    RESET,
    BANNER_ART,
    MODAIC_REPO_PATH,
    DEFAULT_HISTORY_LIMIT,
)
from utils.display import render_markdown, separator
from utils.models import handle_model_command, resolve_startup_models
from utils.mcp import handle_add_mcp_command, register_mcp_server
from utils.paste import consume_paste_for_input, read_user_input

app = typer.Typer(add_completion=False, help="Microcode interactive CLI.")


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
    env = os.getenv("MODAIC_ENV")
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
        f"{DIM}RLM:{RESET}",
        f"  {DIM}model:{RESET} {model.removeprefix('openrouter/')}",
        f"  {DIM}sub_model:{RESET} {sub_lm.removeprefix('openrouter/')}",
        "",
        f"{DIM}Settings:{RESET}",
        f"  {DIM}max_turns:{RESET} {history_limit}",
        f"  {DIM}max_tokens:{RESET} {format_setting(max_tokens)}",
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


def print_status_line(model: str, sub_lm: str, cwd: str, mcp_servers: dict) -> None:
    """
    Print the status line with current configuration.

    Args:
        model: The primary model ID
        sub_lm: The sub model ID
        cwd: The current working directory
        mcp_servers: Dictionary of MCP servers
    """
    mcp_label = f"{len(mcp_servers)}" if mcp_servers else "0"
    click.echo(
        f"{DIM}cwd:{RESET} {cwd}  {DIM}RLM(model):{RESET} {model.removeprefix('openrouter/')}  "
        f"{DIM}sub_model:{RESET} {sub_lm.removeprefix('openrouter/')}  {DIM}mcp_tools:{RESET} {mcp_label}"
        "\n"
    )


def run_interactive(
    history_limit: int,
    show_banner: bool,
    model: str | None = None,
    sub_lm: str | None = None,
    api_key: str | None = None,
    max_iterations: int | None = None,
    max_tokens: int | None = None,
    max_output_chars: int | None = None,
    api_base: str | None = None,
    verbose: bool | None = None,
    env: str | None = None,
) -> None:
    """
    Run the interactive CLI session.

    This function initializes the agent and starts the interactive loop.
    It handles user input, processes commands, and manages the conversation history.

    Args:
        history_limit: Maximum number of messages to keep in history
        show_banner: Whether to display the startup banner
        model: Override for the primary model ID
        sub_lm: Override for the sub model ID
        api_key: Override for the API key
        max_iterations: Maximum number of iterations
        max_tokens: Maximum number of tokens
        max_output_chars: Maximum number of output characters
        api_base: Override for the API base URL
        verbose: Enable verbose logging
        env: Set the environment (dev or prod)
    """
    if model is None:
        model = os.getenv("MICROCODE_MODEL")
    if sub_lm is None:
        sub_lm = os.getenv("MICROCODE_SUB_LM")
    if env is None:
        env = os.getenv("MODAIC_ENV") or os.getenv("MICROCODE_ENV")
    cached_settings = load_settings_config()
    if verbose is None:
        env_verbose = os.getenv("MICROCODE_VERBOSE")
        if env_verbose is not None:
            verbose = env_verbose == "1"
        elif "verbose" in cached_settings:
            verbose = bool(cached_settings["verbose"])
        else:
            verbose = False
    if max_iterations is None:
        max_iterations = read_int_env("MICROCODE_MAX_ITERATIONS")
        if max_iterations is None:
            max_iterations = cached_settings.get("max_iters")
    if max_tokens is None:
        max_tokens = read_int_env("MICROCODE_MAX_TOKENS")
        if max_tokens is None:
            max_tokens = cached_settings.get("max_tokens")
    if max_output_chars is None:
        max_output_chars = read_int_env("MICROCODE_MAX_OUTPUT_CHARS")
        if max_output_chars is None:
            max_output_chars = cached_settings.get("max_output_chars")
    if api_base is None:
        api_base = os.getenv("MICROCODE_API_BASE")
        if api_base is None:
            api_base = cached_settings.get("api_base")

    if env:
        os.environ["MODAIC_ENV"] = env
    if api_key and not os.getenv("OPENROUTER_API_KEY"):
        os.environ["OPENROUTER_API_KEY"] = api_key

    openrouter_key = load_openrouter_key()
    if openrouter_key and not os.getenv("OPENROUTER_API_KEY"):
        os.environ["OPENROUTER_API_KEY"] = openrouter_key

    model, sub_lm = resolve_startup_models(model, sub_lm)

    config = {"lm": model, "sub_lm": sub_lm, "verbose": verbose}
    if max_iterations is not None:
        config["max_iters"] = max_iterations
    if max_tokens is not None:
        config["max_tokens"] = max_tokens
    if max_output_chars is not None:
        config["max_output_chars"] = max_output_chars
    if api_base:
        config["api_base"] = api_base

    save_settings_config(
        max_iters=max_iterations,
        max_tokens=max_tokens,
        max_output_chars=max_output_chars,
        api_base=api_base,
        verbose=verbose,
    )

    agent = AutoProgram.from_precompiled(  # Load rlm program from modaic
        MODAIC_REPO_PATH,
        rev=os.getenv("MODAIC_ENV", "prod"),
        config=config,
    )

    cwd = os.getcwd()

    if show_banner:
        print_banner(
            model,
            sub_lm,
            cwd,
            history_limit,
            max_iterations,
            max_tokens,
            max_output_chars,
            verbose,
        )
        click.echo()
        click.echo()
        click.echo()

    history = []
    mcp_servers = {}

    while True:
        try:
            click.echo(separator())
            user_input = read_user_input(f"{BOLD}{BLUE}❯{RESET} ").strip()

            if not user_input:
                continue

            if user_input in ("/q", "exit"):
                break

            if user_input in ("/help", "/h", "?"):
                print_help()
                continue

            if user_input in ("/clear", "/cls"):
                click.clear()
                continue

            if user_input.startswith("/key"):
                parts = shlex.split(user_input)
                args = parts[1:]

                if args and args[0] in ("clear", "unset", "remove"):
                    clear_openrouter_key()
                    os.environ.pop("OPENROUTER_API_KEY", None)
                    click.echo(f"{GREEN}⏺ OpenRouter key cleared{RESET}")
                    continue

                key = (
                    args[0]
                    if args
                    else getpass.getpass(
                        f"{BOLD}{BLUE}❯{RESET} Enter OpenRouter API key (input hidden): "
                    ).strip()
                )

                if not key:
                    click.echo(f"{RED}⏺ OpenRouter key not set (empty input){RESET}")
                    continue

                save_openrouter_key(key)
                os.environ["OPENROUTER_API_KEY"] = key
                click.echo(f"{GREEN}⏺ OpenRouter key saved to cache{RESET}")
                continue

            if user_input == "/c":
                history = []
                click.echo(f"{GREEN}⏺ Cleared conversation{RESET}")
                continue

            handled = False
            if user_input.startswith("/model"):
                handled, agent, new_sub_lm = handle_model_command(
                    user_input,
                    agent,
                    mcp_servers,
                    register_mcp_server,
                    MODAIC_REPO_PATH,
                )
                click.echo(separator())
                print_status_line(model, sub_lm, cwd, mcp_servers)

            if handled:
                if new_sub_lm:
                    sub_lm = new_sub_lm
                continue

            if user_input.startswith("/mcp"):
                if handle_add_mcp_command(user_input, agent, mcp_servers):
                    continue

            context = f"Working directory: {os.getcwd()}\nTime: {datetime.now(UTC).strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            if history:
                context += "Previous conversation:\n"
                for h in history[-history_limit:]:
                    context += f"User: {h['user']}\nAssistant: {h['assistant']}\n\n"

            paste_payload = consume_paste_for_input(user_input)
            if paste_payload:
                context += f"\nPasted content:\n{paste_payload['text']}\n"

            task = f"Current task: {user_input}\n{context}\n"

            with open("debug.txt", "w") as f:
                f.write(task)

            click.echo(f"\n{CYAN}⏺{RESET} Thinking...", nl=True)

            result = agent(task=task)

            click.echo(f"\n{CYAN}⏺{RESET} {render_markdown(result.answer)}")
            # click.echo(f"\n{MAGENTA}⏺ Affected files: {result.affected_files}{RESET}")

            history.append({"user": user_input, "assistant": result.answer})
            click.echo()

        except (KeyboardInterrupt, EOFError):
            break

        except Exception as err:
            auth_message = format_auth_error(err)
            if auth_message:
                click.echo(f"{RED}⏺ {auth_message}{RESET}")
                continue

            import traceback

            traceback.print_exc()
            click.echo(f"{RED}⏺ Error: {err}{RESET}")


@app.callback(invoke_without_command=True)
def cli(
    ctx: typer.Context,
    model: str | None = typer.Option(
        None, "--lm", "-m", help="Override primary model ID."
    ),
    sub_lm: str | None = typer.Option(
        None, "--sub-lm", help="Override sub_lm model ID."
    ),
    api_key: str | None = typer.Option(None, "--api-key", help="Override API key."),
    max_iterations: int = typer.Option(
        50, "--max-iterations", help="Maximum number of iterations."
    ),
    max_tokens: int = typer.Option(
        50000, "--max-tokens", help="Maximum number of tokens."
    ),
    max_output_chars: int = typer.Option(
        100000, "--max-output-tokens", help="Maximum number of output tokens."
    ),
    api_base: str = typer.Option(
        "https://openrouter.ai/api/v1", "--api-base", help="Override API base URL."
    ),
    verbose: bool = typer.Option(
        False, "--verbose", "-v", help="Enable verbose logging."
    ),
    env: Literal["dev", "prod"] = typer.Option(
        os.getenv("MODAIC_ENV", os.getenv("MICROCODE_ENV", "prod")),
        "--env",
        help="Set MODAIC_ENV.",
    ),
    history_limit: int = typer.Option(
        DEFAULT_HISTORY_LIMIT, "--max-turns", min=1, max=25, help="History size."
    ),
    no_banner: bool = typer.Option(
        False, "--no-banner", help="Disable the startup banner."
    ),
) -> None:
    """
    Main CLI entry point.

    This function handles the main command-line interface for the microcode tool.
    It processes various options and sets environment variables accordingly.
    If a subcommand is invoked, it returns early without executing the main loop.

    Args:
        ctx: The Typer context object
        model: Override for the primary model ID
        sub_lm: Override for the sub model ID
        api_key: Override for the API key
        max_iterations: Maximum number of iterations
        max_tokens: Maximum number of tokens
        max_output_chars: Maximum number of output characters
        api_base: Override for the API base URL
        verbose: Enable verbose logging
        env: Set the environment (dev or prod)
        history_limit: History size limit
        no_banner: Disable the startup banner
    """
    if ctx.invoked_subcommand is not None:
        return
    if model:
        os.environ["MICROCODE_MODEL"] = model
    if sub_lm:
        os.environ["MICROCODE_SUB_LM"] = sub_lm
    if env:
        os.environ["MODAIC_ENV"] = env
    if verbose:
        os.environ["MICROCODE_VERBOSE"] = "1"
    if max_iterations:
        os.environ["MICROCODE_MAX_ITERATIONS"] = str(max_iterations)
    if max_tokens:
        os.environ["MICROCODE_MAX_TOKENS"] = str(max_tokens)
    if max_output_chars:
        os.environ["MICROCODE_MAX_OUTPUT_CHARS"] = str(max_output_chars)
    if api_base:
        os.environ["MICROCODE_API_BASE"] = api_base
    if api_key:
        os.environ["OPENROUTER_API_KEY"] = api_key
    if no_banner:
        os.environ["MICROCODE_NO_BANNER"] = "1"

    show_banner = not no_banner

    run_interactive(
        history_limit=history_limit,
        show_banner=show_banner,
        model=model,
        sub_lm=sub_lm,
        api_key=api_key,
        max_iterations=max_iterations,
        max_tokens=max_tokens,
        max_output_chars=max_output_chars,
        api_base=api_base,
        verbose=verbose,
        env=env,
    )


def main() -> None:
    app()


if __name__ == "__main__":
    main()
