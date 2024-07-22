import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer


nltk.download('all')


sia = SentimentIntensityAnalyzer()


def analyze_sentiment(text):
    sentiment_scores = sia.polarity_scores(text)
    return sentiment_scores


if __name__ == "__main__":
    text = "this is a test."
    sentiment = analyze_sentiment(text)
    print(sentiment)
