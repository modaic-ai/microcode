import os
import shlex
import getpass
import click
import typer
from modaic import AutoProgram

from utils.cache import clear_openrouter_key, load_openrouter_key, save_openrouter_key
from utils.display import (
    BOLD,
    BLUE,
    CYAN,
    DIM,
    GREEN,
    RED,
    RESET,
    render_markdown,
    separator,
)
from utils.models import handle_model_command, resolve_startup_models
from utils.mcp import handle_add_mcp_command, register_mcp_server
from utils.paste import consume_paste_for_input, read_user_input

MODAIC_REPO_PATH = "farouk1/nanocode"
DEFAULT_HISTORY_LIMIT = 5
app = typer.Typer(add_completion=False, help="Microcode interactive CLI.")


def format_auth_error(err: Exception) -> str | None:
    message = str(err)
    if (
        "OpenrouterException" in message
        and "No cookie auth credentials found" in message
    ):
        return (
            "OpenRouter authentication failed: no credentials found. "
            "Set `OPENROUTER_API_KEY` or run `/openrouter-key` to cache it."
        )
    if "AuthenticationError" in message and "OpenrouterException" in message:
        return (
            "OpenRouter authentication failed. "
            "Set `OPENROUTER_API_KEY` or run `/openrouter-key` to cache it."
        )
    return None


def short_cwd(path: str) -> str:
    parts = path.split(os.sep)
    if len(parts) <= 2:
        return path
    return os.sep.join(parts[-2:])


def print_banner(model: str, sub_lm: str, cwd: str, history_limit: int) -> None:
    env = os.getenv("MODAIC_ENV")
    env_label = f"{DIM}env:{RESET} {env}" if env else f"{DIM}env:{RESET} prod"
    click.echo(
        f"{BOLD}{BLUE}MICROCODE{RESET} {DIM} RLM TERMINAL AGENT{RESET}\n"
        f"{DIM}RLM(model):{RESET} {model.removeprefix('openrouter/')}\n"
        f"{DIM}sub model:{RESET} {sub_lm.removeprefix('openrouter/')}"
    )
    click.echo(
        f"{DIM}cwd:{RESET} {cwd} | {env_label} | {DIM}history:{RESET} {history_limit}"
    )
    click.echo(
        f"{DIM}Quick commands:{RESET} \n{BLUE}/help{RESET}\n{BLUE}/model{RESET}\n{BLUE}/openrouter-key{RESET}\n{BLUE}/c{RESET}\n{BLUE}/q{RESET}"
    )


def print_help() -> None:
    click.echo(f"\n{BOLD}Microcode commands{RESET}")
    click.echo(f"  {BLUE}/help{RESET}            Show this help")
    click.echo(f"  {BLUE}/model{RESET}           Change model and sub_lm")
    click.echo(f"  {BLUE}/openrouter-key{RESET}  Set or clear OpenRouter key")
    click.echo(f"  {BLUE}/clear{RESET}           Clear the screen")
    click.echo(f"  {BLUE}/c{RESET}               Clear conversation history")
    click.echo(f"  {BLUE}/q{RESET}               Quit")


def print_status_line(model: str, sub_lm: str, cwd: str, mcp_servers: dict) -> None:
    mcp_label = f"{len(mcp_servers)}" if mcp_servers else "0"
    click.echo(
        f"{DIM}cwd:{RESET} {cwd}  {DIM}RLM(model):{RESET} {model.removeprefix('openrouter/')}  "
        f"{DIM}sub model:{RESET} {sub_lm.removeprefix('openrouter/')}  {DIM}mcp tools:{RESET} {mcp_label}"
        "\n"
    )


def run_interactive(history_limit: int, show_banner: bool) -> None:
    cached_key = load_openrouter_key()
    if cached_key and not os.getenv("OPENROUTER_API_KEY"):
        os.environ["OPENROUTER_API_KEY"] = cached_key
        click.echo(f"{GREEN}⏺ Loaded OpenRouter key from cache{RESET}")

    model, sub_lm = resolve_startup_models()

    agent = AutoProgram.from_precompiled(  # load rlm program from modaic
        MODAIC_REPO_PATH,
        rev=os.getenv("MODAIC_ENV", "prod"),
        config={"lm": model, "sub_lm": sub_lm, "verbose": True},
    )

    cwd = short_cwd(os.getcwd())

    if show_banner:
        print_banner(model, sub_lm, cwd, history_limit)
        print()

    history = []
    mcp_servers = {}

    while True:
        try:
            print(separator())
            print_status_line(model, sub_lm, cwd, mcp_servers)
            user_input = read_user_input(f"{BOLD}{BLUE}❯{RESET} ").strip()
            print(separator())

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

            if user_input.startswith("/openrouter-key"):
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

            handled, agent, new_sub_lm = handle_model_command(
                user_input, agent, mcp_servers, register_mcp_server, MODAIC_REPO_PATH
            )

            if handled:
                if new_sub_lm:
                    sub_lm = new_sub_lm
                continue

            if handle_add_mcp_command(user_input, agent, mcp_servers):
                continue

            context = f"Working directory: {os.getcwd()}\n"
            if history:
                context += "\nPrevious conversation:\n"
                for h in history[-history_limit:]:
                    context += f"User: {h['user']}\nAssistant: {h['assistant']}\n\n"

            paste_payload = consume_paste_for_input(user_input)
            if paste_payload:
                context += f"\nPasted content:\n{paste_payload['text']}\n"
            task = f"{context}\nCurrent task: {user_input}"
            with open("debug.txt", "w") as f:
                f.write(task)

            click.echo(f"\n{CYAN}⏺{RESET} Thinking...", nl=True)

            result = agent(task=task)

            click.echo(f"\n{CYAN}⏺{RESET} {render_markdown(result.answer)}")
            # click.echo(f"\n{MAGENTA}⏺ Affected files: {result.affected_files}{RESET}")

            history.append({"user": user_input, "assistant": result.answer})
            print()

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
    api_base: str | None = typer.Option(
        None, "--api-base", help="Override API base URL."
    ),
    verbose: bool | None = typer.Option(
        False, "--verbose", "-v", help="Enable verbose logging."
    ),
    env: str | None = typer.Option(None, "--env", help="Set MODAIC_ENV."),
    history_limit: int = typer.Option(
        DEFAULT_HISTORY_LIMIT, "--max-turns", min=1, max=25, help="History size."
    ),
    no_banner: bool = typer.Option(
        False, "--no-banner", help="Disable the startup banner."
    ),
) -> None:
    if ctx.invoked_subcommand is not None:
        return
    if model:
        os.environ["MODEL"] = model
    if sub_lm:
        os.environ["SUB_LM"] = sub_lm
    if env:
        os.environ["MODAIC_ENV"] = env
    if verbose is not None:
        os.environ["VERBOSE"] = "1" if verbose else "0"
    if api_base:
        os.environ["API_BASE"] = api_base
    run_interactive(history_limit=history_limit, show_banner=not no_banner)


def main() -> None:
    app()


if __name__ == "__main__":
    main()
