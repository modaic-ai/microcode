import os
from typing import Any, Callable

import click
from textual.app import App, ComposeResult
from textual.widgets import OptionList, Static
from textual.widgets.option_list import Option

from modaic import PrecompiledProgram

from .cache import load_model_config, save_model_config
from .display import BOLD, DIM, GREEN, RED, RESET

AVAILABLE_MODELS = {
    "1": ("GPT-5.2 Codex", "openai/gpt-5.2-codex"),
    "2": ("GPT-5.2", "openai/gpt-5.2"),
    "3": ("Claude Opus 4.5", "anthropic/claude-opus-4.5"),
    "4": ("Claude Opus 4", "anthropic/claude-opus-4"),
    "5": ("Qwen 3 Coder", "qwen/qwen3-coder"),
    "6": ("Gemini 3 Flash Preview", "google/gemini-3-flash-preview"),
    "7": ("Kimi K2 0905", "moonshotai/kimi-k2-0905"),
    "8": ("Minimax M2.1", "minimax/minimax-m2.1"),
}


def normalize_model_id(model_id: str) -> str:
    assert isinstance(model_id, str), "model_id must be a str"
    return model_id if model_id.startswith("openrouter/") else f"openrouter/{model_id}"


CUSTOM_OPTION = "__custom__"
KEEP_OPTION = "__keep__"
PRIMARY_OPTION = "__primary__"


class ModelSelectApp(App[None]):
    BINDINGS = [("q", "quit", "Quit")]

    def __init__(self, title: str, options: list[Option]):
        super().__init__()
        self.title = title
        self.options = options
        self.selection: str | None = None

    def compose(self) -> ComposeResult:
        yield Static(self.title, id="title")
        yield OptionList(*self.options, id="options")

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        self.selection = event.option_id
        self.exit()

    def on_mount(self) -> None:
        # Add subtle dimming to the title
        title_widget = self.query_one("#title", Static)
        title_widget.styles.padding = 1


def prompt_model_tui(title: str, options: list[Option]) -> str | None:
    app = ModelSelectApp(title, options)
    app.run()
    return app.selection


def _build_model_options(
    include_custom: bool = False,
    include_keep: bool = False,
    include_primary: bool = False,
) -> list[Option]:
    options = [
        Option(f"{name} ({model_id})", id=model_id)
        for name, model_id in AVAILABLE_MODELS.values()
    ]

    if include_primary:
        options.append(Option("Use primary model", id=PRIMARY_OPTION))

    if include_custom:
        options.append(Option("Custom model (enter manually)", id=CUSTOM_OPTION))

    if include_keep:
        options.append(Option("Keep current model", id=KEEP_OPTION))
    return options


def select_model() -> str:
    """Interactive model selection."""
    assert isinstance(AVAILABLE_MODELS, dict), "AVAILABLE_MODELS must be a dict"

    while True:
        selection = prompt_model_tui(
            "Select a model",
            _build_model_options(include_custom=True),
        )

        if selection is None:
            click.echo(f"{RED}⏺ Model selection cancelled{RESET}")
            exit(1)

        if selection == CUSTOM_OPTION:
            custom_model = click.prompt(
                "Enter model ID (e.g., openai/gpt-4)",
                default="",
                show_default=False,
            ).strip()
            if custom_model:
                click.echo(f"{GREEN}⏺ Selected custom model: {custom_model}{RESET}")
                return custom_model
            click.echo(f"{RED}⏺ Invalid model ID{RESET}")
            continue

        name = next(
            name
            for name, model_id in AVAILABLE_MODELS.values()
            if model_id == selection
        )

        click.echo(f"{GREEN}⏺ Selected: {name}{RESET}")
        return selection


def resolve_startup_models() -> tuple[str, str]:
    assert isinstance(AVAILABLE_MODELS, dict), "AVAILABLE_MODELS must be a dict"

    model_env = os.getenv("MODEL")
    sub_env = os.getenv("SUB_LM")
    cached_model, cached_sub_lm = load_model_config()

    if model_env:
        assert isinstance(model_env, str), "MODEL must be a str"
        model = model_env

    elif cached_model:
        model = cached_model

    else:
        model = select_model()
        normalized_model = normalize_model_id(model)
        save_model_config(normalized_model, normalized_model)
        cached_sub_lm = normalized_model

    if sub_env:
        assert isinstance(sub_env, str), "SUB_LM must be a str"
        sub_lm = sub_env
    elif cached_sub_lm:
        if cached_model and not model_env:
            print()
        sub_lm = cached_sub_lm
    else:
        sub_lm = model

    if cached_model and not cached_sub_lm:
        save_model_config(normalize_model_id(model), normalize_model_id(sub_lm))

    return normalize_model_id(model), normalize_model_id(sub_lm)


def handle_model_command(
    user_input: str,
    agent: PrecompiledProgram,
    mcp_servers: dict[str, dict[str, Any]],
    register_mcp_server: Callable[[PrecompiledProgram, str, Any], list[str]],
    repo_path: str,
) -> tuple[bool, PrecompiledProgram, str]:
    assert isinstance(user_input, str), "user_input must be a str"
    assert isinstance(agent, PrecompiledProgram), "agent must be PrecompiledProgram"
    assert isinstance(mcp_servers, dict), "mcp_servers must be a dict"
    assert callable(register_mcp_server), "register_mcp_server must be callable"
    assert isinstance(repo_path, str), "repo_path must be a str"

    if user_input != "/model":
        return False, agent, ""

    print(f"\n{BOLD}Current RLM(model): {agent.config.lm.removeprefix('openrouter/')}{RESET}")
    print(f"{BOLD}Current sub model: {agent.config.sub_lm.removeprefix('openrouter/')}{RESET}")

    new_model = agent.config.lm
    model_selection = prompt_model_tui(
        "Select a new RLM(model):",
        _build_model_options(include_custom=True, include_keep=True),
    )

    if model_selection is None:
        print(f"{GREEN}⏺ Keeping current model: {agent.config.lm.removeprefix('openrouter/')}{RESET}")
        print(
            f"{GREEN}⏺ Keeping current sub model: {agent.config.sub_lm.removeprefix('openrouter/')}{RESET}"
        )
        return True, agent, normalize_model_id(agent.config.sub_lm)

    if model_selection == KEEP_OPTION:
        print(f"{GREEN}⏺ Keeping current model: {agent.config.lm.removeprefix('openrouter/')}{RESET}")

    elif model_selection == CUSTOM_OPTION:
        custom_model = click.prompt(
            "Enter model ID",
            default="",
            show_default=False,
        ).strip()

        if not custom_model:
            print(f"{RED}⏺ Invalid model ID, keeping current model{RESET}")
            return True, agent, normalize_model_id(agent.config.sub_lm)
        new_model = normalize_model_id(custom_model)
        print(f"{GREEN}⏺ Selected custom model: {new_model}{RESET}")

    else:
        new_model = normalize_model_id(model_selection)
        name = next(
            name
            for name, model_id in AVAILABLE_MODELS.values()
            if model_id == model_selection
        )
        print(f"{GREEN}⏺ Selected: {name} ({new_model}){RESET}")

    sub_selection = prompt_model_tui(
        "Select a sub model:",
        _build_model_options(
            include_custom=True,
            include_keep=True,
            include_primary=True,
        ),
    )

    if sub_selection is None or sub_selection == KEEP_OPTION:
        new_sub_lm = normalize_model_id(agent.config.sub_lm)
        print(f"{GREEN}⏺ Keeping current sub model: {new_sub_lm.removeprefix('openrouter/')}{RESET}")

    elif sub_selection == PRIMARY_OPTION:
        new_sub_lm = normalize_model_id(new_model)
        print(f"{GREEN}⏺ sub model set to primary model: {new_sub_lm.removeprefix('openrouter/')}{RESET}")

    elif sub_selection == CUSTOM_OPTION:
        custom_sub = click.prompt(
            "Enter sub model ID",
            default="",
            show_default=False,
        ).strip()

        if not custom_sub:
            print(f"{RED}⏺ Invalid sub model ID, keeping current sub model{RESET}")
            new_sub_lm = normalize_model_id(agent.config.sub_lm)

        else:
            new_sub_lm = normalize_model_id(custom_sub)
            print(f"{GREEN}⏺ Selected custom sub model: {new_sub_lm.removeprefix('openrouter/')}{RESET}")

    else:
        new_sub_lm = normalize_model_id(sub_selection)
        print(f"{GREEN}⏺ Selected sub model: {new_sub_lm.removeprefix('openrouter/')}{RESET}")

    agent = agent.__class__.from_precompiled(
        repo_path, config={"lm": normalize_model_id(new_model), "sub_lm": new_sub_lm}
    )
    for server_name, info in mcp_servers.items():
        info["tools"] = register_mcp_server(agent, server_name, info["server"])

    save_model_config(normalize_model_id(new_model), new_sub_lm)
    print(
        f"{GREEN}⏺ Switched to: {normalize_model_id(new_model)} | sub model: {new_sub_lm.removeprefix('openrouter/')}{RESET}"
    )
    return True, agent, new_sub_lm
