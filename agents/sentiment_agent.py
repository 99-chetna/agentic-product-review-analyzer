from transformers import pipeline

# Load model once
sentiment_model = pipeline("sentiment-analysis")

class SentimentAgent:

    def analyze(self, text):
        try:
            result = sentiment_model(str(text)[:512])[0]
            return result['label']
        except:
            return "UNKNOWN"