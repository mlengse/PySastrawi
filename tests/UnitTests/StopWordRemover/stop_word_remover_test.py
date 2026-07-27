import unittest
from Sastrawi.Dictionary.ArrayDictionary import ArrayDictionary
from Sastrawi.StopWordRemover.StopWordRemover import StopWordRemover

class TestStopWordRemover(unittest.TestCase):
    def setUp(self):
        self.dictionary = ArrayDictionary(['di', 'ke'])
        self.stopWordRemover = StopWordRemover(self.dictionary)
        return super().setUp()

    def test_getDictionaryPreserveInstance(self):
        self.assertEqual(self.dictionary, self.stopWordRemover.get_dictionary())

    def test_removeStopWord(self):
        self.assertEqual('pergi sekolah', self.stopWordRemover.remove('pergi ke sekolah'))
        self.assertEqual('makan rumah', self.stopWordRemover.remove('makan di rumah'))

    def test_remove_raises_TypeError_for_non_string(self):
        with self.assertRaises(TypeError):
            self.stopWordRemover.remove(123)

    def test_remove_raises_ValueError_for_oversized_input(self):
        with self.assertRaises(ValueError):
            self.stopWordRemover.remove('a' * 1000001)

    def test_remove_empty_string(self):
        self.assertEqual('', self.stopWordRemover.remove(''))

    def test_remove_all_stop_words(self):
        self.assertEqual('', self.stopWordRemover.remove('di ke'))

    def test_remove_no_stop_words(self):
        self.assertEqual('pergi sekolah', self.stopWordRemover.remove('pergi sekolah'))

if __name__ == '__main__':
    unittest.main()
