import os
import sys
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import tensorflow_datasets as tfds

sys.path.append('C:\\Users\\noudy\\PycharmProjects\\Cassidy\\application')
from D_Analyzers.Sentiment_Analysis.sentiment_analyzer import SentimentAnalyzer

# Load the IMDB dataset
dataset = tfds.load(name="imdb_reviews")
train_dataset, test_dataset = dataset['train'], dataset['test']

# Transform the datasets into lists
train_texts = [x.decode('utf-8') for x in tfds.as_dataframe(train_dataset)['text']]
train_labels = [x for x in tfds.as_dataframe(train_dataset)['label']]
test_texts = [x.decode('utf-8') for x in tfds.as_dataframe(test_dataset)['text']]
test_labels = [x for x in tfds.as_dataframe(test_dataset)['label']]

# Perform sentiment analysis using TextBlob
test_preds = []
for text in test_texts:
    sa = SentimentAnalyzer(text)
    polarity = sa.analyze('vader_analysis')
    # Map polarity to binary labels. Assumes neutral (polarity = 0) reviews are negative.
    label = 1 if polarity > 0 else 0
    test_preds.append(label)

# Compute accuracy
accuracy = accuracy_score(test_labels, test_preds)
print(f"Accuracy: {accuracy*100:.2f}%")

# Compute confusion matrix
matrix = confusion_matrix(test_labels, test_preds)
print('Confusion Matrix:')
print(matrix)

# Print classification report
report = classification_report(test_labels, test_preds)
print('Classification Report:')
print(report)