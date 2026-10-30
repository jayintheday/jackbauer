# /jackbauer

Interrogates your second brain, personal OS, or multi-step agent workflow for **silent failures**: things that go wrong without anyone noticing.

- Rules in `CLAUDE.md`, `AGENTS.md`, skills and prompts that quietly contradict each other, or don't load at all when the job runs unattended
- PDFs, CSVs and RAG lookups that drop data while the model answers fluently anyway
- Web search or tools blocked in headless runs, so the agent answers from memory
- Cron/launchd jobs with swallowed errors, no alerts, daily caps, backlogs that keep growing
- Context bloat, compaction, and sub-agent handoffs that lose instructions
- **Optional:** where your tokens go and how to spend fewer

It reads your configuration **and run history** (logs, transcripts, queue state) but never runs the workflow. Each finding is backed by evidence and graded *Confirmed*, *Latent* or *Suspected*. You get a ranked report, then it offers to apply fixes one at a time with your approval.

## How it runs

1. **Intake.** Asks how the workflow is triggered, where it lives, what it should produce, and whether you want the token audit.
2. **Case file.** Maps the pipeline step by step, including the full set of instructions each step actually sees at run time. You confirm the map.
3. **Interrogation.** Parallel sub-agents, one per axis: instruction conflicts · retrieval & tools · orchestration & reliability · context management · (tokens).
4. **Verify.** Re-checks the evidence behind every high-severity finding.
5. **Debrief.** Writes `jackbauer-report-YYYY-MM-DD.md` in the workflow's folder.
6. **Fixes.** Applies them one at a time with your approval.

## Install (Claude Code)

```bash
ln -s ~/Desktop/Testrepo/jackbauer/skills/jackbauer ~/.claude/skills/jackbauer
```

Then type `/jackbauer`. Asking in plain words ("audit my cron agent jobs for silent failures") also works, unless you have a very large number of skills installed: Claude Code then trims skill descriptions from what it loads, so the skill can only be reached by name.

Needs Claude Code (it uses sub-agents and reads files). Works on any stack: Claude Code routines, cron/launchd, n8n, Python scripts, Hermes/OpenClaw and others.

## Files

| File | Purpose |
|---|---|
| `skills/jackbauer/SKILL.md` | The process |
| `skills/jackbauer/SILENT-FAILURES.md` | Failure catalogue the sub-agents work from |
| `skills/jackbauer/TOKEN-AUDIT.md` | Optional token-efficiency method |
| `skills/jackbauer/REPORT-FORMAT.md` | Severity rubric and report template |
| `skills/jackbauer/scripts/token-usage.py` | Read-only token breakdown of Claude Code transcripts |

```bash
python3 skills/jackbauer/scripts/token-usage.py ~/.claude/projects/<project>/<session>.jsonl
```

The script de-duplicates by request ID. Claude Code repeats the usage numbers on every content block of a response, so naive sums overcount.
