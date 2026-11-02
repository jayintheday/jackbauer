# Meridian weekly digest

Every Monday morning the partners get a digest of the week's client reports and pricing moves.

1. GitHub Actions (`.github/workflows/weekly-digest.yml`) runs on a schedule.
2. `scripts/fetch_reports.py` pulls the client list from Notion and downloads each client's latest PDF report.
3. `scripts/extract.py` turns PDFs into text.
4. `scripts/summarise.py` asks Claude for the digest (prompt in `prompts/`).
5. The workflow posts the digest to an n8n webhook; n8n (`n8n/digest-distribution.json`) sends it to Slack and email.

Owner: ops@meridian.example
