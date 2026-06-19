# Production Startup Guide

This guide describes how to deploy and run the Deep Research Agent platform.

## Prerequisites

- Docker and Docker Compose
- API Keys for LLM (Anthropic/OpenAI) and Search (Serper/Tavily)

## Configuration

Create a `.env` file in the root directory:

```env
ANTHROPIC_API_KEY=your_key
OPENAI_API_KEY=your_key
SERPER_API_KEY=your_key
DATABASE_URL=postgresql+asyncpg://postgres:postgres@postgres:5432/research
REDIS_URL=redis://redis:6379/0
```

## Running the Platform

To start the entire stack (Frontend, Backend, Database, Redis, Observability):

```bash
docker compose up --build
```

### Access Points

- **Frontend**: [http://localhost:3000](http://localhost:3000)
- **Backend API**: [http://localhost:8000](http://localhost:8000)
- **API Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Prometheus**: [http://localhost:9090](http://localhost:9090)
- **Grafana**: [http://localhost:3001](http://localhost:3001)
- **Jaeger**: [http://localhost:16686](http://localhost:16686)

## Testing

Run the test suite:

```bash
pytest tests/unit
```

## Evaluation

Run the evaluation harness:

```bash
export PYTHONPATH=$PYTHONPATH:src:.
python eval/runner.py
```
