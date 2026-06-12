#!/usr/bin/env python3
"""Shuffle quiz answer positions in LLM-engineering-course.html.

The HTML uses a __bundler/template script tag containing a JSON-encoded string.
Inside the decoded string, quiz questions follow the JS literal format:
  { q: "...", options: [...], answer: N, explain: "..." }

This script decodes the template, shuffles options per question (keeping the
correct answer), updates the answer index, then re-encodes and writes back.
"""

import json
import random
import re
import sys


def randomise_quiz(html_path: str, output_path: str | None = None) -> None:
    if output_path is None:
        output_path = html_path

    with open(html_path, encoding="utf-8") as f:
        content = f.read()

    m = re.search(
        r'(<script type="__bundler/template">)(.*?)(</script>)',
        content,
        re.DOTALL,
    )
    if not m:
        raise ValueError("Could not find __bundler/template script tag")

    template_raw = m.group(2)
    template_html = json.loads(template_raw)

    count = 0

    def shuffle_question(qm: re.Match) -> str:
        nonlocal count
        options = json.loads(qm.group(2))
        answer = int(qm.group(4))
        correct = options[answer]
        random.shuffle(options)
        new_answer = options.index(correct)
        count += 1
        return qm.group(1) + json.dumps(options, ensure_ascii=False) + qm.group(3) + str(new_answer)

    modified_html = re.sub(
        r"(options: )(\[[^\]]*\])(, answer: )(\d+)",
        shuffle_question,
        template_html,
    )

    new_template_raw = json.dumps(modified_html, ensure_ascii=False)
    # Prevent </script> from prematurely closing the outer script tag.
    # The original file encoded all "/" as "/"; we only need to cover "</"
    # but encoding all "/" matches the original approach and is harmless.
    new_template_raw = new_template_raw.replace("/", "\\u002F")
    new_content = content[: m.start(2)] + new_template_raw + content[m.end(2) :]

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"Shuffled {count} questions → {output_path}")


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "learning/LLM-engineering-course.html"
    randomise_quiz(path)
