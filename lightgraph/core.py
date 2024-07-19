from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from typing import Any, Dict, List
from pydantic import BaseModel
import asyncio
import json
from langchain_core.messages import AIMessage, HumanMessage

class LightGraph:
    def __init__(self, runnable: Any, allowed_hosts: List[str] = None):
        self.runnable = runnable
        self.allowed_hosts = allowed_hosts or ["localhost", "127.0.0.1"]

    def create_app(self) -> FastAPI:
        app = FastAPI()

        # Add TrustedHostMiddleware
        app.add_middleware(
            TrustedHostMiddleware,
            allowed_hosts=self.allowed_hosts,
        )

        class TextInput(BaseModel):
            text: str
            thread_id: str

        @app.post("/stream_with_steps")
        async def stream_with_steps(input: TextInput):
            return StreamingResponse(self._stream_with_steps_generator(input.text, input.thread_id), media_type="application/json")

        return app

    def _serialize_step(self, step):
        if isinstance(step, (HumanMessage, AIMessage)):
            return {
                "type": step.type,
                "content": step.content,
                "additional_kwargs": step.additional_kwargs,
            }
        elif isinstance(step, dict):
            return {k: self._serialize_step(v) for k, v in step.items()}
        elif isinstance(step, list):
            return [self._serialize_step(v) for v in step]
        else:
            return step

    async def _stream_with_steps_generator(self, text: str, thread_id: str):
        params = {"messages": [HumanMessage(content=f"{text}")]}
        config = {
            "configurable": {
                "thread_id": thread_id,
            },
            "recursion_limit": 150,
        }
        intermediate_responses = []
        try:
            for step in self.runnable.stream(params, config):
                serialized_step = self._serialize_step(step)
                intermediate_responses.append(serialized_step)
                yield json.dumps({"event": "intermediate", "data": serialized_step}) + "\n"
            
            final_response = intermediate_responses[-1] if intermediate_responses else {}
            yield json.dumps({"event": "final", "data": final_response}) + "\n"
        except Exception as e:
            yield json.dumps({"event": "error", "data": str(e)}) + "\n"

def create_lightgraph(runnable: Any, allowed_hosts: List[str] = None) -> LightGraph:
    return LightGraph(runnable, allowed_hosts)