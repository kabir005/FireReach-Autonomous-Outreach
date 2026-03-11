"""Pydantic models for FireReach."""
from typing import Literal
from pydantic import BaseModel, EmailStr, Field


class Signal(BaseModel):
    """A single buyer intent signal."""
    type: str = Field(..., description="Signal type: funding, hiring, leadership, tech_stack, news")
    summary: str = Field(..., description="Brief summary of the signal")
    source_url: str = Field(..., description="URL source of the signal")
    detected_at: str = Field(..., description="ISO timestamp of detection")


class SignalHarvesterInput(BaseModel):
    """Input for signal harvester tool."""
    company_name: str
    signal_types: list[str] = ["funding", "hiring", "leadership", "tech_stack", "news"]


class SignalHarvesterOutput(BaseModel):
    """Output from signal harvester tool."""
    company_name: str
    signals: list[Signal]
    raw_search_results: str


class ResearchAnalystInput(BaseModel):
    """Input for research analyst tool."""
    company_name: str
    icp_description: str
    signals: list[Signal]


class ResearchAnalystOutput(BaseModel):
    """Output from research analyst tool."""
    account_brief: str = Field(..., description="Exactly 2 paragraphs")
    pain_points: list[str] = Field(..., description="2-4 identified pain points")
    strategic_alignment: str = Field(..., description="1-2 sentences on why ICP fits")


class OutreachSenderInput(BaseModel):
    """Input for outreach sender tool."""
    recipient_email: EmailStr
    company_name: str
    account_brief: str
    pain_points: list[str]
    signals: list[Signal]
    icp_description: str


class OutreachSenderOutput(BaseModel):
    """Output from outreach sender tool."""
    email_subject: str
    email_body: str
    send_status: Literal["sent", "failed"]
    message_id: str


class FireReachRequest(BaseModel):
    """Request to launch FireReach agent."""
    icp_description: str = Field(..., description="Ideal Customer Profile description")
    company_name: str = Field(..., description="Target company name")
    recipient_email: EmailStr = Field(..., description="Email address to send outreach")


class AgentState(BaseModel):
    """State tracked throughout agent execution."""
    icp: str
    company_name: str
    recipient_email: str
    signals: list[Signal] = []
    account_brief: str = ""
    pain_points: list[str] = []
    strategic_alignment: str = ""
    email_subject: str = ""
    email_body: str = ""
    send_status: str = "pending"
    message_id: str = ""
    agent_log: list[str] = []
    current_step: str = "initializing"
    error: str = ""


class FireReachResponse(BaseModel):
    """Response from FireReach agent."""
    status: Literal["success", "failed"]
    current_step: str
    signals: list[Signal]
    account_brief: str
    pain_points: list[str]
    strategic_alignment: str
    email_subject: str
    email_body: str
    send_status: str
    message_id: str
    agent_log: list[str]
    error: str = ""
