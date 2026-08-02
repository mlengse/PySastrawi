import re


class InvalidAffixPairSpecification:
    """Asian J. (2007) "Effective Techniques for Indonesian Text Retrieval". page 26

    @link http://researchbank.rmit.edu.au/eserv/rmit:6312/Asian.pdf
    """
    _INVALID_AFFIXES = (
        re.compile(r'^ber(.*)i$'),
        re.compile(r'^di(.*)an$'),
        re.compile(r'^ke(.*)i$'),
        re.compile(r'^ke(.*)an$'),
        re.compile(r'^me(.*)an$'),
        re.compile(r'^ter(.*)an$'),
        re.compile(r'^per(.*)an$'),
    )

    def is_satisfied_by(self, word):
        if re.match(r'^me(.*)kan$', word):
            return False

        if word == 'ketahui':
            return False

        return any(affix.match(word) for affix in self._INVALID_AFFIXES)


