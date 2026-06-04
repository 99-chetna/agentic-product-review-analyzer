class RecommendationAgent:

    def generate(self, df):

        strengths = []
        complaints = []
        recommendations = []

        positive_reviews = len(
            df[df["sentiment"] == "POSITIVE"]
        )

        negative_reviews = len(
            df[df["sentiment"] == "NEGATIVE"]
        )

        # Strengths

        if positive_reviews > negative_reviews:
            strengths.append(
                "Most customers are satisfied with the product."
            )

        # Aspect Complaints

        aspect_text = " ".join(
            df["aspects"].astype(str)
        ).lower()

        if "quality" in aspect_text:
            complaints.append(
                "Quality issues mentioned by customers."
            )

        if "delivery" in aspect_text:
            complaints.append(
                "Delivery delays reported."
            )

        if "service" in aspect_text:
            complaints.append(
                "Customer service concerns identified."
            )

        # Recommendations

        if "quality" in aspect_text:
            recommendations.append(
                "Improve product quality control."
            )

        if "delivery" in aspect_text:
            recommendations.append(
                "Optimize delivery process."
            )

        if "service" in aspect_text:
            recommendations.append(
                "Provide better customer support."
            )

        if not recommendations:
            recommendations.append(
                "Maintain current quality standards."
            )

        return {
            "strengths": strengths,
            "complaints": complaints,
            "recommendations": recommendations
        }