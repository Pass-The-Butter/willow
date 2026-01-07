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
from dotenv import load_dotenv

load_dotenv()

# Configuration
DB_HOST = os.getenv("PG_HOST", "bunny")
DB_PORT = os.getenv("PG_PORT", "5432")
DB_NAME = os.getenv("PG_DB", "population")
DB_USER = os.getenv("PG_USER", "willow")
DB_PASS = os.getenv("PG_PASS", "willowdev123")

# Ollama Configuration (Frank)
OLLAMA_URL = "http://frank.clouded-newton.ts.net:11434/api/generate"
OLLAMA_MODEL = "deepseek-r1:32b"
USE_LLM_FOR_QUOTES = False 

TARGET_COUNT = 5000  # Customers
BATCH_SIZE = 50 
PROCESSES = 4 

fake = Faker('en_GB') 

DOG_BREEDS = ['Labrador', 'Cocker Spaniel', 'French Bulldog', 'Golden Retriever', 'German Shepherd', 'Pug', 'Beagle', 'Staffordshire Bull Terrier']
CAT_BREEDS = ['British Shorthair', 'Persian', 'Maine Coon', 'Siamese', 'Ragdoll', 'Bengal', 'Sphynx']

def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )

def generate_batch(batch_id):
    conn = get_connection()
    cur = conn.cursor()
    
    customers_data = []
    pets_data = []
    quotes_data = []

    for _ in range(BATCH_SIZE):
        # Customer
        full_name = fake.name()
        email = f"{fake.user_name()}_{uuid.uuid4().hex[:6]}@{fake.free_email_domain()}"
        phone = fake.phone_number()
        address1 = fake.street_address()
        address2 = fake.secondary_address() if random.random() > 0.7 else None
        city = fake.city()
        postcode = fake.postcode()
        dob = fake.date_of_birth(minimum_age=18, maximum_age=80)
        segment = random.choice(['dog_person', 'cat_person', 'multi_pet', 'first_time_owner'])
        
        # We'll use a placeholder for the vector (384 dimensions)
        # In a real scenario, we'd generate this with an embedding model
        # For now, NULL is fine as per schema allows it
        
        cur.execute("""
            INSERT INTO customers (full_name, email, phone_mobile, address_line_1, address_line_2, city, postcode, date_of_birth, marketing_segment)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        """, (full_name, email, phone, address1, address2, city, postcode, dob, segment))
        
        customer_id = cur.fetchone()[0]

        # Pets
        num_pets = random.randint(1, 2)
        for _ in range(num_pets):
            pet_name = fake.first_name()
            species = random.choice(['Dog', 'Cat'])
            breed = random.choice(DOG_BREEDS if species == 'Dog' else CAT_BREEDS)
            pet_dob = fake.date_between(start_date='-12y', end_date='today')
            gender = random.choice(['Male', 'Female'])
            chipped = random.random() > 0.3
            acquired = pet_dob + timedelta(days=random.randint(0, 30))
            
            cur.execute("""
                INSERT INTO pets (customer_id, pet_name, species, breed, date_of_birth, gender, microchipped, acquired_date)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id
            """, (customer_id, pet_name, species, breed, pet_dob, gender, chipped, acquired))
            
            pet_id = cur.fetchone()[0]

            # Quotes
            num_quotes = random.randint(1, 2)
            for _ in range(num_quotes):
                cover_type = random.choice(['Accident Only', 'Time Limited', 'Lifetime'])
                excess = random.choice([0, 99, 149, 199])
                limit = random.choice([2000, 4000, 7000, 12000])
                monthly = round(random.uniform(10, 50), 2)
                annual = round(monthly * 11, 2) # Slight discount for annual
                status = random.choice(['generated', 'accepted', 'rejected', 'expired'])
                
                quotes_data.append((
                    customer_id, pet_id, cover_type, excess, limit, monthly, annual, status
                ))

    if quotes_data:
        cur.executemany("""
            INSERT INTO quotes (customer_id, pet_id, cover_type, excess_amount, vet_fee_limit, monthly_premium, annual_premium, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, quotes_data)
    
    conn.commit()
    cur.close()
    conn.close()
    return BATCH_SIZE

def main():
    print(f"🚀 Initializing Population Run: {TARGET_COUNT} customers...")
    start_time = time.time()
    
    total_batches = TARGET_COUNT // BATCH_SIZE
    pool = Pool(PROCESSES)
    
    completed = 0
    # Use batch_id as an index for imap_unordered
    for result in pool.imap_unordered(generate_batch, range(total_batches)):
        completed += result
        elapsed = time.time() - start_time
        rate = completed / elapsed
        print(f"✨ Generated {completed:,} customers. Rate: {rate:.1f} customers/sec")
            
    pool.close()
    pool.join()
    print(f"✅ Generation complete in {time.time() - start_time:.2f}s.")

if __name__ == "__main__":
    main()
