"""
Scores one answer, and records the facts each criterion in criteria.md needs.

run_eval.py calls judge(question, expects, answer, results) once per question
per run. judge returns True when the answer is correct: it contains the
`expects` phrase (a spelled-out number also counts as its digits, so "week 10"
matches "week ten") and it is not a refusal.

As a side effect it appends one JSON line per call to
results/criteria_data_<AI201_EVAL_LABEL>.jsonl, which summarize.py turns into
the run log: for each question and run, whether a retrieved chunk contains the
expects phrase (criterion 1), whether the answer names a retrieved file
(criterion 2), and whether every file it names contains the phrase (criterion 5).
"""

import json
import os
import re

import config
import gate

_NUMBERS = {
    "one": "1", "two": "2", "three": "3", "four": "4", "five": "5", "six": "6",
    "seven": "7", "eight": "8", "nine": "9", "ten": "10",
}

_label = os.getenv("AI201_EVAL_LABEL", "run")
_path = config.RESULTS_DIR / f"criteria_data_{_label}.jsonl"
_started = False


def _norm(text: str) -> str:
    text = text.lower()
    for word, digit in _NUMBERS.items():
        text = re.sub(rf"\b{word}\b", digit, text)
    return re.sub(r"\s+", " ", text)


def _source_text(source: str) -> str:
    path = config.corpus_path() / source
    return path.read_text(encoding="utf-8") if path.exists() else ""


def judge(question: str, expects: str, answer: str, results) -> bool:
    global _started
    config.RESULTS_DIR.mkdir(exist_ok=True)
    if not _started:
        _path.write_text("", encoding="utf-8")
        _started = True

    want = _norm(expects)
    refused = answer.strip() == gate.REFUSAL
    cited = sorted({r.source for r in results if r.source in answer})

    row = {
        "question": question,
        "expects": expects,
        "chunk_has_answer": any(want in _norm(r.text) for r in results),
        "rank_of_answer": next(
            (i + 1 for i, r in enumerate(results) if want in _norm(r.text)), None
        ),
        "named_a_source": bool(cited),
        "sources_named": cited,
        "cited_files_contain_answer": bool(cited)
        and all(want in _norm(_source_text(s)) for s in cited),
        "answer_correct": (not refused) and want in _norm(answer),
        "refused": refused,
    }
    with _path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row) + "\n")
    return row["answer_correct"]
