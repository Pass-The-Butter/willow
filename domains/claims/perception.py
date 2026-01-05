"""
Neural Perception Module
========================
Uses LLMs to "read" unstructured claim text and extract symbolic facts for the Graph.
"""

import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SCHEMA = {
    "type": "object",
    "properties": {
        "incident_date": {
            "type": "string",
            "description": "Date of the incident in YYYY-MM-DD format"
        },
        "incident_type": {
            "type": "string", 
            "enum": ["Theft", "Fire", "Water Damage", "Accidental Damage", "Liability"],
            "description": "Category of the loss"
        },
        "claimed_amount": {
            "type": "number",
            "description": "Estimated value of the loss in GBP"
        },
        "summary": {
            "type": "string",
            "description": "Concise 1-sentence summary of what happened"
        },
        "entities_involved": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Names of people, items, or locations mentioned"
        }
    },
    "required": ["incident_date", "incident_type", "summary"]
}

def extract_claim_facts(text: str) -> dict:
    """
    Extracts structured facts from raw claim description using OpenAI.
    """
    prompt = f"""
    You are an expert insurance adjuster AI. 
    Analyze the following claim description and extract structured facts.
    
    CLAIM TEXT:
    "{text}"
    
    Return JSON only.
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Fast and capable enough for extraction
            messages=[
                {"role": "system", "content": "You are a helpful assistant that outputs JSON."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0
        )
        
        content = response.choices[0].message.content
        data = json.loads(content)
        return data
        
    except Exception as e:
        print(f"Neural Perception Failed: {e}")
        return {
            "error": str(e),
            "summary": "Extraction failed"
        }

if __name__ == "__main__":
    # Test
    test_text = "On Jan 1st 2024, my laptop was stolen from my car while parked at Sainsbury's. It was a Macbook Pro worth £2000."
    print(json.dumps(extract_claim_facts(test_text), indent=2))
