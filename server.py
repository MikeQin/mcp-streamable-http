from mcp.server.fastmcp import FastMCP

mcp = FastMCP(
    name="Demo-Server",
    stateless_http=True,
    host="127.0.0.1",      # Set host here
    port=8080,             # Set port here
    log_level="INFO",      # Optional
)

def authenticate():
    pass

@mcp.tool(description="Sum two numbers")
def add(a: int, b: int) -> int:
    result = a + b
    print(f"a: {a} + b: {b} = sum: {result}")
    return result

if __name__ == "__main__":
    mcp.run(transport="streamable-http")