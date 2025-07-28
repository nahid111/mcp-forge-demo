import uvicorn

from fastmcp import FastMCP

from core.settings import settings
from server.tools import get_weather
from fastmcp.server.auth import BearerAuthProvider
from fastmcp.server.auth.providers.bearer import RSAKeyPair

# Generate a new key pair
key_pair = RSAKeyPair.generate()

# Configure the auth provider with the public key
auth = BearerAuthProvider(
    public_key=key_pair.public_key,
    issuer='https://dev.example.com',
    audience='my-dev-server',
)

# Generate a token for testing
token = key_pair.create_token(
    subject='dev-user',
    issuer='https://dev.example.com',
    audience='my-dev-server',
    scopes=['read', 'write'],
)


mcp = FastMCP('Weather MCP Server', auth=auth)


mcp.tool(get_weather)

# Get the app instance
app = mcp.http_app(
    path='/mcp', transport='streamable-http', stateless_http=True
)
# Run with uvicorn on your desired port
if __name__ == '__main__':
    print(f'\n>>>>> WEATHER_SERVER_TOKEN: \n{token}\n')
    uvicorn.run(
        app,
        host=settings.MCP_SERVER_HOST,
        port=settings.MCP_SERVER_PORT,
        log_level='debug',
    )
