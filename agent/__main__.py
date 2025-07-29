import asyncio

from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent

from agent.utils import print_messages
from core.model_selector import get_langchain_model
from core.settings import settings


SERVER_CONFIG = {}

if settings.USE_MCP_FORGE:
    SERVER_CONFIG = {
        'gateway': {
            'url': 'http://localhost:4444/mcp',
            'transport': 'streamable_http',
            'headers': {
                'Authorization': f'Bearer {settings.MCP_FORGE_BEARER_TOKEN}'
            },
        }
    }
else:
    SERVER_CONFIG = {
        'weather': {
            'url': settings.MCP_SERVER_URL,
            'transport': 'streamable_http',
            'headers': {
                'Authorization': f'Bearer {settings.WEATHER_SERVER_TOKEN}'
            },
        }
    }


async def main():
    client = MultiServerMCPClient(SERVER_CONFIG)
    tools = await client.get_tools()
    agent = create_react_agent(get_langchain_model(), tools)
    response = await agent.ainvoke(
        {'messages': 'what is the weather in dhaka?'}
    )
    print_messages(response)


if __name__ == '__main__':
    asyncio.run(main())
