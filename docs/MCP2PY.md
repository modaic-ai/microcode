Owner avatar
mcp2py
Public
MaximeRivest/mcp2py
Go to file
t
Name		
MaximeRivest
MaximeRivest
Merge pull request #2 from steipete/fix/accept-header-sse
ba5c477
 · 
2 months ago
.github/workflows
fix: add write permissions to GitHub Action for README rendering
2 months ago
README_files/libs
tst
2 months ago
docs
feat: v0.5.0 - HTTP/SSE transport and authentication support
2 months ago
examples
feat: v0.4.0 - Complete MCP feature support with zero-config IDE auto…
3 months ago
src/mcp2py
test: ensure sampling handler detects missing api keys
2 months ago
tests
feat: v0.5.0 - HTTP/SSE transport and authentication support
2 months ago
.gitignore
feat: v0.5.0 - HTTP/SSE transport and authentication support
2 months ago
.python-version
feat: initial project structure with README, implementation plan, and…
3 months ago
CHANGELOG.md
chore: bump version to 0.5.1
2 months ago
IMPLEMENTATION_PLAN.md
feat: implement Phase 1.4 - high-level load() API (v0.2.0)
3 months ago
IMPLEMENTATION_REVIEW.md
refactor: migrate to official MCP Python SDK
3 months ago
LICENSE
feat: initial project structure with README, implementation plan, and…
3 months ago
README.html
tst
2 months ago
README.md
Auto-render README.md from README.qmd
2 months ago
README.qmd
tweaks
2 months ago
README_EXAMPLES.qmd
feat: v0.5.0 - HTTP/SSE transport and authentication support
2 months ago
READMEbak.md
tst
2 months ago
RELEASE_v0.3.0.md
docs: add release notes for v0.3.0
3 months ago
notion_research_server.py
full loop
2 months ago
pyproject.toml
feat: v0.4.0 - Complete MCP feature support with zero-config IDE auto…
3 months ago
test_auth_interactive.py
feat: v0.5.0 - HTTP/SSE transport and authentication support
2 months ago
test_complete_server.py
feat: v0.4.0 - Complete MCP feature support with zero-config IDE auto…
3 months ago
uv.lock
feat: v0.4.0 - Complete MCP feature support with zero-config IDE auto…
3 months ago
Repository files navigation
README
MIT license
mcp2py: Turn any MCP server into a python module
MCP (Model Context Protocol) is an emerging standard for AI tools and resources. The standard is compatible with normal REST API servers, but adds extra metadata to describe tools, resources, and prompts in a machine-readable way. This provides us with a great opportunity to create Python modules that completely and automatically map to these MCP servers. The biggest advantage of this approach is that we can use any MCP server as if it were a native Python library, with zero configuration. This can be quite a big deal as creating Python software development kits that map to REST APIs is extremely common and was quite a manual process. Now, if the organization hosting the REST API also provides an MCP interface, we can automatically generate a Python SDK for it with zero effort! Don’t worry if this is not all clear to you. You can still leverage the power of mcp2py without knowing all the details of MCP. All you need to know is: if you want to programmatically interact with a website, it is likely that they have an API and as time goes on it is very likely that they have an MCP interface for that API. If they do, you don’t have to learn a whole set of web programming skills, you can just use mcp2py to load the MCP server and start calling functions right away as if it were a native Python library!

Another cool thing to note is that servers don’t have to be running remotely. You can (and have) a lot of servers running on your own personal computer right now. This is useful to have different programs, possibly in different programming languages, talking to each other. As apps that you install will more and more open up a small local server on your machine to let LLMs interact with them, you will also be able to leverage mcp2py to interact with these local servers. That could look like Slack opening a server that lets you query your messages. If so, you could then use mcp2py and have a Python module (a library in essence) that lets you query your Slack messages directly from Python. Super powerful!

Overview
Here is a very simple example of using mcp2py to interact with your local filesystem. That is not very useful as you could just use the built-in Python libraries to do that, but it serves as a very simple example to illustrate how mcp2py works. In this snippet of code we use load to both start the MCP server (which is a Node.js server in this case) and connect to it. Once connected we can call the list_directory tool as if it were a native Python function:

from mcp2py import load
fstools = load("npx -y @modelcontextprotocol/server-filesystem /home")
fstools.list_directory("/home")
[DIR] maxime
This is similar to using the os library in Python:

import os
os.listdir("/home")
['maxime']
The main difference is that instead of going directly from Python to the system, we send commands to a local Node (JavaScript) server and that server has some ‘security’ features. For example, we are not allowed to search outside of /home because that is what we have set as the root. Those features are very useful when you want to expose your file system to an LLM.

Quick Start
1. Install

You can install mcp2py via pip:

pip install mcp2py
Python has had the pesky problem of not having a standard way to manage dependencies for a long time. To avoid dependency conflicts, it is recommended to use virtual environments. My favorite way to do this is with uv (see here: https://docs.astral.sh/uv/getting-started/installation/). Then you can create a new environment and install mcp2py like this:

# Install uv (if you haven't already)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create a new project with a virtual environment
uv init my-mcp-project
cd my-mcp-project

# Install mcp2py
uv add mcp2py

# Activate the environment and start coding
uv run python
2. Use it

from mcp2py import load

# Load any MCP server with OAuth authentication
notion = load("https://mcp.notion.com/mcp", auth="oauth")

# Browser opens automatically for OAuth login
# Once authenticated, you can use the tools

notion.notion_get_self()
3. That’s it!

The server runs as a subprocess, tools are Python methods, everything just works.

What is MCP?
MCP servers expose tools, resources, and prompts via a protocol. mcp2py turns them into {python}:

🔧 Tools → {python} functions
📦 Resources → {python} constants/attributes
📝 Prompts → Template functions/strings
Philosophy
It Just Works™ - But You Can Customize Everything

mcp2py is designed for researchers, data analysts, and {python} beginners who want to try MCP servers without complexity. At the same time, it provides full control for developers building production applications.

Zero configuration by default: - OAuth login? Browser opens automatically - Need user input? Terminal prompts appear - Server needs an LLM? We handle it - Everything “just works” out of the box

No ceiling for advanced users: - Override any default behavior - Customize auth flows - Build production apps - Full control when you need it

Your {python} REPL/code becomes an MCP client. The server is a separate process (Node.js, {python}, whatever) that mcp2py communicates with via JSON-RPC. Your {python} code can: - Call tools (server functions) as if they’re local {python} functions - Access resources (server data) as {python} attributes - Handle server requests (sampling, elicitation) automatically or via custom callbacks - Work seamlessly with any AI SDK (Anthropic, OpenAI, DSPy, etc.)

Getting Started
For Beginners & Researchers: It Just Works
from mcp2py import load

# Load any MCP server - that's it!
server = load("https://api.example.com/mcp")

# If it needs login:
#   → Browser opens automatically
#   → You log in once
#   → Browser closes
#   → Done!

# If it needs your input:
#   → Nice terminal prompts appear
#   → You answer
#   → Code continues!

# If it needs AI help (sampling):
#   → Uses your ANTHROPIC_API_KEY or OPENAI_API_KEY
#   → Handles it automatically
#   → You don't even notice!

# Just use the tools!
result = server.analyze_data(dataset="sales_2024.csv")
print(result)
That’s it. No configuration. No setup. It just works.

Interface Design
Basic Usage
from mcp2py import load

# Load an MCP server - simple and clean
weather = load("npx -y @h1deya/mcp-server-weather")

# Or from a remote HTTP server (SSE/HTTP Stream transport)
api = load("https://api.example.com/mcp")

# With authentication
api = load("https://api.example.com/mcp", headers={"Authorization": "Bearer YOUR_TOKEN"})

# Or from a {python} script
travel = load("{python} my_mcp_server.py")

# Tools become functions
alerts = weather.get_alerts(state="CA")
forecast = weather.get_forecast(latitude=37.7749, longitude=-122.4194)
print(forecast)

# Resources become attributes
print(weather.API_DOCUMENTATION)  # Constant resource
print(weather.current_config)      # Dynamic resource

# Prompts become template functions
prompt = weather.create_weather_report(location="NYC", style="casual")
Use with AI Frameworks (DSPy, Claudette, etc.)
The .tools attribute gives you a list of callable {python} functions:

from mcp2py import load

server = load("npx -y @modelcontextprotocol/server-filesystem /tmp")

# Get tools as callable functions
tools = server.tools
# [<function read_file>, <function write_file>, ...]

# Each function has __name__ and __doc__
print(tools[0].__name__)  # "read_file"
print(tools[0].__doc__)   # "Read a file from the filesystem"

# And they're callable!
result = tools[0](path="/tmp/test.txt")
Working with AI Frameworks
The .tools attribute gives you callable functions ready for frameworks like DSPy and Claudette:

from mcp2py import load
import dspy

# Load MCP server
travel = load("{python} airline_server.py")

# Use with DSPy - pass callable functions directly
class CustomerService(dspy.Signature):
    user_request: str = dspy.InputField()
    result: str = dspy.OutputField()

dspy.configure(lm=dspy.LM("openai/gpt-4o-mini"))

# Pass tools directly to DSPy (it expects callables)
react = dspy.ReAct(CustomerService, tools=travel.tools)

result = react(user_request="Book a flight from SFO to JFK on 09/01/2025")
print(result)
# Also works with Claudette
from mcp2py import load
from claudette import Chat

weather = load("npx -y @h1deya/mcp-server-weather")

# Claudette expects callable functions
chat = Chat(model="claude-3-5-sonnet-20241022", tools=weather.tools)

response = chat("What's the weather in Tokyo?")
# Claudette automatically calls the tools as needed
print(response)
Note: For SDKs that have native MCP support (Anthropic, OpenAI, Google Gemini), use their built-in MCP integration directly. The .tools attribute is for frameworks like DSPy and Claudette that expect {python} callables.

Type Safety & IDE Support
Auto-generated stubs for perfect autocomplete:

from mcp2py import load

# Stubs auto-generated to ~/.cache/mcp2py/stubs/
server = load("npx my-server")

# IDE now has full autocomplete and type hints!
server.search_files(
    pattern="*.py",  # type: str - IDE knows this!
    max_results=10   # type: int, optional - IDE suggests this!
)  # Returns: dict[str, Any] - IDE shows return type!
Manual stub generation:

# Generate stub to specific location for your project
server = load("npx weather-server")
server.generate_stubs("./stubs/weather.pyi")

# Or let it auto-cache (default behavior)
# Stubs saved to: ~/.cache/mcp2py/stubs/<command_hash>.pyi
How it works: - load() returns a dynamically typed class with all methods pre-defined - Your IDE sees proper type hints immediately - no configuration needed! - Type hints include parameter names, types, defaults, and return types - Works in VS Code, PyCharm, Jupyter notebooks, and any {python} IDE - Also generates .pyi stub files to ~/.cache/mcp2py/stubs/ for reference

Zero configuration required - autocomplete just works! ✨

MCP Client Features
When your {python} code acts as an MCP client, servers may request these capabilities:

Sampling
When a server needs LLM completions, mcp2py handles it automatically.

Default: Works Out of the Box

from mcp2py import load

# Just works! Uses your default LLM
server = load("npx travel-server")

# If server needs LLM help, mcp2py:
# 1. Checks for ANTHROPIC_API_KEY or OPENAI_API_KEY in environment
# 2. Calls the LLM automatically
# 3. Returns result to server
# 4. Your code continues!

result = server.book_flight(destination="Tokyo")
Configure your preferred LLM:

# Set via environment (recommended)
import os
os.environ["ANTHROPIC_API_KEY"] = "sk-..."

# Or configure globally using LiteLLM model strings
from mcp2py import configure

configure(
    model="claude-3-5-sonnet-20241022"  # or "gpt-4o", "gemini/gemini-pro", etc.
)

# LiteLLM automatically detects the right API based on model name
# Uses standard env vars: ANTHROPIC_API_KEY, OPENAI_API_KEY, etc.

# Now all servers use this LLM for sampling
server = load("npx travel-server")
Advanced: Custom Sampling Handler

from mcp2py import load

def my_sampling_handler(messages, model_prefs, system_prompt, max_tokens):
    """Full control over LLM calls."""
    import anthropic
    client = anthropic.Anthropic()
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        messages=messages,
        max_tokens=max_tokens
    )
    return response.content[0].text

server = load(
    "npx travel-server",
    on_sampling=my_sampling_handler  # Override default
)
Disable sampling (for security/cost control):

server = load(
    "npx travel-server",
    allow_sampling=False  # Raises error if server requests LLM
)
Elicitation
When a server needs user input, mcp2py prompts automatically.

Default: Terminal Prompts

from mcp2py import load

# Just works! Terminal prompts appear automatically
server = load("npx travel-server")

# Server asks: "Confirm booking for $500?"
# Terminal shows:
#
#   Server asks: Confirm booking for $500?
#   confirm_booking (boolean): y/n
#
# You type: y
# Code continues!

result = server.book_flight(destination="Paris")
What you see:

Calling book_flight...

┌─────────────────────────────────────────┐
│ 🔔 Server needs your input              │
├─────────────────────────────────────────┤
│ Confirm booking for $500?               │
│                                         │
│ confirm_booking (boolean): y/n          │
│ seat_preference (window/aisle/middle):  │
│ meal_preference (optional):             │
└─────────────────────────────────────────┘

> y
> window
> vegetarian

Booking confirmed!
Advanced: Custom Elicitation Handler

from mcp2py import load

def my_input_handler(message, schema):
    """Custom UI for user input."""
    # Build a GUI, web form, voice input, etc.
    from tkinter import simpledialog
    return simpledialog.askstring("Server Request", message)

server = load(
    "npx travel-server",
    on_elicitation=my_input_handler
)
Disable elicitation (for automated scripts):

server = load(
    "npx travel-server",
    allow_elicitation=False  # Raises error if server asks for input
)

# Or provide pre-filled answers
server = load(
    "npx travel-server",
    elicitation_defaults={
        "confirm_booking": True,
        "seat_preference": "window"
    }
)
Roots
Servers can ask which directories to focus on. Optional, simple:

# Single directory
server = load("npx filesystem-server", roots="/home/user/projects")

# Multiple directories
server = load(
    "npx filesystem-server",
    roots=["/home/user/projects", "/tmp/workspace"]
)

# Update roots dynamically
server.set_roots(["/home/user/new-project"])
Design Rules
1. Tools → Functions
MCP tools map to {python} functions with full support for:

Arguments: Both required and optional parameters
Type hints: Generated from JSON Schema inputSchema
Docstrings: Built from tool description
Return types: Typed as dict[str, Any] (MCP tools return JSON)
Naming convention: Snake_case (MCP getWeather → {python} get_weather)

# MCP Tool Definition:
# {
#   "name": "searchFiles",
#   "description": "Search for files matching a pattern",
#   "inputSchema": {
#     "type": "object",
#     "properties": {
#       "pattern": {"type": "string", "description": "Glob pattern"},
#       "maxResults": {"type": "integer", "default": 100}
#     },
#     "required": ["pattern"]
#   }
# }

# Generated {python}:
def search_files(pattern: str, max_results: int = 100) -> dict[str, Any]:
    """Search for files matching a pattern.

    Args:
        pattern: Glob pattern
        max_results: Maximum results to return (default: 100)
    """
    ...
2. Resources → Constants or Properties
Resources map differently based on their nature:

Static resources (like documentation, schemas): Module-level constants (UPPER_CASE)
Dynamic resources (may change): Properties with getters (lowercase)
# Static resource (cached)
API_DOCS: str = server._get_resource("api://docs")

# Dynamic resource (fetched on access)
@property
def current_status() -> dict[str, Any]:
    """Current server status."""
    return server._get_resource("status://current")
Naming convention: - Static: UPPER_SNAKE_CASE - Dynamic: lower_snake_case properties

3. Prompts → Template Functions
Prompts become functions that return formatted strings:

# MCP Prompt:
# {
#   "name": "reviewCode",
#   "description": "Generate a code review prompt",
#   "arguments": [
#     {"name": "code", "description": "Code to review", "required": true},
#     {"name": "focus", "description": "Review focus area", "required": false}
#   ]
# }

# Generated {python}:
def review_code(code: str, focus: str | None = None) -> str:
    """Generate a code review prompt.

    Args:
        code: Code to review
        focus: Review focus area (optional)

    Returns:
        Formatted prompt string ready for LLM
    """
    ...
4. Error Handling
{python}ic exceptions for common failures:

from mcp2py.exceptions import (
    MCPConnectionError,    # Can't connect to server
    MCPToolError,          # Tool execution failed
    MCPResourceError,      # Resource not found
    MCPValidationError,    # Invalid arguments
)

try:
    result = server.expensive_operation(data=large_data)
except MCPValidationError as e:
    print(f"Invalid input: {e}")
except MCPToolError as e:
    print(f"Tool failed: {e}")
5. Async Support
Use aload() for async MCP servers:

from mcp2py import aload

# Async version - all tools become async
server = await aload("npx async-server")

result = await server.fetch_data(url="https://example.com")
status = await server.get_current_status()
6. Context Managers
Automatic cleanup when using with:

from mcp2py import load

# Sync version
with load("npx my-server") as server:
    result = server.do_work()
# Server process automatically terminated

# Async version
async with aload("npx my-server") as server:
    result = await server.do_work()
Configuration
Server Registry (Optional)
Register commonly-used servers once, then load by name:

from mcp2py import register, load

# Register servers (run once, e.g., in your setup script)
register(
    weather="npx -y @h1deya/mcp-server-weather",
    brave="npx -y brave-search-mcp-server",
    filesystem="npx -y @modelcontextprotocol/server-filesystem /tmp",
    myserver="{python} my_mcp_server.py"
)

# Then load by name anywhere
weather = load("weather")
brave = load("brave")

# Or use commands directly (no registration needed)
custom = load("npx my-custom-server")
Registry is saved to ~/.config/mcp2py/servers.json automatically.

Remote Servers & Authentication
MCP servers can be hosted remotely over HTTP (using SSE or HTTP Stream transport):

from mcp2py import load, register

# Connect to remote MCP server
api = load("https://api.example.com/mcp")

# With Bearer token authentication
secure_api = load(
    "https://api.example.com/mcp",
    headers={"Authorization": "Bearer sk-1234567890"}
)

# With custom headers (API keys, etc.)
custom_api = load(
    "https://api.example.com/mcp",
    headers={
        "X-API-Key": "your-api-key",
        "X-Client-ID": "your-client-id"
    }
)

# Register remote servers too
register(
    production_api="https://api.prod.example.com/mcp",
    staging_api="https://api.staging.example.com/mcp"
)

# Load with auth at runtime
prod = load("production_api", headers={"Authorization": f"Bearer {get_token()}"})
Use cases for remote MCP servers: - Company-hosted internal tools - Paid API services via MCP - Shared team resources (databases, analytics, etc.) - Cloud-based AI tool marketplaces

OAuth Authentication (Google, GitHub, etc.)
Default: Zero Configuration (For beginners, researchers, data analysts)

mcp2py handles OAuth automatically - just load and go:

from mcp2py import load

# That's it! Browser opens, you log in, then continue coding
server = load("https://api.example.com/mcp")

# First tool call triggers OAuth if needed:
# 1. Browser window pops up
# 2. You log in (Google/GitHub/etc.)
# 3. Window closes automatically
# 4. Your code continues!

result = server.my_tool()  # Works immediately after login
What happens under the hood: - mcp2py detects OAuth requirement (401 response) - Discovers OAuth endpoints automatically - Opens browser for login (PKCE-secured) - Stores tokens in ~/.config/mcp2py/tokens.json - Refreshes tokens automatically when they expire

You never think about tokens.

Advanced: Custom OAuth (For production apps)

Override defaults when building applications:

from mcp2py import load

# Option 1: Custom token provider
def get_google_token():
    """Your custom OAuth logic."""
    from google.oauth2.credentials import Credentials
    # Your implementation here
    return creds.token

server = load(
    "https://api.example.com/mcp",
    auth=get_google_token  # Called when token needed
)

# Option 2: Service account (no browser)
from google.oauth2 import service_account

credentials = service_account.Credentials.from_service_account_file(
    'service-account.json'
)

server = load(
    "https://api.example.com/mcp",
    auth=credentials
)

# Option 3: Manual token management
server = load(
    "https://api.example.com/mcp",
    headers={"Authorization": f"Bearer {your_token}"}
)

# Option 4: Disable auto-browser (for servers/CI)
server = load(
    "https://api.example.com/mcp",
    auto_auth=False  # Raises error instead of opening browser
)
Environment variable support (for production):

# Set token via environment
export MCP_TOKEN="your-token-here"
# Automatically used if available
server = load("https://api.example.com/mcp")
Security Considerations
Client-Side (mcp2py handles automatically): - ✅ Secure token storage - OAuth tokens cached in ~/.fastmcp/oauth-mcp-client-cache/ - ✅ PKCE support for OAuth flows (Proof Key for Code Exchange) - ✅ Automatic token refresh before expiration - ✅ Environment variable support (MCP_TOKEN)

Server-Side (your responsibility when connecting): - Use HTTPS URLs for production servers (not HTTP) - Ensure the MCP servers you connect to implement proper authentication - Rotate tokens/credentials regularly - Never commit tokens to version control

Best Practices:

# Good: Use environment variables
import os
server = load("https://api.example.com/mcp", auth=os.getenv("MCP_TOKEN"))

# Good: HTTPS for production
server = load("https://api.example.com/mcp", auth="oauth")

# Avoid: Hardcoded tokens in code
# server = load("https://api.example.com/mcp", auth="sk-secret-123")  # Don't do this!
Advanced Features
Stub Generation
Stubs are automatically generated when you use load(). They’re cached to ~/.cache/mcp2py/stubs/ for reuse.

Programmatic API:

from mcp2py import load

# Stubs auto-generated on load
server = load("npx weather-server")

# Generate to specific path
stub_path = server.generate_stubs("./stubs/weather.pyi")
print(f"Stub saved to: {stub_path}")

# Check cache location
from mcp2py.stubs import get_stub_cache_path
cache_path = get_stub_cache_path("npx weather-server")
print(f"Cached at: {cache_path}")
Complete Client Example
"""Full example of {python} as MCP client with all features."""
from mcp2py import load
import anthropic

# Setup callbacks for server requests
def handle_sampling(messages, model_prefs, system_prompt, max_tokens):
    """Server wants LLM completion."""
    client = anthropic.Anthropic()
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        messages=messages,
        system=system_prompt,
        max_tokens=max_tokens
    )
    return response.content[0].text

def handle_elicitation(message, schema):
    """Server needs user input."""
    print(f"\n🔔 Server asks: {message}")

    if schema.get("type") == "string":
        return input("→ ")

    if schema.get("type") == "boolean":
        return input("→ (y/n): ").lower() in ["y", "yes", "true"]

    if schema.get("type") == "object":
        result = {}
        for prop, details in schema.get("properties", {}).items():
            result[prop] = input(f"  {prop} ({details.get('description', '')}): ")
        return result

    import json
    return json.loads(input("→ (JSON): "))

# Connect to server with all features
server = load(
    "npx travel-booking-server",
    on_sampling=handle_sampling,
    on_elicitation=handle_elicitation,
    roots="/home/user/travel-docs"
)

# Use the server - callbacks invoked automatically when needed
booking = server.book_flight(destination="Barcelona", dates="June 15-22")
print(booking)
Inspection
from mcp2py import load

server = load("npx my-server")

# List all available tools
print(server.tools)  # List of tool schemas for AI SDKs

# Get tool info
print(server.get_weather.__doc__)
print(server.get_weather.__signature__)

# List resources
print(server.resources)

# List prompts
print(server.prompts)
Middleware & Hooks
from mcp2py import load

def log_tool_calls(tool_name: str, args: dict, result: dict):
    print(f"Called {tool_name} with {args} → {result}")

server = load(
    "npx my-server",
    on_tool_call=log_tool_calls,
    timeout=30.0
)
Implementation Priorities
Phase 1: Core Functionality
load() function with stdio transport
Tool → function mapping with type hints
Simple resource access
Prompt → template function mapping
.tools attribute for AI SDK integration
Phase 2: Developer Experience
Stub generation for IDE support
Server registry (~/.config/mcp2py/servers.json)
Context manager protocol
Better error messages and exceptions
Phase 3: Advanced Features
aload() for async support
SSE transport for HTTP servers
Middleware/hooks system
Sampling and elicitation callbacks
Design Principles
Delightful Defaults: Authentication, sampling, elicitation all work automatically
No Ceiling: Every default can be overridden for production use cases
Beginner-Friendly: Data analysts and researchers can start immediately
Production-Ready: Full control for developers building apps
Progressive Disclosure: Simple by default, powerful when you need it
Type Safety: Generate types wherever possible for IDE support
{python}ic: Convert MCP conventions to {python} conventions automatically
Clear Errors: Helpful messages when things go wrong, with suggestions
Complete Examples
Example 1: Synchronous - Weather Analysis with DSPy
#!/usr/bin/env {python}3
"""Analyze weather alerts using DSPy and MCP."""

from mcp2py import load
import dspy

# Configure DSPy
dspy.configure(lm=dspy.LM("openai/gpt-4o-mini"))

# Load MCP weather server
weather = load("npx -y @h1deya/mcp-server-weather")

# Define DSPy signature
class WeatherAnalyzer(dspy.Signature):
    """Analyze weather alerts and provide recommendations."""
    state: str = dspy.InputField()
    analysis: str = dspy.OutputField(desc="Weather analysis and travel recommendations")

# Create agent with MCP tools
agent = dspy.ReAct(WeatherAnalyzer, tools=weather.tools)

# Analyze weather for multiple states
states = ["CA", "NY", "TX", "FL"]

for state in states:
    # Agent automatically calls weather.get_alerts() and weather.get_forecast()
    result = agent(state=state)
    print(f"\n{state}:")
    print(result.analysis)
Example 2: Asynchronous - Travel Booking System
#!/usr/bin/env {python}3
"""Async travel booking system with MCP and Anthropic."""

import asyncio
from mcp2py import aload
import anthropic

async def book_trip(user_request: str):
    """Book a trip using MCP travel server and Claude."""

    # Load async MCP server
    travel = await aload("{python} travel_server.py")

    # Setup Anthropic client
    client = anthropic.Anthropic()

    # Initial request to Claude with MCP tools
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=2048,
        tools=travel.tools,  # MCP tools passed to Claude
        messages=[{"role": "user", "content": user_request}]
    )

    # Handle tool calls in a loop
    messages = [{"role": "user", "content": user_request}]

    while response.stop_reason == "tool_use":
        # Extract tool calls from response
        tool_results = []

        for content_block in response.content:
            if content_block.type == "tool_use":
                # Call MCP tool asynchronously
                tool_name = content_block.name
                tool_args = content_block.input

                print(f"Calling {tool_name}({tool_args})...")

                # Execute tool via MCP
                tool_func = getattr(travel, tool_name)
                result = await tool_func(**tool_args)

                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": content_block.id,
                    "content": str(result)
                })

        # Add assistant response and tool results to conversation
        messages.append({"role": "assistant", "content": response.content})
        messages.append({"role": "user", "content": tool_results})

        # Continue conversation
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2048,
            tools=travel.tools,
            messages=messages
        )

    # Extract final response
    return response.content[0].text

async def main():
    result = await book_trip(
        "Book a round-trip flight from SFO to JFK on Sept 1-8, 2025. "
        "My name is Adam Smith. I prefer window seats and morning flights."
    )
    print("\n" + "="*60)
    print("BOOKING RESULT:")
    print("="*60)
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
Example 3: Simple Synchronous - Direct Tool Calls
#!/usr/bin/env {python}3
"""Simple weather check without AI - just direct MCP tool calls."""

from mcp2py import load

# Load weather server
weather = load("npx -y @h1deya/mcp-server-weather")

# Direct tool calls (no LLM needed)
print("Weather Alerts for California:")
alerts = weather.get_alerts(state="CA")
print(alerts)

print("\nSan Francisco Forecast:")
forecast = weather.get_forecast(latitude=37.7749, longitude=-122.4194)
print(forecast)

# MCP tools are just {python} functions!
Testing with Real Servers
Here are real MCP servers you can test right now:

from mcp2py import load

# Weather server (Node.js via npx)
weather = load("npx -y @h1deya/mcp-server-weather")

# Brave search (requires API key)
brave = load("npx -y brave-search-mcp-server")

# Filesystem operations
fs = load("npx -y @modelcontextprotocol/server-filesystem /tmp")

# Memory/knowledge graph
memory = load("npx -y @modelcontextprotocol/server-memory")

# Remote HTTP server
api = load("https://api.example.com/mcp")

# Remote server with authentication
secure_api = load(
    "https://api.example.com/mcp",
    headers={"Authorization": "Bearer YOUR_TOKEN"}
)

# Inspect what's available
print(weather.tools)      # List of tool schemas
print(weather.get_alerts) # Callable function
result = weather.get_alerts(state="CA")
Clean, simple, {python}ic. That’s the goal. 🎯

Architecture Overview
┌─────────────────────────────────────────────────────────────────┐
│ Your {python} Code (MCP Client)                                   │
│                                                                  │
│  from mcp2py import load                                        │
│                                                                  │
│  server = load("npx weather-server")                        │
│  result = server.get_forecast(lat=37.7, lon=-122.4)            │
│                                                                  │
│  ┌──────────────────────────────────────────────────────┐      │
│  │ Optional: Use with AI SDKs                           │      │
│  │                                                       │      │
│  │  import dspy                                          │      │
│  │  agent = dspy.ReAct(                                 │      │
│  │    Signature,                                         │      │
│  │    tools=server.tools  # ← mcp2py                    │      │
│  │  )                                                    │      │
│  └──────────────────────────────────────────────────────┘      │
└─────────────────────────────────────────────────────────────────┘
                            ↕ JSON-RPC over stdio
┌─────────────────────────────────────────────────────────────────┐
│ MCP Server Process (separate process)                           │
│                                                                  │
│  Node.js / {python} / Rust / whatever                             │
│  Exposes: tools, resources, prompts                             │
│  May request: sampling, elicitation, roots                      │
└─────────────────────────────────────────────────────────────────┘
Key Points: 1. mcp2py is the client - it speaks JSON-RPC to the server 2. Server is a separate process - started via command parameter 3. Low-level and generic - works with any AI SDK or standalone 4. Bidirectional - client calls server tools, server can request client capabilities

Advanced Tutorial: Composing MCP Servers with DSPy
This tutorial demonstrates the full power of mcp2py by showing how to: 1. Use Notion MCP in a DSPy agent 2. Wrap that agent as its own MCP server 3. Use that server in another DSPy program

This showcases true composability - building complex AI systems by chaining MCP servers together.

Step 1: DSPy Agent with Notion MCP
First, let’s create a DSPy agent that can search and organize information in Notion:

import dspy
from mcp2py import load

# Configure DSPy with your LLM
dspy.configure(lm=dspy.LM("openai/gpt-4.1"))

# Load Notion MCP server
notion = load("https://mcp.notion.com/mcp", auth="oauth")

# Define a DSPy signature for a research assistant

class NotionResearcher(dspy.Signature):
    """Research assistant that searches Notion workspace."""
    query: str = dspy.InputField(desc="Research query")
    summary: str = dspy.OutputField(desc="Summary of findings")

# Create DSPy agent with Notion tools
researcher = dspy.ReAct(NotionResearcher, tools=notion.tools)

# Test the agent
result = researcher(query="What are our Q1 2025 goals?")
print(result.summary)
[11/03/25 07:20:44] INFO     OAuth authorization URL:  oauth.py:340
https://mcp.notion.com/authorizresponse_typ...                                                                              
    INFO     🎧 OAuth callback server started on http://localhost:40621                   oauth.py:358

AI response > No information was found regarding our Q1 2025 goals due to repeated execution errors when attempting to search or create documentation in Notion. All attempts to gather relevant data or create a new page were unsuccessful.
Step 2: Wrap the Agent as an MCP Server
Now let’s turn this Notion-powered agent into its own MCP server using FastMCP:

# notion_research_server.py
from fastmcp import FastMCP
from mcp2py import load
import dspy

# Initialize FastMCP
mcp = FastMCP("Notion Research Server")

# Load Notion and configure DSPy
notion = load("https://mcp.notion.com/mcp", auth="oauth")
dspy.configure(lm=dspy.LM("openai/gpt-4.1"))

class NotionResearcher(dspy.Signature):
    """Research assistant that searches Notion workspace."""
    query: str = dspy.InputField(desc="Research query")
    summary: str = dspy.OutputField(desc="Summary of findings")

researcher = dspy.ReAct(NotionResearcher, tools=notion.tools)

@mcp.tool()
def research_notion(query: str) -> str:
    """Research a topic by searching the Notion workspace.

    Args:
        query: The research question or topic to investigate

    Returns:
        A comprehensive summary of findings from Notion
    """
    result = researcher(query=query)
    return result.summary

# Run the server
if __name__ == "__main__":
    mcp.run()
Save this as notion_research_server.py and you now have a custom MCP server!

Step 3: Use the Custom Server in Another DSPy Program
Finally, let’s use our custom Notion Research Server in a higher-level DSPy agent:

import dspy
from mcp2py import load

# Configure DSPy
dspy.configure(lm=dspy.LM("openai/gpt-4.1"))

# Load our custom Notion Research Server
research_server = load("uv run notion_research_server.py")

# Create a high-level report writer
class ReportWriter(dspy.Signature):
    """Executive assistant that creates comprehensive reports."""
    topic: str = dspy.InputField(desc="Report topic")
    sections: str = dspy.InputField(desc="Comma-separated section topics")
    report: str = dspy.OutputField(desc="Comprehensive markdown report")

# Create agent with our research server tools
report_writer = dspy.ReAct(ReportWriter, tools=research_server.tools)

# Generate a comprehensive report
result = report_writer(
    topic="Company Strategy Review",
    sections="Q1 Goals, Recent Achievements, Upcoming Initiatives, Team Updates"
)

print("="*60)
print(result.report)
print("="*60)
============================================================
# Company Strategy Review

## Q1 Goals
*Unable to retrieve specific information due to access issues.*

## Recent Achievements
*Unable to retrieve specific information due to access issues.*

## Upcoming Initiatives
*Unable to retrieve specific information due to access issues.*

## Team Updates
*Unable to retrieve specific information due to access issues.*

---

*Note: This report could not be completed with current data access. Please provide the necessary information or resolve access issues to enable a comprehensive review.*
============================================================
What Just Happened?
This example demonstrates three levels of composition:

Level 1: Notion MCP provides raw tools (search, fetch, create)
Level 2: DSPy agent + Notion MCP = Research Assistant (wrapped as MCP server)
Level 3: Another DSPy agent uses the Research Assistant to create comprehensive reports
Key Benefits
Modularity: Each layer is independent and reusable
Abstraction: Higher levels don’t need to know about Notion’s API
Composability: Mix and match different MCP servers and agents
Type Safety: Full type hints and IDE support throughout the chain
Testability: Each layer can be tested independently
Real-World Applications
This pattern enables powerful workflows:

Multi-Source Research: Combine Notion, GitHub, Slack, and other MCP servers
Specialized Agents: Create domain-specific assistants (HR, Engineering, Sales)
Agent Chains: Build complex pipelines where agents call other agents
API Abstraction: Hide complexity behind simple, high-level tools
Next Steps
Try creating your own composed systems:

Add more MCP servers (GitHub, Slack, Google Drive)
Create specialized agents for different domains
Build agent hierarchies with supervisors and workers
Deploy as microservices for production use
The possibilities are endless when you can turn any MCP server into Python, and any Python code into an MCP server!