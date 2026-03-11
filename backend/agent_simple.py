"""FireReach Agent - Simple sequential execution without LangGraph."""
from models import (
    AgentState, Signal, SignalHarvesterInput, ResearchAnalystInput, 
    OutreachSenderInput, FireReachRequest
)
from tools.signal_harvester import tool_signal_harvester
from tools.research_analyst import tool_research_analyst
from tools.outreach_sender import tool_outreach_automated_sender


async def run_firereach_agent(request: FireReachRequest) -> AgentState:
    """Execute the FireReach agent sequentially."""
    
    # Initialize state
    state = AgentState(
        icp=request.icp_description,
        company_name=request.company_name,
        recipient_email=request.recipient_email,
        signals=[],
        account_brief="",
        pain_points=[],
        strategic_alignment="",
        email_subject="",
        email_body="",
        send_status="pending",
        message_id="",
        agent_log=[
            f"[INIT] FireReach agent initialized for company: {request.company_name}",
            f"[INIT] ICP: {request.icp_description[:100]}...",
            f"[INIT] Target email: {request.recipient_email}"
        ],
        current_step="initializing",
        error=""
    )
    
    try:
        # Step 1: Harvest Signals
        state.current_step = "harvesting_signals"
        state.agent_log.append(
            f"[REASONING] Starting signal harvester for company: {state.company_name}"
        )
        
        signal_input = SignalHarvesterInput(
            company_name=state.company_name,
            signal_types=["funding", "hiring", "leadership", "tech_stack", "news"]
        )
        
        signal_result = await tool_signal_harvester(signal_input)
        state.signals = signal_result.signals
        state.agent_log.append(
            f"[ACTION] Signal harvester completed. Found {len(signal_result.signals)} signals"
        )
        
        # Step 2: Generate Brief
        state.current_step = "generating_brief"
        state.agent_log.append(
            f"[REASONING] Analyzing {len(state.signals)} signals against ICP"
        )
        
        research_input = ResearchAnalystInput(
            company_name=state.company_name,
            icp_description=state.icp,
            signals=state.signals
        )
        
        research_result = await tool_research_analyst(research_input)
        state.account_brief = research_result.account_brief
        state.pain_points = research_result.pain_points
        state.strategic_alignment = research_result.strategic_alignment
        state.agent_log.append(
            f"[ACTION] Research analyst completed. Generated brief with {len(research_result.pain_points)} pain points"
        )
        
        # Step 3: Send Outreach
        state.current_step = "sending_email"
        state.agent_log.append(
            "[REASONING] Drafting hyper-personalized email"
        )
        
        outreach_input = OutreachSenderInput(
            recipient_email=state.recipient_email,
            company_name=state.company_name,
            account_brief=state.account_brief,
            pain_points=state.pain_points,
            signals=state.signals,
            icp_description=state.icp
        )
        
        outreach_result = await tool_outreach_automated_sender(outreach_input)
        state.email_subject = outreach_result.email_subject
        state.email_body = outreach_result.email_body
        state.send_status = outreach_result.send_status
        state.message_id = outreach_result.message_id
        state.agent_log.append(
            f"[ACTION] Email send status: {outreach_result.send_status}"
        )
        
        state.current_step = "completed"
        
    except Exception as e:
        state.error = str(e)
        state.agent_log.append(f"[ERROR] {state.error}")
    
    return state
