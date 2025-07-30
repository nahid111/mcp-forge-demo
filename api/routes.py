import json

from typing import Annotated
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from api.dependencies import get_weather_agent
from api.langgraph_weather_agent import WeatherAgent
from api.logger import logger


class MessagePayload(BaseModel):
    """Message Payload schema."""

    message: str
    thread_id: str = str(uuid4())


router = APIRouter()


@router.post('/invoke')
async def send_message(
    payload: MessagePayload,
    agent: Annotated[WeatherAgent, Depends(get_weather_agent)],
):
    """Invoke function."""
    try:
        response = await agent.invoke(**payload.model_dump())
        return response
    except Exception as e:
        logger.error(f'Error sending message: {e}')
        raise HTTPException(
            status_code=500, detail='Failed to send message'
        ) from e


@router.post('/stream')
async def send_message_stream(
    payload: MessagePayload,
    agent: Annotated[WeatherAgent, Depends(get_weather_agent)],
):
    """Streaming function."""
    try:

        async def event_stream():
            response = agent.stream(payload.message, payload.thread_id)
            async for chunk in response:
                yield (json.dumps(chunk, indent=2) + '\n\n')

        return StreamingResponse(
            event_stream(),
            media_type='application/json',
        )

    except Exception as e:
        logger.error(f'Error sending message: {e}')
        raise HTTPException(
            status_code=500, detail='Failed to send message'
        ) from e


@router.get('/health')
def health_check():
    """Health check endpoint."""
    return {'status': 'ok'}
