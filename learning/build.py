#!/usr/bin/env python3
"""Build a self-contained interactive course HTML from a YAML source.

Usage:
    python build.py example-course.yaml example-course.html

What it does:
  - Parses the YAML course definition.
  - Converts each topic's `lesson` markdown to HTML (tables supported).
  - Converts the human-friendly quiz format (correct + distractors) into the
    renderer's internal format (options[] + answer index), shuffling option
    positions with Fisher-Yates so the correct answer isn't always in the same
    place.
  - Injects `window.COURSE_DATA = {...}` into course-template.html.
  - Writes the finished single-file HTML.

Requires the `markdown` library (`pip install markdown`).
"""

import json
import random
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("Missing dependency: PyYAML. Install with `pip install pyyaml`.")

try:
    import markdown as md
except ImportError:
    sys.exit("Missing dependency: markdown. Install with `pip install markdown`.")


TEMPLATE_NAME = "course-template.html"
INJECT_MARKER = "window.COURSE_DATA = window.COURSE_DATA || {"


def md_to_html(text: str) -> str:
    """Convert a markdown string to HTML with table + fenced-code support."""
    if not text:
        return ""
    return md.markdown(
        text,
        extensions=["tables", "fenced_code", "sane_lists"],
    )


def fisher_yates(seq: list, rng: random.Random) -> None:
    """Shuffle a list in place using the Fisher-Yates algorithm."""
    for i in range(len(seq) - 1, 0, -1):
        j = rng.randint(0, i)
        seq[i], seq[j] = seq[j], seq[i]


def build_quiz(raw_quiz: list, rng: random.Random) -> list:
    """Convert YAML quiz entries (correct/distractors) to {q, options, answer, explain}."""
    out = []
    for q in raw_quiz or []:
        correct = q["correct"]
        options = [correct] + list(q.get("distractors", []))
        fisher_yates(options, rng)
        out.append(
            {
                "q": q["q"],
                "options": options,
                "answer": options.index(correct),
                "explain": q.get("explain", ""),
            }
        )
    return out


def build_topic(raw: dict, rng: random.Random) -> dict:
    """Transform a raw YAML topic into the renderer's topic shape."""
    topic = {"id": raw["id"], "title": raw["title"]}

    if raw.get("lesson"):
        topic["lesson"] = md_to_html(raw["lesson"])
    if raw.get("model"):
        # model is a short inline string; strip trailing whitespace from YAML folding
        topic["model"] = raw["model"].strip()
    if raw.get("terms"):
        topic["terms"] = [{"term": t["term"], "def": t["def"]} for t in raw["terms"]]
    if raw.get("mistakes"):
        topic["mistakes"] = [
            {"title": m["title"], "detail": m.get("detail", "")} for m in raw["mistakes"]
        ]
    if raw.get("cards"):
        topic["cards"] = [{"q": c["q"], "a": c["a"]} for c in raw["cards"]]
    if raw.get("quiz"):
        topic["quiz"] = build_quiz(raw["quiz"], rng)
    if raw.get("recap"):
        topic["recap"] = raw["recap"].strip()

    return topic


def build_course(data: dict, rng: random.Random) -> dict:
    """Transform the full parsed YAML into the COURSE_DATA object."""
    return {
        "title": data.get("title", "Course"),
        "description": data.get("description", ""),
        "modules": [
            {
                "id": m["id"],
                "title": m["title"],
                "topics": [build_topic(t, rng) for t in m.get("topics", [])],
            }
            for m in data.get("modules", [])
        ],
    }


def inject(template: str, course: dict) -> str:
    """Replace the template's fallback COURSE_DATA with the real course JSON."""
    payload = json.dumps(course, ensure_ascii=False, indent=2)
    # Encode "/" as "/" so an embedded "</script>" can't close the tag early
    # (same approach as randomise_quiz.py).
    payload = payload.replace("/", "\\u002F")
    js = "window.COURSE_DATA = " + payload + ";\n"

    # Find the fallback assignment and replace the whole statement up to its
    # closing "};" so we don't leave the default object behind.
    start = template.find(INJECT_MARKER)
    if start == -1:
        raise ValueError(
            f"Could not find COURSE_DATA marker in template. Expected: {INJECT_MARKER!r}"
        )
    # The fallback object ends at the first "};" after the marker.
    end = template.find("};", start)
    if end == -1:
        raise ValueError("Could not find end of fallback COURSE_DATA object.")
    end += len("};")
    return template[:start] + js.rstrip("\n") + template[end:]


def main(argv: list) -> int:
    if len(argv) != 3:
        print(f"Usage: python {Path(argv[0]).name} <course.yaml> <output.html>")
        return 1

    yaml_path = Path(argv[1])
    out_path = Path(argv[2])
    template_path = Path(__file__).resolve().parent / TEMPLATE_NAME

    with yaml_path.open(encoding="utf-8") as f:
        data = yaml.safe_load(f)

    template = template_path.read_text(encoding="utf-8")

    # Seed deterministically off the file content so rebuilds are reproducible.
    rng = random.Random(json.dumps(data, sort_keys=True, ensure_ascii=False))
    course = build_course(data, rng)

    html = inject(template, course)
    out_path.write_text(html, encoding="utf-8")

    n_modules = len(course["modules"])
    n_topics = sum(len(m["topics"]) for m in course["modules"])
    print(f"Built {out_path}  ({n_modules} modules, {n_topics} topics)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
