from datasets import load_dataset

from C_DataProcessors.text_preprocessor import TextPreprocessor


class NewsArticles:
    def __init__(self):
        self.text_preprocessor = TextPreprocessor(steps=['clean_data', 'split_sentences'])

    def cnndm(self):
        """
        Size: 376 MB
        :return:
        """
        cnndm_dataset = load_dataset("cnn_dailymail", "3.0.0", split="test")
        cnndm_dict = {}
        for index, row in enumerate(cnndm_dataset):
            data = {
                "text": row["article"],
                "reference_summary": self.text_preprocessor.preprocess(row["highlights"]),
                'model_summary': ''
            }

            cnndm_dict[index] = data

        # return first ten items of cnndm_dict
        print(cnndm_dict)
        return {k: cnndm_dict[k] for k in list(cnndm_dict)[:10]}


class StateBills:
    def __init__(self):
        self.text_preprocessor = TextPreprocessor(steps=['clean_data', 'split_sentences'])

    def billsum(self):
        """
        Size: 1.2 GB
        :return:
        """
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
    def __init__(self):
        self.text_preprocessor = TextPreprocessor(steps=['clean_data', 'split_sentences'])

    def arxiv(self):
        """
        Size: 1.2 GB
        :return:
        """
        arxiv_dataset = load_dataset("arxiv_dataset", split="test")
        arxiv_dict = {}
        for index, row in enumerate(arxiv_dataset):
            data = {
                "text": row["article"],
                "reference_summary": self.text_preprocessor.preprocess(row["abstract"]),
                'model_summary': ''
            }

            arxiv_dict[index] = data

        # return first ten items of arxiv_dict
        return {k: arxiv_dict[k] for k in list(arxiv_dict)[:10]}

    def pubmed(self):
        """
        Size: Outrageous
        :return:
        """
        pubmed_dataset = load_dataset("pubmed", split="test")
        pubmed_dict = {}
        for index, row in enumerate(pubmed_dataset):
            data = {
                "text": row["article"],
                "reference_summary": self.text_preprocessor.preprocess(row["abstract"]),
                'model_summary': ''
            }

            pubmed_dict[index] = data

        # return first ten items of pubmed_dict
        return {k: pubmed_dict[k] for k in list(pubmed_dict)[:10]}


class OnlineForumDiscussions:
    pass
