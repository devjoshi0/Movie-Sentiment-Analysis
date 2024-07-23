import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.classify import NaiveBayesClassifier
from nltk.classify.util import accuracy
import string

# Download necessary NLTK data
nltk.download('punkt')
nltk.download('stopwords')

# Load CSV file
df = pd.read_csv('IMDB Dataset.csv')

# Preprocess the data
stop_words = set(stopwords.words('english'))

def preprocess_text(text):
    # Tokenize the text
    words = word_tokenize(text)
    # Remove punctuation and stop words, and convert to lowercase
    words = [word.lower() for word in words if word.isalpha() and word.lower() not in stop_words]
    return words

df['processed_text'] = df['text'].apply(preprocess_text)

def get_features(words):
    return {word: True for word in words}

# Create a list of tuples for training
train_data = [(get_features(words), label) for words, label in zip(df['processed_text'], df['label'])]

# Train a Naive Bayes classifier
classifier = NaiveBayesClassifier.train(train_data)

# Calculate and print the accuracy of the classifier on the training data
train_accuracy = accuracy(classifier, train_data)
print(f'Accuracy: {train_accuracy * 100:.2f}%')

def analyze_sentiment(text):
    processed_text = preprocess_text(text)
    features = get_features(processed_text)
    sentiment_prob_dist = classifier.prob_classify(features)
    sentiment_score = sentiment_prob_dist.prob(1)  # Probability of positive sentiment
    return sentiment_score

# Example usage
text = "I love this product!"
sentiment_score = analyze_sentiment(text)
print(f'Sentiment score: {sentiment_score * 100:.2f}%')
