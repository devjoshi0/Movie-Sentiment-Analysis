import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.classify import NaiveBayesClassifier
from nltk.classify.util import accuracy

nltk.download('punkt')
nltk.download('stopwords')

data_frame = pd.read_csv('IMDB Dataset.csv')


stop_words = set(stopwords.words('english'))


def preprocess_text(text):
    words = word_tokenize(text)
    words = {word.lower() for word in words if word.isalpha() and word.lower() not in stop_words}
    return list(words)

data_frame['processed_text'] = data_frame['text'].apply(preprocess_text)


label_map = {'positive': 1, 'negative': 0}
data_frame['label'] = data_frame['label'].map(label_map)


def get_features(words):
    return {word: True for word in words}

train_data = [(get_features(words), label) for words, label in zip(data_frame['processed_text'], data_frame['label'])]


classifier = NaiveBayesClassifier.train(train_data)

# Calculate accuracy
train_accuracy = accuracy(classifier, train_data)
print(f'Training Accuracy: {train_accuracy * 100:.2f}%')

# Analyze sentiment
def analyze_sentiment(text):
    processed_text = preprocess_text(text)
    features = get_features(processed_text)
    sentiment_prob_dist = classifier.prob_classify(features)
    sentiment_score = sentiment_prob_dist.prob(1)  # Probability of positive sentiment
    return sentiment_score

text = "movie"
sentiment_score = analyze_sentiment(text)
print(f'Sentiment Score: {sentiment_score * 100:.2f}%')
