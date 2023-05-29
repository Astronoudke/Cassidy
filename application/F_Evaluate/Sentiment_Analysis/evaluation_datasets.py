from datasets import load_dataset

from C_DataProcessors.text_preprocessor import TextPreprocessor


class Reviews:
    def __init__(self):
        self.text_preprocessor = TextPreprocessor(steps=['clean_data', 'split_sentences'])

    def imdb(self):
        """
        Size: 84 MB
        :return:
        """
        imdb_dataset = load_dataset("imdb", split="test")
        imdb_dict = {}
        for index, row in enumerate(imdb_dataset):
            data = {
                "text": row["text"],
                "reference_summary": self.text_preprocessor.preprocess(row["label"]),
                'model_summary': ''
            }

            imdb_dict[index] = data

        # return first ten items of imdb_dict
        return {k: imdb_dict[k] for k in list(imdb_dict)[:10]}