#!/usr/bin/env python3
"""Fidelity comparison: original LLM course vs the YAML-rebuilt v2.

  - Original (LLM-engineering-course.html) stores the course inside a
    `<script type="__bundler/template">` tag as JS that sets `window.COURSE`.
  - v2 (llm-engineering-course-v2.html) stores it as `window.COURSE_DATA = {...}`
    injected by build.py, with "/" escaped as "\\u002F".

For each topic we compare, order-independent where shuffling applies:
  - topic title
  - number of quiz questions
  - set of answer options per quiz question (we shuffle, so order is ignored)
  - correct answer text per quiz question
  - number of flashcards
  - number of terms
  - number of mistakes

Usage:
    python3 compare-courses.py
"""

import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ORIG_HTML = HERE / "LLM-engineering-course.html"
V2_HTML = HERE / "llm-engineering-course-v2.html"


def load_original() -> dict:
    html = ORIG_HTML.read_text(encoding="utf-8")
    m = re.search(
        r'<script type="__bundler/template"[^>]*>([\s\S]*?)</script>', html
    )
    js_source = json.loads(m.group(1).strip())
    helper = (
        "const fs=require('fs');"
        "const raw=fs.readFileSync(process.argv[1],'utf8');"
        "const window={};"
        "const i=raw.indexOf('window.COURSE = {');"
        "const sub=raw.substring(i);"
        "const end=sub.indexOf('\\n};');"
        "const obj=sub.substring('window.COURSE = '.length, end+2);"
        "const COURSE=eval('('+obj+')');"
        "process.stdout.write(JSON.stringify(COURSE));"
    )
    with tempfile.NamedTemporaryFile(
        "w", suffix=".js", delete=False, encoding="utf-8"
    ) as f:
        f.write(js_source)
        src_path = f.name
    out = subprocess.run(
        ["node", "-e", helper, src_path],
        capture_output=True, text=True, check=True,
    )
    return json.loads(out.stdout)


def load_v2() -> dict:
    html = V2_HTML.read_text(encoding="utf-8")
    m = re.search(r"window\.COURSE_DATA = (\{[\s\S]*?\});", html)
    if not m:
        sys.exit("Could not find window.COURSE_DATA in v2 HTML.")
    payload = m.group(1).replace("\\u002F", "/")
    return json.loads(payload)


def topic_index(course: dict) -> dict:
    """Map topic id -> topic dict across all modules."""
    idx = {}
    for mod in course["modules"]:
        for t in mod["topics"]:
            idx[t["id"]] = t
    return idx


def quiz_correct(q: dict) -> str:
    return q["options"][q["answer"]]


def quiz_options(q: dict) -> set:
    return set(q["options"])


def main() -> int:
    orig = load_original()
    v2 = load_v2()

    o_idx = topic_index(orig)
    v_idx = topic_index(v2)

    mismatches = []
    o_ids = set(o_idx)
    v_ids = set(v_idx)

    if o_ids != v_ids:
        only_o = o_ids - v_ids
        only_v = v_ids - o_ids
        if only_o:
            mismatches.append(f"Topics missing from v2: {sorted(only_o)}")
        if only_v:
            mismatches.append(f"Extra topics in v2: {sorted(only_v)}")

    checked = 0
    for tid in sorted(o_ids & v_ids):
        ot, vt = o_idx[tid], v_idx[tid]
        checked += 1

        if ot["title"] != vt["title"]:
            mismatches.append(
                f"[{tid}] title: {ot['title']!r} != {vt['title']!r}"
            )

        oq, vq = ot.get("quiz", []), vt.get("quiz", [])
        if len(oq) != len(vq):
            mismatches.append(
                f"[{tid}] quiz count: {len(oq)} != {len(vq)}"
            )
        else:
            for i, (a, b) in enumerate(zip(oq, vq)):
                if a["q"] != b["q"]:
                    mismatches.append(f"[{tid}] quiz#{i} question text differs")
                if quiz_options(a) != quiz_options(b):
                    mismatches.append(
                        f"[{tid}] quiz#{i} option set differs\n"
                        f"    orig: {sorted(quiz_options(a))}\n"
                        f"    v2:   {sorted(quiz_options(b))}"
                    )
                if quiz_correct(a) != quiz_correct(b):
                    mismatches.append(
                        f"[{tid}] quiz#{i} correct answer: "
                        f"{quiz_correct(a)!r} != {quiz_correct(b)!r}"
                    )

        for field in ("cards", "terms", "mistakes"):
            no, nv = len(ot.get(field, [])), len(vt.get(field, []))
            if no != nv:
                mismatches.append(f"[{tid}] {field} count: {no} != {nv}")

    # ---- report ----
    n_topics_o = len(o_idx)
    n_topics_v = len(v_idx)
    print("=" * 60)
    print("FIDELITY COMPARISON: original vs v2")
    print("=" * 60)
    print(f"Original topics : {n_topics_o}")
    print(f"v2 topics       : {n_topics_v}")
    print(f"Topics compared : {checked}")
    print(f"Mismatches      : {len(mismatches)}")
    print("-" * 60)
    if mismatches:
        for m in mismatches:
            print("  MISMATCH:", m)
        print("-" * 60)
        print("RESULT: FAIL")
        return 1
    print("RESULT: PASS — all topics match (titles, quiz Q/options/correct,")
    print("        flashcard / term / mistake counts).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
