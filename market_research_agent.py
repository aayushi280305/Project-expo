"""
Agent 1 — Market Research Analyst
Analyzes industry trends, demand patterns, and competitor strategies.
"""

import os
from anthropic import Anthropic


SYSTEM_PROMPT = """You are a Senior Market Research Analyst at a top-tier consulting firm (McKinsey/BCG level).

Your role is to provide sharp, data-driven market intelligence. Structure your response EXACTLY as follows:

**KEY INDUSTRY TRENDS**
• [3-4 specific, quantified trends with percentages or data points]

**DEMAND PATTERNS**
• [2-3 demand insights relevant to the business problem]

**COMPETITIVE LANDSCAPE**
• [3-4 competitor strategies and market positioning insights]

**MARKET OPPORTUNITY**
• [1-2 specific opportunity statements with size/scale estimates]

Be concise, specific, and data-driven. Use real industry knowledge. Max 250 words total.
Do NOT use markdown headers with #. Use ** for bold section titles."""


class MarketResearchAgent:
    def __init__(self):
        self.client = Anthropic()
        self.name = "Market Research Analyst"

    def analyze(self, context: dict) -> dict:
        """Run market research analysis and return structured results."""
        industry  = context["industry"]
        problem   = context["problem"]
        budget    = context["budget"]
        timeline  = context["timeline"]

        user_message = (
            f"Industry: {industry}\n"
            f"Business Challenge: {problem}\n"
            f"Budget: {budget}\n"
            f"Timeline: {timeline}\n\n"
            "Provide your market research analysis covering trends, demand, competition, and opportunity."
        )

        message = self.client.messages.create(
            model="claude-opus-4-5",
            max_tokens=800,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_message}],
        )

        raw_text = message.content[0].text
        html_output = self._format_html(raw_text)

        return {"raw": raw_text, "html": html_output}

    def _format_html(self, text: str) -> str:
        """Convert raw text to styled HTML for the dashboard."""
        lines = text.strip().split("\n")
        html_parts = []

        for line in lines:
            line = line.strip()
            if not line:
                continue
            if line.startswith("**") and line.endswith("**"):
                title = line.strip("*")
                html_parts.append(
                    f"<p style='color:#e8d5a3;font-size:12px;font-weight:600;"
                    f"text-transform:uppercase;letter-spacing:0.07em;"
                    f"margin:12px 0 4px 0'>{title}</p>"
                )
            elif line.startswith("•"):
                content = line[1:].strip()
                html_parts.append(
                    f"<p style='color:#c8c8e0;font-size:13px;margin:3px 0 3px 8px;"
                    f"line-height:1.6'>· {content}</p>"
                )
            else:
                html_parts.append(
                    f"<p style='color:#c8c8e0;font-size:13px;margin:4px 0;line-height:1.6'>{line}</p>"
                )

        return "\n".join(html_parts)
