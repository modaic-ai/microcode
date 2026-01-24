import os
from typing import Any, Callable

import click
from textual.app import App, ComposeResult
from textual.widgets import OptionList, Static
from textual.widgets.option_list import Option

from modaic import AutoProgram, PrecompiledProgram

from .cache import load_model_config, save_model_config
from .constants import AVAILABLE_MODELS, GREEN, RED, RESET


def normalize_model_id(model_id: str) -> str:
    """
    Normalize a model ID by ensuring it starts with "openrouter/".

    Args:
        model_id: The model ID to normalize

    Returns:
        The normalized model ID
    """
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
    """
    Prompt the user to select a model using a TUI.

    Args:
        title: The title to display in the TUI
        options: List of Option objects to display

    Returns:
        The selected option ID, or None if cancelled
    """
    app = ModelSelectApp(title, options)
    app.run()
    return app.selection


def _build_model_options(
    include_custom: bool = False,
    include_keep: bool = False,
    include_primary: bool = False,
) -> list[Option]:
    """
    Build a list of model options for selection.

    Args:
        include_custom: Whether to include a "Custom model" option
        include_keep: Whether to include a "Keep current model" option
        include_primary: Whether to include a "Use primary model" option

    Returns:
        List of Option objects
    """
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
    """
    Interactive model selection.

    Returns:
        The selected model ID
    """
    assert isinstance(AVAILABLE_MODELS, dict), "AVAILABLE_MODELS must be a dict"

    while True:
        selection = prompt_model_tui(
            "Select a base RLM model:",
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

        return selection


def select_sub_model(primary_model: str) -> str:
    """
    Interactive sub model selection.

    Args:
        primary_model: The primary model ID

    Returns:
        The selected sub model ID
    """
    assert isinstance(primary_model, str), "primary_model must be a str"

    while True:
        selection = prompt_model_tui(
            "Select the RLM's sub model (usually a smaller, faster model than the base):",
            _build_model_options(include_custom=True, include_primary=True),
        )

        if selection is None:
            click.echo(f"{RED}⏺ Sub model selection cancelled{RESET}")
            exit(1)

        if selection == PRIMARY_OPTION:
            click.echo(
                f"{GREEN}⏺ sub model set to primary model: {primary_model.removeprefix('openrouter/')}{RESET}"
            )
            return primary_model

        if selection == CUSTOM_OPTION:
            custom_sub = click.prompt(
                "Enter sub model ID",
                default="",
                show_default=False,
            ).strip()
            if custom_sub:
                click.echo(f"{GREEN}⏺ Selected custom sub model: {custom_sub}{RESET}")
                return custom_sub
            click.echo(f"{RED}⏺ Invalid sub model ID{RESET}")
            continue

        return selection


def resolve_startup_models(
    model_override: str | None = None,
    sub_lm_override: str | None = None,
) -> tuple[str, str]:
    """
    Resolve the primary and sub model IDs from environment variables, cache, or user selection.

    Args:
        model_override: Override for the primary model ID
        sub_lm_override: Override for the sub model ID

    Returns:
        Tuple of (primary_model_id, sub_model_id)
    """
    assert isinstance(AVAILABLE_MODELS, dict), "AVAILABLE_MODELS must be a dict"

    model_env = model_override or os.getenv("MICROCODE_MODEL")
    sub_env = sub_lm_override or os.getenv("MICROCODE_SUB_LM")
    cached_model, cached_sub_lm = load_model_config()

    first_time = False

    if model_env:
        assert isinstance(model_env, str), "MICROCODE_MODEL must be a str"
        model = model_env

    elif cached_model:
        model = cached_model

    else:
        model = select_model()
        first_time = True

    normalized_model = normalize_model_id(model)

    if sub_env:
        assert isinstance(sub_env, str), "MICROCODE_SUB_LM must be a str"
        sub_lm = sub_env

    elif model_env:
        sub_lm = model

    elif first_time:
        sub_lm = select_sub_model(normalized_model)

    elif cached_sub_lm:
        if cached_model and not model_env:
            print()
        sub_lm = cached_sub_lm

    else:
        sub_lm = model

    normalized_sub_lm = normalize_model_id(sub_lm)

    if model_env or sub_env or first_time:
        save_model_config(normalized_model, normalized_sub_lm)
    elif cached_model and not cached_sub_lm:
        save_model_config(normalized_model, normalized_sub_lm)

    return normalized_model, normalized_sub_lm


def handle_model_command(
    user_input: str,
    agent: PrecompiledProgram,
    mcp_servers: dict[str, dict[str, Any]],
    register_mcp_server: Callable[[PrecompiledProgram, str, Any], list[str]],
    repo_path: str,
) -> tuple[bool, PrecompiledProgram, str]:
    """
    Handle the /model command.

    Args:
        user_input: The user input string
        agent: The PrecompiledProgram agent
        mcp_servers: Dictionary of registered MCP servers
        register_mcp_server: Function to register MCP servers
        repo_path: The repository path

    Returns:
        Tuple of (handled, agent, new_model)
    """
    assert isinstance(user_input, str), "user_input must be a str"
    assert isinstance(agent, PrecompiledProgram), "agent must be PrecompiledProgram"
    assert isinstance(mcp_servers, dict), "mcp_servers must be a dict"
    assert callable(register_mcp_server), "register_mcp_server must be callable"
    assert isinstance(repo_path, str), "repo_path must be a str"

    new_model = agent.config.lm
    model_selection = prompt_model_tui(
        "Select a base RLM model:",
        _build_model_options(include_custom=True, include_keep=True),
    )

    if model_selection is None:
        print(
            f"{GREEN}⏺ Keeping current model: {agent.config.lm.removeprefix('openrouter/')}{RESET}"
        )
        print(
            f"{GREEN}⏺ Keeping current sub model: {agent.config.sub_lm.removeprefix('openrouter/')}{RESET}"
        )
        return True, agent, normalize_model_id(agent.config.sub_lm)

    if model_selection == KEEP_OPTION:
        print(
            f"{GREEN}⏺ Keeping current model: {agent.config.lm.removeprefix('openrouter/')}{RESET}"
        )

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

    else:
        new_model = normalize_model_id(model_selection)

    sub_selection = prompt_model_tui(
        "Select the RLM's sub model (usually a smaller, faster model than the base):",
        _build_model_options(
            include_custom=True,
            include_keep=True,
            include_primary=True,
        ),
    )

    if sub_selection is None or sub_selection == KEEP_OPTION:
        new_sub_lm = normalize_model_id(agent.config.sub_lm)

    elif sub_selection == PRIMARY_OPTION:
        new_sub_lm = normalize_model_id(new_model)

    elif sub_selection == CUSTOM_OPTION:
        custom_sub = click.prompt(
            "Enter sub model ID",
            default="",
            show_default=False,
        ).strip()

        if not custom_sub:
            new_sub_lm = normalize_model_id(agent.config.sub_lm)

        else:
            new_sub_lm = normalize_model_id(custom_sub)

    else:
        new_sub_lm = normalize_model_id(sub_selection)

    config = {"lm": normalize_model_id(new_model), "sub_lm": new_sub_lm}
    for key in ("max_iters", "max_tokens", "max_output_chars", "api_base", "verbose"):
        if hasattr(agent.config, key):
            value = getattr(agent.config, key)
            if value is not None:
                config[key] = value

    agent = AutoProgram.from_precompiled(
        repo_path, rev=os.getenv("MODAIC_ENV", "prod"), config=config
    )
    for server_name, info in mcp_servers.items():
        info["tools"] = register_mcp_server(agent, server_name, info["server"])

    save_model_config(normalize_model_id(new_model), new_sub_lm)
    return True, agent, new_sub_lm
