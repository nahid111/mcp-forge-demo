from collections.abc import AsyncIterable
from typing import Any

from langchain_core.load import dumpd
from langchain_core.messages import HumanMessage
from langchain_core.messages.base import BaseMessage
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt import create_react_agent

from api.logger import logger
from core.model_selector import get_langchain_model
from core.settings import settings


class WeatherAgent:
    """WeatherAgent - a specialized assistant for Weather."""

    SYSTEM_INSTRUCTION = (
        'You are a helpful assistant tasked with fetching weather data.'
    )

    def __init__(self, model, tools, agent):
        self.model = model
        self.tools = tools
        self.agent: CompiledStateGraph = agent

    @classmethod
    async def initialize(cls):
        """Initialize the WeatherAgent with model and tools."""
        logger.info('\n>>>>> Initializing WeatherAgent...\n')
        model = get_langchain_model()
        tools = await cls._get_tools_static()
        agent = create_react_agent(
            model,
            tools=tools,
            checkpointer=MemorySaver(),
            prompt=cls.SYSTEM_INSTRUCTION,
        )
        return cls(model, tools, agent)

    @staticmethod
    async def _get_tools_static():
        server_config = {}
        if settings.USE_MCP_FORGE:
            server_config = {
                'gateway': {
                    'url': 'http://localhost:4444/mcp',
                    'transport': 'streamable_http',
                    'headers': {
                        'Authorization': f'Bearer {settings.MCP_FORGE_BEARER_TOKEN}'
                    },
                }
            }
        else:
            server_config = {
                'weather': {
                    'url': settings.MCP_SERVER_URL,
                    'transport': 'streamable_http',
                    'headers': {
                        'Authorization': f'Bearer {settings.WEATHER_SERVER_TOKEN}'
                    },
                }
            }
        client = MultiServerMCPClient(server_config)
        return await client.get_tools()

    async def invoke(self, message, thread_id) -> dict[str, Any]:
        inputs = {'messages': [HumanMessage(content=message)]}
        config = {'configurable': {'thread_id': thread_id}}

        response = await self.agent.ainvoke(inputs, config)
        return dumpd(response)

    async def stream(self, query, context_id) -> AsyncIterable[dict[str, Any]]:
        inputs = {'messages': [HumanMessage(content=query)]}
        config = {'configurable': {'thread_id': context_id}}

        async for item in self.agent.astream(
            inputs, config, stream_mode='values'
        ):
            message: BaseMessage = item['messages'][-1]
            message.pretty_print()
            yield dumpd(message)
