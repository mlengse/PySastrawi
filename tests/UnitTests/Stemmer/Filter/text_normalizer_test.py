import unittest
from Sastrawi.Stemmer.Filter.TextNormalizer import TextNormalizer


class TestTextNormalizer(unittest.TestCase):
    def test_lowercase(self):
        self.assertEqual('abcd', TextNormalizer.normalize_text('ABCD'))
        self.assertEqual('abcd', TextNormalizer.normalize_text('AbCd'))

    def test_remove_punctuation(self):
        self.assertEqual('abc', TextNormalizer.normalize_text('abc!'))
        self.assertEqual('abc', TextNormalizer.normalize_text('abc.'))
        self.assertEqual('a b c', TextNormalizer.normalize_text('a,b,c'))
        self.assertEqual('a b c', TextNormalizer.normalize_text('a.b.c'))
        self.assertEqual('a1 b2', TextNormalizer.normalize_text('a1!b2'))
        self.assertEqual('abc', TextNormalizer.normalize_text('"abc"'))

    def test_collapse_multiple_spaces(self):
        self.assertEqual('a b', TextNormalizer.normalize_text('a   b'))
        self.assertEqual('a b', TextNormalizer.normalize_text('a    b'))
        self.assertEqual('a b c', TextNormalizer.normalize_text('a  b   c'))

    def test_newlines_and_tabs(self):
        self.assertEqual('a b', TextNormalizer.normalize_text('a\nb'))
        self.assertEqual('a b', TextNormalizer.normalize_text('a\r\nb'))
        self.assertEqual('a b', TextNormalizer.normalize_text('a\tb'))

    def test_empty_string(self):
        self.assertEqual('', TextNormalizer.normalize_text(''))

    def test_only_punctuation(self):
        self.assertEqual('', TextNormalizer.normalize_text('!@#$%'))


if __name__ == '__main__':
    unittest.main()
