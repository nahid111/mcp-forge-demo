from fastapi import FastAPI

from api.dependencies import lifespan
from api.routes import router


app = FastAPI(lifespan=lifespan)
app.include_router(router)


if __name__ == '__main__':
    import uvicorn

    uvicorn.run('api.main:app', host='0.0.0.0', port=5000, reload=True)
