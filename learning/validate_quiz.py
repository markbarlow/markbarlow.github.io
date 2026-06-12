#!/usr/bin/env python3
"""Validate quiz randomisation between two HTML files.

Usage: python3 validate_quiz.py original.html modified.html

Checks per question:
  1. q text unchanged
  2. explain text unchanged
  3. set(options) identical
  4. options[answer] == original correct text

Then prints answer position distributions for both files.
"""

import json
import re
import sys
from collections import Counter


_Q_PATTERN = re.compile(
    r'\{ q: ("(?:[^"\\]|\\.)*"), options: (\[[^\]]*\]), answer: (\d+), explain: ("(?:[^"\\]|\\.)*") \}'
)


def extract_questions(html_path: str) -> list[dict]:
    with open(html_path, encoding="utf-8") as f:
        content = f.read()

    m = re.search(r'<script type="__bundler/template">(.*?)</script>', content, re.DOTALL)
    if not m:
        raise ValueError(f"No __bundler/template found in {html_path}")

    template_html = json.loads(m.group(1))

    questions = []
    for qm in _Q_PATTERN.finditer(template_html):
        questions.append(
            {
                "q": json.loads(qm.group(1)),
                "options": json.loads(qm.group(2)),
                "answer": int(qm.group(3)),
                "explain": json.loads(qm.group(4)),
            }
        )
    return questions


def validate(orig_path: str, modified_path: str) -> bool:
    orig_qs = extract_questions(orig_path)
    mod_qs = extract_questions(modified_path)

    if len(orig_qs) != len(mod_qs):
        print(f"ERROR: question count mismatch — {len(orig_qs)} vs {len(mod_qs)}")
        return False

    errors: list[str] = []
    for i, (orig, mod) in enumerate(zip(orig_qs, mod_qs), 1):
        if orig["q"] != mod["q"]:
            errors.append(f"Q{i}: question text changed")
        if orig["explain"] != mod["explain"]:
            errors.append(f"Q{i}: explain text changed")
        if set(orig["options"]) != set(mod["options"]):
            errors.append(f"Q{i}: options set changed — orig {orig['options']}, mod {mod['options']}")
        elif orig["options"][orig["answer"]] != mod["options"][mod["answer"]]:
            errors.append(
                f"Q{i}: correct answer mismatch — "
                f"expected '{orig['options'][orig['answer']]}', "
                f"got '{mod['options'][mod['answer']]}'"
            )

    if errors:
        for e in errors:
            print(f"ERROR: {e}")
        return False

    total = len(orig_qs)
    print(f"All {total} questions validated successfully.\n")

    def print_dist(label: str, qs: list[dict]) -> None:
        dist = Counter(q["answer"] for q in qs)
        print(f"{label} answer position distribution:")
        for pos in range(4):
            n = dist.get(pos, 0)
            print(f"  [{pos}]  {n:3d}  ({n / total * 100:.1f}%)")
        print()

    print_dist("Original", orig_qs)
    print_dist("Modified", mod_qs)
    return True


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} original.html modified.html")
        sys.exit(1)
    ok = validate(sys.argv[1], sys.argv[2])
    sys.exit(0 if ok else 1)
