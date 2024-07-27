import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.classify import NaiveBayesClassifier
from nltk.classify.util import accuracy

nltk.download('punkt')
nltk.download('stopwords')

data_frame = pd.read_csv('dataset/IMDB Dataset.csv')


stop_words = set(stopwords.words('english'))


def preprocess_text(text):
    words = word_tokenize(text.translate(str.maketrans('', '', string.punctuation))
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

text = "I was lucky to see Avatar at a pre-screening a few hours ago. It completely blew me and the whole room away and i dare to say it will do so to 80% of any audience anywhere. The remaining 20%, who always finds something to complain about, will whine about character development, dialog, story or the pop-corn.Well, let me tell you: they went to this movie with the wrong expectations.You have most likely met Cameron's previous work(s): Aliens, Terminator 1 & 2, The Abyss, Titanic (!), just to name a few.So WHAT should you expect from Avatar??? MORE of the same!!! More of revolutionary film-making, more of grandiose new ideas, more of never-before-seen special effects, more of 150 minutes without relapsing, more of the James Cameron genius...I am very happy that the trailers didn't give the full story away. Lots of emotions are waiting for the viewer, laughter and tears also. Cameron was very smart keeping the teasers as teasers, nothing more... as the full movie will take your breath away.You will practically not notice that you are watching a non-existing world, it is sooo real. Attention to detail is superb. You computer geeks will know what I am talking about. This move was not rushed in the making. No wonder it could not have been done before - not having the proper computing power.The wild life, the jungle, the animals, the Na'vi-s, or the dragon-like flying creatures are all so life-like, they almost pop-off the screen (and in 3D they actually do :) .The sound effects were so well done, that when I saw at the credits that Skywalker Sound was behind it, i could only think of \"yessss... now THAT makes sense.\"Cameron is a visionaire - and again, he delivers, with full blast.A certain character says in the movie that Pandora (the planet where the story takes place) became his real world. My advice to you: let Pandora become YOUR real world for two and a half hours, let it make you completely forget about your life and problems, let it entertain you, move you, let it carry you away.Because THAT is what i expect as an exchange for my ticket.And a few hours ago i got tens of tickets worth of that."
sentiment_score = analyze_sentiment(text)
print(f'Sentiment Score: {sentiment_score * 100:.2f}%')
