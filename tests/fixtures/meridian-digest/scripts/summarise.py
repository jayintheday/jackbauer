import json
import pathlib
import sys

import anthropic

MODEL = "claude-3-opus-latest"


def build_prompt():
    system = pathlib.Path("prompts/system.md").read_text()
    style = pathlib.Path("reference/style-guide.md").read_text()
    reports = "\n\n".join(
        f"### {p.stem}\n{p.read_text()}" for p in sorted(pathlib.Path("text").glob("*.txt"))
    )
    pricing = "\n\n".join(p.read_text() for p in sorted(pathlib.Path("data/pricing").glob("*.csv")))
    return system, f"{style}\n\n# Client reports\n{reports}\n\n# Pricing\n{pricing}"


def main():
    system, user = build_prompt()
    client = anthropic.Anthropic()
    try:
        msg = client.messages.create(
            model=MODEL,
            max_tokens=2000,
            system=system,
            messages=[{"role": "user", "content": user}],
        )
        text = msg.content[0].text
    except Exception:
        text = ""
    try:
        digest = json.loads(text)
    except json.JSONDecodeError:
        digest = {"headline": "Weekly digest", "clients": [], "pricing_total_change_pct": 0}
    json.dump(digest, sys.stdout)
    print("OK", file=sys.stderr)


if __name__ == "__main__":
    main()
