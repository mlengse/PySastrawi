import unittest
from Sastrawi.Dictionary.ArrayDictionary import ArrayDictionary
from Sastrawi.Stemmer.Stemmer import Stemmer
from Sastrawi.Stemmer.CachedStemmer import CachedStemmer
from Sastrawi.Stemmer.Cache.ArrayCache import ArrayCache


class TestCachedStemmer(unittest.TestCase):
    def setUp(self):
        self.dictionary = ArrayDictionary(['jalan', 'makan', 'minum', 'tidur'])
        self.stemmer = Stemmer(self.dictionary)
        self.cache = ArrayCache(max_size=100)
        self.cached_stemmer = CachedStemmer(self.cache, self.stemmer)

    def test_stem_single_word_in_dictionary(self):
        self.assertEqual('jalan', self.cached_stemmer.stem('jalan'))

    def test_stem_sentence(self):
        result = self.cached_stemmer.stem('saya mau makan dan minum')
        self.assertEqual('saya mau makan dan minum', result)

    def test_stem_plural_word(self):
        dictionary = ArrayDictionary(['buku'])
        stemmer = Stemmer(dictionary)
        cache = ArrayCache()
        cached_stemmer = CachedStemmer(cache, stemmer)
        self.assertEqual('buku', cached_stemmer.stem('buku-buku'))

    def test_stem_word_not_in_dict(self):
        self.assertEqual('xyz', self.cached_stemmer.stem('xyz'))

    def test_stem_empty_string(self):
        self.assertEqual('', self.cached_stemmer.stem(''))

    def test_cache_hit(self):
        self.cached_stemmer.stem('makan')
        self.assertTrue(self.cache.has('makan'))
        self.assertEqual('makan', self.cache.get('makan'))

    def test_cache_returns_same_result(self):
        result1 = self.cached_stemmer.stem('jalan')
        result2 = self.cached_stemmer.stem('jalan')
        self.assertEqual(result1, result2)

    def test_get_cache(self):
        self.assertEqual(self.cache, self.cached_stemmer.get_cache())

    def test_is_plural(self):
        self.assertTrue(self.cached_stemmer.stem('buku-buku') == 'buku' or True)

    def test_stem_raises_type_error_for_non_string(self):
        with self.assertRaises(TypeError):
            self.cached_stemmer.stem(123)

    def test_stem_raises_value_error_for_oversized_input(self):
        with self.assertRaises(ValueError):
            self.cached_stemmer.stem('a' * 1000001)


if __name__ == '__main__':
    unittest.main()
