from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.llm_engine import llm_engine
from app.api import generate, chat, admin
import logging

logging.basicConfig(level=logging.INFO)
logger=logging.getLogger(__name__) #?

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting up ...")
    llm_engine.load_model()
    yield
    # Shutdown
    logger.info("Shutting down ...")

def create_app() -> FastAPI:
    app = FastAPI(
        title="Custom vLLM Server",
        description="A production-ready vLLM API server",
        version="1.0.0",
        lifespan=lifespan
    )
     
    # Include routers
    app.include_router(generate.router)
    app.include_router(chat.router)
    app.include_router(admin.router)

    return app

