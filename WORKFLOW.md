# 🔄 FireReach Workflow Guide

Visual guide to how FireReach works from start to finish.

---

## Complete User Journey

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER JOURNEY                             │
└─────────────────────────────────────────────────────────────────┘

1. USER OPENS DASHBOARD
   │
   ├─ Sees input form
   ├─ Sees empty progress tracker
   └─ Sees "Launch FireReach" button
   │
   ▼

2. USER FILLS FORM
   │
   ├─ ICP: "We sell cybersecurity training to Series B startups"
   ├─ Company: "Wiz"
   └─ Email: "prospect@wiz.io"
   │
   ▼

3. USER CLICKS "LAUNCH FIREREACH"
   │
   ├─ Button shows loading spinner
   ├─ Form is disabled
   └─ Progress tracker activates
   │
   ▼

4. AGENT EXECUTES (10-18 seconds)
   │
   ├─ Step 1: Harvesting Signals (5-10s)
   │   ├─ Progress: 🔍 Active (pulsing)
   │   ├─ Backend: Searching 5 signal types
   │   └─ User sees: "Harvesting Signals" active
   │
   ├─ Step 2: Generating Brief (3-5s)
   │   ├─ Progress: 📊 Active (pulsing)
   │   ├─ Backend: Claude analyzing signals
   │   └─ User sees: "Generating Brief" active
   │
   └─ Step 3: Sending Outreach (2-3s)
       ├─ Progress: ✉️ Active (pulsing)
       ├─ Backend: Claude drafting + sending
       └─ User sees: "Sending Outreach" active
   │
   ▼

5. RESULTS DISPLAYED
   │
   ├─ All steps show green checkmarks ✓
   ├─ Signals card appears (8 signals found)
   ├─ Account Brief card appears (2 paragraphs)
   ├─ Email Preview card appears (Sent ✓)
   └─ Button re-enables
   │
   ▼

6. USER REVIEWS RESULTS
   │
   ├─ Reads harvested signals
   ├─ Reviews account brief
   ├─ Previews sent email
   └─ Sees "Sent ✓" badge
   │
   ▼

7. PROSPECT RECEIVES EMAIL
   │
   ├─ Email arrives in inbox
   ├─ Subject references specific signals
   ├─ Body mentions funding + hiring
   └─ Ends with meeting request
```

---

## Backend Agent Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                      AGENT EXECUTION                             │
└─────────────────────────────────────────────────────────────────┘

REQUEST RECEIVED
│
├─ Validate input (Pydantic)
├─ Create initial state
└─ Log: [INIT] Agent initialized
│
▼
┌──────────────────────────────────────────────────────────────┐
│                    NODE 1: HARVEST SIGNALS                    │
└──────────────────────────────────────────────────────────────┘
│
├─ Log: [REASONING] Starting signal harvester...
├─ Build search queries (5 types)
├─ Call SerpAPI/Tavily for each type:
│   ├─ "Wiz funding round site:techcrunch.com"
│   ├─ "Wiz is hiring site:linkedin.com"
│   ├─ "Wiz new CTO OR CEO site:linkedin.com"
│   ├─ "Wiz adopts technology"
│   └─ "Wiz expanding OR Series B"
├─ Parse results into Signal objects
├─ Update state: signals = [Signal, Signal, ...]
├─ Log: [ACTION] Found 8 signals
└─ Log: [OBSERVATION] Top signals: funding, hiring, news
│
▼
┌──────────────────────────────────────────────────────────────┐
│                  NODE 2: GENERATE BRIEF                       │
└──────────────────────────────────────────────────────────────┘
│
├─ Log: [REASONING] Analyzing signals against ICP...
├─ Format signals for Claude prompt
├─ Build research analyst prompt
├─ Call Claude with function calling:
│   ├─ Tool: submit_account_brief
│   ├─ Input: company, icp, signals
│   └─ Output: brief, pain_points, alignment
├─ Extract structured response
├─ Update state: account_brief, pain_points, alignment
├─ Log: [ACTION] Generated 2-paragraph brief
└─ Log: [OBSERVATION] Strategic alignment: ...
│
▼
┌──────────────────────────────────────────────────────────────┐
│                   NODE 3: SEND OUTREACH                       │
└──────────────────────────────────────────────────────────────┘
│
├─ Log: [REASONING] Drafting personalized email...
├─ Format all data for email prompt
├─ Build email drafting prompt
├─ Call Claude with function calling:
│   ├─ Tool: submit_email_draft
│   ├─ Input: all previous data
│   └─ Output: subject, body
├─ Extract email draft
├─ Verify: References 2+ signals ✓
├─ Call SendGrid/Resend API:
│   ├─ To: prospect@wiz.io
│   ├─ Subject: "Re: Wiz's Series D and security hiring"
│   └─ Body: [personalized email]
├─ Capture message_id
├─ Update state: email_subject, email_body, send_status, message_id
├─ Log: [ACTION] Email send status: sent
└─ Log: [OBSERVATION] Outreach successfully delivered
│
▼
RETURN RESPONSE
│
├─ Assemble FireReachResponse
├─ Include all outputs
├─ Include agent_log
└─ Send to frontend
```

---

## Data Flow Through Tools

```
┌─────────────────────────────────────────────────────────────────┐
│                         DATA FLOW                                │
└─────────────────────────────────────────────────────────────────┘

INPUT
├─ icp: "We sell cybersecurity training..."
├─ company_name: "Wiz"
└─ recipient_email: "prospect@wiz.io"
    │
    ▼
TOOL 1: SIGNAL HARVESTER
    │
    ├─ Input: company_name, signal_types
    ├─ Process: 5 web searches
    └─ Output: signals[]
        │
        ├─ Signal 1: {type: "funding", summary: "Wiz raises $300M..."}
        ├─ Signal 2: {type: "hiring", summary: "Wiz hiring 15 engineers..."}
        ├─ Signal 3: {type: "news", summary: "Wiz expands to Europe..."}
        └─ ... (5 more signals)
        │
        ▼
TOOL 2: RESEARCH ANALYST
    │
    ├─ Input: company_name, icp, signals[]
    ├─ Process: Claude analysis
    └─ Output: account_brief, pain_points[], alignment
        │
        ├─ account_brief: "Wiz recently closed a $300M Series D..."
        ├─ pain_points: ["Rapid onboarding...", "Hypergrowth..."]
        └─ alignment: "High-end training is perfectly timed..."
        │
        ▼
TOOL 3: OUTREACH SENDER
    │
    ├─ Input: ALL previous data
    ├─ Process: Claude drafting + SendGrid sending
    └─ Output: email_subject, email_body, send_status, message_id
        │
        ├─ email_subject: "Re: Wiz's Series D and security hiring"
        ├─ email_body: "Hi there, I noticed Wiz just raised..."
        ├─ send_status: "sent"
        └─ message_id: "sg-msg-abc123xyz"
        │
        ▼
RESPONSE
├─ status: "success"
├─ signals: [8 signals]
├─ account_brief: "..."
├─ pain_points: [3 points]
├─ email_subject: "..."
├─ email_body: "..."
├─ send_status: "sent"
├─ message_id: "sg-msg-abc123xyz"
└─ agent_log: [15 log entries]
```

---

## State Evolution

```
┌─────────────────────────────────────────────────────────────────┐
│                    STATE TRANSITIONS                             │
└─────────────────────────────────────────────────────────────────┘

INITIAL STATE
{
  icp: "We sell cybersecurity training...",
  company_name: "Wiz",
  recipient_email: "prospect@wiz.io",
  signals: [],                    ← Empty
  account_brief: "",              ← Empty
  pain_points: [],                ← Empty
  strategic_alignment: "",        ← Empty
  email_subject: "",              ← Empty
  email_body: "",                 ← Empty
  send_status: "pending",
  message_id: "",                 ← Empty
  agent_log: ["[INIT] ..."],
  current_step: "initializing",
  error: ""
}
    │
    ▼ After Tool 1
{
  ...
  signals: [Signal, Signal, ...], ← Populated (8 items)
  agent_log: [..., "[ACTION] Found 8 signals"],
  current_step: "harvesting_signals",
  ...
}
    │
    ▼ After Tool 2
{
  ...
  account_brief: "Wiz recently...", ← Populated
  pain_points: ["...", "..."],      ← Populated (3 items)
  strategic_alignment: "...",       ← Populated
  agent_log: [..., "[ACTION] Generated brief"],
  current_step: "generating_brief",
  ...
}
    │
    ▼ After Tool 3
{
  ...
  email_subject: "Re: Wiz's...",  ← Populated
  email_body: "Hi there...",      ← Populated
  send_status: "sent",            ← Changed
  message_id: "sg-msg-abc123",    ← Populated
  agent_log: [..., "[ACTION] Email sent"],
  current_step: "sending_email",
  ...
}
    │
    ▼ FINAL STATE (returned to frontend)
```

---

## Error Handling Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                      ERROR SCENARIOS                             │
└─────────────────────────────────────────────────────────────────┘

SCENARIO 1: Signal Harvesting Fails
│
├─ Tool 1 throws exception
├─ Catch: Log [ERROR] Signal harvesting failed
├─ Set: state.error = "Signal harvesting failed: ..."
├─ Set: state.current_step = "harvesting_signals"
├─ Conditional edge: → END
└─ Return: Partial response with error
    │
    Result: Frontend shows error at step 1

SCENARIO 2: Research Analysis Fails
│
├─ Tool 1 succeeds (signals populated)
├─ Tool 2 throws exception
├─ Catch: Log [ERROR] Research analysis failed
├─ Set: state.error = "Research analysis failed: ..."
├─ Set: state.current_step = "generating_brief"
├─ Conditional edge: → END
└─ Return: Partial response with signals but no brief
    │
    Result: Frontend shows signals but error at step 2

SCENARIO 3: Email Sending Fails
│
├─ Tool 1 succeeds (signals populated)
├─ Tool 2 succeeds (brief populated)
├─ Tool 3 drafts email successfully
├─ SendGrid API fails
├─ Catch: Set send_status = "failed"
├─ Set: state.message_id = error message
├─ Log: [ERROR] Email sending failed
└─ Return: Complete response with send_status = "failed"
    │
    Result: Frontend shows all data but "Failed ✗" badge

SCENARIO 4: Invalid Input
│
├─ Request validation fails (Pydantic)
├─ FastAPI returns 422 Unprocessable Entity
└─ Frontend displays validation error
    │
    Result: Agent never runs
```

---

## Frontend State Management

```
┌─────────────────────────────────────────────────────────────────┐
│                    FRONTEND WORKFLOW                             │
└─────────────────────────────────────────────────────────────────┘

INITIAL RENDER
│
├─ formData: {icp: "", company: "", email: ""}
├─ loading: false
├─ result: null
└─ error: null
    │
    ▼ User fills form
    │
FORM SUBMISSION
│
├─ Set: loading = true
├─ Set: error = null
├─ Set: result = null
├─ Call: axios.post("/api/firereach", formData)
└─ Wait for response...
    │
    ▼ Response received
    │
SUCCESS PATH
│
├─ Set: result = response.data
├─ Set: loading = false
├─ Render: Progress tracker (all steps completed)
├─ Render: Signals card
├─ Render: Account Brief card
└─ Render: Email Preview card
    │
    OR
    │
ERROR PATH
│
├─ Set: error = error.message
├─ Set: loading = false
└─ Render: Error message in red box
```

---

## Time-Based Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                      TIMELINE VIEW                               │
└─────────────────────────────────────────────────────────────────┘

T=0s    User clicks "Launch FireReach"
        ├─ Frontend: Button disabled, loading spinner
        └─ Backend: Request received, validation starts

T=0.1s  Agent initialized
        ├─ State created
        └─ Log: [INIT] messages

T=0.2s  Tool 1 starts (Signal Harvester)
        ├─ Frontend: Step 1 shows "active" (pulsing)
        └─ Backend: First search query sent

T=2s    Search 1 completes (funding signals)
T=4s    Search 2 completes (hiring signals)
T=6s    Search 3 completes (leadership signals)
T=8s    Search 4 completes (tech_stack signals)
T=10s   Search 5 completes (news signals)

T=10.1s Tool 1 completes
        ├─ Frontend: Step 1 shows "completed" (green ✓)
        ├─ Frontend: Step 2 shows "active" (pulsing)
        └─ Backend: 8 signals found, logged

T=10.2s Tool 2 starts (Research Analyst)
        └─ Backend: Claude API call initiated

T=13s   Claude responds with account brief
        └─ Backend: Brief parsed and validated

T=13.1s Tool 2 completes
        ├─ Frontend: Step 2 shows "completed" (green ✓)
        ├─ Frontend: Step 3 shows "active" (pulsing)
        └─ Backend: Brief, pain points, alignment stored

T=13.2s Tool 3 starts (Outreach Sender)
        └─ Backend: Claude API call for email draft

T=15s   Claude responds with email draft
        └─ Backend: Email validated (references 2+ signals ✓)

T=15.1s SendGrid API call initiated
        └─ Backend: Email payload sent

T=16s   SendGrid responds with message_id
        └─ Backend: send_status = "sent"

T=16.1s Tool 3 completes
        ├─ Frontend: Step 3 shows "completed" (green ✓)
        └─ Backend: All data logged

T=16.2s Response sent to frontend
        └─ Backend: FireReachResponse assembled

T=16.3s Frontend receives response
        ├─ Signals card renders (8 signals)
        ├─ Account Brief card renders
        ├─ Email Preview card renders
        └─ "Sent ✓" badge shows

T=16.5s User reviews results
        └─ Frontend: All data displayed

T=17s   Prospect's email server receives email
        └─ External: Email delivered to inbox

TOTAL TIME: ~16-17 seconds
```

---

## Decision Points

```
┌─────────────────────────────────────────────────────────────────┐
│                    CONDITIONAL LOGIC                             │
└─────────────────────────────────────────────────────────────────┘

After Tool 1 (Signal Harvester):
│
├─ If error: → END (return partial response)
└─ If success: → Tool 2 (Research Analyst)

After Tool 2 (Research Analyst):
│
├─ If error: → END (return partial response)
└─ If success: → Tool 3 (Outreach Sender)

After Tool 3 (Outreach Sender):
│
└─ Always: → END (return complete response)
    ├─ send_status = "sent" → Success
    └─ send_status = "failed" → Partial success

Frontend Display Logic:
│
├─ If result.status === "success" && result.send_status === "sent"
│   └─ Show: All green checkmarks, "Sent ✓" badge
│
├─ If result.status === "success" && result.send_status === "failed"
│   └─ Show: Steps 1-2 green, Step 3 red, "Failed ✗" badge
│
└─ If result.status === "failed"
    └─ Show: Error at failed step, partial results
```

---

## Integration Points

```
┌─────────────────────────────────────────────────────────────────┐
│                   EXTERNAL INTEGRATIONS                          │
└─────────────────────────────────────────────────────────────────┘

1. SerpAPI / Tavily (Search)
   ├─ When: Tool 1 execution
   ├─ Calls: 5 searches per execution
   ├─ Rate Limit: Depends on plan
   └─ Fallback: Continue with fewer signals

2. Anthropic Claude (LLM)
   ├─ When: Tool 2 and Tool 3
   ├─ Calls: 2 per execution
   ├─ Model: claude-sonnet-4-20250514
   ├─ Method: Function calling (tool_use)
   └─ Fallback: Return error, stop execution

3. SendGrid / Resend (Email)
   ├─ When: Tool 3 execution
   ├─ Calls: 1 per execution
   ├─ Rate Limit: Depends on plan
   └─ Fallback: Return draft with send_status = "failed"

4. Frontend ↔ Backend (HTTP)
   ├─ Protocol: HTTPS
   ├─ Method: POST /api/firereach
   ├─ Format: JSON
   └─ CORS: Configured for frontend domain
```

---

**This workflow ensures reliable, transparent, and efficient autonomous outreach.** 🔄
