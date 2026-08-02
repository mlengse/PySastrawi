class StopWordRemover:
    """Remove stop words from a text using a dictionary of stop words."""

    MAX_CHARACTER_LENGTH = 1000000

    def __init__(self, dictionary):
        self.dictionary = dictionary

    def get_dictionary(self):
        return self.dictionary

    def remove(self, text):
        """Remove stop words."""
        if not isinstance(text, str):
            raise TypeError("Text must be a string, received " + str(type(text)))

        if len(text) > self.MAX_CHARACTER_LENGTH:
            raise ValueError("Text length exceeds the maximum allowed length of " + str(self.MAX_CHARACTER_LENGTH) + " characters.")

        words = text.split(' ')
        stopped_words = [word for word in words if not self.dictionary.contains(word)]

        return ' '.join(stopped_words)
