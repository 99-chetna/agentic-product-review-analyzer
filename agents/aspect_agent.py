class AspectAgent:

    def __init__(self, sentiment_agent):

        self.sentiment_agent = sentiment_agent

        self.aspects = [
            "price",
            "quality",
            "delivery",
            "battery",
            "camera",
            "display",
            "performance",
            "service",
            "design",
            "packaging"
        ]

    def analyze(self, text):

        result = {}

        text_lower = str(text).lower()

        for aspect in self.aspects:

            if aspect in text_lower:

                result[aspect] = self.sentiment_agent.analyze(text)

        return result