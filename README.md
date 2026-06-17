# VeriLift 🔬

**Pay for verified lift, not self-reported ROAS.**

VeriLift is a settlement and verification layer for retail media networks. It independently verifies the true incremental lift of marketing campaigns using exposed vs holdout groups, and automatically adjusts the performance-linked payout based on that verification.

## Theme 02 Alignment
**AI for seamless customer experiences across channels while defining clear measures of success.**

By defining the ultimate success metric as **verified incremental lift**, VeriLift ensures that brands stop scaling campaigns that simply retarget customers who would have bought anyway. This protects brand budgets, forces media networks to improve their targeting, and ensures customers stop getting spammed with irrelevant ads—driving a truly seamless customer experience.

## Tech Stack
- **Backend/Logic:** Python 3, FastAPI, Uvicorn
- **Data & Math:** Pandas, NumPy
- **Frontend UI:** React, Vite, Tailwind CSS v4, Recharts
- **AI Insights:** Groq (via LangChain)
- **UI Generation:** Stitch MCP (Landing Page)

## Setup Instructions

1. **Clone the repository**
2. **Install Backend Requirements**
   ```bash
   pip install -r requirements.txt
   pip install fastapi uvicorn groq python-dotenv pydantic
   ```
3. **Set up your environment variables**
   Rename `.env.example` to `.env` and add your Groq API key.
   ```text
   GROQ_API_KEY=gsk_your_key_here
   ```
4. **Install Frontend Requirements**
   ```bash
   cd frontend
   npm install
   ```

## How to Run

You can run the full backend data generation and calculation pipeline to build the datasets:
```bash
python src/data_generator.py
python src/lift_calculator.py
python src/settlement_engine.py
python src/reliability_scorer.py
```

**To launch the prototype application:**

You need two terminal windows.

**Terminal 1 (Backend):**
```bash
python -m uvicorn api:app --reload --port 8000
```

**Terminal 2 (Frontend):**
```bash
cd frontend
npm run dev
```
Open `http://localhost:5173` in your browser.

## Demo Flow

1. **Overview / Landing Page:** The beautiful Stitch MCP-generated landing page explaining the core problem (self-reported metrics) and VeriLift's solution (verified lift settlement).
2. **Campaign Verification:** Select a campaign to see how VeriLift compares the network's claimed lift against the mathematically verified lift (Exposed CR vs Holdout CR).
3. **Settlement Engine:** See how the verified lift ratio determines the release of the at-risk performance pool.
4. **Reliability Leaderboard:** View the aggregated trust score of different retail media networks based on their historical accuracy.
5. **AI Insights:** Read an executive summary of the discrepancy, CX impact, and recommended contract splits powered by Groq AI.

## Folder Structure

```text
VeriLift/
│
├── api.py                     # FastAPI Backend Server
├── app.py                     # Legacy Streamlit app (optional)
├── requirements.txt           # Python dependencies
├── .env.example               # Environment variables template
├── README.md                  # Project documentation
│
├── frontend/                  # React + Vite UI App
│   ├── src/
│   │   ├── App.jsx            # Main React Dashboard
│   │   ├── LandingPage.jsx    # Generated Landing Page
│   │   └── index.css          # Tailwind configurations
│   ├── package.json
│   └── vite.config.js         # Vite + Tailwind v4 config
│
├── data/                      # Generated CSVs and calculation outputs
│   ├── raw_campaigns.csv
│   ├── lift_results.csv
│   ├── settlement_results.csv
│   └── network_reliability.csv
│
├── docs/                      # Documentation and Context
│   ├── PROJECT_CONTEXT.md
│   ├── PRD.md
│   ├── DEMO_SCRIPT.md
│   └── VERILIFT_ANTIGRAVITY_MICRO_PHASE_PLAN.md
│
└── src/                       # Core Logic Modules
    ├── data_generator.py      # Synthetic data creator
    ├── lift_calculator.py     # exposed vs holdout math
    ├── settlement_engine.py   # payout calculation logic
    ├── reliability_scorer.py  # network scoring logic
    ├── ai_insights.py         # Groq AI enhancement
    └── utils.py               # Shared helpers (e.g. safe division)
```
