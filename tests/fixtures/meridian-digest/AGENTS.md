# Agent instructions

- The digest is consumed by n8n. Output must be a single JSON object: {"headline": str, "clients": [{"name": str, "summary": str}], "pricing_total_change_pct": number}.
- Keep each client summary under 60 words.
- Never invent figures. If a report is missing, say "no report this week".
