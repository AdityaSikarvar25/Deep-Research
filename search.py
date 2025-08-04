from ddgs import DDGS
from newspaper import Article
from openai import OpenAI
from typing import List
import os
from dotenv import load_dotenv
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))  # assumes OPENAI_API_KEY is set

def search_and_summarize(query: str, max_results: int = 3):
    texts = []
    with DDGS() as ddgs:
        results = ddgs.text(query, region='wt-wt', safesearch='moderate', max_results=max_results)
        for result in results:
            try:
                url = result.get("href")
                if not url:
                    continue
                article = Article(url)
                article.download()
                article.parse()
                texts.append(article.text)
            except Exception as e:
                print(f"❌ Failed: {url} → {e}")
    
    combined = "\n\n".join(texts)
    
    # Summarize using GPT-4o-mini
    summary_prompt = f"""
You are a research assistant. Given the following extracted text for the query: "{query}", create a concise summary (2-3 paragraphs, under 300 words). Write succinctly. Ignore fluff.
Text:
{combined}
"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": summary_prompt}]
    )
    return response.choices[0].message.content
