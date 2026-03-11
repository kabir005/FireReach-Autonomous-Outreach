"""Quick test to verify deployment readiness."""
import asyncio
from agent_simple import run_firereach_agent
from models import FireReachRequest

async def test_agent():
    """Test the agent with a simple request."""
    request = FireReachRequest(
        icp_description="We sell cybersecurity training to Series B startups",
        company_name="Test Company",
        recipient_email="test@example.com"
    )
    
    try:
        result = await run_firereach_agent(request)
        print("✅ Agent executed successfully!")
        print(f"Current step: {result.current_step}")
        print(f"Signals found: {len(result.signals)}")
        print(f"Error: {result.error if result.error else 'None'}")
        return True
    except Exception as e:
        print(f"❌ Agent failed: {str(e)}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_agent())
    exit(0 if success else 1)
