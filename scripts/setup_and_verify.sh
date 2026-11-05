#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# 🛡️ AegisMed — Local Environment Verification & Setup Script
# Run: bash scripts/setup_and_verify.sh
# ─────────────────────────────────────────────────────────────────────────────
set -e

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; BLUE='\033[0;34m'; NC='\033[0m'
BOLD='\033[1m'

print_header() { echo -e "\n${BLUE}${BOLD}══════════════════════════════════════════${NC}"; echo -e "${BLUE}${BOLD}  $1${NC}"; echo -e "${BLUE}${BOLD}══════════════════════════════════════════${NC}\n"; }
print_ok()     { echo -e "${GREEN}  ✅  $1${NC}"; }
print_warn()   { echo -e "${YELLOW}  ⚠️   $1${NC}"; }
print_error()  { echo -e "${RED}  ❌  $1${NC}"; }
print_info()   { echo -e "  ℹ️   $1"; }

print_header "🏥 🛡️ AegisMed — Environment Setup & Verification"

# ─── Python Version ──────────────────────────────────────────────────────────
print_header "Step 1: Python Version Check"
PYTHON=$(command -v python3 || command -v python)
if [ -z "$PYTHON" ]; then
  print_error "Python not found. Install Python 3.10+."
  exit 1
fi
PY_VER=$($PYTHON --version 2>&1 | grep -oE '[0-9]+\.[0-9]+')
MAJOR=$(echo $PY_VER | cut -d. -f1)
MINOR=$(echo $PY_VER | cut -d. -f2)
if [ "$MAJOR" -ge 3 ] && [ "$MINOR" -ge 10 ]; then
  print_ok "Python $($PYTHON --version) detected."
else
  print_error "Python 3.10+ required. Found: $($PYTHON --version)"
  exit 1
fi

# ─── Virtual Environment ──────────────────────────────────────────────────────
print_header "Step 2: Virtual Environment"
if [ ! -d ".venv" ]; then
  print_info "Creating virtual environment…"
  $PYTHON -m venv .venv
  print_ok "Virtual environment created."
else
  print_ok "Virtual environment already exists."
fi

source .venv/bin/activate
print_ok "Virtual environment activated."

# ─── Upgrade pip ─────────────────────────────────────────────────────────────
print_header "Step 3: Upgrade pip"
pip install --upgrade pip -q
print_ok "pip upgraded."

# ─── Install Dependencies ─────────────────────────────────────────────────────
print_header "Step 4: Install Dependencies"
pip install -r requirements.txt -q
print_ok "All dependencies installed."

# ─── Key Imports ──────────────────────────────────────────────────────────────
print_header "Step 5: Verify Key Imports"
IMPORT_CHECKS=(
  "fastapi"
  "uvicorn"
  "streamlit"
  "fitz"          # PyMuPDF
  "chromadb"
  "pydantic"
  "pydantic_settings"
  "openai"
  "langchain"
  "pandas"
  "plotly"
)

ALL_OK=true
for pkg in "${IMPORT_CHECKS[@]}"; do
  if $PYTHON -c "import $pkg" 2>/dev/null; then
    print_ok "$pkg imported successfully."
  else
    print_error "$pkg import FAILED."
    ALL_OK=false
  fi
done

# Ragas (optional, may fail due to numpy compat)
if $PYTHON -c "import ragas" 2>/dev/null; then
  print_ok "ragas imported successfully."
else
  print_warn "ragas import failed (optional — heuristic fallback will be used)."
fi

if [ "$ALL_OK" = false ]; then
  print_error "Some required imports failed. Check requirements.txt and Python version."
  exit 1
fi

# ─── Directory Structure ──────────────────────────────────────────────────────
print_header "Step 6: Directory Structure"
mkdir -p data/uploads data/chroma_db data/policies
print_ok "data/ directories created."

# ─── .env file ───────────────────────────────────────────────────────────────
print_header "Step 7: Environment File"
if [ ! -f ".env" ]; then
  cp .env.example .env
  print_warn ".env created from .env.example. Set OPENAI_API_KEY if you have one."
else
  print_ok ".env file found."
fi

# ─── Seed Policies ────────────────────────────────────────────────────────────
print_header "Step 8: Seed Policy Database"
$PYTHON -c "
import sys, os
sys.path.insert(0, '.')
os.environ.setdefault('OPENAI_API_KEY', 'dummy')
from backend.seed_policies import seed_policies
seed_policies()
" && print_ok "Policy database seeded." || print_warn "Seeding failed (will retry on first backend start)."

# ─── Syntax Verification ──────────────────────────────────────────────────────
print_header "Step 9: Python Syntax Check"
FILES=(
  "backend/config.py"
  "backend/main.py"
  "backend/modules/document_intelligence.py"
  "backend/modules/policy_rag.py"
  "backend/modules/appointment_assistant.py"
  "backend/modules/evaluation_pipeline.py"
  "backend/seed_policies.py"
  "frontend/app.py"
)
for f in "${FILES[@]}"; do
  if $PYTHON -m py_compile "$f" 2>/dev/null; then
    print_ok "$f — syntax OK"
  else
    print_error "$f — syntax ERROR"
    $PYTHON -m py_compile "$f"
  fi
done

# ─── Done ─────────────────────────────────────────────────────────────────────
print_header "✨ Setup Complete!"
echo -e "${GREEN}${BOLD}🛡️ AegisMed is ready to run!${NC}"
echo ""
echo -e "  Start Backend:   ${YELLOW}source .venv/bin/activate && uvicorn backend.main:app --reload --port 8000${NC}"
echo -e "  Start Frontend:  ${YELLOW}source .venv/bin/activate && streamlit run frontend/app.py${NC}"
echo -e "  API Docs:        ${YELLOW}http://localhost:8000/docs${NC}"
echo -e "  Streamlit UI:    ${YELLOW}http://localhost:8501${NC}"
echo ""
print_info "For full LLM features, add your OpenAI API key to .env"
