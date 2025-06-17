# Streamable HTTP MCP Server

### Setup
```sh
# Create a new directory for our project
uv init stream_http
cd stream_http

# Create virtual environment and activate it
uv venv
source .venv/Scripts/activate

# Install dependencies
uv add "mcp[cli]" httpx

# OAuth
uv pip install authlib starlette uvicorn python-dotenv
uv pip install itsdangerous

# Run
uv run server.py
```

### Claude Config

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
