from vllm import LLM, SamplingParams
from .config import settings
import logging
from typing import List

logger = logging.getLogger()

class LLMEngine: #Borrows settings from config
    def __init__(self):
        self.llm = None
    
    def load_model(self):
        """Load the vLLM model"""
        logger.info(f"Loading Model: {settings.model_name}")
        self.llm = LLM(
            model=settings.model_name,
            dtype=settings.dtype,
            gpu_memory_utilization=settings.gpu_memory_utilization,
            max_model_len=settings.max_model_len,
            tensor_parallel_size=settings.tensor_parallel_size,
        )
        logger.info(f"Model Loaded Successfully")
    
    def generate(self, prompts: List[str], sampling_params: SamplingParams):
        """Generate text using loaded model"""
        if self.llm is None:
            raise RuntimeError("Model not loaded")
        return self.llm.generate(prompts, sampling_params) #calling llm
    
    def is_loaded(self) -> bool:
        return self.llm is not None

llm_engine = LLMEngine()
