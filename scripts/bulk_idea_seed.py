

import sqlite3
import os
from google import genai
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

class IdeaList(BaseModel):
    topics: list[str]
    contexts: list[str]

def seed_100_ideas():
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    
    prompt = """
    Generate 100 distinct LinkedIn post ideas for a Senior AI Research Engineer. 
    The ideas should be split into 4 categories: 
    1. Technical Deep Dives (Architectures, Optimizers, CUDA)
    2. Research Trends (LLMs, Agents, Multimodal)
    3. Engineering Best Practices (RAG, Evaluation, Deployment)
    4. Opinions on the AI Industry.

    For each idea, provide a short 1-sentence 'context' which is a technical hook or observation.
    """

    print("🧠 Generating 100 ideas via Gemini... (This might take a moment)")
    
    response = client.models.generate_content(
        model="gemini-flash-latest",
        contents=prompt,
        config={
            'response_mime_type': 'application/json',
            'response_schema': IdeaList,
        }
    )

    data = response.parsed
    
    conn = sqlite3.connect('data/engine.db')
    cursor = conn.cursor()
    
    count = 0
    for t, c in zip(data.topics, data.contexts):
        cursor.execute(
            "INSERT INTO ideas (topic, context, status) VALUES (?, ?, ?)",
            (t, c, 'pending')
        )
        count += 1
    
    conn.commit()
    conn.close()
    print(f"✅ Successfully seeded {count} ideas into the Idea Bank.")

if __name__ == "__main__":
    seed_100_ideas()