import unittest

from Sastrawi.Stemmer.Context.Visitor.DontStemShortWord import DontStemShortWord
from Sastrawi.Stemmer.Context.Visitor.PrefixDisambiguator import PrefixDisambiguator
from Sastrawi.Stemmer.Context.Visitor.RemoveDerivationalSuffix import RemoveDerivationalSuffix
from Sastrawi.Stemmer.Context.Visitor.RemoveInflectionalParticle import RemoveInflectionalParticle
from Sastrawi.Stemmer.Context.Visitor.RemoveInflectionalPossessivePronoun import RemoveInflectionalPossessivePronoun
from Sastrawi.Stemmer.Context.Visitor.RemovePlainPrefix import RemovePlainPrefix
from Sastrawi.Stemmer.Context.Visitor.VisitorProvider import VisitorProvider


class TestVisitorProvider(unittest.TestCase):
    def setUp(self):
        self.provider = VisitorProvider()

    def test_visitors_are_tuples(self):
        self.assertIsInstance(self.provider.visitors, tuple)
        self.assertIsInstance(self.provider.suffix_visitors, tuple)
        self.assertIsInstance(self.provider.prefix_visitors, tuple)

    def test_get_visitors_returns_tuple(self):
        self.assertIsInstance(self.provider.get_visitors(), tuple)
        self.assertIsInstance(self.provider.get_suffix_visitors(), tuple)
        self.assertIsInstance(self.provider.get_prefix_visitors(), tuple)

    def test_lists_are_not_empty(self):
        self.assertTrue(len(self.provider.visitors) > 0)
        self.assertTrue(len(self.provider.suffix_visitors) > 0)
        self.assertTrue(len(self.provider.prefix_visitors) > 0)

    def test_first_general_visitor_is_dont_stem_short_word(self):
        self.assertIsInstance(self.provider.visitors[0], DontStemShortWord)

    def test_suffix_visitors_order(self):
        self.assertIsInstance(self.provider.suffix_visitors[0], RemoveInflectionalParticle)
        self.assertIsInstance(self.provider.suffix_visitors[1], RemoveInflectionalPossessivePronoun)
        self.assertIsInstance(self.provider.suffix_visitors[2], RemoveDerivationalSuffix)

    def test_first_prefix_visitor_is_plain_prefix(self):
        self.assertIsInstance(self.provider.prefix_visitors[0], RemovePlainPrefix)

    def test_prefix_visitors_contain_disambiguators(self):
        self.assertTrue(
            all(isinstance(v, (RemovePlainPrefix, PrefixDisambiguator))
                for v in self.provider.prefix_visitors)
        )
        self.assertGreaterEqual(
            sum(1 for v in self.provider.prefix_visitors
                if isinstance(v, PrefixDisambiguator)),
            40
        )


if __name__ == '__main__':
    unittest.main()
