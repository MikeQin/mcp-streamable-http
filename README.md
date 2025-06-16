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

# Run
uv run server.py
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