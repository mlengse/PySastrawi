import unittest
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.Stemmer.CachedStemmer import CachedStemmer

class TestStemmerFactory(unittest.TestCase):
    def setUp(self):
        self.factory = StemmerFactory()
        return super().setUp()

    def test_createStemmerReturnCachedStemmer(self):
        stemmer = self.factory.create_stemmer()
        self.assertIsNotNone(stemmer)
        self.assertIsInstance(stemmer, CachedStemmer)

    def test_fungsional(self):
        factory = StemmerFactory()
        stemmer = factory.create_stemmer()

        sentence = 'malaikat-malaikat-Nya'
        expected = 'malaikat'
        output = stemmer.stem(sentence)

        self.assertEqual(expected, output)

    def test_getWordsFromFile(self):
        factory = StemmerFactory()
        result = factory.get_words_from_file()
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)

if __name__ == '__main__':
    unittest.main()
