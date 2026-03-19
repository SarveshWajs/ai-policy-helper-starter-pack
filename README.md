# AI Policy & Product Helper

# Local Setup Guide

1. Download and install Docker Desktop (https://www.docker.com/products/docker-desktop/).
   - Make sure virtualization is enabled in your BIOS/UEFI settings (required for Docker).
   - On Windows, enable WSL2 integration if prompted.
2. Clone this repository and navigate to the project folder.
3. Copy `.env.example` to `.env` and edit as needed for your environment.
4. Open Docker Desktop and ensure it is running.
5. In your terminal, run:
   ```bash
   docker compose up --build
   ```
6. Access the app:
   - Frontend: http://localhost:3000
   - Backend API docs: http://localhost:8000/docs
   - Qdrant UI: http://localhost:6333
7. Use the Admin panel to ingest sample docs and check metrics/health.
8. Use the Chat UI to ask questions and view citations.
9. Run backend tests:
   ```bash
   docker compose run --rm backend pytest -v --capture=no
   ```

# Architecture Summary

- Backend: FastAPI, Qdrant vector DB, supports stub and real LLMs, exposes metrics and health endpoints.
- Frontend: Next.js, chat UI, admin panel, responsive and accessible.
- Metrics: Latency and counters available via API and UI.

# Trade-offs

- Local-first for reproducibility and easy demo.
- Stub LLM for offline use; real LLM for richer answers.
- Simple chunking/citation logic for clarity.

## Setup & Architecture

- **Backend:** FastAPI app with endpoints for ingestion, Q&A, metrics, and health. Uses Qdrant for vector storage and supports both stub and real LLMs.
- **Frontend:** Next.js app with chat UI and admin panel. Responsive, accessible, and shows loading/errors.
- **Observability:** Metrics endpoint exposes latency and counters; health endpoint for status checks.

## Trade-offs

- Local-first design for easy testing and demo.
- Stub LLM ensures offline functionality; real LLM can be enabled for richer answers.
- Simple chunking and citation logic for clarity and reproducibility.

## Next Steps

- Add more advanced reranking or chunking.
- Improve accessibility (ARIA, keyboard navigation).
- Expand test coverage for frontend and backend.
- Add streaming answers and feedback logging.

## Code Changes

## Documented Code Changes

- Fixed Qdrant UUID bug for point IDs in backend/app/rag.py.
- Enabled CORS for local development in backend/app/main.py.
- Improved backend tests: added error handling, edge cases, feedback, and metrics validation in backend/app/tests/test_api.py.
- Updated backend Dockerfile to set PYTHONPATH for module resolution.
- Updated docker-compose.yml: improved healthcheck reliability, removed healthcheck for backend startup.
- Enhanced frontend: loading states, error handling, health check button in AdminPanel.tsx, citation chip expansion in Chat.tsx.
- Fixed `docker-compose.yml`: starter code passed `OPENAI_API_KEY` to the backend container instead of `OPENROUTER_API_KEY`, so the key never reached the app and it silently fell back to the stub LLM.

## OpenRouter API Key

The project uses [OpenRouter](https://openrouter.ai) to call real LLMs (default: `openai/gpt-4o-mini`).

**Getting a key:**
1. Sign up at https://openrouter.ai (free)
2. Go to **Keys** → **Create Key**
3. Copy the key and paste it into `.env`:
   ```
   OPENROUTER_API_KEY=sk-or-v1-your-key-here
   LLM_PROVIDER=openrouter
   ```

**Using a free model (no credits needed):**
```
LLM_MODEL=meta-llama/llama-3.1-8b-instruct:free
```

**Offline / no key:** Set `LLM_PROVIDER=stub` in `.env` — the deterministic stub LLM works without any key.

## Running & Testing

- Start all services:
  `docker compose up --build`
- Run backend tests:
  `docker compose run --rm backend pytest -v --capture=no`
- Use Admin panel to ingest docs and check metrics/health.
- Chat UI for Q&A with citations and chunk expansion.

