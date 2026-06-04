from review_collection_agent import ReviewCollectionAgent

agent = ReviewCollectionAgent()

reviews = agent.collect_reviews(
    "Samsung Galaxy S25"
)

print("\n====================")
print("TOTAL REVIEWS:", len(reviews))
print("====================\n")

for i, review in enumerate(
    reviews[:10],
    start=1
):
    print(f"{i}. {review}")