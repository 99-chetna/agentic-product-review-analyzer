class FakeReviewAgent:

    def detect(self, review):

        review = str(review).lower()

        score = 0

        suspicious_words = [
            "best ever",
            "must buy",
            "100% recommended",
            "perfect product",
            "amazing amazing",
            "excellent excellent"
        ]

        # Very short review
        if len(review.split()) < 3:
            score += 1

        # Suspicious phrases
        for word in suspicious_words:
            if word in review:
                score += 1

        # Excessive exclamation marks
        if review.count("!") > 3:
            score += 1

        if score >= 2:
            return "Suspicious"

        return "Genuine"