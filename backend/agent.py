"""FireReach Agent - ReAct pattern with LangGraph orchestration."""
from typing import TypedDict
from langgraph.graph import StateGraph, END
from operator import add
from typing_extensions import Annotated
from models import (
    AgentState, Signal, SignalHarvesterInput, ResearchAnalystInput, 
    OutreachSenderInput, FireReachRequest
)
from tools.signal_harvester import tool_signal_harvester
from tools.research_analyst import tool_research_analyst
from tools.outreach_sender import tool_outreach_automated_sender


class GraphState(TypedDict):
    """State for LangGraph."""
    icp: str
    company_name: str
    recipient_email: str
    signals: list[Signal]
    account_brief: str
    pain_points: list[str]
    strategic_alignment: str
    email_subject: str
    email_body: str
    send_status: str
    message_id: str
    agent_log: Annotated[list[str], add]
    current_step: str
    error: str


async def signal_harvester_node(state: GraphState) -> dict:
    """Node 1: Harvest buyer intent signals."""
    updates = {
        "current_step": "harvesting_signals",
        "agent_log": [
            f"[REASONING] Starting signal harvester for company: {state['company_name']}. "
            f"Will search for funding, hiring, leadership, tech_stack, and news signals."
        ]
    }
    
    try:
        input_data = SignalHarvesterInput(
            company_name=state["company_name"],
            signal_types=["funding", "hiring", "leadership", "tech_stack", "news"]
        )
        
        result = await tool_signal_harvester(input_data)
        
        updates["signals"] = result.signals
        updates["agent_log"].append(
            f"[ACTION] Signal harvester completed. Found {len(result.signals)} signals across "
            f"{len(set(s.type for s in result.signals))} categories."
        )
        
        if result.signals:
            updates["agent_log"].append(
                f"[OBSERVATION] Top signals: {', '.join([s.type for s in result.signals[:3]])}"
            )
        else:
            updates["agent_log"].append(
                "[OBSERVATION] No signals found. Will proceed with limited data."
            )
        
    except Exception as e:
        updates["error"] = f"Signal harvesting failed: {str(e)}"
        updates["agent_log"].append(f"[ERROR] {updates['error']}")
    
    return updates


async def research_analyst_node(state: GraphState) -> dict:
    """Node 2: Generate account brief."""
    updates = {
        "current_step": "generating_brief",
        "agent_log": [
            f"[REASONING] Analyzing {len(state['signals'])} signals against ICP to generate account brief. "
            f"Will identify pain points and strategic alignment."
        ]
    }
    
    try:
        input_data = ResearchAnalystInput(
            company_name=state["company_name"],
            icp_description=state["icp"],
            signals=state["signals"]
        )
        
        result = await tool_research_analyst(input_data)
        
        updates["account_brief"] = result.account_brief
        updates["pain_points"] = result.pain_points
        updates["strategic_alignment"] = result.strategic_alignment
        
        updates["agent_log"].append(
            f"[ACTION] Research analyst completed. Generated 2-paragraph brief with "
            f"{len(result.pain_points)} pain points identified."
        )
        updates["agent_log"].append(
            f"[OBSERVATION] Strategic alignment: {result.strategic_alignment[:100]}..."
        )
        
    except Exception as e:
        updates["error"] = f"Research analysis failed: {str(e)}"
        updates["agent_log"].append(f"[ERROR] {updates['error']}")
    
    return updates


async def outreach_sender_node(state: GraphState) -> dict:
    """Node 3: Draft and send personalized email."""
    updates = {
        "current_step": "sending_email",
        "agent_log": [
            "[REASONING] Drafting hyper-personalized email that references specific signals. "
            "Will ensure at least 2 signals are mentioned, then send via email API."
        ]
    }
    
    try:
        input_data = OutreachSenderInput(
            recipient_email=state["recipient_email"],
            company_name=state["company_name"],
            account_brief=state["account_brief"],
            pain_points=state["pain_points"],
            signals=state["signals"],
            icp_description=state["icp"]
        )
        
        result = await tool_outreach_automated_sender(input_data)
        
        updates["email_subject"] = result.email_subject
        updates["email_body"] = result.email_body
        updates["send_status"] = result.send_status
        updates["message_id"] = result.message_id
        
        updates["agent_log"].append(
            f"[ACTION] Email drafted with subject: '{result.email_subject}'"
        )
        updates["agent_log"].append(
            f"[ACTION] Email send status: {result.send_status} (Message ID: {result.message_id})"
        )
        
        if result.send_status == "sent":
            updates["agent_log"].append(
                "[OBSERVATION] Outreach successfully delivered. FireReach sequence complete."
            )
        else:
            updates["error"] = f"Email sending failed: {result.message_id}"
            updates["agent_log"].append(f"[ERROR] {updates['error']}")
        
    except Exception as e:
        updates["error"] = f"Outreach sending failed: {str(e)}"
        updates["agent_log"].append(f"[ERROR] {updates['error']}")
    
    return updates


def should_continue(state: GraphState) -> str:
    """Determine if agent should continue or stop."""
    if state["error"]:
        return "end"
    
    if state["current_step"] == "harvesting_signals":
        return "research"
    elif state["current_step"] == "generating_brief":
        return "send"
    elif state["current_step"] == "sending_email":
        return "end"
    
    return "end"


def create_firereach_graph() -> StateGraph:
    """Create the FireReach agent graph."""
    workflow = StateGraph(GraphState)
    
    # Add nodes
    workflow.add_node("harvest_signals", signal_harvester_node)
    workflow.add_node("generate_brief", research_analyst_node)
    workflow.add_node("send_outreach", outreach_sender_node)
    
    # Set entry point
    workflow.set_entry_point("harvest_signals")
    
    # Add conditional edges
    workflow.add_conditional_edges(
        "harvest_signals",
        should_continue,
        {
            "research": "generate_brief",
            "end": END
        }
    )
    
    workflow.add_conditional_edges(
        "generate_brief",
        should_continue,
        {
            "send": "send_outreach",
            "end": END
        }
    )
    
    workflow.add_conditional_edges(
        "send_outreach",
        should_continue,
        {
            "end": END
        }
    )
    
    return workflow.compile()


async def run_firereach_agent(request: FireReachRequest) -> AgentState:
    """Execute the FireReach agent."""
    graph = create_firereach_graph()
    
    # Initialize state
    initial_state: GraphState = {
        "icp": request.icp_description,
        "company_name": request.company_name,
        "recipient_email": request.recipient_email,
        "signals": [],
        "account_brief": "",
        "pain_points": [],
        "strategic_alignment": "",
        "email_subject": "",
        "email_body": "",
        "send_status": "pending",
        "message_id": "",
        "agent_log": [
            f"[INIT] FireReach agent initialized for company: {request.company_name}",
            f"[INIT] ICP: {request.icp_description[:100]}...",
            f"[INIT] Target email: {request.recipient_email}"
        ],
        "current_step": "initializing",
        "error": ""
    }
    
    # Run graph
    final_state = await graph.ainvoke(initial_state)
    
    # Convert to AgentState for response
    return AgentState(
        icp=final_state["icp"],
        company_name=final_state["company_name"],
        recipient_email=final_state["recipient_email"],
        signals=final_state["signals"],
        account_brief=final_state["account_brief"],
        pain_points=final_state["pain_points"],
        strategic_alignment=final_state["strategic_alignment"],
        email_subject=final_state["email_subject"],
        email_body=final_state["email_body"],
        send_status=final_state["send_status"],
        message_id=final_state["message_id"],
        agent_log=final_state["agent_log"],
        current_step=final_state["current_step"],
        error=final_state["error"]
    )
