import os

from Sastrawi.Dictionary.ArrayDictionary import ArrayDictionary
from Sastrawi.StopWordRemover.StopWordRemover import StopWordRemover

__all__ = ['StopWordRemoverFactory']

class StopWordRemoverFactory:
    """Factory for creating a pre-configured StopWordRemover."""

    def create_stop_word_remover(self):
        stop_words = self.get_stop_words()
        dictionary = ArrayDictionary(stop_words)
        stop_word_remover = StopWordRemover(dictionary)

        return stop_word_remover

    def get_stop_words(self):
        return self.get_stop_words_from_file()

    def get_stop_words_from_file(self):
        current_dir = os.path.dirname(os.path.realpath(__file__))
        data_file = os.path.join(current_dir, 'data', 'stop-words.txt')
        if not os.path.isfile(data_file):
            raise RuntimeError('Stop words file is missing. It seems that your installation is corrupted.')

        with open(data_file, 'r', encoding='utf-8') as f:
            content = f.read()

        return content.split('\n')




