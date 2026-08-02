from Sastrawi.Stemmer.Context.RemovalInterface import RemovalInterface

class Removal(RemovalInterface):
    """Record of an affix removal performed during the stemming process."""

    def __init__(self, visitor, subject, result, removed_part, affix_type):
        self.visitor = visitor
        self.subject = subject
        self.result = result
        self.removed_part = removed_part
        self.affix_type = affix_type

    def get_visitor(self):
        return self.visitor

    def get_subject(self):
        return self.subject

    def get_result(self):
        return self.result

    def get_removed_part(self):
        return self.removed_part

    def get_affix_type(self):
        return self.affix_type



