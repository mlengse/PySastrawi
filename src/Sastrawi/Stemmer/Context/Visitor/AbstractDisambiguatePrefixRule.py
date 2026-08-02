from Sastrawi.Stemmer.Context.Removal import Removal

class AbstractDisambiguatePrefixRule:
    """Base visitor that applies an ordered list of prefix disambiguators."""

    def __init__(self):
        self.disambiguators = []

    def visit(self, context):
        result = None

        for disambiguator in self.disambiguators:
            result = disambiguator.disambiguate(context.current_word)
            if context.dictionary.contains(result):
                break

        if result is None:
            return

        removed_part = context.current_word.replace(result, '', 1)

        removal = Removal(self, context.current_word, result, removed_part, 'DP')

        context.add_removal(removal)
        context.current_word = result

    def add_disambiguators(self, disambiguators):
        for disambiguator in disambiguators:
            self.add_disambiguator(disambiguator)

    def add_disambiguator(self, disambiguator):
        self.disambiguators.append(disambiguator)



