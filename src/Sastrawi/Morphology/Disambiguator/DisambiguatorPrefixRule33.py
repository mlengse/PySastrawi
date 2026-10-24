import re

class DisambiguatorPrefixRule33:
    """Disambiguate Prefix Rule 33
    Rule 33 : peCerV -> per-erV where C != {r|w|y|l|m|n}
    """

    def disambiguate(self, word):
        """Disambiguate Prefix Rule 33
        Rule 33 : peCerV -> per-erV where C != {r|w|y|l|m|n}
        """
        matches = re.match(r'^pe([bcdfghjkpqstvxz])er([aiueo])(.*)$', word)
        if matches:
            return 'er' + matches.group(2) + matches.group(3)
