import os
import uuid
from typing import Any, Dict, Optional

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from agent import Agent


load_dotenv()


app = FastAPI(
    title="Memory Agent API",
    description="Multi-tenant conversational agent with semantic memory",
    version="1.0.0",
)


_session_cache: Dict[str, Agent] = {}


def _session_key(user_id: str, run_id: str) -> str:
    """Build a cache key."""
    return f"{user_id}:{run_id}"


def _get_mem0_api_key() -> str:
    """Load the Mem0 API key."""
    api_key = os.getenv("MEM0_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="MEM0_API_KEY is not configured",
        )
    return api_key


def _get_or_create_agent(user_id: str, run_id: str) -> Agent:
    """Get existing Agent for a session or create a new one."""
    cache_key = _session_key(user_id, run_id)
    if cache_key in _session_cache:
        return _session_cache[cache_key]

    agent = Agent(
        user_id=user_id,
        run_id=run_id,
        api_key=_get_mem0_api_key(),
    )
    _session_cache[cache_key] = agent
    return agent


class InvocationRequest(BaseModel):
    """Request body for agent invocation."""
    user_id: str = Field(..., min_length=1, description="User identifier")
    run_id: Optional[str] = Field(
        default=None,
        min_length=1,
        description="Session identifier",
    )
    query: str = Field(..., min_length=1, description="User message")
    metadata: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Optional metadata for the request",
    )


class InvocationResponse(BaseModel):
    """Response body for agent invocation."""
    user_id: str
    run_id: str
    response: str
    metadata: Optional[Dict[str, Any]] = None


class PingResponse(BaseModel):
    """Response body for health checks."""
    status: str
    message: str


@app.get("/ping", response_model=PingResponse)
def ping() -> PingResponse:
    """Health check endpoint."""
    return PingResponse(
        status="ok",
        message="Memory Agent API is running",
    )


@app.post("/invocation", response_model=InvocationResponse)
def invocation(request: InvocationRequest) -> InvocationResponse:
    """Process a user message through the memory agent."""
    try:
        run_id = request.run_id or f"{request.user_id}-{uuid.uuid4().hex[:8]}"
        agent = _get_or_create_agent(request.user_id, run_id)
        response_text = agent.chat(request.query)

        return InvocationResponse(
            user_id=request.user_id,
            run_id=run_id,
            response=response_text,
            metadata=request.metadata,
        )
    except HTTPException:
        raise
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc