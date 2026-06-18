from prometheus_client import Counter, Histogram, Gauge

# Tool Metrics
TOOL_EXECUTION_COUNT = Counter(
    "tool_execution_total",
    "Total number of tool executions",
    ["tool_id", "status"]
)

TOOL_LATENCY = Histogram(
    "tool_latency_seconds",
    "Latency of tool executions",
    ["tool_id"]
)

TOOL_TOKENS_TOTAL = Counter(
    "tool_tokens_total",
    "Total tokens used by tools",
    ["tool_id", "token_type"]
)

# Subagent Metrics
SUBAGENT_RUN_COUNT = Counter(
    "subagent_run_total",
    "Total number of subagent runs",
    ["subagent_name", "status"]
)

SUBAGENT_RUNTIME = Histogram(
    "subagent_runtime_seconds",
    "Runtime of subagent execution loop",
    ["subagent_name"]
)

SUBAGENT_TOOL_CALLS = Counter(
    "subagent_tool_calls_total",
    "Total tool calls made by subagents",
    ["subagent_name", "tool_id"]
)

# System Metrics
ACTIVE_RESEARCH_SESSIONS = Gauge(
    "active_research_sessions",
    "Number of currently active research sessions"
)
