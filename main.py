import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from nltk.classify import NaiveBayesClassifier
from nltk.classify.util import accuracy
import pandas as pd
import string
from sklearn import *
from sklearn.model_selection import train_test_split


nltk.download('all')

dataset = pd.read_csv('IMDB Dataset.csv')

stop_words = stopwords.words('english')

def preprocess(text):
    tokens = nltk.word_tokenize(text.lower())
    filtered_tokens = [token for token in tokens if token not in stop_words]

    lemma = nltk.WordNetLemmatizer()
    lemma_tokens = [lemma.lemmatize(token) for token in filtered_tokens]

    processed_text = ' '.join(lemma_tokens)
    return processed_text



dataset['processed_text'] = dataset['text'].apply(preprocess)


train_data, test_data = train_test_split(dataset[['review', 'sentiment']], test_size=0.2)


train_data = [(row['review'], row['sentiment']) for index, row in train_data.iterrows()]
test_data = [(row['review'], row['sentiment']) for index, row in test_data.iterrows()]


classifier = NaiveBayesClassifier.train(train_data)


print(f"Accuracy: {accuracy(classifier, test_data) * 100:.2f}%")
classifier.show_most_informative_features(10)

def predict_sentiment(text):
    processed_text = preprocess(text)
    features = get_features(processed_text)
    return classifier.classify(features)

new_text = "I love programming in Python!"
predicted_sentiment = predict_sentiment(new_text)
print(f"The predicted sentiment for the text is: {predicted_sentiment}")
