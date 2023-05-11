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
                "title": row["title"],
                'model_summary': ''
            }

            billsum_dict[index] = data

        return billsum_dict

class ScientificPapers:
    pass

class OnlineForumDiscussions:
    pass


billsum = load_dataset("billsum", split="ca_test")

num_rows = len(billsum)
print("Number of rows:", num_rows)

example_index = 0  # Index of the example you want to access
example = billsum[example_index]
print("Example text:", example["text"])
print("Example summary:", example["summary"])
print("Example title:", example["title"])