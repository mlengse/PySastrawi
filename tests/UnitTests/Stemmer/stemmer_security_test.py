import unittest
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.Stemmer.Stemmer import Stemmer

class StemmerSecurityTest(unittest.TestCase):
    def setUp(self):
        self.factory = StemmerFactory()
        self.stemmer = self.factory.create_stemmer()

    def test_large_input_raises_error(self):
        # Create a string larger than the maximum allowed length
        limit = Stemmer.MAX_CHARACTER_LENGTH
        large_text = "a" * (limit + 1)

        with self.assertRaises(ValueError):
            self.stemmer.stem(large_text)

    def test_input_within_limit_works(self):
        # Verify that a string within the limit does not raise an error
        self.stemmer.stem("test")

if __name__ == '__main__':
    unittest.main()
