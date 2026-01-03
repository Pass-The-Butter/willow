import os
import random
import uuid
import psycopg2
import time
from faker import Faker

# Configuration
DB_HOST = os.getenv("DB_HOST", "agilemesh-postgres")
DB_PORT = "5432"
DB_NAME = "population"
DB_USER = "willow"
DB_PASS = "willowdev123"

def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )

def test_run():
    print("Testing basic DB connectivity...")
    conn = get_connection()
    cur = conn.cursor()
    
    start_time = time.time()
    fake = Faker('en_GB')
    
    print("Inserting 100 test people...")
    for _ in range(100):
        person_id = str(uuid.uuid4())
        cur.execute("""
            INSERT INTO people (id, first_name, last_name, age, risk_score, policy_start_date, active)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (person_id, fake.first_name(), fake.last_name(), random.randint(18, 90), random.random(), fake.date_between(start_date='-5y', end_date='today'), True))
        
    conn.commit()
    elapsed = time.time() - start_time
    print(f"✅ Success! 100 people inserted in {elapsed:.2f}s.")
    
    cur.close()
    conn.close()

if __name__ == "__main__":
    test_run()
