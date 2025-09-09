from fastapi import APIRouter, HTTPException
from vllm import SamplingParams
from app.core.llm_engine import llm_engine
from app.data_models.schemas import GenerateRequest, GenerateResponse, BatchRequest
from app.utils.prompt_utils import do_job_prompt

router = APIRouter(prefix="/api", tags=["generation"])

@router.post("/generate", response_model=GenerateResponse)
async def generate_text(request: GenerateRequest):
    if not llm_engine.is_loaded():
        raise HTTPException(status_code=503, detail="Model not loaded")
    try:
        sampling_params = SamplingParams(
            temperature=request.temperature,
            top_p=request.top_p,
            top_k=request.top_k,
            max_tokens=request.max_tokens,
            repetition_penalty=request.repetition_penalty,
            stop=request.stop
        )
        outputs=llm_engine.generate([request.prompt], sampling_params)
        output = outputs[0]

        return GenerateResponse(
            text=output.outputs[0].text,
            finish_reason=output.outputs[0].finish_reason,
            prompt_tokens=len(output.prompt_token_ids),
            completion_tokens=len(output.outputs[0].token_ids)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/batch_generate")
async def batch_generate(request: BatchRequest):
    if not llm_engine.is_loaded():
        raise HTTPException(status_code=503, detail="Model not loaded")
    try:
        sampling_params=SamplingParams(
            temperature=request.temperature,
            max_tokens=request.max_tokens
        )

        outputs = llm_engine.generate(request.prompts, sampling_params)
        results = []
        for output in outputs:
            results.append({
                "prompt": output.prompt,
                "text":output.outputs[0].text,
                "tokens_used": len(output.outputs[0].token_ids)
            })
        return {"results":results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("do_job")
async def do_job(prompt: str, context:str, max_tokens:int=200):
    if not llm_engine.is_loaded():
        raise HTTPException(status_code=503, detail="Model not found")
    job_prompt=do_job_prompt(prompt, context)
    sampling_params=SamplingParams(
        temperature=0.2,
        max_tokens=max_tokens,
        stop=["```", "\n\n\n"]
    )
    outputs = llm_engine.generate([job_prompt], sampling_params)
    result=outputs[0].outputs[0].text_strip()

    return {
        "result": result,
        "context": context,
        "prompt": prompt
    }
    
    
    