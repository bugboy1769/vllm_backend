from fastapi import APIRouter, HTTPException
from app.core.llm_engine import llm_engine
from app.core.config import settings

router = APIRouter(tags=["admin"])

@router.get("/health")
async def health_check():
    return {"status": "healthy", "model_laoded":llm_engine.is_loaded()}

@router.get("/model_info")
async def model_info():
    if not llm_engine.is_loaded():
        raise HTTPException(status_code=503, detail="Model not loaded")
    return {
        "model_name": settings.model_name,
        "max_model_len": settings.max_model_len,
        "dtype": settings.dtype,
        "gpu_memory_utilization": settings.gpu_memory_utilization,
    }
