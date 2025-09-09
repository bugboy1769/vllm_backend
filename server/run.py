import uvicorn
from fastapi import HTTPException
from app.main import create_app
from app.core.config import settings

if __name__=="__main__":
    try:
        print("Creating app...")
        app=create_app()
        print("App created successfully!")
        print(f"Starting server on {settings.host}:{settings.port}")
        uvicorn.run(
            app,
            host=settings.host,
            port=settings.port,
            log_level="info"
        )
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=999, detail=str(e))
