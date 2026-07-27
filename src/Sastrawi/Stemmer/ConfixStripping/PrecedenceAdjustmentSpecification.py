import re

class PrecedenceAdjustmentSpecification:
    """Confix Stripping Rule Precedence Adjustment Specification.
    Asian J. (2007) "Effective Techniques for Indonesian Text Retrieval" page 78-79.

    @link   http://researchbank.rmit.edu.au/eserv/rmit:6312/Asian.pdf
    """

    _rules = [
        re.compile(r'^be(.*)lah$'),
        re.compile(r'^be(.*)an$'),
        re.compile(r'^me(.*)i$'),
        re.compile(r'^di(.*)i$'),
        re.compile(r'^pe(.*)i$'),
        re.compile(r'^ter(.*)i$'),
    ]

    def is_satisfied_by(self, value):
        return any(rule.match(value) for rule in self._rules)
