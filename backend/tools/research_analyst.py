"""Research Analyst Tool - Generates account briefs using Groq."""
from groq import AsyncGroq
from config import config
from models import ResearchAnalystInput, ResearchAnalystOutput
import json


async def tool_research_analyst(input_data: ResearchAnalystInput) -> ResearchAnalystOutput:
    """Generate a 2-paragraph Account Brief using Groq AI."""
    client = AsyncGroq(api_key=config.GROQ_API_KEY)
    
    # Format signals
    signals_summary = "\n".join([
        f"- [{s.type.upper()}] {s.summary[:150]}..." if len(s.summary) > 150 else f"- [{s.type.upper()}] {s.summary}"
        for s in input_data.signals[:5]  # Limit to 5 signals
    ])
    
    prompt = f"""Analyze this company and create an account brief.

Company: {input_data.company_name}
ICP: {input_data.icp_description}
Signals: {signals_summary if signals_summary else "No signals found"}

Create a JSON response with:
1. account_brief: Exactly 2 paragraphs analyzing the company
2. pain_points: Array of 2-4 specific pain points
3. strategic_alignment: 1-2 sentences on why ICP fits

Return ONLY valid JSON in this format:
{{"account_brief": "...", "pain_points": ["...", "..."], "strategic_alignment": "..."}}"""
    
    response = await client.chat.completions.create(
        model=config.LLM_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=1500
    )
    
    response_text = response.choices[0].message.content
    
    try:
        start_idx = response_text.find('{')
        end_idx = response_text.rfind('}') + 1
        json_str = response_text[start_idx:end_idx]
        result = json.loads(json_str)
    except:
        result = {
            "account_brief": f"{input_data.company_name} is a growing company in the {input_data.icp_description} space. Based on available signals, they show strong growth potential.",
            "pain_points": ["Scaling challenges", "Training needs"],
            "strategic_alignment": "Good fit for the ICP offering."
        }
    
    return ResearchAnalystOutput(
        account_brief=result.get("account_brief", ""),
        pain_points=result.get("pain_points", []),
        strategic_alignment=result.get("strategic_alignment", "")
    )
