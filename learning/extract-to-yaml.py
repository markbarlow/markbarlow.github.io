#!/usr/bin/env python3
"""Extract the LLM Engineering course from the original bundled HTML to YAML.

The original file (LLM-engineering-course.html) embeds the whole course inside a
`<script type="__bundler/template">` tag whose body is a JSON-encoded string of
JavaScript source. That source assigns the full course to `window.COURSE`, with
every topic carrying its lesson/model/terms/mistakes/cards/quiz/recap inline.

This script:
  1. Decodes the bundler template back to JS source.
  2. Uses Node to eval `window.COURSE` and emit it as clean JSON.
  3. Converts each topic to the build.py YAML schema:
       - lesson : kept as raw HTML  (lesson_format: html)
       - model  : kept as raw HTML/text (bold preserved)
       - terms    {t,d} -> {term, def}
       - mistakes {t,d} -> {title, detail}
       - cards    {q,a} -> {q, a}
       - quiz     {q, options[], answer, explain}
                  -> {q, correct, distractors[], explain}
       - recap  : plain string
  4. Writes llm-engineering-course-content.yaml.

Usage:
    python3 extract-to-yaml.py
"""

import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
SRC_HTML = HERE / "LLM-engineering-course.html"
OUT_YAML = HERE / "llm-engineering-course-content.yaml"


def decode_bundler(html: str) -> str:
    """Return the JS source embedded in the __bundler/template script tag."""
    m = re.search(
        r'<script type="__bundler/template"[^>]*>([\s\S]*?)</script>', html
    )
    if not m:
        sys.exit("Could not find __bundler/template script tag.")
    return json.loads(m.group(1).strip())


def eval_course(js_source: str) -> dict:
    """Use Node to eval the JS source and dump window.COURSE as JSON."""
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
        capture_output=True,
        text=True,
        check=True,
    )
    return json.loads(out.stdout)


def convert_quiz(quiz: list) -> list:
    out = []
    for q in quiz or []:
        options = q["options"]
        answer = q["answer"]
        correct = options[answer]
        distractors = [o for i, o in enumerate(options) if i != answer]
        out.append(
            {
                "q": q["q"],
                "correct": correct,
                "distractors": distractors,
                "explain": q.get("explain", ""),
            }
        )
    return out


def convert_topic(t: dict) -> dict:
    topic = {"id": t["id"], "title": t["title"]}
    if t.get("lesson"):
        topic["lesson_format"] = "html"
        topic["lesson"] = t["lesson"]
    if t.get("model"):
        topic["model"] = t["model"]
    if t.get("terms"):
        topic["terms"] = [{"term": x["t"], "def": x["d"]} for x in t["terms"]]
    if t.get("mistakes"):
        topic["mistakes"] = [
            {"title": x["t"], "detail": x["d"]} for x in t["mistakes"]
        ]
    if t.get("cards"):
        topic["cards"] = [{"q": x["q"], "a": x["a"]} for x in t["cards"]]
    if t.get("quiz"):
        topic["quiz"] = convert_quiz(t["quiz"])
    if t.get("recap"):
        topic["recap"] = t["recap"]
    return topic


def convert_course(course: dict) -> dict:
    return {
        "title": course.get("title", "Course"),
        "description": course.get("description", ""),
        "modules": [
            {
                "id": m["id"],
                "title": m["title"],
                "topics": [convert_topic(t) for t in m.get("topics", [])],
            }
            for m in course.get("modules", [])
        ],
    }


# --- YAML formatting: use literal block scalars for multiline / HTML strings ---
class _LiteralStr(str):
    pass


def _literal_representer(dumper, data):
    return dumper.represent_scalar("tag:yaml.org,2002:str", str(data), style="|")


yaml.add_representer(_LiteralStr, _literal_representer)


def _markup(s: str) -> object:
    """Wrap HTML / long text so it serialises as a readable block scalar."""
    if isinstance(s, str) and ("<" in s or "\n" in s or len(s) > 80):
        return _LiteralStr(s)
    return s


def _wrap_markup(obj):
    if isinstance(obj, dict):
        return {k: _wrap_markup(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_wrap_markup(v) for v in obj]
    if isinstance(obj, str):
        return _markup(obj)
    return obj


def main() -> int:
    html = SRC_HTML.read_text(encoding="utf-8")
    js_source = decode_bundler(html)
    course = eval_course(js_source)
    converted = convert_course(course)

    with OUT_YAML.open("w", encoding="utf-8") as f:
        f.write(
            "# LLM Engineering course — extracted from LLM-engineering-course.html\n"
            "# Generated by extract-to-yaml.py. Lessons are raw HTML (lesson_format: html).\n\n"
        )
        yaml.dump(
            _wrap_markup(converted),
            f,
            allow_unicode=True,
            sort_keys=False,
            default_flow_style=False,
            width=100000,
        )

    n_mods = len(converted["modules"])
    n_topics = sum(len(m["topics"]) for m in converted["modules"])
    print(f"Wrote {OUT_YAML.name}  ({n_mods} modules, {n_topics} topics)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
