from rouge import Rouge
from datasets import load_dataset

from .evaluation_datasets import StateBills
from D_Analyzers.Summarization.extractive_summarizer import ExtractiveSummarizer


class ROUGE:
    def __init__(self, model: ExtractiveSummarizer):
        self.model = model

    def state_bills(self):
        """
        Standard format of the datasets:
        {
            "text": "string",
            "reference_summary": "list",
            "title": "string",
            "model_summary": "list"
        }
        :return:
        """
        billsum = StateBills().billsum()
        for index, row in billsum.items():
            model_summary = self.model.summarize(row["text"])
            billsum[index]["model_summary"] = model_summary

        return "ROUGE score for State Bills datasets:\n"\
            + "- BillSum: " + str(self.rouge(billsum))


