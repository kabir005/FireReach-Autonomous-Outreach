# 🏗️ FireReach Architecture

Detailed architecture documentation for FireReach.

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER BROWSER                             │
│                    (React + Tailwind CSS)                        │
└────────────────────────┬────────────────────────────────────────┘
                         │ HTTPS
                         │ POST /api/firereach
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                      FASTAPI SERVER                              │
│                    (Python 3.11 + Uvicorn)                       │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    CORS Middleware                       │   │
│  └────────────────────┬────────────────────────────────────┘   │
│                       │                                          │
│  ┌────────────────────▼────────────────────────────────────┐   │
│  │              Request Validation                          │   │
│  │              (Pydantic Models)                           │   │
│  └────────────────────┬────────────────────────────────────┘   │
│                       │                                          │
│  ┌────────────────────▼────────────────────────────────────┐   │
│  │              Agent Orchestrator                          │   │
│  │              (LangGraph StateGraph)                      │   │
│  └────────────────────┬────────────────────────────────────┘   │
└───────────────────────┼──────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────────┐
│                      AGENT EXECUTION                             │
│                    (ReAct Pattern Loop)                          │
│                                                                   │
│  ┌──────────────┐      ┌──────────────┐      ┌──────────────┐  │
│  │   Node 1:    │      │   Node 2:    │      │   Node 3:    │  │
│  │   Harvest    │─────▶│   Research   │─────▶│   Outreach   │  │
│  │   Signals    │      │   Analyst    │      │   Sender     │  │
│  └──────┬───────┘      └──────┬───────┘      └──────┬───────┘  │
│         │                     │                     │            │
└─────────┼─────────────────────┼─────────────────────┼────────────┘
          │                     │                     │
          ▼                     ▼                     ▼
    ┌──────────┐          ┌──────────┐          ┌──────────┐
    │ SerpAPI  │          │ Claude   │          │ Claude   │
    │    or    │          │ Sonnet   │          │ Sonnet   │
    │  Tavily  │          │   4.5    │          │   4.5    │
    └──────────┘          └──────────┘          └────┬─────┘
                                                      │
                                                      ▼
                                                ┌──────────┐
                                                │SendGrid  │
                                                │    or    │
                                                │  Resend  │
                                                └──────────┘
```

---

## Data Flow

### Request Flow

```
1. User Input
   ├─ icp_description: "We sell..."
   ├─ company_name: "Wiz"
   └─ recipient_email: "prospect@wiz.io"
        │
        ▼
2. FastAPI Validation (Pydantic)
   ├─ Validate email format
   ├─ Validate required fields
   └─ Create FireReachRequest object
        │
        ▼
3. Agent Initialization
   ├─ Create GraphState
   ├─ Initialize agent_log: []
   └─ Set current_step: "initializing"
        │
        ▼
4. Tool 1: Signal Harvester
   ├─ Input: company_name, signal_types
   ├─ Action: Search APIs (5 queries)
   ├─ Parse: Extract signals from results
   └─ Output: signals: [Signal, Signal, ...]
        │
        ▼
5. Tool 2: Research Analyst
   ├─ Input: company_name, icp, signals
   ├─ Action: Claude function calling
   ├─ Generate: 2-paragraph brief
   └─ Output: account_brief, pain_points, alignment
        │
        ▼
6. Tool 3: Outreach Sender
   ├─ Input: All previous data
   ├─ Action: Claude drafts email
   ├─ Send: Via SendGrid/Resend API
   └─ Output: subject, body, status, message_id
        │
        ▼
7. Response Assembly
   ├─ Collect all outputs
   ├─ Add agent_log entries
   └─ Return FireReachResponse
        │
        ▼
8. Frontend Display
   ├─ Show signals in card
   ├─ Show brief in card
   ├─ Show email preview
   └─ Update status badges
```

---

## State Management

### LangGraph State Schema

```python
GraphState = {
    # Input data
    "icp": str,
    "company_name": str,
    "recipient_email": str,
    
    # Tool 1 outputs
    "signals": list[Signal],
    
    # Tool 2 outputs
    "account_brief": str,
    "pain_points": list[str],
    "strategic_alignment": str,
    
    # Tool 3 outputs
    "email_subject": str,
    "email_body": str,
    "send_status": str,
    "message_id": str,
    
    # Agent metadata
    "agent_log": list[str],  # Accumulated reasoning
    "current_step": str,     # Current node
    "error": str             # Error message if any
}
```

### State Transitions

```
initializing
    ↓
harvesting_signals
    ↓ (signals added to state)
generating_brief
    ↓ (brief, pain_points added to state)
sending_email
    ↓ (email data added to state)
completed
```

---

## Tool Architecture

### Tool 1: Signal Harvester

```
Input Schema:
{
  company_name: str,
  signal_types: list[str]
}

Processing:
1. For each signal_type:
   ├─ Build search query
   ├─ Call search API (SerpAPI/Tavily)
   ├─ Parse results
   └─ Create Signal objects

2. Aggregate all signals

3. Store raw results for debugging

Output Schema:
{
  company_name: str,
  signals: [
    {
      type: str,
      summary: str,
      source_url: str,
      detected_at: ISO timestamp
    }
  ],
  raw_search_results: str
}
```

### Tool 2: Research Analyst

```
Input Schema:
{
  company_name: str,
  icp_description: str,
  signals: list[Signal]
}

Processing:
1. Format signals for prompt
2. Build analysis prompt
3. Call Claude with function calling:
   ├─ Tool: submit_account_brief
   ├─ Schema: account_brief, pain_points, alignment
   └─ Force tool use
4. Extract structured output

Output Schema:
{
  account_brief: str (2 paragraphs),
  pain_points: list[str] (2-4 items),
  strategic_alignment: str (1-2 sentences)
}
```

### Tool 3: Outreach Sender

```
Input Schema:
{
  recipient_email: str,
  company_name: str,
  account_brief: str,
  pain_points: list[str],
  signals: list[Signal],
  icp_description: str
}

Processing:
1. Format all data for prompt
2. Build email drafting prompt
3. Call Claude with function calling:
   ├─ Tool: submit_email_draft
   ├─ Schema: subject, body
   └─ Force tool use
4. Extract email draft
5. Send via email API:
   ├─ SendGrid: Mail object + send
   └─ Resend: HTTP POST
6. Capture message_id

Output Schema:
{
  email_subject: str,
  email_body: str,
  send_status: "sent" | "failed",
  message_id: str
}
```

---

## Agent Reasoning Pattern

### ReAct Loop

```
For each node:
  1. REASON
     ├─ Log: "[REASONING] Why calling this tool..."
     ├─ Consider: Current state
     └─ Decide: Which tool to call
  
  2. ACT
     ├─ Log: "[ACTION] Calling tool with inputs..."
     ├─ Execute: Tool function
     └─ Wait: For tool completion
  
  3. OBSERVE
     ├─ Log: "[OBSERVATION] Tool returned..."
     ├─ Update: State with outputs
     └─ Check: For errors
  
  4. CONTINUE or END
     ├─ If error: END
     ├─ If more tools: CONTINUE to next node
     └─ If done: END
```

### Example Reasoning Log

```
[INIT] FireReach agent initialized for company: Wiz
[INIT] ICP: We sell high-end cybersecurity training...
[INIT] Target email: prospect@wiz.io

[REASONING] Starting signal harvester for company: Wiz. 
            Will search for funding, hiring, leadership, 
            tech_stack, and news signals.

[ACTION] Signal harvester completed. Found 8 signals 
         across 4 categories.

[OBSERVATION] Top signals: funding, hiring, news

[REASONING] Analyzing 8 signals against ICP to generate 
            account brief. Will identify pain points and 
            strategic alignment.

[ACTION] Research analyst completed. Generated 2-paragraph 
         brief with 3 pain points identified.

[OBSERVATION] Strategic alignment: High-end cybersecurity 
              training is perfectly timed for Wiz's current 
              growth phase...

[REASONING] Drafting hyper-personalized email that references 
            specific signals. Will ensure at least 2 signals 
            are mentioned, then send via email API.

[ACTION] Email drafted with subject: 'Re: Wiz's Series D 
         and security hiring'

[ACTION] Email send status: sent (Message ID: sg-msg-abc123)

[OBSERVATION] Outreach successfully delivered. FireReach 
              sequence complete.
```

---

## Error Handling

### Error Flow

```
Any Node
    │
    ├─ Try: Execute tool
    │
    ├─ Catch Exception:
    │   ├─ Log: "[ERROR] Tool failed: {error}"
    │   ├─ Set: state["error"] = error message
    │   └─ Set: state["current_step"] = failed step
    │
    └─ Conditional Edge:
        ├─ If error: → END
        └─ If success: → Next Node
```

### Error Types

1. **Configuration Errors**
   - Missing API keys
   - Invalid credentials
   - Caught at startup

2. **Tool Execution Errors**
   - API rate limits
   - Network timeouts
   - Invalid responses
   - Caught per-tool

3. **Validation Errors**
   - Invalid email format
   - Missing required fields
   - Caught at request validation

---

## Security Architecture

### API Key Management

```
Environment Variables (.env)
    ↓
Config Class (config.py)
    ↓
Validation on Startup
    ↓
Used in Tools (never logged)
```

### CORS Configuration

```
Frontend Domain
    ↓
CORS Middleware
    ├─ Check: Origin header
    ├─ Allow: Configured domains only
    └─ Reject: Unknown origins
    ↓
Backend Endpoint
```

### Data Flow Security

```
User Input
    ↓
Pydantic Validation (sanitization)
    ↓
Agent Processing (no PII in logs)
    ↓
External APIs (HTTPS only)
    ↓
Response (no API keys exposed)
```

---

## Performance Considerations

### Async Architecture

```
FastAPI (async)
    ↓
Agent (async)
    ↓
Tools (async)
    ├─ Signal Harvester (async httpx)
    ├─ Research Analyst (async anthropic)
    └─ Outreach Sender (async anthropic + httpx)
```

### Bottlenecks

1. **Signal Harvesting**: 5-10 seconds
   - 5 sequential API calls
   - Could be parallelized

2. **Claude Calls**: 3-5 seconds each
   - 2 calls total (research + email)
   - Already async

3. **Email Sending**: 1-2 seconds
   - Single API call
   - Fast

**Total**: 10-18 seconds (acceptable for use case)

### Optimization Opportunities

1. **Parallel Signal Searches**
   ```python
   results = await asyncio.gather(
       search("funding"),
       search("hiring"),
       search("leadership")
   )
   ```

2. **Caching**
   - Cache signals for 24 hours
   - Reduce API calls for repeated companies

3. **Connection Pooling**
   - Reuse HTTP connections
   - Already handled by httpx

---

## Deployment Architecture

### Development

```
Localhost:3000 (Frontend)
    ↓ HTTP
Localhost:8000 (Backend)
    ↓ HTTPS
External APIs
```

### Production

```
Vercel CDN (Frontend)
    ↓ HTTPS
Render.com (Backend)
    ↓ HTTPS
External APIs
```

### Scaling Strategy

1. **Horizontal Scaling**
   - Add more Render instances
   - Load balancer distributes requests

2. **Vertical Scaling**
   - Upgrade Render plan
   - More CPU/RAM per instance

3. **Caching Layer**
   - Redis for signal caching
   - Reduce API costs

---

## Monitoring Architecture

### Metrics to Track

```
Request Level:
├─ Total requests
├─ Success rate
├─ Error rate
└─ Response time (p50, p95, p99)

Tool Level:
├─ Signal harvester success rate
├─ Research analyst success rate
├─ Email sender success rate
└─ Per-tool execution time

Business Level:
├─ Emails sent
├─ Email delivery rate
└─ Cost per outreach
```

### Logging Strategy

```
Application Logs:
├─ Agent reasoning (INFO)
├─ Tool executions (INFO)
├─ Errors (ERROR)
└─ Performance metrics (DEBUG)

Access Logs:
├─ Request path
├─ Response status
├─ Response time
└─ User agent
```

---

## Technology Stack Summary

### Backend
- **Language**: Python 3.11
- **Framework**: FastAPI 0.109
- **LLM**: Anthropic Claude Sonnet 4.5
- **Agent**: LangGraph 0.0.20
- **Validation**: Pydantic 2.6
- **HTTP Client**: httpx 0.26
- **Email**: SendGrid 6.11 or Resend API

### Frontend
- **Language**: JavaScript (ES6+)
- **Framework**: React 18.2
- **Build Tool**: Vite 5.0
- **Styling**: Tailwind CSS 3.4
- **HTTP Client**: Axios 1.6

### Infrastructure
- **Backend Host**: Render.com
- **Frontend Host**: Vercel
- **Container**: Docker (optional)

---

**Architecture designed for reliability, scalability, and maintainability.** 🏗️
