from datasets import load_dataset

from C_DataProcessors.text_preprocessor import TextPreprocessor


class NewsArticles:
    pass

class StateBills:
    def __init__(self):
        self.text_preprocessor = TextPreprocessor(steps=['clean_data', 'split_sentences'])

    def billsum(self):
        billsum_dataset = load_dataset("billsum", split="ca_test")
        billsum_dict = {}
        for index, row in enumerate(billsum_dataset):
            data = {
                "text": row["text"],
                "reference_summary": self.text_preprocessor.preprocess(row["summary"]),
                'model_summary': ''
            }

            billsum_dict[index] = data

        # return first ten items of billsun_dict
        return {k: billsum_dict[k] for k in list(billsum_dict)[:10]}

class ScientificPapers:
    pass

class OnlineForumDiscussions:
    pass
