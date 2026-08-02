import os

from Sastrawi.Dictionary.ArrayDictionary import ArrayDictionary
from Sastrawi.StopWordRemover.StopWordRemover import StopWordRemover

__all__ = ['StopWordRemoverFactory']

class StopWordRemoverFactory:
    """Factory for creating a pre-configured StopWordRemover."""

    def create_stop_word_remover(self):
        stopWords = self.get_stop_words()
        dictionary = ArrayDictionary(stopWords)
        stopWordRemover = StopWordRemover(dictionary)

        return stopWordRemover

    def get_stop_words(self):
        return self.get_stop_words_from_file()

    def get_stop_words_from_file(self):
        current_dir = os.path.dirname(os.path.realpath(__file__))
        dataFile = os.path.join(current_dir, 'data', 'stop-words.txt')
        if not os.path.isfile(dataFile):
            raise RuntimeError('Stop words file is missing. It seems that your installation is corrupted.')

        with open(dataFile, 'r', encoding='utf-8') as f:
            content = f.read()

        return content.split('\n')




