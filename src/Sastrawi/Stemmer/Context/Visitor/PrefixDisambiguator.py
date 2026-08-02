from Sastrawi.Stemmer.Context.Visitor.AbstractDisambiguatePrefixRule import AbstractDisambiguatePrefixRule

class PrefixDisambiguator(AbstractDisambiguatePrefixRule):
    """Visitor that applies a specific set of prefix disambiguation rules."""

    def __init__(self, disambiguators):
        super().__init__()

        self.add_disambiguators(disambiguators)



