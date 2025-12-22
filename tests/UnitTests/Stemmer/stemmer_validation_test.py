import unittest
from Sastrawi.Dictionary.ArrayDictionary import ArrayDictionary
from Sastrawi.Stemmer.Stemmer import Stemmer

class Test_StemmerValidationTest(unittest.TestCase):
    def setUp(self):
        self.dictionary = ArrayDictionary([])
        self.stemmer = Stemmer(self.dictionary)

    def test_StemRaisesTypeErrorOnNonStringInput(self):
        with self.assertRaises(TypeError):
            self.stemmer.stem(None)

        with self.assertRaises(TypeError):
            self.stemmer.stem(123)

        with self.assertRaises(TypeError):
            self.stemmer.stem(['list'])

        with self.assertRaises(TypeError):
            self.stemmer.stem(object())

    def test_StemAcceptsStringInput(self):
        # Should not raise
        result = self.stemmer.stem("string")
        self.assertIsInstance(result, str)

if __name__ == '__main__':
    unittest.main()
