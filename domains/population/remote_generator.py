import os
import random
import uuid
import psycopg2
import time
import requests
import json
from faker import Faker
from multiprocessing import Pool, cpu_count
from datetime import datetime, timedelta

# Configuration
DB_HOST = "127.0.0.1" # Connect to Xeon Server (Localhost)
DB_PORT = "5432"
DB_NAME = "population"
DB_USER = "willow"
DB_PASS = "willowdev123"

# Ollama Configuration (Frank)
# Ollama Configuration (Frank)
OLLAMA_URL = "http://frank.clouded-newton.ts.net:11434/api/generate"
OLLAMA_MODEL = "deepseek-r1:32b" # High reasoning model
USE_LLM_FOR_QUOTES = True # Set to False for speed

TARGET_COUNT = 100_000_000
BATCH_SIZE = 100 # Reduced batch size when using LLM
PROCESSES = 4 # Limit processes to avoid OOM on GPU if using LLM

fake = Faker('en_GB') # Use UK Locale

def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )

def generate_llm_quote(person_name, hobby):
    """Generate a unique quote using Ollama on Frank"""
    if not USE_LLM_FOR_QUOTES:
        return fake.sentence()
        
    prompt = f"Generate a short, 1-sentence customer review for an insurance company from {person_name} who loves {hobby}. Be British."
    
    try:
        response = requests.post(OLLAMA_URL, json={
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False
        }, timeout=10)
        return response.json().get('response', fake.sentence()).strip()
    except:
        return fake.sentence() # Fallback

def generate_batch(batch_id):
    conn = get_connection()
    cur = conn.cursor()
    
    people_data = []
    quotes_data = []
    claims_data = []

    # Special Postcodes for Testing
    TEST_POSTCODES = ['XM4 5HQ', 'BS98 1TL', 'BX1 1LT', 'SW1A 1AA', 'SW1A 2AA', 'E98 1SN', 'CV4 8UW']

    for _ in range(BATCH_SIZE):
        # Logic: Skew towards 25-45 age group
        if random.random() < 0.6:
            age = random.randint(25, 45)
        else:
            age = random.randint(18, 90)
            
        risk_score = random.betavariate(2, 5)
        person_id = str(uuid.uuid4())
        policy_start_date = fake.date_between(start_date='-5y', end_date='today')
        
        # Random Traits (UK Statistics)
        traits = {}
        
        # Postcode Logic
        if random.random() < 0.1: # 10% get a "Special" postcode
            traits['postcode'] = random.choice(TEST_POSTCODES)
        else:
            traits['postcode'] = fake.postcode()

        # Color Blindness (approx 1 in 12 men, 1 in 200 women)
        # Simplified: 4.5% overall population
        if random.random() < 0.045:
            traits['color_blindness'] = random.choice(['Deuteranomaly', 'Protanomaly', 'Protanopia', 'Deuteranopia'])
            
        # Hobbies (Top UK Hobbies)
        if random.random() < 0.7: # 70% have a listed hobby
            hobbies = ['Gardening', 'Reading', 'Walking', 'Cooking', 'Knitting', 'DIY', 'Video Games', 'Football']
            traits['hobby'] = random.choice(hobbies)
            
        # Left Handedness (approx 10%)
        if random.random() < 0.10:
            traits['handedness'] = 'Left'
            
        # Person
        first_name = fake.first_name()
        last_name = fake.last_name()
        
        people_data.append((
            person_id,
            first_name,
            last_name,
            age,
            round(risk_score, 4),
            policy_start_date,
            True
        ))

        # Quotes (1-3 per person)
        num_quotes = random.randint(1, 3)
        for _ in range(num_quotes):
            quote_id = str(uuid.uuid4())
            product_type = random.choice(['Auto', 'Home', 'Life', 'Cyber'])
            premium = round(random.uniform(500, 5000), 2)
            status = random.choice(['ISSUED', 'ISSUED', 'ISSUED', 'DRAFT', 'REJECTED'])
            created_at = fake.date_between(start_date='-2y', end_date='today')
            valid_until = created_at + timedelta(days=30)
            
            # Generate LLM Quote occasionally (10% chance to save time, or 100% if you want full load)
            if random.random() < 0.1: 
                quote_text = generate_llm_quote(f"{first_name} {last_name}", traits.get('hobby', 'Tea'))
            else:
                quote_text = fake.sentence()

            # Note: We need to update the schema to store the quote text if it's not there.
            # Assuming 'quotes' table has a 'text' column or similar. 
            # If not, we might need to add it or store it in a separate table.
            # For now, let's assume we append it to the tuple, but we need to check the INSERT statement below.
            
            quotes_data.append((
                quote_id,
                person_id,
                product_type,
                premium,
                status,
                created_at,
                created_at,
                valid_until,
                quote_text # Added text
            ))

            # Claims (for ISSUED quotes)
            if status == 'ISSUED' and random.random() < 0.3:
                num_claims = random.randint(1, 2)
                for _ in range(num_claims):
                    claim_id = str(uuid.uuid4())
                    incident_date = fake.date_between(start_date=created_at, end_date='today')
                    report_date = incident_date + timedelta(days=random.randint(0, 10))
                    claim_amount = round(random.uniform(100, 10000), 2)
                    claim_status = random.choice(['FILED', 'INVESTIGATING', 'APPROVED', 'PAID', 'DENIED'])
                    description = fake.sentence()
                    
                    claims_data.append((
                        claim_id,
                        quote_id,
                        incident_date,
                        report_date,
                        description,
                        claim_amount,
                        claim_status,
                        report_date
                    ))
    
    # Bulk Insert People
    args_str = ','.join(cur.mogrify("(%s,%s,%s,%s,%s,%s,%s)", x).decode('utf-8') for x in people_data)
    cur.execute("INSERT INTO people (id, first_name, last_name, age, risk_score, policy_start_date, active) VALUES " + args_str)
    
    # Bulk Insert Quotes
    # Updated to include quote_text
    if quotes_data:
        args_str = ','.join(cur.mogrify("(%s,%s,%s,%s,%s,%s,%s,%s)", x).decode('utf-8') for x in quotes_data)
        cur.execute("INSERT INTO quotes (id, person_id, product_type, premium_amount, status, created_at, valid_until, text) VALUES " + args_str)

    # Bulk Insert Claims
    if claims_data:
        args_str = ','.join(cur.mogrify("(%s,%s,%s,%s,%s,%s,%s,%s)", x).decode('utf-8') for x in claims_data)
        cur.execute("INSERT INTO claims (id, quote_id, incident_date, report_date, description, claim_amount, status, created_at) VALUES " + args_str)
    
    conn.commit()
    cur.close()
    conn.close()
    return BATCH_SIZE

def main():
    print(f"Starting generation of {TARGET_COUNT} entities using {PROCESSES} processes...")
    start_time = time.time()
    
    total_batches = TARGET_COUNT // BATCH_SIZE
    pool = Pool(PROCESSES)
    
    completed = 0
    for result in pool.imap_unordered(generate_batch, range(total_batches)):
        completed += result
        if completed % (BATCH_SIZE * 10) == 0:
            elapsed = time.time() - start_time
            rate = completed / elapsed
            print(f"Generated {completed:,} rows. Rate: {rate:.0f} rows/sec")
            
    pool.close()
    pool.join()
    print("✓ Generation complete.")

if __name__ == "__main__":
    main()
