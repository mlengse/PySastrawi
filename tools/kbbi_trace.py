import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.Stemmer.Context.Context import Context

WORDS = ["memakani", "menanya", "menumbuhkembangkan", "pejalan", "penanya", "selari", "tetumbuhan"]


def trace(word):
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()
    dictionary = stemmer.delegated_stemmer.get_dictionary()

    visitor_provider = stemmer.delegated_stemmer.visitor_provider
    context = Context(word, dictionary, visitor_provider)
    context.execute()

    print(f"=== {word} -> {context.result}")
    for removal in context.get_removals():
        visitor = removal.get_visitor()
        print(
            f"  {type(visitor).__name__:45s} "
            f"subject={removal.get_subject():20s} "
            f"removed={removal.get_removed_part():8s} "
            f"type={removal.get_affix_type()} "
            f"result={removal.get_result()}"
        )
    print(f"  final: current_word={context.current_word!r}, in_dict={dictionary.contains(context.current_word)}")


if __name__ == "__main__":
    for w in WORDS:
        trace(w)
        print()
