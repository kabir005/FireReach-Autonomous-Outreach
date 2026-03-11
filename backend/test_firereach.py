"""Test script for FireReach agent."""
import asyncio
import sys
from models import FireReachRequest
from agent import run_firereach_agent
from config import config


async def test_firereach():
    """Test the FireReach agent with the challenge scenario."""
    
    # Validate configuration
    print("🔍 Validating configuration...")
    errors = config.validate()
    if errors:
        print("❌ Configuration errors found:")
        for error in errors:
            print(f"   - {error}")
        print("\nPlease check your .env file and add the required API keys.")
        sys.exit(1)
    
    print("✅ Configuration valid\n")
    
    # Create test request
    print("🚀 Launching FireReach agent...")
    print("=" * 60)
    
    request = FireReachRequest(
        icp_description="We sell high-end cybersecurity training to Series B startups.",
        company_name="Wiz",
        recipient_email="test@example.com"  # Change this to your test email
    )
    
    print(f"ICP: {request.icp_description}")
    print(f"Company: {request.company_name}")
    print(f"Recipient: {request.recipient_email}")
    print("=" * 60)
    print()
    
    # Run agent
    try:
        result = await run_firereach_agent(request)
        
        # Print agent log
        print("📋 Agent Execution Log:")
        print("-" * 60)
        for log_entry in result.agent_log:
            print(log_entry)
        print("-" * 60)
        print()
        
        # Print results
        print("📊 Results:")
        print("-" * 60)
        print(f"Status: {result.send_status}")
        print(f"Current Step: {result.current_step}")
        print(f"Signals Found: {len(result.signals)}")
        
        if result.signals:
            print("\n🔍 Top Signals:")
            for signal in result.signals[:3]:
                print(f"  [{signal.type.upper()}] {signal.summary[:80]}...")
        
        if result.account_brief:
            print(f"\n📝 Account Brief:")
            print(f"  {result.account_brief[:200]}...")
        
        if result.pain_points:
            print(f"\n💡 Pain Points:")
            for point in result.pain_points:
                print(f"  - {point}")
        
        if result.email_subject:
            print(f"\n✉️  Email Subject:")
            print(f"  {result.email_subject}")
        
        if result.email_body:
            print(f"\n📧 Email Body:")
            print(f"  {result.email_body[:200]}...")
        
        print(f"\n📬 Send Status: {result.send_status}")
        if result.message_id:
            print(f"📨 Message ID: {result.message_id}")
        
        if result.error:
            print(f"\n❌ Error: {result.error}")
        
        print("-" * 60)
        
        # Final verdict
        if result.send_status == "sent" and not result.error:
            print("\n✅ SUCCESS! FireReach agent completed successfully.")
            print("   Check your email for the outreach message.")
        else:
            print("\n⚠️  Agent completed with issues. Check the logs above.")
        
    except Exception as e:
        print(f"\n❌ Error running agent: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    print("🔥 FireReach Test Script")
    print("=" * 60)
    print()
    
    asyncio.run(test_firereach())
