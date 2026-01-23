import json
import re
import shlex
from typing import Any

from modaic import PrecompiledProgram

from .constants import GREEN, RED, RESET, YELLOW


def register_mcp_server(agent: PrecompiledProgram, name: str, server: Any) -> list[str]:
    """
    Register MCP server tools with the agent.

    Args:
        agent: The PrecompiledProgram agent to register tools with
        name: The name of the MCP server
        server: The MCP server object with tools

    Returns:
        List of registered tool names
    """
    assert isinstance(name, str), "name must be a str"
    assert isinstance(agent, PrecompiledProgram), "agent must be PrecompiledProgram"
    assert hasattr(server, "tools"), "server must expose tools"

    tool_names: list[str] = []
    for tool in server.tools:
        tool_name = f"{name}_{tool.__name__}"
        agent.set_tool(tool_name, tool)
        tool_names.append(tool_name)
    return tool_names


def handle_add_mcp_command(
    user_input: str, agent: PrecompiledProgram, mcp_servers: dict[str, dict[str, Any]]
) -> bool:
    """
    Handle the /mcp add command.

    Args:
        user_input: The user input string
        agent: The PrecompiledProgram agent
        mcp_servers: Dictionary of registered MCP servers

    Returns:
        True if command was handled, False otherwise
    """
    assert isinstance(user_input, str), "user_input must be a str"
    assert isinstance(agent, PrecompiledProgram), "agent must be PrecompiledProgram"
    assert isinstance(mcp_servers, dict), "mcp_servers must be a dict"

    parts = shlex.split(user_input)
    args = parts[1:]
    if not args:
        print(
            f"{YELLOW}⏺ Usage: /mcp <name> <server> [--auth <auth>|--oauth] [--headers '<json>'] [--auto-auth|--no-auto-auth]{RESET}"
        )
        return True

    name = None
    auth = None
    headers = None
    auto_auth = None
    positional = []
    i = 0
    while i < len(args):
        if args[i] in ("--name", "-n") and i + 1 < len(args):
            name = args[i + 1]
            i += 2
        elif args[i].startswith("--auth="):
            auth = args[i].split("=", 1)[1]
            i += 1
        elif args[i] == "--auth" and i + 1 < len(args):
            auth = args[i + 1]
            i += 2
        elif args[i] == "--oauth":
            auth = "oauth"
            i += 1
        elif args[i] == "--auto-auth":
            auto_auth = True
            i += 1
        elif args[i] == "--no-auto-auth":
            auto_auth = False
            i += 1
        elif args[i].startswith("--headers="):
            headers = json.loads(args[i].split("=", 1)[1])
            i += 1
        elif args[i] == "--headers" and i + 1 < len(args):
            headers = json.loads(args[i + 1])
            i += 2
        else:
            positional.append(args[i])
            i += 1

    server_cmd = None
    if positional:
        if name is None and len(positional) >= 2:
            name = positional[0]
            server_cmd = " ".join(positional[1:])
        else:
            server_cmd = " ".join(positional)

    if not server_cmd:
        print(
            f"{YELLOW}⏺ Usage: /mcp <name> <server> [--auth <auth>|--oauth] [--headers '<json>'] [--auto-auth|--no-auto-auth]{RESET}"
        )
        return True

    if not name:
        name = re.sub(r"[^a-zA-Z0-9_]+", "_", server_cmd).strip("_")
        if not name:
            name = f"mcp_{len(mcp_servers) + 1}"

    if name in mcp_servers:
        for tool_name in mcp_servers[name]["tools"]:
            agent.remove_tool(tool_name)

    try:
        from mcp2py import load

        kwargs = {}
        if auth is not None:
            kwargs["auth"] = auth
        if headers:
            kwargs["headers"] = headers
        if auto_auth is not None:
            kwargs["auto_auth"] = auto_auth

        server = load(server_cmd, **kwargs)
        tool_names = register_mcp_server(agent, name, server)
        mcp_servers[name] = {"server": server, "tools": tool_names}

        print(f"{GREEN}⏺ Added MCP server '{name}' with {len(tool_names)} tools{RESET}")
        print(f"{GREEN}⏺ Tools: {list(agent.tools.keys())}{RESET}")
    except Exception as err:
        print(f"{RED}⏺ Failed to add MCP server: {err}{RESET}")

    return True
