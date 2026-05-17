# AI Bollywood Script Generator

Full-stack app that turns normal situations into absurd cinematic scripts using an LLM (OpenRouter).

Features
- Situation input textarea
- Mood selection
- Generates movie title, tagline, character cards, scenes with dialogues
- History stored in browser localStorage
- Regenerate options (backend supports regenerate requests)

Architecture
- Frontend: React + Vite + Tailwind (frontend/)
- Backend: FastAPI (backend/)

Setup
1. Backend

```bash
cd backend
python -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\.venv\Scripts\Activate.ps1  # PowerShell on Windows
pip install -r requirements.txt
cp ..\.env.example .env
# fill .env with OPENROUTER_API_KEY
python -m uvicorn app.main:app --reload --port 8000
```

If you use Command Prompt instead of PowerShell, activate the virtual environment with `.\venv\Scripts\activate.bat`.

2. Frontend

```bash
cd frontend
npm install
npm run dev
```

Environment
- See `.env.example` for backend environment variables. Set `OPENROUTER_API_KEY`.

OpenRouter
- Uses `OPENROUTER_MODEL` (recommended `google/gemma-4-31b-it:free`).

Notes
- The backend validates JSON output and retries if malformed.
- The frontend stores drama entries in `localStorage`.
