#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# 🛡️ AegisMed — Start both backend and frontend in parallel
# Usage: bash scripts/run_all.sh
# ─────────────────────────────────────────────────────────────────────────────
set -e

# Activate venv if it exists
if [ -d ".venv" ]; then
  source .venv/bin/activate
fi

echo "🏥 Starting 🛡️ AegisMed..."
echo ""
echo "  📡 Backend (FastAPI) → http://localhost:8000"
echo "  🖥️  Frontend (Streamlit) → http://localhost:8501"
echo "  📖 API Docs → http://localhost:8000/docs"
echo ""
echo "  Press Ctrl+C to stop all services."
echo ""

# Start FastAPI in background
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!
echo "  ✅ Backend started (PID $BACKEND_PID)"

# Wait for backend to be ready
sleep 3

# Start Streamlit in background
streamlit run frontend/app.py --server.port 8501 --server.address 0.0.0.0 &
FRONTEND_PID=$!
echo "  ✅ Frontend started (PID $FRONTEND_PID)"

# Trap Ctrl+C to kill both
trap "echo ''; echo 'Stopping 🛡️ AegisMed...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; echo 'Stopped.'; exit 0" INT TERM

# Wait for both processes
wait $BACKEND_PID $FRONTEND_PID
