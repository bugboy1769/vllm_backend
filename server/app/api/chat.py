from fastapi import APIRouter, HTTPException
from vllm import LLM, SamplingParams
from app.data_models.schemas import ChatRequest
from app.core.llm_engine import llm_engine
from app.utils.prompt_utils import format_chat_prompt

router = APIRouter(prefix="/v1", tags=["chat"])

@router.post("/chat/completions")
async def chat_completions(request: ChatRequest):
    if not llm_engine.is_loaded():
        raise HTTPException(status_code=503, detail="Model not loaded")
    try:
        prompt = format_chat_prompt(request.messages)

        sampling_params = SamplingParams(
            temperature=request.temperature,
            top_p=request.top_p,
            max_tokens=request.max_tokens,
            stop=["Human", "\n\n"]
        )
        outputs = llm_engine.generate([prompt], sampling_params)
        response_text = outputs[0].outputs[0].text.strip()

        return {
            "choices": [{
                "message": {
                    "role":"assistant",
                    "content":response_text,
                },
                "finish_reason": outputs[0].outputs[0].finish_reason
            }],
            "usage": {
                "prompt_tokens": len(outputs[0].prompt_token_ids),
                "completion_tokens": len(outputs[0].prompt_token_ids),
                "total_tokens": len(outputs[0].prompt_token_ids) + len(outputs[0].outputs[0].token_ids)
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))