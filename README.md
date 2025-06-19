# Streamable HTTP MCP Server

[MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk?tab=readme-ov-file#adding-mcp-to-your-python-project)

[Model Context Protocol (MCP) Server + Google OAuth](https://github.com/cloudflare/ai/tree/main/demos/remote-mcp-google-oauth)

### What is MCP?

The Model Context Protocol (MCP) lets you build servers that expose data and functionality to LLM applications in a secure, standardized way. Think of it like a web API, but specifically designed for LLM interactions. MCP servers can:

* Expose data through Resources (think of these sort of like GET endpoints; they are used to load information into the LLM's context)
* Provide functionality through Tools (sort of like POST endpoints; they are used to execute code or otherwise produce a side effect)
* Define interaction patterns through Prompts (reusable templates for LLM interactions)
* And more!

Learn more at [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk?tab=readme-ov-file#adding-mcp-to-your-python-project)

### Setup
```sh
# Create a new directory for our project
uv init stream_http
cd stream_http

# Create virtual environment and activate it
uv venv
source .venv/Scripts/activate

# Install dependencies
uv add "mcp[cli]" httpx requests

# OAuth
uv pip install authlib starlette uvicorn python-dotenv
uv pip install itsdangerous

# Run
uv run server.py
python server.py
mcp run server.py
```

### Authentication

[Model Context Protocol (MCP) Server + Google OAuth](https://github.com/cloudflare/ai/tree/main/demos/remote-mcp-google-oauth)

Authentication can be used by servers that want to expose tools accessing protected resources.

`mcp.server.auth` implements an OAuth 2.0 server interface, which servers can use by providing an implementation of the `OAuthAuthorizationServerProvider` protocol.

```python
from mcp import FastMCP
from mcp.server.auth.provider import OAuthAuthorizationServerProvider
from mcp.server.auth.settings import (
    AuthSettings,
    ClientRegistrationOptions,
    RevocationOptions,
)

class MyOAuthServerProvider(OAuthAuthorizationServerProvider):
    # See an example on how to implement at `examples/servers/simple-auth`
    # ...
    pass

mcp = FastMCP(
    "My App",
    auth_server_provider=MyOAuthServerProvider(),
    auth=AuthSettings(
        issuer_url="https://myapp.com",
        revocation_options=RevocationOptions(
            enabled=True,
        ),
        client_registration_options=ClientRegistrationOptions(
            enabled=True,
            valid_scopes=["myscope", "myotherscope"],
            default_scopes=["myscope"],
        ),
        required_scopes=["myscope"],
    ),
)
```

### Development

The fastest way to test and debug your server is with the MCP Inspector:
```sh
mcp dev server.py

# Add dependencies
mcp dev server.py --with pandas --with numpy

# Mount local code
mcp dev server.py --with-editable .
```

### Testing with MCP Inspector

Alternatively, you can test it with the MCP Inspector:

```sh
mcp dev server.py
```

### Claude Desktop Integration

Once your server is ready, install it in Claude Desktop:
```sh
mcp install server.py

# Custom name
mcp install server.py --name "My Analytics Server"

# Environment variables
mcp install server.py -v API_KEY=abc123 -v DB_URL=postgres://...
mcp install server.py -f .env
```

You can install this server in Claude Desktop and interact with it right away by running:
```sh
mcp install server.py
```

claude_desktop_config.json
```json
{
  "mcpServers": {
    "add_server": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "http://localhost:8080/mcp/"
      ]
    }
  }
}
```

### Direct Execution

For advanced scenarios like custom deployments:
```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("My App")

if __name__ == "__main__":
    mcp.run()
```

Run it with:
```sh
python server.py
# or
mcp run server.py
```
Note that `mcp run` or `mcp dev` only supports server using FastMCP and not the low-level server variant.

### Streamable HTTP Transport

```python
from mcp.server.fastmcp import FastMCP

# Stateful server (maintains session state)
mcp = FastMCP("StatefulServer")

# Stateless server (no session persistence)
mcp = FastMCP("StatelessServer", stateless_http=True)

# Stateless server (no session persistence, no sse stream with supported client)
mcp = FastMCP("StatelessServer", stateless_http=True, json_response=True)

# Run server with streamable_http transport
mcp.run(transport="streamable-http")
```

You can mount multiple FastMCP servers in a FastAPI application:

```python
# ----------------------------------------
# echo.py
from mcp.server.fastmcp import FastMCP

mcp = FastMCP(name="EchoServer", stateless_http=True)


@mcp.tool(description="A simple echo tool")
def echo(message: str) -> str:
    return f"Echo: {message}"

# ----------------------------------------
# math.py
from mcp.server.fastmcp import FastMCP

mcp = FastMCP(name="MathServer", stateless_http=True)

@mcp.tool(description="A simple add tool")
def add_two(n: int) -> int:
    return n + 2

# ----------------------------------------
# main.py
import contextlib
from fastapi import FastAPI
from mcp.echo import echo
from mcp.math import math

# Create a combined lifespan to manage both session managers
@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    async with contextlib.AsyncExitStack() as stack:
        await stack.enter_async_context(echo.mcp.session_manager.run())
        await stack.enter_async_context(math.mcp.session_manager.run())
        yield

app = FastAPI(lifespan=lifespan)
app.mount("/echo", echo.mcp.streamable_http_app())
app.mount("/math", math.mcp.streamable_http_app())
```

### Run Scripts and Client

```sh
sh stateful.sh
sh stateless.sh
uv run client.py
```

### MCP Inspector

```sh
npx @modelcontextprotocol/inspector
# optional
npx @modelcontextprotocol/inspector uvx --directory "C:\\dev\\mcp-projects\\weather-server" run server.py
# For example
npx @modelcontextprotocol/inspector uvx mcp-server-git --repository ~/code/mcp/servers.git
```

### Simple Auth

https://github.com/modelcontextprotocol/python-sdk/tree/main/examples/servers/simple-auth
