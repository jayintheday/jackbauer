# Report format

## Severity

| Severity | Meaning |
|---|---|
| **Critical** | Output is wrong or missing right now, or will be on the next run. |
| **High** | Wrong/missing output under conditions that happen regularly (sleep, a cap, an expired token, a large file). |
| **Medium** | Degraded quality or waste; output is usable but worse than the user thinks. |
| **Low** | Hygiene; raises the odds of future failure. |

## Silence

| Silence | Meaning |
|---|---|
| **Silent** | Nobody would notice until they rely on the output. |
| **Quiet** | Visible only if someone reads a log or checks a folder. |
| **Loud** | An error, alert or obvious gap reaches the user. |

Rank findings within each axis by severity, then silence (Silent first), then grade (Confirmed first).

## Length budget

The report is read by someone deciding what to fix, not by an auditor. Aim for under ~150 lines.

- **Verdict:** at most 5 sentences, ending with the one thing to fix first.
- **Top fixes:** at most 10 rows, each naming the finding IDs it resolves.
- **Each finding:** at most ~6 lines. Quote only the evidence line that proves it.
- **Low findings:** one line each, under a "Low" list at the end of the axis.
- **Same root cause on several axes:** full finding once, under the axis that owns the fix; one-line "see C1" elsewhere.
- **Unchecked leads:** at most 5, ranked by how much harm they'd do if real.
- **What's working:** at most 5 bullets.

## Template

```markdown
# Jack Bauer report — <workflow name> — <YYYY-MM-DD>

## Verdict
<One paragraph: is this pipeline doing what the user thinks? The single most important thing to fix and why.>

## Pipeline map
1. <trigger> → <step> (<actor>, tools: …) → <output>   · evidence: <path>
2. …

## Top fixes
| # | Fix | Findings | Severity | Effort |
|---|---|---|---|---|
| 1 | … | C2, A4 | Critical | 15 min |

## A. Instruction conflicts
### A1. <title> — <Severity> · <Silence> · <Confirmed|Latent|Suspected>
- **Where:** step <n>, `<file:line>`
- **Evidence:** <quote or redacted log excerpt>
- **Why it's silent:** …
- **Fix:** …  (effort: …)

## B. Retrieval & tools
## C. Orchestration & reliability
## D. Context management
## E. Token efficiency   <!-- only if opted in -->

## Unchecked leads
<Things that look risky but had no evidence either way; say what would settle each.>

## What's working
<Short: safeguards that are already in place, so the user doesn't remove them.>
```

Keep each axis's findings in its own section; don't merge or re-rank across axes. The **Top fixes** table is the only cross-axis view. Write axes with no findings as "Nothing found" plus one line on what was checked.
