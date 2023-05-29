import os
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.tokenize import sent_tokenize
from rouge import Rouge
from fuzzywuzzy import fuzz
import sys
sys.path.append('/application')

from A_DataCollectors.ScientificLiteratureCollector.scientific_literature_collector import ScientificLiteratureCollector
from C_DataProcessors.text_preprocessor import TextPreprocessor
from D_Analyzers.Summarization.extractive_summarizer import ExtractiveSummarizer
from F_UserInterface.ApplicationManager.application_manager import ScientificLiteratureAnalyzer, ForumAnalyzer

rouge = Rouge()

def similar_sentences_count(summarizer_sentences, researcher_sentences, threshold=90):
    count = 0
    for sent1 in summarizer_sentences:
        for sent2 in researcher_sentences:
            if fuzz.ratio(sent1, sent2) >= threshold:
                count += 1
                break  # break inner loop once a match is found
    return count

# Fetch the PDF files and corresponding text files.
papers_dir = '/application/F_Evaluate/Summarization/datasets/manual/papers'
sentences_dir = '/application/F_Evaluate/Summarization/datasets/manual/sentences'
file_names = [name[:-4] for name in os.listdir(papers_dir) if name.endswith('.pdf')]

for file_name in file_names:
    pdf_file = os.path.join(papers_dir, f"{file_name}.pdf")
    txt_file = os.path.join(sentences_dir, f"{file_name}.txt")

    # Collect data
    collector = ScientificLiteratureCollector(pdf_file)
    text = collector.collect('pdf', 'local', 'scipy')

    # Preprocess data
    summarization_steps = ['clean_data', 'split_sentences']
    preprocessor = TextPreprocessor(summarization_steps)
    preprocessed_text = preprocessor.preprocess_grobid(text)

    # Consolidate all sentences in one list
    all_sentences = []
    for header, sentences in preprocessed_text.items():
        all_sentences.extend(sentences)

    # Summarize data
    es = ExtractiveSummarizer(all_sentences)
    summary = es.summarize('textrank', top_n=40, order_by_rank=False)

    # filter out sentences less than four words long
    summary = '. '.join(sentence for sentence in summary.split('. ') if len(sentence.split()) >= 4)

    print(summary)

    # Load the researcher's summary.
    with open(txt_file, 'r') as f:
        researcher_summary = f.read().replace('\n', ' ')

    # Convert summaries to sentence lists
    auto_summary_sentences = sent_tokenize(summary)
    researcher_summary_sentences = sent_tokenize(researcher_summary)

    similar_count = similar_sentences_count(auto_summary_sentences, researcher_summary_sentences)
    print(f"Number of similar sentences for {file_name}: {similar_count}")

    # Compute ROUGE scores
    rouge_scores = rouge.get_scores(summary, researcher_summary)

    print(f"ROUGE scores for {file_name}:", rouge_scores)
