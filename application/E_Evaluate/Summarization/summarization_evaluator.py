from rouge import Rouge

from .evaluation_datasets import StateBills
from C_DataProcessors.text_preprocessor import TextPreprocessor
from D_Analyzers.Summarization.extractive_summarizer import ExtractiveSummarizer


class ROUGE:
    def __init__(self, model: str):
        self.text_preprocessor = TextPreprocessor(steps=['clean_data', 'split_sentences'])
        self.model = model
        self.rouge = Rouge()  # Initialize Rouge class here

    def state_bills(self):
        rouge_1 = []
        rouge_2 = []
        rouge_l = []

        billsum = StateBills().billsum()

        for index, row in billsum.items():
            length_reference_summary = len(row["reference_summary"])
            preprocessed_text = self.text_preprocessor.preprocess(row["text"])
            obj = ExtractiveSummarizer(preprocessed_text)
            model_summary = obj.summarize(self.model, top_n=length_reference_summary)
            billsum[index]["model_summary"] = model_summary

            all_rouge_scores = self.rouge.get_scores(' '.join(model_summary), ' '.join(row["reference_summary"]))

            # Update the lists with the scores of each metric
            for metric in ['rouge-1', 'rouge-2', 'rouge-l']:
                metric_scores = [score[metric] for score in all_rouge_scores]
                average_scores = {
                    'r': sum([score['r'] for score in metric_scores]) / len(metric_scores),
                    'p': sum([score['p'] for score in metric_scores]) / len(metric_scores),
                    'f': sum([score['f'] for score in metric_scores]) / len(metric_scores)
                }

                if metric == 'rouge-1':
                    rouge_1.append(average_scores)
                elif metric == 'rouge-2':
                    rouge_2.append(average_scores)
                elif metric == 'rouge-l':
                    rouge_l.append(average_scores)

        # Compute the average for each list
        avg_rouge_1 = {key: sum(d[key] for d in rouge_1) / len(rouge_1) for key in rouge_1[0]}
        avg_rouge_2 = {key: sum(d[key] for d in rouge_2) / len(rouge_2) for key in rouge_2[0]}
        avg_rouge_l = {key: sum(d[key] for d in rouge_l) / len(rouge_l) for key in rouge_l[0]}

        print("Average ROUGE-1: ", avg_rouge_1)
        print("Average ROUGE-2: ", avg_rouge_2)
        print("Average ROUGE-L: ", avg_rouge_l)


