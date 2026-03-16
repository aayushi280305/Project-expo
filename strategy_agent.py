import os
import re
from anthropic import Anthropic

SYSTEM_PROMPT = """You are a Managing Director and Strategy Consultant at a top-tier consulting firm.

Synthesize the market research and financial analysis provided into an executive-level strategic recommendation.

Structure your response EXACTLY as:

**EXECUTIVE SUMMARY**
[2 sentences capturing the core opportunity and recommended approach]

**STRATEGIC IMPERATIVES**
1. [First priority action — specific, actionable, with expected impact]
2. [Second priority action — specific, actionable, with expected impact]
3. [Third priority action — specific, actionable, with expected impact]
4. [Fourth priority action — specific, actionable, with expected impact]

**IMPLEMENTATION ROADMAP**
Phase 1 (Month 1-3): [Quick wins]
Phase 2 (Month 4-8): [Core initiatives]
Phase 3 (Month 9+): [Scale & optimize]

**FINANCIAL OUTLOOK**
[2-3 sentences with specific numbers: revenue gain %, ROI, payback period]

SUMMARY_METRICS
revenue_gain: [e.g. $450K-$530K]
impl_cost: [e.g. $140K]
roi: [e.g. 221%]
payback: [e.g. 7 months]
END_METRICS

Be decisive. Reference specific numbers from the financial analysis. Write at an executive level."""


class StrategyAgent:
    def __init__(self):
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        self.client = Anthropic(api_key=api_key)
        self.name = "Strategy Consultant"

    def analyze(self, context: dict, market_insights: str, financial_insights: str) -> dict:
        user_message = (
            f"Industry: {context['industry']}\n"
            f"Business Challenge: {context['problem']}\n"
            f"Budget: {context['budget']}\n"
            f"Timeline: {context['timeline']}\n\n"
            f"MARKET RESEARCH:\n{market_insights}\n\n"
            f"FINANCIAL ANALYSIS:\n{financial_insights}\n\n"
            "Synthesize both into a final executive-level strategic recommendation."
        )
        message = self.client.messages.create(
            model="claude-opus-4-5",
            max_tokens=1200,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_message}],
        )
        raw = message.content[0].text
        return {
            "raw": raw,
            "summary_html": self._summary_html(raw),
            "full_html":    self._full_html(raw),
            "metrics":      self._extract_metrics(raw),
        }

    def _extract_metrics(self, text: str) -> dict:
        metrics = {}
        try:
            match = re.search(r"SUMMARY_METRICS\s*(.*?)\s*END_METRICS", text, re.DOTALL)
            if match:
                for line in match.group(1).strip().split("\n"):
                    if ":" in line:
                        k, v = line.split(":", 1)
                        metrics[k.strip()] = v.strip()
        except Exception:
            pass
        return metrics

    def _summary_html(self, text: str) -> str:
        parts = []
        exec_match = re.search(
            r"\*\*EXECUTIVE SUMMARY\*\*\s*(.*?)(?=\*\*|$)", text, re.DOTALL
        )
        if exec_match:
            parts.append(
                f"<p style='color:#c8c8e0;font-size:13px;line-height:1.7;"
                f"margin-bottom:8px'>{exec_match.group(1).strip()}</p>"
            )
        imp_match = re.search(
            r"\*\*STRATEGIC IMPERATIVES\*\*\s*(.*?)(?=\*\*|$)", text, re.DOTALL
        )
        if imp_match:
            parts.append(
                "<p style='color:#e8d5a3;font-size:12px;font-weight:600;"
                "text-transform:uppercase;letter-spacing:0.07em;"
                "margin:8px 0 4px'>PRIORITIES</p>"
            )
            for line in imp_match.group(1).strip().split("\n"):
                line = line.strip()
                if re.match(r"^\d+\.", line):
                    parts.append(
                        f"<p style='color:#c8c8e0;font-size:12px;"
                        f"margin:3px 0 3px 4px;line-height:1.5'>"
                        f"→ {line[2:].strip()}</p>"
                    )
        return "\n".join(parts)

    def _full_html(self, text: str) -> str:
        text = re.sub(r"SUMMARY_METRICS.*?END_METRICS", "", text, flags=re.DOTALL).strip()
        parts = []
        for line in text.split("\n"):
            line = line.strip()
            if not line:
                continue
            if line.startswith("**") and line.endswith("**"):
                parts.append(
                    f"<p style='color:#e8d5a3;font-size:13px;font-weight:600;"
                    f"text-transform:uppercase;letter-spacing:0.07em;"
                    f"margin:18px 0 6px;padding-top:12px;"
                    f"border-top:1px solid #2a2a3d'>{line.strip('*')}</p>"
                )
            elif re.match(r"^\d+\.", line):
                parts.append(
                    f"<p style='color:#c8c8e0;font-size:14px;margin:6px 0;"
                    f"line-height:1.7;padding:8px 12px;background:#1e1e35;"
                    f"border-radius:6px;border-left:3px solid #e8d5a3'>{line}</p>"
                )
            elif line.startswith("Phase"):
                phase, _, rest = line.partition(":")
                parts.append(
                    f"<p style='color:#c8c8e0;font-size:13px;margin:5px 0;"
                    f"line-height:1.6'><span style='color:#ef9f27;"
                    f"font-weight:600'>{phase}:</span>{rest}</p>"
                )
            elif line.startswith("•"):
                parts.append(
                    f"<p style='color:#c8c8e0;font-size:13px;"
                    f"margin:3px 0 3px 8px;line-height:1.6'>"
                    f"· {line[1:].strip()}</p>"
                )
            else:
                parts.append(
                    f"<p style='color:#c8c8e0;font-size:14px;"
                    f"margin:5px 0;line-height:1.75'>{line}</p>"
                )
        return "\n".join(parts)
