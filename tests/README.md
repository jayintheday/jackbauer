# Tests

One end-to-end fixture: **meridian-digest**, a small fictional pipeline (GitHub Actions → Python → Claude → n8n) with 17 planted silent failures and 3 decoys. Company names, people and addresses are invented.

| Path | What |
|---|---|
| `fixtures/meridian-digest/` | The pipeline, with logs and artifacts from two fake runs |
| `setup-fixture.sh` | Copies the fixture to a temp dir as its own git repo (one commit, 2026-09-08) |
| `meridian-answer-key.md` | Planted issues, expected grades, decoys and the pass bar. **Don't let the agent under test read it.** |
| `results/` | Reports from past runs, named `<fixture>-<date>.md` |

## Run it

```bash
tests/setup-fixture.sh            # prints the path of the fresh copy
```

Open Claude Code **in that printed directory** (not in this repo, so the answer key stays out of reach) and run `/jackbauer`. At intake, say it's a GitHub Actions workflow in the current folder, and answer yes to the token audit if you want to score #18.

Score the report against `meridian-answer-key.md`, save the report to `results/meridian-<date>.md`, and add a line under **Results** in the key.
