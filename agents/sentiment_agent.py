from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

class SentimentAgent:

    def analyze(self, text):

        try:

            score = analyzer.polarity_scores(
                str(text)
            )

            if score["compound"] >= 0:
                return "POSITIVE"

            return "NEGATIVE"

        except:

            return "UNKNOWN"