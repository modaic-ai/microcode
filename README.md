# Microcode
> Minimal Terminal Agent powered by RLMs

[![Python Version](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-0.1.6-orange.svg)](https://github.com/modaic-ai/microcode)

Microcode is an efficient terminal-based AI agent that provides an interactive REPL experience for coding assistance. It leverages Reasoning Language Models (RLMs) to help developers with coding tasks directly from the command line. Because we are using RLMs, it can handle extra large code snippets, file contents, and pasted content with ease.

## Features

- **Interactive CLI** - Seamless conversational interface with AI models
- **Multiple Model Support** - Choose from various AI providers (OpenAI, Anthropic, Google, Qwen, etc.)
- **MCP Integration** - Model Context Protocol server support for extended capabilities
- **Smart Caching** - Persistent settings, API keys, and model configurations
- **Rich Terminal UI** - Beautiful output with markdown rendering, gradient banners, and status indicators
- **Paste Support** - Handle large code snippets and file contents with ease
- **Configurable** - Environment variables and CLI flags for full customization

## Installation

### Prerequisites

- Python 3.13 or higher
- [uv](https://github.com/astral-sh/uv) (recommended) or pip

### Install via pip

```bash
pip install microcode
```

### Install from source

```bash
git clone https://github.com/modaic-ai/microcode.git
cd microcode
uv sync  # or: pip install -e .
```

## Configuration

### API Key Setup

Microcode uses [OpenRouter](https://openrouter.ai/) for model access. Set your API key using one of these methods:

1. **Environment Variable** (recommended for CI/CD):
   ```bash
   export OPENROUTER_API_KEY="your-api-key"
   ```

2. **Interactive Setup** (persisted to cache):
   ```bash
   microcode
   /key  # Then enter your API key when prompted
   ```

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENROUTER_API_KEY` | OpenRouter API key | - |
| `MICROCODE_MODEL` | Primary model ID | Auto-selected |
| `MICROCODE_SUB_LM` | Sub-model for auxiliary tasks | Auto-selected |
| `MICROCODE_MAX_ITERATIONS` | Max iterations per task | - |
| `MICROCODE_MAX_TOKENS` | Max tokens per response | - |
| `MICROCODE_MAX_OUTPUT_CHARS` | Max output characters | - |
| `MICROCODE_API_BASE` | Custom API base URL | - |
| `MICROCODE_VERBOSE` | Enable verbose logging (`1`/`0`) | `0` |
| `MODAIC_ENV` / `MICROCODE_ENV` | Environment (`dev`/`prod`) | `prod` |

## Usage

### Starting the CLI

```bash
microcode
```

### CLI Options

```bash
microcode --help
```

| Flag | Description |
|------|-------------|
| `--model, -m` | Override primary model |
| `--sub-lm, -s` | Override sub-model |
| `--api-key, -k` | Provide API key directly |
| `--max-iterations` | Set max iterations |
| `--max-tokens` | Set max tokens |
| `--max-output-chars` | Set max output characters |
| `--api-base` | Custom API base URL |
| `--verbose, -v` | Enable verbose output |
| `--env` | Set environment (dev/prod) |
| `--history-limit` | Conversation history limit |
| `--no-banner` | Disable startup banner |

### Interactive Commands

Once in the CLI, use these commands:

| Command | Description |
|---------|-------------|
| `/help`, `/h`, `?` | Show help menu |
| `/q`, `exit` | Exit the CLI |
| `/clear`, `/cls` | Clear the terminal screen |
| `/c` | Clear conversation history |
| `/key [key]` | Set OpenRouter API key (or enter interactively) |
| `/key clear` | Remove stored API key |
| `/model` | Change primary model via TUI selector |
| `/model <id>` | Set primary model directly |
| `/mcp add <name> <command>` | Add an MCP server |

### Available Models

| # | Model | Provider |
|---|-------|----------|
| 1 | GPT-5.2 Codex | OpenAI |
| 2 | GPT-5.2 | OpenAI |
| 3 | Claude Opus 4.5 | Anthropic |
| 4 | Claude Opus 4 | Anthropic |
| 5 | Qwen 3 Coder | Qwen |
| 6 | Gemini 3 Flash Preview | Google |
| 7 | Kimi K2 0905 | Moonshot AI |
| 8 | Minimax M2.1 | Minimax |

## Project Structure

```
microcode/
├── main.py              # Entry point and interactive CLI loop
├── pyproject.toml       # Project configuration and dependencies
├── utils/
│   ├── __init__.py
│   ├── cache.py         # API key and settings persistence
│   ├── constants.py     # Colors, models, paths, and banner art
│   ├── display.py       # Terminal rendering and UI utilities
│   ├── mcp.py           # MCP server integration
│   ├── models.py        # Model selection and configuration
│   └── paste.py         # Clipboard and paste handling
└── tests/
    └── test_main_settings.py
```

### Key Components

- **`main.py`** - Orchestrates the interactive session, handles user input, manages conversation history, and invokes the AI agent via Modaic's `AutoProgram`
- **`utils/cache.py`** - Secure storage for API keys and user preferences using JSON files
- **`utils/constants.py`** - Centralized configuration including available models, ANSI color codes, and file paths
- **`utils/display.py`** - Terminal output formatting, markdown rendering, and the startup banner
- **`utils/models.py`** - Model selection TUI using Textual, model ID normalization, and agent reconfiguration
- **`utils/mcp.py`** - Model Context Protocol server registration and management
- **`utils/paste.py`** - Handles large text inputs via placeholder replacement

## Development

### Setting Up Development Environment

```bash
git clone https://github.com/modaic-ai/microcode.git
cd microcode
uv sync --dev
```

### Running Tests

```bash
uv run pytest tests/
```

### Code Style

The project follows standard Python conventions. Use type hints for all function signatures.

## Dependencies

Core dependencies:
- **[click](https://click.palletsprojects.com/)** / **[typer](https://typer.tiangolo.com/)** - CLI framework
- **[modaic](https://modaic.dev/)** - RLM program execution
- **[dspy](https://github.com/stanfordnlp/dspy)** - Language model programming
- **[mcp2py](https://github.com/modelcontextprotocol/python-sdk)** - MCP integration
- **[rich](https://rich.readthedocs.io/)** - Rich terminal output
- **[textual](https://textual.textualize.io/)** - Terminal UI framework
- **[prompt-toolkit](https://python-prompt-toolkit.readthedocs.io/)** - Input handling

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Links

- **Homepage**: [https://modaic.dev/](https://modaic.dev/)
- **Repository**: [https://github.com/modaic-ai/microcode](https://github.com/modaic-ai/microcode)
- **Issues**: [https://github.com/modaic-ai/microcode/issues](https://github.com/modaic-ai/microcode/issues)

---

<p align="center">
  <em>Built with  by <a href="https://modaic.dev">Modaic</a></em>
</p>