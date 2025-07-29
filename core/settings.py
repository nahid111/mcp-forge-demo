import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings


load_dotenv()


class Settings(BaseSettings):
    """App Settings."""

    MODEL_NAME: str = os.environ.get('MODEL_NAME', 'gpt-4o-mini')
    OPENAI_API_KEY: str = os.environ.get('OPENAI_API_KEY', '')
    OPENWEATHERMAP_API_KEY: str = os.environ.get('OPENWEATHERMAP_API_KEY', '')

    USE_BEDROCK: bool = os.environ.get('USE_BEDROCK', 'false').lower() == 'true'
    BEDROCK_MODEL_NAME: str = os.environ.get(
        'BEDROCK_MODEL_NAME',
        'anthropic.claude-3-5-sonnet-20240620-v1:0',
    )
    AWS_ACCESS_KEY_ID: str = os.environ.get('AWS_ACCESS_KEY_ID', '')
    AWS_SECRET_ACCESS_KEY: str = os.environ.get('AWS_SECRET_ACCESS_KEY', '')
    AWS_SESSION_TOKEN: str = os.environ.get('AWS_SECRET_ACCESS_KEY', '')

    MCP_SERVER_HOST: str = os.environ.get('MCP_SERVER_HOST', 'localhost')
    MCP_SERVER_PORT: int = int(os.environ.get('MCP_SERVER_URL', '5001'))
    USE_MCP_FORGE: bool = (
        os.environ.get('USE_MCP_FORGE', 'false').lower() == 'true'
    )
    MCP_FORGE_BEARER_TOKEN: str = os.environ.get('MCP_FORGE_BEARER_TOKEN', '')

    WEATHER_SERVER_TOKEN: str = os.environ.get('WEATHER_SERVER_TOKEN', '')

    @property
    def MCP_SERVER_URL(self) -> str:
        """Construct the MCP server URL."""
        return f'http://{self.MCP_SERVER_HOST}:{self.MCP_SERVER_PORT}/mcp'


settings = Settings()
