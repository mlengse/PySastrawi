import re

class TextNormalizer(object):
    """description of class"""

    # Pre-compile regex patterns
    _regex_normalize_chars = re.compile(r'[^a-z0-9 -]', re.IGNORECASE|re.MULTILINE)
    _regex_normalize_spaces = re.compile(r'( +)', re.IGNORECASE|re.MULTILINE)

    @staticmethod
    def normalize_text(text):
        result = text.lower() #lower the text even unicode given
        result = TextNormalizer._regex_normalize_chars.sub(' ', result)
        result = TextNormalizer._regex_normalize_spaces.sub(' ', result)

        return result.strip()
