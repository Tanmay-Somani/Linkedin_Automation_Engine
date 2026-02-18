import os
import json
from google import genai
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

# We define the structure using a standard Python class (Pydantic)
# This is the most robust way to handle JSON in the new SDK
class LinkedInPackage(BaseModel):
    hooks: list[str]
    post_body: str
    hashtags: list[str]

class ContentEngine:
    def __init__(self, api_key):
        # The new client syntax
        self.client = genai.Client(api_key=api_key)
        self.model_id = "gemini-flash-latest"

    def generate(self, topic, context):
        prompt = f"Write a professional technical LinkedIn post. Topic: {topic}. Context: {context}."
        
        # New SDK call format
        response = self.client.models.generate_content(
            model=self.model_id,
            contents=prompt,
            config={
                'response_mime_type': 'application/json',
                'response_schema': LinkedInPackage, # Uses our class above
                'system_instruction': "You are a Senior AI Engineer. Write technical, punchy LinkedIn posts."
            }
        )
        
        # The new SDK returns an object that we can convert to a dict
        return json.loads(response.text)