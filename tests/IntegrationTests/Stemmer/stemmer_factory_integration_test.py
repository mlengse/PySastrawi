import unittest
import os
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

class TestStemmerFactoryIntegration(unittest.TestCase):
    def test_get_words_from_file_loads_dictionary(self):
        factory = StemmerFactory()
        words = factory.get_words_from_file()

        # Verify that we got a list of words
        self.assertIsInstance(words, list)
        self.assertTrue(len(words) > 0)

        # Check for a known word
        self.assertIn('makan', words)

    def test_dictionary_loading_with_utf8(self):
        # This test ensures the file is read as UTF-8.
        # Since the original file is ASCII, this just confirms it doesn't crash.
        # Ideally we'd test with a non-ASCII file, but we shouldn't modify the source data in test.
        factory = StemmerFactory()
        words = factory.get_words_from_file()
        self.assertTrue(len(words) > 1000)

if __name__ == '__main__':
    unittest.main()
