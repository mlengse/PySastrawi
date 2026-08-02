import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from Sastrawi.Stemmer.StemmerFactory import StemmerFactory


def main():
    data_path = os.path.join(os.path.dirname(__file__), "kbbi_validation_data.json")
    with open(data_path, encoding="utf-8") as f:
        expected = json.load(f)

    factory = StemmerFactory()
    stemmer = factory.create_stemmer()

    total = len(expected)
    correct = 0
    mismatches = []
    for word, want in sorted(expected.items()):
        got = stemmer.stem(word)
        if got == want:
            correct += 1
        else:
            mismatches.append((word, want, got))

    print(f"Dataset: {total} kata turunan dari 16 kata dasar (KBBI)")
    print(f"Accuracy: {correct}/{total} = {correct / total * 100:.1f}%")
    print(f"Mismatches: {len(mismatches)}")
    print()
    print("word\t\tKBBI root\tstemmer output")
    for word, want, got in sorted(mismatches):
        print(f"{word}\t\t{want}\t\t{got}")


if __name__ == "__main__":
    main()
