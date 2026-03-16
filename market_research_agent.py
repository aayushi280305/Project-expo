import os
from anthropic import Anthropic

SYSTEM_PROMPT = """You are a Senior Market Research Analyst at a top-tier consulting firm.

Structure your response EXACTLY as follows:

**KEY INDUSTRY TRENDS**
- [3-4 specific, quantified trends with percentages or data points]

**DEMAND PATTERNS**
- [2-3 demand insights relevant to the business problem]

**COMPETITIVE LANDSCAPE**
- [3-4 competitor strategies and market positioning insights]

**MARKET OPPORTUNITY**
- [1-2 specific opportunity statements with size/scale estimates]

Be concise, specific, and data-driven. Max 250 words. Use ** for bold section titles."""


class MarketResearchAgent:
    def __init__(self):
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        self.client = Anthropic(api_key=api_key)

    def analyze(self, context: dict) -> dict:
        user_message = (
            f"Industry: {context['industry']}\n"
            f"Business Challenge: {context['problem']}\n"
            f"Budget: {context['budget']}\n"
            f"Timeline: {context['timeline']}\n\n"
            "Provide your market research analysis covering trends, demand, competition, and opportunity."
        )
        message = self.client.messages.create(
            model="claude-opus-4-5",
            max_tokens=800,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_message}],
        )
        raw = message.content[0].text
        return {"raw": raw, "html": self._to_html(raw)}

    def _to_html(self, text):
        parts = []
        for line in text.strip().split("\n"):
            line = line.strip()
            if not line:
                continue
            if line.startswith("**") and line.endswith("**"):
                parts.append(f"<p style='color:#e8d5a3;font-size:12px;font-weight:600;text-transform:uppercase;letter-spacing:0.07em;margin:12px 0 4px'>{line.strip('*')}</p>")
            elif line.startswith("•"):
                parts.append(f"<p style='color:#c8c8e0;font-size:13px;margin:3px 0 3px 8px;line-height:1.6'>· {line[1:].strip()}</p>")
            else:
                parts.append(f"<p style='color:#c8c8e0;font-size:13px;margin:4px 0;line-height:1.6'>{line}</p>")
        return "\n".join(parts)
