"""
Agent 2 — Financial Analyst
Analyzes revenue impact, cost estimates, ROI, and financial projections.
"""

import os
import json
import re
from anthropic import Anthropic


SYSTEM_PROMPT = """You are a Senior Financial Analyst at a top-tier consulting firm.

Using the market research provided, produce a financial analysis. Structure your output EXACTLY as follows:

**FINANCIAL OVERVIEW**
[2-3 sentences summarizing the financial opportunity]

**STRATEGY ROI TABLE**
JSON_START
[
  {"strategy": "Strategy Name", "cost_k": 40, "revenue_gain_k": 150, "roi_pct": 275, "timeline_months": 6},
  {"strategy": "Strategy Name", "cost_k": 25, "revenue_gain_k": 100, "roi_pct": 300, "timeline_months": 4},
  {"strategy": "Strategy Name", "cost_k": 60, "revenue_gain_k": 200, "roi_pct": 233, "timeline_months": 9},
  {"strategy": "Strategy Name", "cost_k": 15, "revenue_gain_k": 80, "roi_pct": 433, "timeline_months": 3}
]
JSON_END

**KEY FINANCIAL METRICS**
METRICS_START
total_revenue_gain: $450K
total_investment: $140K
blended_roi: 221%
payback_months: 7
METRICS_END

**RISK FACTORS**
• [2-3 financial risks with mitigation notes]

Rules:
- cost_k and revenue_gain_k are in thousands of USD
- ROI = ((revenue_gain - cost) / cost) * 100
- Strategies must be specific to the industry and problem
- Use realistic numbers based on industry benchmarks"""


class FinancialAgent:
    def __init__(self):
        self.client = Anthropic()
        self.name = "Financial Analyst"

    def analyze(self, context: dict, market_insights: str) -> dict:
        """Run financial analysis using market research as input."""
        user_message = (
            f"Industry: {context['industry']}\n"
            f"Business Challenge: {context['problem']}\n"
            f"Budget: {context['budget']}\n"
            f"Timeline: {context['timeline']}\n\n"
            f"MARKET RESEARCH FINDINGS:\n{market_insights}\n\n"
            "Provide financial analysis with ROI projections for specific strategies."
        )

        message = self.client.messages.create(
            model="claude-opus-4-5",
            max_tokens=1000,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_message}],
        )

        raw_text = message.content[0].text
        strategies = self._extract_strategies(raw_text)
        metrics    = self._extract_metrics(raw_text)
        html_output = self._format_html(raw_text, strategies)

        return {
            "raw":        raw_text,
            "html":       html_output,
            "strategies": strategies,
            "metrics":    metrics,
        }

    def _extract_strategies(self, text: str) -> list:
        """Extract JSON strategy table from response."""
        try:
            match = re.search(r"JSON_START\s*(.*?)\s*JSON_END", text, re.DOTALL)
            if match:
                return json.loads(match.group(1))
        except Exception:
            pass
        # Fallback sample data
        return [
            {"strategy": "Dynamic Pricing",    "cost_k": 40,  "revenue_gain_k": 150, "roi_pct": 275, "timeline_months": 6},
            {"strategy": "AI Marketing",        "cost_k": 25,  "revenue_gain_k": 100, "roi_pct": 300, "timeline_months": 4},
            {"strategy": "Loyalty Program",     "cost_k": 60,  "revenue_gain_k": 200, "roi_pct": 233, "timeline_months": 9},
            {"strategy": "Mobile UX Overhaul",  "cost_k": 15,  "revenue_gain_k": 80,  "roi_pct": 433, "timeline_months": 3},
        ]

    def _extract_metrics(self, text: str) -> dict:
        """Extract summary metrics from METRICS_START/END block."""
        metrics = {}
        try:
            match = re.search(r"METRICS_START\s*(.*?)\s*METRICS_END", text, re.DOTALL)
            if match:
                for line in match.group(1).strip().split("\n"):
                    if ":" in line:
                        key, val = line.split(":", 1)
                        metrics[key.strip()] = val.strip()
        except Exception:
            pass
        return metrics

    def _format_html(self, text: str, strategies: list) -> str:
        """Format financial output as HTML including a strategy table."""
        parts = []

        # Overview paragraph
        overview_match = re.search(
            r"\*\*FINANCIAL OVERVIEW\*\*\s*(.*?)(?=\*\*STRATEGY|JSON_START|$)",
            text, re.DOTALL
        )
        if overview_match:
            overview = overview_match.group(1).strip()
            parts.append(
                f"<p style='color:#c8c8e0;font-size:13px;line-height:1.7;margin-bottom:12px'>{overview}</p>"
            )

        # Strategy table
        if strategies:
            parts.append(
                "<p style='color:#e8d5a3;font-size:12px;font-weight:600;"
                "text-transform:uppercase;letter-spacing:0.07em;margin:12px 0 6px 0'>"
                "STRATEGY ROI BREAKDOWN</p>"
            )
            table = (
                "<table style='width:100%;border-collapse:collapse;font-size:12px'>"
                "<tr>"
                "<th style='text-align:left;padding:6px 8px;color:#7a7a9a;border-bottom:1px solid #2a2a3d'>Strategy</th>"
                "<th style='text-align:right;padding:6px 8px;color:#7a7a9a;border-bottom:1px solid #2a2a3d'>Cost</th>"
                "<th style='text-align:right;padding:6px 8px;color:#7a7a9a;border-bottom:1px solid #2a2a3d'>Revenue</th>"
                "<th style='text-align:right;padding:6px 8px;color:#7a7a9a;border-bottom:1px solid #2a2a3d'>ROI</th>"
                "</tr>"
            )
            for s in strategies:
                table += (
                    f"<tr>"
                    f"<td style='padding:5px 8px;color:#c8c8e0;border-bottom:1px solid #1e1e30'>{s['strategy']}</td>"
                    f"<td style='padding:5px 8px;text-align:right;color:#ef9f27;border-bottom:1px solid #1e1e30'>${s['cost_k']}K</td>"
                    f"<td style='padding:5px 8px;text-align:right;color:#639922;border-bottom:1px solid #1e1e30'>${s['revenue_gain_k']}K</td>"
                    f"<td style='padding:5px 8px;text-align:right;color:#e8d5a3;border-bottom:1px solid #1e1e30'>{s['roi_pct']}%</td>"
                    f"</tr>"
                )
            table += "</table>"
            parts.append(table)

        # Risk factors
        risk_match = re.search(r"\*\*RISK FACTORS\*\*(.*?)$", text, re.DOTALL)
        if risk_match:
            parts.append(
                "<p style='color:#e8d5a3;font-size:12px;font-weight:600;"
                "text-transform:uppercase;letter-spacing:0.07em;margin:12px 0 4px 0'>RISK FACTORS</p>"
            )
            for line in risk_match.group(1).strip().split("\n"):
                line = line.strip()
                if line.startswith("•"):
                    parts.append(
                        f"<p style='color:#c8c8e0;font-size:12px;margin:3px 0 3px 8px'>· {line[1:].strip()}</p>"
                    )

        return "\n".join(parts)
