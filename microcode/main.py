from datetime import datetime
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
    MODAIC_REPO_PATH,
    DEFAULT_HISTORY_LIMIT,
)
from utils.display import (
    render_markdown,
    separator,
    print_banner,
    print_status_line,
    print_help,
    format_auth_error,
    read_int_env,
)
from utils.models import handle_model_command, resolve_startup_models
from utils.mcp import handle_add_mcp_command, register_mcp_server
from utils.paste import consume_paste_for_input, read_user_input

app = typer.Typer(add_completion=False, help="Microcode interactive CLI.")


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
    paste_store = {}
    paste_counter = 0

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
                print_status_line(
                    agent.lm.model.removeprefix("openrouter/"),
                    agent.sub_lm.model.removeprefix("openrouter/"),
                    cwd,
                    mcp_servers,
                )

            if handled:
                if new_sub_lm:
                    sub_lm = new_sub_lm
                continue

            if user_input.startswith("/mcp"):
                if handle_add_mcp_command(user_input, agent, mcp_servers):
                    continue

            paste_payload = consume_paste_for_input(user_input)
            if paste_payload:
                paste_counter += 1
                paste_id = f"paste_{paste_counter}"
                paste_store[paste_id] = paste_payload["text"]
                user_input = user_input.replace(
                    paste_payload["placeholder"], f"[{paste_id}]"
                )

            context_lines = [
                f"cwd: {os.getcwd()}",
                f"time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                f"Current Task: {user_input}",
                "Previous Conversation History:",
            ]
            if history:
                for h in history[-history_limit:]:
                    context_lines.append(f"  User: {h['user']}")
                    context_lines.append(f"  Assistant: {h['assistant']}")
            else:
                context_lines.append("  None")

            context_lines.append("All Pasted Content:")
            if paste_store:
                for paste_id in paste_store:
                    context_lines.append(f"[{paste_id}]")
                context_lines.append(str(paste_store))
            else:
                context_lines.append("  None")

            task = "\n".join(context_lines) + "\n"
            if os.getenv("MODAIC_ENV") == "dev":
                with open("debug.txt", "w") as f:
                    f.write(task + "\n")

            click.echo(f"\n{CYAN}⏺{RESET} Thinking...", nl=True)
            result = agent(task=task)

            click.echo(f"\n{CYAN}⏺{RESET} {render_markdown(result.answer)}")

            history.append(
                {"user": user_input, "assistant": result.answer, "pasted_content": None}
            )
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
