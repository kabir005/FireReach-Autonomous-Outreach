"""Outreach Sender Tool - Drafts and sends personalized emails."""
from groq import AsyncGroq
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import config
from models import OutreachSenderInput, OutreachSenderOutput
import json


async def draft_email_with_groq(input_data: OutreachSenderInput) -> tuple[str, str]:
    """Use Groq to draft a personalized email."""
    client = AsyncGroq(api_key=config.GROQ_API_KEY)
    
    signals_json = json.dumps([
        {"type": s.type, "summary": s.summary, "source": s.source_url}
        for s in input_data.signals[:6]
    ], indent=2)
    
    pain_points_str = ", ".join(input_data.pain_points)
    
    prompt = f"""You are an elite B2B sales copywriter who writes emails that get replies. Write a cold outreach email that feels like it was written by a human SDR who spent 20 minutes researching this company.

STRICT RULES:
1. Subject line: Must be specific, under 8 words, reference a real signal (e.g. "Congrats on the $1B round, quick thought")
2. Opening line: Reference a SPECIFIC signal with a detail (amount, number, name) — never generic
3. Bridge paragraph: Connect their specific situation to a concrete pain point (use the pain points provided)
4. Value paragraph: Explain what the seller offers in 1-2 sentences, tied to THEIR specific context
5. CTA: Soft ask — offer a specific value (e.g. "a 15-min call to share how we helped [similar company] reduce breach risk during rapid hiring")
6. Signature: Professional — include name, title, company, one-liner
7. Total length: 180-220 words (not too short, not too long)
8. Tone: Confident, peer-to-peer, never salesy or desperate
9. Must include at least 2 specific data points from the signals (numbers, names, dates)
10. Never use phrases like: "I hope this finds you well", "I wanted to reach out", "touching base", "synergy", "leverage"

ICP Context: {input_data.icp_description}
Target Company: {input_data.company_name}
Account Brief: {input_data.account_brief}
Pain Points: {pain_points_str}
Live Signals (use specific details from these): {signals_json}

Output format — return JSON only:
{{
  "subject": "string",
  "greeting": "string",
  "opening_line": "string",
  "bridge_paragraph": "string",
  "value_paragraph": "string",
  "cta": "string",
  "signature": "string",
  "full_body": "string (complete assembled email body)"
}}"""
    
    response = await client.chat.completions.create(
        model=config.LLM_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.8,
        max_tokens=1200
    )
    
    response_text = response.choices[0].message.content
    
    try:
        start_idx = response_text.find('{')
        end_idx = response_text.rfind('}') + 1
        json_str = response_text[start_idx:end_idx]
        result = json.loads(json_str)
        subject = result.get("subject", f"Re: {input_data.company_name}'s growth")
        body = result.get("full_body", response_text)
    except:
        subject = f"Re: {input_data.company_name}'s recent growth"
        body = response_text
    
    return subject, body


def send_email_gmail(to_email: str, subject: str, body: str) -> tuple[str, str]:
    """Send email via Gmail SMTP."""
    try:
        msg = MIMEMultipart('alternative')
        msg['From'] = f"{config.FROM_NAME} <{config.GMAIL_EMAIL}>"
        msg['To'] = to_email
        msg['Subject'] = subject
        
        html_body = body.replace("\n", "<br>")
        msg.attach(MIMEText(html_body, 'html'))
        
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user=config.GMAIL_EMAIL, password=config.GMAIL_APP_PASSWORD)
            connection.sendmail(from_addr=config.GMAIL_EMAIL, to_addrs=to_email, msg=msg.as_string())
        
        return "sent", f"gmail_{to_email}"
    except Exception as e:
        return "failed", str(e)


async def tool_outreach_automated_sender(input_data: OutreachSenderInput) -> OutreachSenderOutput:
    """Draft and send a hyper-personalized outreach email."""
    subject, body = await draft_email_with_groq(input_data)
    
    status, message_id = send_email_gmail(input_data.recipient_email, subject, body)
    
    return OutreachSenderOutput(
        email_subject=subject,
        email_body=body,
        send_status=status,
        message_id=message_id
    )
