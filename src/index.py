#!/usr/bin/env python3
"""
email-sequence-writer — product + funnel stage → complete drip email sequence
Welcome series, abandoned cart, post-purchase, win-back, nurture — with
subject lines, preview text, body copy, CTAs, send timing
"""
import anthropic, json, re, sys

SYSTEM = """You are a world-class email copywriter and marketing automation specialist.
Write email sequences that convert — every email has a job and does it.

Framework:
- Subject line: open (curiosity/benefit/urgency)
- Preview text: adds context, not a repeat
- Email body: one big idea, one CTA
- Timing: spaced for the psychology of the funnel stage

Return ONLY valid JSON — no markdown, no explanation.

{
  "sequence_name": "string",
  "sequence_type": "welcome|abandoned_cart|post_purchase|win_back|nurture|launch|trial|onboarding",
  "total_emails": number,
  "estimated_conversion_lift": "percentage range e.g. '15-25%'",
  "emails": [
    {
      "email_number": number,
      "send_timing": "immediately|1 hour later|Day 2|Day 5|...",
      "purpose": "one sentence: what this email is designed to do",
      "subject_line": {
        "primary": "main subject line",
        "ab_variants": ["variant B","variant C"],
        "character_count": number,
        "open_trigger": "curiosity|benefit|urgency|social_proof|personalization|question"
      },
      "preview_text": "under 90 chars — complements not repeats subject",
      "from_name": "suggested sender name",
      "body": {
        "opening_line": "first line — hooks after the open",
        "main_content": "full email body — conversational, scannable, focused",
        "cta_text": "button or link text",
        "cta_url_placeholder": "[LINK]",
        "ps_line": "optional P.S. line or null"
      },
      "design_notes": "layout and visual suggestions",
      "personalization_tokens": ["{{first_name}}","{{product_name}}","..."],
      "segment_conditions": "who should receive this email (if conditional)",
      "goal_metric": "open_rate|click_rate|conversion|reply"
    }
  ],
  "sequence_strategy": "paragraph explaining the psychological arc across all emails",
  "a_b_test_recommendations": [
    {"email_number":number,"element":"subject|cta|timing","test":"what to test"}
  ],
  "suppression_rules": ["remove from sequence if X happens"],
  "success_benchmarks": {
    "open_rate_target": "string",
    "click_rate_target": "string",
    "conversion_rate_target": "string"
  }
}"""

def write_sequence(
    product: str,
    sequence_type: str = "welcome",
    audience: str = "",
    tone: str = "friendly",
    email_count: int = 5,
    brand_name: str = "",
    value_prop: str = ""
) -> dict:
    client = anthropic.Anthropic()
    context_parts = [
        f"Product/Service: {product}",
        f"Sequence type: {sequence_type}",
        f"Number of emails: {email_count}",
        f"Target audience: {audience}" if audience else "",
        f"Brand name: {brand_name}" if brand_name else "",
        f"Key value prop: {value_prop}" if value_prop else "",
        f"Tone: {tone}",
    ]
    context = "\n".join(p for p in context_parts if p)
    resp = client.messages.create(
        model="claude-sonnet-4-20250514", max_tokens=4096, system=SYSTEM,
        messages=[{"role":"user","content":f"Write email sequence:\n\n{context}"}]
    )
    raw = re.sub(r'^```(?:json)?\s*','',resp.content[0].text.strip(),flags=re.MULTILINE)
    raw = re.sub(r'\s*```$','',raw,flags=re.MULTILINE)
    return json.loads(raw)

def print_sequence(r: dict):
    emails = r.get("emails",[])
    benchmarks = r.get("success_benchmarks",{})
    print(f"\n{'═'*60}")
    print(f"  EMAIL SEQUENCE — {r.get('sequence_name','')}")
    print(f"  Type: {r.get('sequence_type','?')} | {len(emails)} emails")
    print(f"  Est. conversion lift: {r.get('estimated_conversion_lift','?')}")
    print(f"{'═'*60}")
    print(f"\n  Strategy: {r.get('sequence_strategy','')[:200]}")

    for email in emails:
        sl = email.get("subject_line",{})
        body = email.get("body",{})
        print(f"\n{'─'*60}")
        print(f"  Email {email.get('email_number','?')} — {email.get('send_timing','?')}")
        print(f"  Purpose: {email.get('purpose','')}")
        print(f"  Subject: {sl.get('primary','')}")
        if sl.get("ab_variants"): print(f"  A/B: {sl['ab_variants'][0][:60]}")
        print(f"  Preview: {email.get('preview_text','')}")
        print(f"\n  \"{body.get('opening_line','')}\"")
        print(f"  {body.get('main_content','')[:200]}...")
        print(f"\n  [CTA: {body.get('cta_text','')}]")
        if body.get("ps_line"): print(f"  P.S. {body['ps_line'][:80]}")
        print(f"  Goal: {email.get('goal_metric','?')}")

    if benchmarks:
        print(f"\n  BENCHMARKS")
        print(f"  Open: {benchmarks.get('open_rate_target','?')} | Click: {benchmarks.get('click_rate_target','?')} | Conversion: {benchmarks.get('conversion_rate_target','?')}")

    ab = r.get("a_b_test_recommendations",[])
    if ab:
        print(f"\n  A/B TEST OPPORTUNITIES")
        for t in ab[:3]: print(f"  Email {t.get('email_number','?')} — {t.get('element','?')}: {t.get('test','')}")
    print(f"{'═'*60}\n")

if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser(description="Generate complete email drip sequence")
    p.add_argument("product", help="Product or service description")
    p.add_argument("--type","-t",default="welcome",choices=["welcome","abandoned_cart","post_purchase","win_back","nurture","launch","trial","onboarding"])
    p.add_argument("--count","-n",type=int,default=5,help="Number of emails")
    p.add_argument("--audience","-a",default="")
    p.add_argument("--brand","-b",default="")
    p.add_argument("--tone",default="friendly")
    p.add_argument("--value-prop","-v",default="")
    p.add_argument("--json",action="store_true")
    a = p.parse_args()
    r = write_sequence(a.product, a.type, a.audience, a.tone, a.count, a.brand, a.value_prop)
    if a.json: print(json.dumps(r,indent=2,ensure_ascii=False))
    else: print_sequence(r)
