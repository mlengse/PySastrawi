import unittest
from Sastrawi.Stemmer.CachedStemmer import CachedStemmer
from Sastrawi.Stemmer.Stemmer import Stemmer
from Sastrawi.Dictionary.ArrayDictionary import ArrayDictionary
from Sastrawi.Stemmer.Cache.ArrayCache import ArrayCache

class Test_CachedStemmerValidationTest(unittest.TestCase):
    def setUp(self):
        dictionary = ArrayDictionary([])
        stemmer = Stemmer(dictionary)
        cache = ArrayCache()
        self.cached_stemmer = CachedStemmer(cache, stemmer)

    def test_StemRaisesTypeErrorOnNonStringInput(self):
        with self.assertRaises(TypeError):
            self.cached_stemmer.stem(None)

        with self.assertRaises(TypeError):
            self.cached_stemmer.stem(123)

        with self.assertRaises(TypeError):
            self.cached_stemmer.stem(['list'])

        with self.assertRaises(TypeError):
            self.cached_stemmer.stem(object())

    def test_StemAcceptsStringInput(self):
        # Should not raise
        result = self.cached_stemmer.stem("string")
        self.assertIsInstance(result, str)

if __name__ == '__main__':
    unittest.main()
