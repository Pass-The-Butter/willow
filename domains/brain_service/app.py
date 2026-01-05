
from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import asyncio
import json
import os
from .router_gateway import classify_intent
from .context_assembler import assemble_context

app = FastAPI(title="Willow Brain Service", version="1.0.0")

class ChatRequest(BaseModel):
    messages: list
    model: str = "gpt-4-turbo-preview"
    stream: bool = True

async def stream_response_generator(request: ChatRequest):
    """
    The 'News Anchor' Generator:
    1. Yields immediate tokens from LLM (using fast context).
    2. Injects 'proactive' updates if slow context arrives.
    """
    # Analyze Intent
    intent_data = classify_intent(request.messages)
    depth = intent_data['depth']
    
    # Start Async Context Fetch
    context_task = asyncio.create_task(assemble_context(request.messages, depth))
    
    # 1. Start with Fast Context Response (Simulation)
    yield "data: " + json.dumps({"choices": [{"delta": {"content": f"[Intent: {intent_data['intent']} (Depth {depth})]\n"}}]}) + "\n\n"
    yield "data: " + json.dumps({"choices": [{"delta": {"content": "Based on my immediate knowledge... "}}]}) + "\n\n"
    
    # Simulate LLM Stream
    response_text = "I am processing your request. "
    for word in response_text.split():
        yield "data: " + json.dumps({"choices": [{"delta": {"content": word + " "}}]}) + "\n\n"
        await asyncio.sleep(0.1)

    # 2. Wait for Slow Context (News Anchor Injection)
    if not context_task.done():
        yield "data: " + json.dumps({"choices": [{"delta": {"content": " \n\n[Checking archives...] "}}]}) + "\n\n"
        await context_task 
    
    ctx = context_task.result()
    
    # Inject Context if found
    if ctx.get('zep'):
         yield "data: " + json.dumps({"choices": [{"delta": {"content": f"\n\n**Update from Memory**: {ctx['zep']}"}}]}) + "\n\n"
    
    if ctx.get('graphiti'):
         yield "data: " + json.dumps({"choices": [{"delta": {"content": f"\n\n**Update from Graph**: {ctx['graphiti']}"}}]}) + "\n\n"
         
    yield "data: [DONE]\n\n"

@app.post("/v1/chat/completions")
async def chat_completions(request: ChatRequest, background_tasks: BackgroundTasks):
    """
    Main entry point for Chat.
    """
    if request.stream:
        return StreamingResponse(stream_response_generator(request), media_type="text/event-stream")
    else:
        return {"choices": [{"message": {"content": "Non-streaming not fully implemented yet."}}]}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8004)
