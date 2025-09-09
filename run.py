import uvicorn
from server.app.main import create_app
from server.app.core.config import settings

if __name__=="main":
    app=create_app()
    uvicorn.run(
        app,
        host=settings.host,
        port=settings.port,
        log_level="info"
    )