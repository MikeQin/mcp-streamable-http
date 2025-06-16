from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Demo-Server", stateless_http=True)

@mcp.tool(description="Sum two numbers")
def add(a: int, b: int) -> int:
    result = a + b
    print(f"a: {a} + b: {b} = sum: {result}")
    return result

if __name__ == "__main__":
    mcp.run(transport="streamable-http")