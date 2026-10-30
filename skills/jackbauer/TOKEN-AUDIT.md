# Token-efficiency audit (axis E)

Goal: show where tokens go in one run of the workflow, whether that spend buys quality, and what to cut.

## 1. Get real numbers

**Claude Code runs** (interactive, `claude -p`, routines): transcripts are in `~/.claude/projects/<cwd-with-dashes>/<session-id>.jsonl`, with subagents under `<session-id>/subagents/`. Pick the sessions that match recent runs (by timestamp and cwd) and run:

```bash
python3 <skill-dir>/scripts/token-usage.py <session.jsonl | session-dir | project-dir> [--top 15] [--json]
```

It reports totals, per model, per agent (main vs each subagent), per tool (call count and tool-result size), the largest tool results, files read more than once, and peak context per request. Run it on several runs and compare: one run can be unrepresentative.

**Other stacks:** look for provider usage in logs (`usage`, `input_tokens`, `prompt_tokens`), LangSmith/Langfuse/Helicone traces, or provider dashboards. If nothing records usage, estimate from prompt and input sizes (≈4 characters per token for English) and say it is an estimate. The lack of usage logging is itself a finding.

Don't quote prices from memory. If the user wants cost, look up current pricing (the `claude-api` skill, or the provider's pricing page) and show the arithmetic.

## 2. Read the numbers

- **Cache hit ratio** = cache reads ÷ (cache reads + cache writes + uncached input). Low on repeated runs means the prompt prefix changes every call (timestamps or dynamic content near the top, tool lists that reorder) or calls are spaced beyond the cache lifetime.
- **Peak context per request** near the model's window means compaction risk (axis D) and paying for the whole window every turn.
- **Tool-result share**: large tool results (whole files, full web pages, verbose CLI output) are re-sent on every later turn of that session. A 50k-token read early in a 40-turn session is paid ~40 times (cheaply if cached, but still).
- **Repeated reads** of the same file or URL in one run.
- **Model per step**: frontier models on mechanical steps (classify, extract a field, rename, format) that a small model or plain code would do.
- **Output vs thinking**: high thinking spend on routine steps, or long outputs nobody reads.

## 3. Recommend

Rank cuts by tokens saved × risk to quality, and say what each might cost in quality. Typical levers:

- Move deterministic work (parsing, counting, filtering, dedupe, formatting) from LLM to code.
- Smaller model for mechanical steps; keep the strong model where judgement lives.
- Stable prompt prefix for caching: fixed instructions first, variable data last; no timestamps up top.
- Trim tool output at the source (`head`, `jq`, `grep`, targeted reads) instead of reading whole files.
- One fresh, small session per item instead of one ever-growing session.
- Disable MCP servers the job doesn't use; slim always-loaded instruction files.
- Process only what changed since the last run.
- Batch API for non-urgent scheduled work, where the stack supports it.

Report in the token section of the report: a table of the biggest spenders (agent/step/tool, tokens, share), the cache hit ratio, the top cuts with estimated savings, and which of them are safe.
