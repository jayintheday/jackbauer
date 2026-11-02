<p align="center">
  <img src="assets/rw-banners-jackbauer.webp" alt="/jackbauer: a skill to interrogate and optimise multi-step agent workflows" width="1200">
</p>

# /jackbauer

**Find what your agent workflows get wrong without telling you.**

A skill for Claude Code that interrogates your second brain, personal OS, cron jobs or multi-step agent pipeline for **silent failures**: wrong or missing output that nobody notices until they rely on it.

- Rules in `CLAUDE.md`, `AGENTS.md`, skills and prompts that quietly contradict each other, or don't load at all when the job runs unattended
- PDFs, CSVs and RAG lookups that drop data while the model answers fluently anyway
- Web search or tools blocked in headless runs, so the agent answers from memory
- Cron/launchd jobs with swallowed errors, no alerts, daily caps, backlogs that keep growing
- Context bloat, compaction, and sub-agent handoffs that lose instructions
- **Optional:** where your tokens go and how to spend fewer

It reads your configuration **and run history** (logs, transcripts, queue state) but never runs the workflow. Every finding is backed by evidence and graded *Confirmed*, *Latent* or *Suspected*.

## Install

### Claude Code

```bash
claude plugin install jackbauer --marketplace jayintheday/jackbauer
```

Or inside a session: `/plugin install jackbauer --marketplace jayintheday/jackbauer`. Updates arrive when the plugin version changes.

### Other agents (Codex, Cursor, Gemini CLI…), manual updates

```bash
npx skills add jayintheday/jackbauer
```

Copies the skill into your project via [skills.sh](https://skills.sh). Update with `npx skills update`.

### From a clone

```bash
git clone https://github.com/jayintheday/jackbauer.git
ln -s "$PWD/jackbauer/skills/jackbauer" ~/.claude/skills/jackbauer
```

## Use

Type `/jackbauer`, or ask in plain words: *"audit my cron agent jobs for silent failures"*. (If you have a very large number of skills installed, Claude Code trims skill descriptions and the skill is then reachable only by name.)

Works on any stack: Claude Code routines, `claude -p`, cron/launchd/systemd, GitHub Actions, n8n/Make/Zapier, Python scripts, Hermes/OpenClaw and other agent frameworks. Needs a harness with sub-agents and file access.

## What you get

From the [sample report](tests/results/meridian-2026-10-30.md) on the test fixture:

> **Verdict.** No. The last two digests were wrong and the pipeline reported success both times. On 20 Oct partners got invented summaries for two clients whose PDFs had no extractable text. […] On 27 Oct the Claude call failed in 4 seconds, the script swallowed the error, and partners got an email whose whole body was "Weekly digest". The job still said "Job succeeded".

| # | Fix | Findings | Severity | Effort |
|---|---|---|---|---|
| 1 | Summarise: log exception, `usage` and `stop_reason`; exit non-zero; delete the fallback digest and `continue-on-error` | C1, C3 | Critical | 20 min |
| 2 | Pin a current model ID and smoke-test it | C2 | Critical | 5 min |
| 3 | Rewrite `system.md`: delete "fill the gap" and "check news online", embed the JSON schema | A1–A4 | Critical | 30 min |
| 4 | Compute the pricing % in Python and give the model only the number | B5, D2, E | Critical | 30 min |

## How it runs

1. **Intake.** Asks how the workflow is triggered, where it lives, what it should produce, and whether you want the token audit.
2. **Case file.** Maps the pipeline step by step, including the full set of instructions each step actually sees at run time. You confirm the map.
3. **Interrogation.** Parallel sub-agents, one per axis: instruction conflicts · retrieval & tools · orchestration & reliability · context management · (tokens).
4. **Verify.** Re-checks the evidence behind every high-severity finding and downgrades over-confident grades.
5. **Debrief.** Writes `jackbauer-report-YYYY-MM-DD.md` in the workflow's folder.
6. **Fixes.** Applies them one at a time, with your approval for each.

## Files

| File | Purpose |
|---|---|
| `skills/jackbauer/SKILL.md` | The process |
| `skills/jackbauer/failures/*.md` | Failure catalogue, one file per axis; each sub-agent reads only its own |
| `skills/jackbauer/TOKEN-AUDIT.md` | Optional token-efficiency method |
| `skills/jackbauer/REPORT-FORMAT.md` | Severity rubric, length budget and report template |
| `skills/jackbauer/scripts/token-usage.py` | Read-only token breakdown of Claude Code transcripts |
| `tests/` | Fixture with 17 planted failures, answer key and past results; see [tests/README.md](tests/README.md) |

```bash
python3 skills/jackbauer/scripts/token-usage.py ~/.claude/projects/<project>/<session>.jsonl
```

The script de-duplicates by request ID. Claude Code repeats the usage numbers on every content block of a response, so naive sums overcount.

## License

[MIT](LICENSE)
