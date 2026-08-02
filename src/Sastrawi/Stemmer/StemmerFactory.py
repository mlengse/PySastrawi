import os
from Sastrawi.Dictionary.ArrayDictionary import ArrayDictionary
from Sastrawi.Stemmer.Stemmer import Stemmer
from Sastrawi.Stemmer.CachedStemmer import CachedStemmer
from Sastrawi.Stemmer.Cache.ArrayCache import ArrayCache

__all__ = ['StemmerFactory']

class StemmerFactory:
    """ Stemmer factory helps creating pre-configured stemmer """

    def create_stemmer(self):
        """ Returns Stemmer instance """

        words = self.get_words()
        dictionary = ArrayDictionary(words)
        stemmer = Stemmer(dictionary)

        result_cache = ArrayCache()
        cached_stemmer = CachedStemmer(result_cache, stemmer)

        return cached_stemmer

    def get_words(self):
        return self.get_words_from_file()

    def get_words_from_file(self):
        current_dir = os.path.dirname(os.path.realpath(__file__))
        dictionary_file = os.path.join(current_dir, 'data', 'kata-dasar.txt')
        if not os.path.isfile(dictionary_file):
            raise RuntimeError('Dictionary file is missing. It seems that your installation is corrupted.')

        dictionary_content = ''
        with open(dictionary_file, 'r', encoding='utf-8') as f:
            dictionary_content = f.read()

        return dictionary_content.split('\n')