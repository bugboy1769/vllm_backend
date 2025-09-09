from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):

    # Model Settings
    model_name: str = "facebook/opt-125m"
    max_model_len: int = 4096
    gpu_memory_utilization: float = 0.9
    tensor_parallel_size: int = 1
    dtype: str = "float16"

    # Server Settings
    host: str = "0.0.0.0"
    port: int = 8080

    # API Settings
    default_max_tokens: int = 100
    default_temperature: float = 0.7 #what is this?

    class Config:
        env_file = ".env"

settings = Settings()


