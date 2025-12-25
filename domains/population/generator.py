import os
import random
import uuid
import psycopg2
from faker import Faker
from datetime import datetime, timedelta

# Configuration
DB_HOST = "bunny" # Xeon Server
DB_PORT = "5432"
DB_NAME = "population"
DB_USER = "willow"
DB_PASS = "willowdev123"

def generate_people(count=100):
    fake = Faker()
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )
    cur = conn.cursor()
    
    print(f"Generating {count} people...")
    
    for _ in range(count):
        # Logic: Skew towards 25-45 age group
        if random.random() < 0.6:
            age = random.randint(25, 45)
        else:
            age = random.randint(18, 90)
            
        # Logic: Risk score (Beta distribution)
        risk_score = random.betavariate(2, 5) # Skewed towards lower risk
        
        person = {
            "id": str(uuid.uuid4()),
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "age": age,
            "risk_score": round(risk_score, 4),
            "policy_start_date": fake.date_between(start_date='-5y', end_date='today'),
            "active": True
        }
        
        cur.execute("""
            INSERT INTO people (id, first_name, last_name, age, risk_score, policy_start_date, active)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (person["id"], person["first_name"], person["last_name"], person["age"], person["risk_score"], person["policy_start_date"], person["active"]))
        
        # Generate Quotes
        num_quotes = random.randint(1, 3)
        for _ in range(num_quotes):
            quote_id = str(uuid.uuid4())
            product_type = random.choice(['Auto', 'Home', 'Life', 'Cyber'])
            premium = round(random.uniform(500, 5000), 2)
            status = random.choice(['ISSUED', 'ISSUED', 'ISSUED', 'DRAFT', 'REJECTED']) # Skew to ISSUED
            created_at = fake.date_between(start_date='-2y', end_date='today')
            valid_until = created_at + timedelta(days=30)
            
            cur.execute("""
                INSERT INTO quotes (id, person_id, product_type, premium_amount, status, created_at, valid_until)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (quote_id, person["id"], product_type, premium, status, created_at, valid_until))
            
            # Generate Claims for ISSUED quotes
            if status == 'ISSUED' and random.random() < 0.3: # 30% chance of claim
                num_claims = random.randint(1, 2)
                for _ in range(num_claims):
                    claim_id = str(uuid.uuid4())
                    incident_date = fake.date_between(start_date=created_at, end_date='today')
                    report_date = incident_date + timedelta(days=random.randint(0, 10))
                    claim_amount = round(random.uniform(100, 10000), 2)
                    claim_status = random.choice(['FILED', 'INVESTIGATING', 'APPROVED', 'PAID', 'DENIED'])
                    description = fake.sentence()
                    
                    cur.execute("""
                        INSERT INTO claims (id, quote_id, incident_date, report_date, description, claim_amount, status, created_at)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """, (claim_id, quote_id, incident_date, report_date, description, claim_amount, claim_status, report_date))

    conn.commit()
    cur.close()
    conn.close()
    print("✓ Generation complete.")

if __name__ == "__main__":
    # Ensure dependencies: pip install psycopg2-binary faker
    try:
        generate_people()
    except Exception as e:
        print(f"Error: {e}")
