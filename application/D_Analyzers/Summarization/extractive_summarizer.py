
class ExtractiveSummarizer:
    def __init__(self, sentences):
        self.sentences = sentences

    def lead_3(self):
        """
        Returns the first three sentences of the text.
        :return:
        """
        summary = ". ".join(self.sentences[:3])
        return summary
