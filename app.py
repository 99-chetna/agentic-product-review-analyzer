from flask import Flask, render_template, request
import pandas as pd

from llm_helper import ask_llm

from agents.sentiment_agent import SentimentAgent
from agents.aspect_agent import AspectAgent
from agents.fake_review_agent import FakeReviewAgent
from agents.recommendation_agent import RecommendationAgent
from agents.review_collection_agent import ReviewCollectionAgent


app = Flask(__name__)

# Agents

sentiment_agent = SentimentAgent()
aspect_agent = AspectAgent(sentiment_agent)
fake_review_agent = FakeReviewAgent()
recommendation_agent = RecommendationAgent()
review_collection_agent = ReviewCollectionAgent()

# Global Storage

reviews_data = []
current_product = ""


def generate_insight(df):

    positive = (
        df["sentiment"] == "POSITIVE"
    ).sum()

    negative = (
        df["sentiment"] == "NEGATIVE"
    ).sum()

    if positive == 0 and negative == 0:
        return "No clear sentiment detected."

    if negative > positive:
        return (
            "⚠️ Customers are mostly dissatisfied. "
            "Improvements needed."
        )

    return (
        "✅ Customers are generally satisfied "
        "with the product."
    )


def calculate_scores(df):

    total_reviews = len(df)

    positive_reviews = (
        df["sentiment"] == "POSITIVE"
    ).sum()

    suspicious_reviews = (
        df["review_status"] == "Suspicious"
    ).sum()

    if total_reviews == 0:
        return 0, 0, 0

    product_score = int(
        (positive_reviews / total_reviews)
        * 100
    )

    trust_score = int(
        (
            (total_reviews - suspicious_reviews)
            / total_reviews
        )
        * 100
    )

    return (
        product_score,
        trust_score,
        suspicious_reviews
    )


@app.route("/", methods=["GET", "POST"])
def index():

    global reviews_data
    global current_product

    ai_answer = None

    if request.method == "POST":

        question = request.form.get(
            "question"
        )

        # ==========================
        # AI QUESTION SECTION
        # ==========================

        if question:

            if not reviews_data:

                return (
                    "Please analyze a product first."
                )

            df = pd.DataFrame({
                "review_text": reviews_data
            })

        # ==========================
        # PRODUCT ANALYSIS SECTION
        # ==========================

        else:

            product_name = request.form.get(
                "product_name"
            )

            if not product_name:

                return (
                    "Please enter product name."
                )

            current_product = product_name

            print(
                f"\nAnalyzing Product: "
                f"{product_name}"
            )

            reviews_data = (
                review_collection_agent
                .collect_reviews(
                    product_name
                )
            )

            if len(reviews_data) == 0:

                return (
                    f"No review data found "
                    f"for {product_name}"
                )

            print(
                "Reviews Collected:",
                len(reviews_data)
            )

            df = pd.DataFrame({
                "review_text": reviews_data
            })

        # ==========================
        # SENTIMENT AGENT
        # ==========================

        df["sentiment"] = (
            df["review_text"]
            .apply(
                sentiment_agent.analyze
            )
        )

        # ==========================
        # ASPECT AGENT
        # ==========================

        df["aspects"] = (
            df["review_text"]
            .apply(
                aspect_agent.analyze
            )
        )

        # ==========================
        # FAKE REVIEW AGENT
        # ==========================

        df["review_status"] = (
            df["review_text"]
            .apply(
                fake_review_agent.detect
            )
        )

        # ==========================
        # DASHBOARD DATA
        # ==========================

        sentiment_counts = (
            df["sentiment"]
            .value_counts()
            .to_dict()
        )

        insight = generate_insight(
            df
        )

        recommendation_data = (
            recommendation_agent
            .generate(df)
        )

        (
            product_score,
            trust_score,
            suspicious_reviews
        ) = calculate_scores(df)

        # ==========================
        # AI AGENT
        # ==========================

        if question:

            ai_answer = ask_llm(
                question,
                "\n".join(
                    reviews_data[:100]
                )
            )

        # ==========================
        # RENDER DASHBOARD
        # ==========================

        return render_template(
            "result.html",

            results=df.to_dict(
                orient="records"
            ),

            sentiments=sentiment_counts,

            insight=insight,

            ai_answer=ai_answer,

            product_score=product_score,

            trust_score=trust_score,

            suspicious_reviews=suspicious_reviews,

            recommendation_data=
            recommendation_data,

            product_name=
            current_product
        )

    return render_template(
        "index.html"
    )


import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
