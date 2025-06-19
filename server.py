import httpx
from mcp.server.fastmcp import FastMCP
# from my_auth_provider import MyOAuthServerProvider
# from mcp.server.auth.settings import (
#     AuthSettings,
#     ClientRegistrationOptions,
#     RevocationOptions,
# )

mcp = FastMCP(
    name="Demo-Server",
    stateless_http=True,
    host="127.0.0.1",      # Set host here
    port=8080,             # Set port here
    log_level="INFO",      # Optional
    # auth_server_provider=MyOAuthServerProvider(),
    # auth=AuthSettings(
    #     issuer_url="http://localhost:8000",
    #     revocation_options=RevocationOptions(
    #         enabled=True,
    #     ),
    #     client_registration_options=ClientRegistrationOptions(
    #         enabled=True,
    #         valid_scopes=["myscope", "myotherscope"],
    #         default_scopes=["myscope"],
    #     ),
    #     required_scopes=["myscope"],
)

# Add an addition tool
@mcp.tool(title="Add Two Numbers", description="Add two numbers")
def add(a: int, b: int) -> int:
    """Add two numbers"""
    result = a + b
    print(f"a: {a} + b: {b} = sum: {result}")
    return result

@mcp.tool(title="BMI Calculator", description="Calculate BMI given weight in kg and height in meters")
def calculate_bmi(weight_kg: float, height_m: float) -> float:
    """Calculate BMI given weight in kg and height in meters"""
    return weight_kg / (height_m**2)

@mcp.tool(title="Weather Fetcher", description="Fetch current weather for a city")
async def fetch_weather(city: str) -> str:
    """Fetch current weather for a city"""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://api.weather.com/{city}")
        return response.text
    
# Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"

# Optional
if __name__ == "__main__":
    mcp.run(transport="streamable-http")