import unittest
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.Stemmer.Stemmer import Stemmer
from Sastrawi.Stemmer.Cache.ArrayCache import ArrayCache

class MemoryLeakTest(unittest.TestCase):
    def test_cache_is_bounded(self):
        # Setup
        # Create a stemmer with a very small cache limit for testing

        # We need to manually construct the cached stemmer because factory doesn't expose max_size
        factory = StemmerFactory()
        words = factory.get_words()
        from Sastrawi.Dictionary.ArrayDictionary import ArrayDictionary
        dictionary = ArrayDictionary(words)
        stemmer = Stemmer(dictionary)

        from Sastrawi.Stemmer.CachedStemmer import CachedStemmer

        limit = 100
        cache = ArrayCache(max_size=limit)
        cached_stemmer = CachedStemmer(cache, stemmer)

        # Stem more unique words than the limit
        for i in range(limit + 50):
            cached_stemmer.stem("word" + str(i))

        final_size = len(cache.data)

        # Verify cache size is capped at limit
        # print("Final size: {}".format(final_size))
        self.assertEqual(final_size, limit)

        # Verify LRU behavior: "word0" should be evicted, "word149" should be present
        self.assertFalse(cache.has("word0"))
        self.assertTrue(cache.has("word" + str(limit + 49)))

if __name__ == '__main__':
    unittest.main()
