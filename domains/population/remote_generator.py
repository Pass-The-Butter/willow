import os
import random
import uuid
import psycopg2
import time
import requests
import json
from faker import Faker
from multiprocessing import Pool
from datetime import datetime, timedelta

# Configuration
DB_HOST = os.getenv("DB_HOST", "agilemesh-postgres")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "population")
DB_USER = os.getenv("DB_USER", "willow")
DB_PASS = os.getenv("DB_PASS", "willowdev123")

# Ollama Configuration (Frank)
OLLAMA_URL = "http://frank.clouded-newton.ts.net:11434/api/generate"
OLLAMA_MODEL = "deepseek-r1:32b"
USE_LLM_FOR_QUOTES = False 

TARGET_COUNT = 5000
BATCH_SIZE = 100 
PROCESSES = 2 # Lower processes for the initial run to keep logs clean

fake = Faker('en_GB') 

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
        
    prompt = f"Generate a short, 1-sentence customer review for an insurance company from {person_name} who loves {hobby}. Be British and realistic."
    
    try:
        response = requests.post(OLLAMA_URL, json={
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False
        }, timeout=15)
        return response.json().get('response', fake.sentence()).strip()
    except:
        return fake.sentence() 

def generate_batch(batch_id):
    conn = get_connection()
    cur = conn.cursor()
    
    people_data = []
    quotes_data = []
    claims_data = []

    for _ in range(BATCH_SIZE):
        # Age distribution
        if random.random() < 0.6:
            age = random.randint(25, 45)
        else:
            age = random.randint(18, 90)
            
        risk_score = random.betavariate(2, 5)
        person_id = str(uuid.uuid4())
        policy_start_date = fake.date_between(start_date='-5y', end_date='today')
        
        first_name = fake.first_name()
        last_name = fake.last_name()
        
        people_data.append((
            person_id, first_name, last_name, age, round(risk_score, 4), policy_start_date, True
        ))

        # Quotes
        num_quotes = random.randint(1, 3)
        for _ in range(num_quotes):
            quote_id = str(uuid.uuid4())
            product_type = random.choice(['Auto', 'Home', 'Life', 'Cyber'])
            premium = round(random.uniform(500, 5000), 2)
            status = random.choice(['ISSUED', 'ISSUED', 'ISSUED', 'DRAFT', 'REJECTED'])
            created_at = fake.date_between(start_date='-2y', end_date='today')
            valid_until = created_at + timedelta(days=30)
            
            # Generate LLM Quote (10% chance)
            if random.random() < 0.1: 
                quote_text = generate_llm_quote(f"{first_name} {last_name}", random.choice(['Gardening', 'Football', 'Reading']))
            else:
                quote_text = fake.sentence()
            
            quotes_data.append((
                quote_id, person_id, product_type, premium, status, created_at, valid_until, quote_text
            ))

            # Claims
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
                        claim_id, quote_id, incident_date, report_date, description, claim_amount, claim_status, report_date
                    ))
    
    # Bulk Inserts
    if people_data:
        cur.executemany("INSERT INTO people (id, first_name, last_name, age, risk_score, policy_start_date, active) VALUES (%s,%s,%s,%s,%s,%s,%s)", people_data)
    
    if quotes_data:
        cur.executemany("INSERT INTO quotes (id, person_id, product_type, premium_amount, status, created_at, valid_until, text) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)", quotes_data)

    if claims_data:
        cur.executemany("INSERT INTO claims (id, quote_id, incident_date, report_date, description, claim_amount, status, created_at) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)", claims_data)
    
    conn.commit()
    cur.close()
    conn.close()
    return BATCH_SIZE

def main():
    print(f"🚀 Initializing Population Run: {TARGET_COUNT} entities...")
    start_time = time.time()
    
    total_batches = TARGET_COUNT // BATCH_SIZE
    pool = Pool(PROCESSES)
    
    completed = 0
    for result in pool.imap_unordered(generate_batch, range(total_batches)):
        completed += result
        elapsed = time.time() - start_time
        rate = completed / elapsed
        print(f"✨ Generated {completed:,} rows. Rate: {rate:.0f} rows/sec")
            
    pool.close()
    pool.join()
    print(f"✅ Generation complete in {time.time() - start_time:.2f}s.")

if __name__ == "__main__":
    main()
