# Answer key — meridian-digest fixture (do not show the tester)

Score each: Found (with correct evidence) / Partly / Missed. Grade check: was Confirmed vs Latent right?

| # | Planted issue | Where | Expected grade |
|---|---|---|---|
| 1 | AGENTS.md is never loaded: summarise.py only reads prompts/system.md, so "never invent", JSON schema, 60-word cap never reach the model | summarise.py build_prompt | Confirmed (10-20 artifact has invented content) |
| 2 | system.md contradicts AGENTS.md: markdown vs JSON, thorough vs <60 words, "use best knowledge to fill gaps" vs "never invent" | prompts/system.md, AGENTS.md | Confirmed |
| 3 | Vague JSON contract + json.loads fallback → empty digest sent as if fine | summarise.py, system.md last line | Confirmed (10-27 artifact + empty partners email) |
| 4 | Retired model ID `claude-3-opus-latest`; exception swallowed → "" → fallback; 10-27 summarise took 4 s | summarise.py MODEL, try/except | Suspected (20 Oct worked with the same ID — fixture flaw: the exception text was never kept) |
| 5 | Scanned PDFs extract 0 chars (Halden, Quarry Lane) and the model invents summaries | extract.py, 10-20 log + artifact | Confirmed |
| 6 | Text silently truncated to 12,000 chars (Northgate 48k/52k) | extract.py MAX_CHARS | Confirmed |
| 7 | Notion query not paginated — exactly 100 clients every run | fetch_reports.py active_clients | Suspected (count sits on page size; real DB count unknown) |
| 8 | LLM asked to compute total % change over ~1,280 CSV rows with "£1,250" strings | system.md + data/pricing | Latent/Suspected (3.4 unverifiable) |
| 9 | "Check the latest news online" but no web search tool in the API call → answers from memory | system.md vs summarise.py | Confirmed-ish (10-20 Halden text reads like memory) |
| 10 | Download failures swallowed (`except: pass`), non-200 bodies saved as .pdf (no raise_for_status), clients without a URL skipped silently | fetch_reports.py | Latent |
| 11 | `continue-on-error: true` on Summarise, `|| true` on curl, "Digest sent" always printed → job always green | weekly-digest.yml | Confirmed |
| 12 | n8n: continueOnFail on Slack + Gmail, alwaysOutputData on Format, no errorWorkflow, error executions not saved | n8n/digest-distribution.json | Latent (empty email Confirmed) |
| 13 | GitHub disables scheduled workflows after 60 days without repo activity: last commit 2026-09-08 → stops ~7 Nov 2026 | git log + schedule | Latent, imminent (High) |
| 14 | Cron `0 8 * * 1` is UTC, comment says 08:00 London → 09:00 during BST | weekly-digest.yml | Low |
| 15 | Unpinned: actions/checkout@main, python "3.x", unpinned pip installs | weekly-digest.yml | Low |
| 16 | No alerting/heartbeat anywhere; summarise prints "OK" regardless | summarise.py, workflow | Confirmed |
| 17 | One prompt holds all reports + 32 KB style guide + all CSVs; max_tokens=2000 for "thorough paragraph" per client (up to 100) → truncated output → invalid JSON → fallback | summarise.py | Latent (plausible cause on some runs) |
| 18 | (Token audit, if opted in) 32 KB style guide + ~1,280 CSV rows every run, no prompt caching, no usage logging | summarise.py | Suspected/estimate |

## Decoys — should NOT be reported as defects (ideally under "What's working")
- extract.py writes via .tmp + replace (atomic)
- `timeout-minutes: 30` set on the job
- Secrets passed via `secrets.*` env, nothing hardcoded

## Pass bar
- Finds ≥ 13 of 17 (excluding 18 unless the token audit was chosen), including all of 1, 3, 4, 5, 11, 13
- No decoy reported as a defect
- Report within the length budget (~150 lines), no repeated findings across axes

## Fixture notes
- Source is `tests/fixtures/meridian-digest/`. Run `tests/setup-fixture.sh` to get a fresh copy as its own git repo with one commit dated 2026-09-08, and audit that copy, never the source (it sits next to this key).
- Known flaws: the pricing CSVs are labelled 2026-W44, so they can't be the 20 Oct inputs; the 3.4% figure is unverifiable. #13 applies only if the repo is public, and is "imminent" only for runs before ~7 Nov 2026; after that, expect it reported as already past the limit.

## Results
- 2026-10-30: 17/17 found, 0 decoys, 146 lines. One over-confident grade (B5). Report: tests/results/meridian-2026-10-30.md

