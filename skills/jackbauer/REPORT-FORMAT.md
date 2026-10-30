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

## Template

```markdown
# Jack Bauer report — <workflow name> — <YYYY-MM-DD>

## Verdict
<One paragraph: is this pipeline doing what the user thinks? The single most important thing to fix and why.>

## Pipeline map
1. <trigger> → <step> (<actor>, tools: …) → <output>   · evidence: <path>
2. …

## Top fixes
| # | Fix | Axis | Severity | Effort |
|---|---|---|---|---|
| 1 | … | C | Critical | 15 min |

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
