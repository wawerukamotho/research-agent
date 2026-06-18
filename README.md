# Deep Research Agent

A complete production-ready Deep Research Agent built with a multi-agent architecture.

## Project Structure

- `src/orchestrator/`: Central execution engine for research workflows.
- `src/tools/`: Domain-specific tools (Search, Fetch, Analyze, Write).
- `src/subagents/`: Specialized autonomous subagents.
- `src/registry/`: Model-driven tool registry.
- `src/context/`: Context and state management.
- `src/scaffold/`: Base platform scaffolding (DI, Config, Logging).
- `frontend/`: Next.js 15 App Router frontend.
- `eval/`: Evaluation harness and benchmarks.
- `tests/`: Comprehensive test suite.

## Tech Stack

- **Backend**: Python 3.12, FastAPI, SQLModel, LiteLLM.
- **Frontend**: Next.js 15, TypeScript, Tailwind, shadcn/ui.
- **Data**: PostgreSQL, Redis.
- **Observability**: OpenTelemetry, Prometheus, Jaeger.
- **Infrastructure**: Docker, Docker Compose.
