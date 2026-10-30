#!/usr/bin/env python3
"""Summarise token spend in Claude Code transcripts (read-only).

Usage: token-usage.py PATH [PATH ...] [--top N] [--json]
PATH may be a session .jsonl, a session directory (its subagents/ are included),
or a project directory (every transcript beneath it).

Claude Code writes one line per content block, repeating the same usage on each,
so requests are de-duplicated by requestId (falling back to message id).
"""
import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

WRITE_TOOLS = {"Edit", "MultiEdit", "Write", "NotebookEdit"}
USAGE_KEYS = ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens", "output_tokens")


def find_transcripts(paths):
    files = []
    for p in map(Path, paths):
        p = p.expanduser()
        if p.is_file() and p.suffix == ".jsonl":
            files.append(p)
        elif p.is_dir():
            files.extend(sorted(p.rglob("*.jsonl")))
            # a session file sits beside its session directory
            sibling = p.with_suffix(".jsonl")
            if sibling.is_file() and sibling not in files:
                files.append(sibling)
        else:
            print(f"skipping {p}: not a .jsonl file or directory", file=sys.stderr)
    return list(dict.fromkeys(files))


def result_chars(content):
    if isinstance(content, str):
        return len(content)
    if isinstance(content, list):
        return sum(len(c.get("text", "")) if isinstance(c, dict) else len(str(c)) for c in content)
    return len(json.dumps(content)) if content else 0


def summarise(files, top):
    seen = set()
    totals = Counter()
    by_model = defaultdict(Counter)
    by_agent = defaultdict(Counter)
    tool_calls = Counter()
    tool_result_chars = Counter()
    tool_names = {}
    big_results = []
    reads = Counter()
    peak = (0, None, None)
    sessions = set()
    bad_lines = 0

    for f in files:
        with open(f, encoding="utf-8", errors="replace") as fh:
            for line in fh:
                try:
                    d = json.loads(line)
                except json.JSONDecodeError:
                    bad_lines += 1
                    continue
                if d.get("sessionId"):
                    sessions.add(d["sessionId"])
                msg = d.get("message") or {}
                agent = d.get("agentId") or ("subagent:" + f.stem if d.get("isSidechain") else "main")
                content = msg.get("content") if isinstance(msg.get("content"), list) else []

                if d.get("type") == "assistant":
                    for c in content:
                        if c.get("type") == "tool_use":
                            tool_names[c.get("id")] = c.get("name")
                            tool_calls[c.get("name")] += 1
                            inp = c.get("input") or {}
                            target = inp.get("file_path") or inp.get("url")
                            if target and c.get("name") not in WRITE_TOOLS:
                                reads[(c.get("name"), target)] += 1
                    key = d.get("requestId") or msg.get("id")
                    usage = msg.get("usage")
                    if not usage or key in seen:
                        continue
                    seen.add(key)
                    u = Counter({k: usage.get(k) or 0 for k in USAGE_KEYS})
                    totals.update(u)
                    totals["requests"] += 1
                    by_model[msg.get("model", "unknown")].update(u)
                    by_agent[agent].update(u)
                    by_agent[agent]["requests"] += 1
                    ctx = u["input_tokens"] + u["cache_creation_input_tokens"] + u["cache_read_input_tokens"]
                    if ctx > peak[0]:
                        peak = (ctx, agent, d.get("timestamp"))

                elif d.get("type") == "user":
                    for c in content:
                        if c.get("type") == "tool_result":
                            name = tool_names.get(c.get("tool_use_id"), "unknown")
                            n = result_chars(c.get("content"))
                            tool_result_chars[name] += n
                            big_results.append((n, name, agent, d.get("timestamp")))

    cache_in = totals["cache_read_input_tokens"]
    all_in = cache_in + totals["cache_creation_input_tokens"] + totals["input_tokens"]
    big_results.sort(reverse=True)
    return {
        "files": len(files),
        "sessions": len(sessions),
        "unparseable_lines": bad_lines,
        "totals": dict(totals),
        "cache_hit_ratio": round(cache_in / all_in, 3) if all_in else None,
        "peak_context": {"tokens": peak[0], "agent": peak[1], "timestamp": peak[2]},
        "by_model": {k: dict(v) for k, v in by_model.items()},
        "by_agent": {k: dict(v) for k, v in sorted(by_agent.items(), key=lambda kv: -sum(kv[1][x] for x in USAGE_KEYS))},
        "tools": {
            name: {"calls": tool_calls[name], "result_chars": tool_result_chars[name], "approx_result_tokens": tool_result_chars[name] // 4}
            for name in sorted(set(tool_calls) | set(tool_result_chars), key=lambda n: -tool_result_chars[n])
        },
        "largest_tool_results": [
            {"approx_tokens": n // 4, "tool": t, "agent": a, "timestamp": ts} for n, t, a, ts in big_results[:top]
        ],
        "repeated_targets": [
            {"tool": t, "target": tgt, "times": n} for (t, tgt), n in reads.most_common() if n > 1
        ][:top],
    }


def fmt(n):
    return f"{n:,}"


def print_markdown(r):
    t = r["totals"]
    print(f"# Token usage — {r['files']} transcript file(s), {r['sessions']} session(s), {fmt(t.get('requests', 0))} API requests\n")
    if r["unparseable_lines"]:
        print(f"_Skipped {r['unparseable_lines']} unparseable line(s)._\n")
    print("| | tokens |\n|---|---:|")
    for k in USAGE_KEYS:
        print(f"| {k} | {fmt(t.get(k, 0))} |")
    ratio = r["cache_hit_ratio"]
    print(f"\nCache hit ratio: **{ratio:.1%}**" if ratio is not None else "\nCache hit ratio: n/a")
    p = r["peak_context"]
    print(f"Peak context in one request: **{fmt(p['tokens'])}** ({p['agent']}, {p['timestamp']})\n")

    print("## By model\n\n| model | input | cache write | cache read | output |\n|---|---:|---:|---:|---:|")
    for m, u in r["by_model"].items():
        print(f"| {m} | " + " | ".join(fmt(u.get(k, 0)) for k in USAGE_KEYS) + " |")

    print("\n## By agent\n\n| agent | requests | input | cache write | cache read | output |\n|---|---:|---:|---:|---:|---:|")
    for a, u in r["by_agent"].items():
        print(f"| {a} | {fmt(u.get('requests', 0))} | " + " | ".join(fmt(u.get(k, 0)) for k in USAGE_KEYS) + " |")

    print("\n## By tool (result size re-sent on later turns)\n\n| tool | calls | ≈ result tokens |\n|---|---:|---:|")
    for name, v in r["tools"].items():
        print(f"| {name} | {v['calls']} | {fmt(v['approx_result_tokens'])} |")

    print("\n## Largest tool results\n\n| ≈ tokens | tool | agent | time |\n|---:|---|---|---|")
    for x in r["largest_tool_results"]:
        print(f"| {fmt(x['approx_tokens'])} | {x['tool']} | {x['agent']} | {x['timestamp']} |")

    if r["repeated_targets"]:
        print("\n## Read/fetched more than once\n\n| times | tool | target |\n|---:|---|---|")
        for x in r["repeated_targets"]:
            print(f"| {x['times']} | {x['tool']} | `{x['target']}` |")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--top", type=int, default=10)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    files = find_transcripts(args.paths)
    if not files:
        sys.exit("no transcripts found")
    r = summarise(files, args.top)
    if args.json:
        json.dump(r, sys.stdout, indent=2)
        print()
    else:
        print_markdown(r)


if __name__ == "__main__":
    main()
