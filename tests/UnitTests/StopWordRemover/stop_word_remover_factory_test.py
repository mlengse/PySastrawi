import unittest
import unittest.mock
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from Sastrawi.StopWordRemover.StopWordRemover import StopWordRemover

class TestStopWordRemoverFactory(unittest.TestCase):
    def setUp(self):
        self.factory = StopWordRemoverFactory()
        return super().setUp()

    def test_createStopWordRemover(self):
        self.assertIsInstance(self.factory.create_stop_word_remover(), StopWordRemover)

    def test_getStopWordsFromFileRaisesWhenFileMissing(self):
        factory = StopWordRemoverFactory()
        with unittest.mock.patch('os.path.isfile', return_value=False):
            with self.assertRaises(RuntimeError):
                factory.get_stop_words_from_file()

if __name__ == '__main__':
    unittest.main()
