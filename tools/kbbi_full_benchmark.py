import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

DEFAULT_DATA = r"C:\Users\aknpa\dev\bahasa\data\kbbi-harvester-cdn\lexicon\derived_to_root.json"


def categorize(word, want, got, dict_words):
    wl = word.lower()
    if "-" in word:
        return "R1_reduplication"
    if wl in dict_words:
        return "D1_word_itself_in_dict"
    if got != word and got in dict_words:
        return "D2_overstem_collide"
    if got == word and want not in dict_words:
        return "D3_root_missing"
    if got == word:
        return "R2_rule_gap"
    return "M_mixed"


def main():
    data_path = os.environ.get("KBBI_DERIVED_JSON", DEFAULT_DATA)
    with open(data_path, encoding="utf-8") as f:
        derived = json.load(f)

    single = {k: v for k, v in derived.items() if " " not in k}
    multi = {k: v for k, v in derived.items() if " " in k}

    factory = StemmerFactory()
    stemmer = factory.create_stemmer()
    dict_path = os.path.join(os.path.dirname(__file__), "..", "src", "Sastrawi", "Stemmer", "data", "kata-dasar.txt")
    with open(dict_path, encoding="utf-8") as f:
        dict_words = set(w.strip().lower() for w in f)

    total = len(single)
    correct = 0
    wrong = []
    for word, want in sorted(single.items()):
        got = stemmer.stem(word)
        if got == want:
            correct += 1
        else:
            wrong.append((word, want, got))

    print(f"Dataset: {total} kata turunan single-token (KBBI; {len(multi)} multi-token dilewati)")
    print(f"Accuracy: {correct}/{total} = {correct / total * 100:.2f}%")
    print(f"Mismatches: {len(wrong)}")
    print()

    print("Kategorisasi mismatch:")
    cats = {}
    for word, want, got in wrong:
        c = categorize(word, want, got, dict_words)
        cats[c] = cats.get(c, 0) + 1
    for c, n in sorted(cats.items(), key=lambda kv: -kv[1]):
        print(f"  {c}: {n} ({n / len(wrong) * 100:.1f}%)")

    print()
    print("word\t\tKBBI root\tstemmer output")
    for word, want, got in sorted(wrong)[:60]:
        print(f"{word}\t\t{want}\t\t{got}")
    if len(wrong) > 60:
        print(f"... ({len(wrong) - 60} lagi)")


if __name__ == "__main__":
    main()
