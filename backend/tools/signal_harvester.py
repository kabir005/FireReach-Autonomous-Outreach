"""Signal Harvester Tool - Fetches live buyer intent signals."""
import httpx
from datetime import datetime
from typing import Any
from config import config
from models import Signal, SignalHarvesterInput, SignalHarvesterOutput


async def search_serpapi(query: str) -> dict[str, Any]:
    """Search using SerpAPI."""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://serpapi.com/search",
            params={
                "q": query,
                "api_key": config.SERPAPI_KEY,
                "num": 5
            },
            timeout=30.0
        )
        response.raise_for_status()
        return response.json()


async def search_tavily(query: str) -> dict[str, Any]:
    """Search using Tavily API."""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.tavily.com/search",
            json={
                "api_key": config.TAVILY_API_KEY,
                "query": query,
                "search_depth": "basic",
                "max_results": 5
            },
            timeout=30.0
        )
        response.raise_for_status()
        return response.json()


def parse_search_results(results: dict[str, Any], signal_type: str, company: str) -> list[Signal]:
    """Parse search results into Signal objects."""
    signals = []
    timestamp = datetime.utcnow().isoformat()
    
    # Handle SerpAPI format
    if "organic_results" in results:
        for result in results.get("organic_results", [])[:3]:
            signals.append(Signal(
                type=signal_type,
                summary=f"{result.get('title', '')} - {result.get('snippet', '')}",
                source_url=result.get("link", ""),
                detected_at=timestamp
            ))
    
    # Handle Tavily format
    elif "results" in results:
        for result in results.get("results", [])[:3]:
            signals.append(Signal(
                type=signal_type,
                summary=f"{result.get('title', '')} - {result.get('content', '')}",
                source_url=result.get("url", ""),
                detected_at=timestamp
            ))
    
    return signals


async def tool_signal_harvester(input_data: SignalHarvesterInput) -> SignalHarvesterOutput:
    """
    Harvest live buyer intent signals for a company.
    
    This tool performs real web searches to find signals like funding, hiring,
    leadership changes, tech stack updates, and news.
    """
    company = input_data.company_name
    all_signals = []
    raw_results = []
    
    # Define search queries for each signal type
    search_queries = {
        "funding": f'"{company}" funding round site:techcrunch.com OR site:crunchbase.com',
        "hiring": f'"{company}" is hiring site:linkedin.com OR site:greenhouse.io',
        "leadership": f'"{company}" new CTO OR CEO OR VP site:linkedin.com',
        "tech_stack": f'"{company}" adopts OR implements OR uses technology',
        "news": f'"{company}" expanding OR growth OR Series B OR acquisition'
    }
    
    # Choose search provider
    search_func = search_serpapi if config.SERPAPI_KEY else search_tavily
    
    # Execute searches for requested signal types
    for signal_type in input_data.signal_types:
        if signal_type not in search_queries:
            continue
        
        try:
            query = search_queries[signal_type]
            results = await search_func(query)
            raw_results.append(f"[{signal_type}] {str(results)[:500]}")
            
            parsed_signals = parse_search_results(results, signal_type, company)
            all_signals.extend(parsed_signals)
        
        except Exception as e:
            # Log error but continue with other signal types
            raw_results.append(f"[{signal_type}] Error: {str(e)}")
    
    return SignalHarvesterOutput(
        company_name=company,
        signals=all_signals,
        raw_search_results="\n\n".join(raw_results)
    )
