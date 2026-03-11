"""FastAPI main application for FireReach."""
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from config import config
from models import FireReachRequest, FireReachResponse
from agent_simple import run_firereach_agent


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Validate configuration on startup."""
    errors = config.validate()
    if errors:
        print("⚠️  Configuration warnings:")
        for error in errors:
            print(f"  - {error}")
    else:
        print("✅ Configuration validated successfully")
    
    yield


app = FastAPI(
    title="FireReach API",
    description="Autonomous Outreach Engine by Rabbitt AI",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "service": "FireReach",
        "status": "operational",
        "tagline": "Autonomous Outreach. Zero Templates."
    }


@app.get("/health")
async def health():
    """Detailed health check."""
    errors = config.validate()
    return {
        "status": "healthy" if not errors else "degraded",
        "configuration_errors": errors
    }


@app.post("/api/firereach", response_model=FireReachResponse)
async def launch_firereach(request: FireReachRequest):
    """
    Launch the FireReach autonomous outreach agent.
    
    The agent will:
    1. Harvest live buyer intent signals
    2. Generate an account brief
    3. Draft and send a personalized email
    """
    try:
        result = await run_firereach_agent(request)
        
        return FireReachResponse(
            status="success" if not result.error else "failed",
            current_step=result.current_step,
            signals=result.signals,
            account_brief=result.account_brief,
            pain_points=result.pain_points,
            strategic_alignment=result.strategic_alignment,
            email_subject=result.email_subject,
            email_body=result.email_body,
            send_status=result.send_status,
            message_id=result.message_id,
            agent_log=result.agent_log,
            error=result.error
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# For Vercel serverless
handler = app


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
