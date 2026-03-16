# Strategic Intelligence Platform
### Multi-Agent AI Consulting System

A production-grade consulting simulation powered by three coordinated AI agents:
**Market Research → Financial Analysis → Strategy Synthesis**

---

## Architecture

```
consulting_platform/
├── app.py                          # Streamlit dashboard (main entry)
├── agents/
│   ├── market_research_agent.py    # Agent 1 — Industry trends & competitors
│   ├── financial_agent.py          # Agent 2 — ROI projections & cost analysis
│   └── strategy_agent.py           # Agent 3 — Executive recommendations
├── utils/
│   └── visualizations.py           # Plotly charts (ROI bar, radar, waterfall)
├── requirements.txt
└── .env.example
```

### Agent Flow

```
User Input (Industry + Problem)
        │
        ▼
┌─────────────────────┐
│  Agent 1            │  → Market Research Analyst
│  Trends, Demand,    │    Analyzes industry trends, demand patterns,
│  Competition        │    competitive landscape, market opportunity
└────────┬────────────┘
         │ raw insights
         ▼
┌─────────────────────┐
│  Agent 2            │  → Financial Analyst
│  ROI, Cost,         │    Models strategy ROI, cost estimates,
│  Revenue Impact     │    revenue projections, risk factors
└────────┬────────────┘
         │ financial data
         ▼
┌─────────────────────┐
│  Agent 3            │  → Strategy Consultant (MD level)
│  Executive          │    Synthesizes both into executive recommendation,
│  Recommendation     │    implementation roadmap, priority actions
└─────────────────────┘
         │
         ▼
   Dashboard Output
   (3 Plotly charts + metrics + full report)
```

---

## Setup

### 1. Clone / download the project

```bash
cd consulting_platform
```

### 2. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set your API key

```bash
cp .env.example .env
# Edit .env and add your Anthropic API key
```

Or export it directly:
```bash
export ANTHROPIC_API_KEY=your_key_here   # macOS/Linux
set ANTHROPIC_API_KEY=your_key_here      # Windows
```

### 5. Run the app

```bash
streamlit run app.py
```

The app opens at **http://localhost:8501**

---

## Usage

1. Select your **Industry** from the sidebar dropdown
2. Describe your **Business Problem** in the text area
3. Set **Budget range** and **Implementation timeline**
4. Click **▶ Run Full Analysis**

The three agents execute sequentially — each agent's output feeds the next.

---

## Example Business Challenges

- "How can a travel startup increase revenue by 20% in the next 12 months?"
- "What strategies should a SaaS company use to reduce churn and grow ARR?"
- "How can a hospital system implement AI to reduce operational costs?"
- "What's the best go-to-market strategy for a fintech entering Southeast Asia?"

---

## Models Used

All three agents use **claude-opus-4-5** via the Anthropic Python SDK.
Each agent has a specialized system prompt defining its role, output format, and analytical framework.

To switch models, edit the `model=` parameter in each agent's `analyze()` method.

---

## Extending the Platform

**Add a new agent:** Create a new file in `agents/`, follow the same pattern
(system prompt + `analyze()` method returning `{"raw": ..., "html": ...}`),
then wire it into `app.py`.

**Add more charts:** Add functions to `utils/visualizations.py` using Plotly,
then call them from `app.py` after the financial analysis step.

**Export to PDF:** Use `pdfkit` or `reportlab` to save the final recommendation.

**Add memory / history:** Store past analyses in a SQLite database using `sqlite3`
or `pandas` + CSV export.

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| UI | Streamlit |
| AI Agents | Anthropic claude-opus-4-5 |
| Charts | Plotly |
| Data | Pandas |
| Language | Python 3.10+ |
