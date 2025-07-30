from contextlib import asynccontextmanager

from fastapi import FastAPI, Request

from api.langgraph_weather_agent import WeatherAgent


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Saving agent in app state."""
    app.state.weather_agent = await WeatherAgent.initialize()
    yield


def get_weather_agent(request: Request) -> WeatherAgent:
    """Get weather_agent from the request state."""
    agent: WeatherAgent | None = getattr(
        request.app.state, 'weather_agent', None
    )
    if agent is None:
        raise AttributeError('Weather agent not initialized in app state.')
    return agent
