class DontStemShortWord:
    """Stop the stemming process for words of at most three characters."""

    def visit(self, context):
        if self.is_short_word(context.current_word):
            context.stopProcess()

    def is_short_word(self, word):
        return len(word) <= 3




