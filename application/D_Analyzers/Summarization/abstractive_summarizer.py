from transformers import BartTokenizer, BartForConditionalGeneration


class AbstractiveSummarizer:
    def __init__(self, sentences):
        self.sentences = sentences

    def summarize(self, model):
        summarization = getattr(self, model)(self.sentences)
        return summarization

    def bart_summarizer(self, sentences):
        tokenizer = BartTokenizer.from_pretrained('facebook/bart-large-cnn')
        model = BartForConditionalGeneration.from_pretrained('facebook/bart-large-cnn')
        # Join sentences to form a single string
        text = ' '.join(sentences)

        # Tokenize the input (batch of size 1)
        inputs = tokenizer([text], max_length=1024, return_tensors='pt')

        # Generate summary
        summary_ids = model.generate(inputs['input_ids'], num_beams=4, max_length=100, early_stopping=True)
        summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

        return summary
