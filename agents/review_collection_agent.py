import feedparser
from bs4 import BeautifulSoup


class ReviewCollectionAgent:

    def collect_reviews(self, product_name):

        reviews = []

        search_queries = [

            f"{product_name} review",
            f"{product_name} user experience",
            f"{product_name} customer feedback",
            f"{product_name} opinion"

        ]

        for query in search_queries:

            rss_url = (
                "https://news.google.com/rss/search?q="
                + query.replace(" ", "+")
            )

            print("Searching News:", query)

            try:

                feed = feedparser.parse(rss_url)

                print(
                    "Articles Found:",
                    len(feed.entries)
                )

                for article in feed.entries:

                    # Article title
                    reviews.append(
                        article.title
                    )

                    # Article summary (clean HTML)
                    if hasattr(article, "summary"):

                        clean_summary = BeautifulSoup(
                            article.summary,
                            "html.parser"
                        ).get_text(
                            separator=" ",
                            strip=True
                        )

                        reviews.append(
                            clean_summary
                        )

            except Exception as e:

                print(e)

        # Remove duplicates
        reviews = list(
            dict.fromkeys(reviews)
        )

        print(
            "Total Reviews Extracted:",
            len(reviews)
        )

        return reviews[:500]