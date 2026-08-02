from Sastrawi.Stemmer.StemmerInterface import StemmerInterface
from Sastrawi.Stemmer.Filter.TextNormalizer import TextNormalizer

__all__ = ['CachedStemmer']

class CachedStemmer(StemmerInterface):
    """Decorator that caches stemming results to avoid redundant computation."""
    MAX_CHARACTER_LENGTH = 1000000

    def __init__(self, cache, delegated_stemmer):
        self.cache = cache
        self.delegated_stemmer = delegated_stemmer

    def stem(self, text):
        if not isinstance(text, str):
            raise TypeError("Text must be a string, received " + str(type(text)))

        if len(text) > self.MAX_CHARACTER_LENGTH:
            raise ValueError("Text length exceeds the maximum allowed length of " + str(self.MAX_CHARACTER_LENGTH) + " characters.")

        normalized_text = TextNormalizer.normalize_text(text)

        words = normalized_text.split(' ')
        stems = []

        for word in words:
            if self.cache.has(word):
                stems.append(self.cache.get(word))
            else:
                stem = self.delegated_stemmer.stem_word(word)
                self.cache.set(word, stem)
                stems.append(stem)

        return ' '.join(stems)
    
    def get_cache(self):
        return self.cache
