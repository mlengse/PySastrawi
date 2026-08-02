import json
import os
import re
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

DATASET_PATH = os.path.join(
    os.path.dirname(__file__),
    "..", "..", "..", "data", "kbbi-harvester-cdn", "lexicon", "derived_to_root.json"
)

def clean_root(root_word):
    if not root_word:
        return ""
    return re.sub(r'[\u00B2\u00B3\u00B9\u2070-\u2079\s]', '', root_word).lower()

def run_benchmark():
    abs_dataset_path = os.path.abspath(DATASET_PATH)
    print(f"Loading dataset from: {abs_dataset_path}")
    with open(abs_dataset_path, "r", encoding="utf-8") as f:
        raw_data = json.load(f)

    test_cases = []
    for word, raw_root in raw_data.items():
        clean_w = word.strip().lower()
        clean_r = clean_root(raw_root)
        if " " not in clean_w and clean_w != clean_r and len(clean_w) > 0 and len(clean_r) > 0:
            test_cases.append({"word": clean_w, "expected": clean_r, "original": word})

    print(f"Total single-token test cases: {len(test_cases)}")

    print("\n--- Running PySastrawi benchmark ---")
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()

    # Warmup
    for _ in range(100):
        stemmer.stem("mempertanyakan")

    t_start = time.perf_counter()
    correct = 0
    failures = []

    for tc in test_cases:
        actual = stemmer.stem(tc["word"]).lower()
        if actual == tc["expected"]:
            correct += 1
        else:
            failures.append({"word": tc["word"], "expected": tc["expected"], "actual": actual})

    t_end = time.perf_counter()
    elapsed_sec = t_end - t_start
    elapsed_ms = elapsed_sec * 1000
    ops_per_sec = len(test_cases) / elapsed_sec if elapsed_sec > 0 else 0
    accuracy = (correct / len(test_cases)) * 100 if test_cases else 0

    print(f"PySastrawi completed in {elapsed_sec:.3f}s")
    print(f"Accuracy: {correct}/{len(test_cases)} ({accuracy:.2f}%)")
    print(f"Throughput: {ops_per_sec:.0f} words/sec")

    # Error categorization
    cat_reduplication = 0
    cat_unchanged = 0
    cat_other = 0

    for f in failures:
        if "-" in f["word"]:
            cat_reduplication += 1
        elif f["actual"] == f["word"]:
            cat_unchanged += 1
        else:
            cat_other += 1

    results = {
        "totalTestCases": len(test_cases),
        "pysastrawi": {
            "name": "PySastrawi",
            "language": "Python 3",
            "correct": correct,
            "total": len(test_cases),
            "accuracyPct": round(accuracy, 2),
            "timeSeconds": round(elapsed_sec, 4),
            "timeMs": round(elapsed_ms, 2),
            "wordsPerSec": round(ops_per_sec, 2),
            "avgLatencyUs": round((elapsed_ms * 1000) / len(test_cases), 2) if test_cases else 0,
            "errorCategories": {
                "reduplication": cat_reduplication,
                "unchanged": cat_unchanged,
                "other": cat_other
            },
            "sampleFailures": failures[:20]
        }
    }

    out_path = os.path.join(os.path.dirname(__file__), "pysastrawi_results.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print(f"\nPySastrawi benchmark results written to {out_path}")

if __name__ == "__main__":
    run_benchmark()
