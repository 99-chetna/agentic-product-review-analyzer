from dotenv import load_dotenv
import os
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def ask_llm(question, reviews):
    try:
        # Limit reviews (avoid token overload)
        sample_reviews = reviews[:50]
        context = "\n".join(sample_reviews)

        # ✅ IMPROVED PROMPT (structured output)
        prompt = f"""
You are a professional business analyst.

Analyze the following customer reviews and answer the question.

Reviews:
{context}

Question:
{question}

Respond STRICTLY in this format:

🔹 Key Issues:
- Issue 1
- Issue 2
- Issue 3

🔹 Insights:
- Short business insight

🔹 Recommendations:
- Action 1
- Action 2
- Action 3

Keep response:
- Clear
- Concise
- Professional
- No long paragraphs
"""

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are a helpful business analyst."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3   # ✅ makes output more stable & clean
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"⚠️ AI Error: {str(e)}"