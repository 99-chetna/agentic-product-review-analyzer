from transformers import pipeline

class SentimentAgent:

    def __init__(self):
        self.sentiment_model = pipeline(
            "sentiment-analysis"
        )

    def analyze(self, text):
        try:
            result = self.sentiment_model(
                str(text)[:512]
            )[0]

            return result["label"]

        except:
            return "UNKNOWN"