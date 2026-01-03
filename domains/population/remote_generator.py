import os
import random
import uuid
import psycopg2
import time
import json
import secrets
from faker import Faker
from multiprocessing import Pool
from datetime import datetime, timedelta

# Configuration
DB_HOST = "bunny" # Connect to Xeon Server (via Tailscale)
DB_PORT = "5432"
DB_NAME = "population"
DB_USER = "willow"
DB_PASS = "willowdev123"

TARGET_COUNT = 1000 # Generate 1k for test
BATCH_SIZE = 50
PROCESSES = 2

fake = Faker('en_GB') # Strict UK Locale

def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )

def generate_random_vector(dim=384):
    """Generate a random normalized vector."""
    vec = [random.gauss(0, 1) for _ in range(dim)]
    mag = sum(x*x for x in vec) ** 0.5
    return [x/mag for x in vec]

def generate_customer_batch(batch_id):
    conn = get_connection()
    cur = conn.cursor()
    
    # Pre-defined lists for consistency
    MARKETING_SEGMENTS = ['Budget Focused', 'Premium Protection', 'Tech Savvy', 'Elderly/Traditional', 'Family Guard']
    DOG_BREEDS = ['Labrador', 'Cocker Spaniel', 'French Bulldog', 'Cockapoo', 'Dachshund', 'Staffordshire Bull Terrier', 'Golden Retriever', 'German Shepherd']
    CAT_BREEDS = ['Domestic Short Hair', 'Domestic Long Hair', 'British Shorthair', 'Ragdoll', 'Maine Coon', 'Siamese', 'Persian']
    
    generated_count = 0
    
    try:
        for _ in range(BATCH_SIZE):
            # --- CUSTOMER ---
            full_name = fake.name()
            # unique email logic: name + random chars
            slug = full_name.lower().replace(' ', '.') + '.' + secrets.token_hex(3)
            email = f"{slug}@example.com"
            
            customer_data = (
                full_name,
                email,
                fake.phone_number(),
                fake.building_number() + " " + fake.street_name(),
                fake.secondary_address(),
                fake.city(),
                fake.postcode(),
                fake.date_of_birth(minimum_age=18, maximum_age=90),
                json.dumps(generate_random_vector(384)), # Pass as JSON string for vector? Or list? Psycopg2 list usually converts to array syntax {1,2}, vector needs [1,2]. String is safest.
                random.choice(MARKETING_SEGMENTS)
            )
            
            # Using RETURNING id to handle the SERIAL pkey
            cur.execute("""
                INSERT INTO customers 
                (full_name, email, phone_mobile, address_line_1, address_line_2, city, postcode, date_of_birth, personality_vector, marketing_segment)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id;
            """, customer_data)
            
            customer_id = cur.fetchone()[0]
            generated_count += 1
            
            # --- PETS (0 to 3 per customer) ---
            num_pets = random.choices([0, 1, 2, 3], weights=[0.1, 0.6, 0.2, 0.1])[0]
            
            for _ in range(num_pets):
                species = random.choice(['Dog', 'Cat'])
                breed = random.choice(DOG_BREEDS if species == 'Dog' else CAT_BREEDS)
                dob = fake.date_of_birth(maximum_age=15)
                acquired = fake.date_between(start_date=dob, end_date='today')
                
                pet_data = (
                    customer_id,
                    fake.first_name(),
                    species,
                    breed,
                    dob,
                    random.choice(['Male', 'Female']),
                    random.choice([True, False]), # Microchipped
                    json.dumps([]), # No conditions for now
                    acquired
                )
                
                cur.execute("""
                    INSERT INTO pets
                    (customer_id, pet_name, species, breed, date_of_birth, gender, microchipped, pre_existing_conditions, acquired_date)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
                """, pet_data)

        conn.commit()
    except Exception as e:
        print(f"Batch failed: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()
        
    return generated_count

def main():
    print(f"Starting generation of {TARGET_COUNT} customers using {PROCESSES} processes...")
    start_time = time.time()
    
    total_batches = TARGET_COUNT // BATCH_SIZE
    pool = Pool(PROCESSES)
    
    completed = 0
    # imap_unordered is good for progress bars
    for result in pool.imap_unordered(generate_customer_batch, range(total_batches)):
        completed += result
        elapsed = time.time() - start_time
        if elapsed > 0:
            rate = completed / elapsed
            print(f"Generated {completed} customers. Rate: {rate:.1f}/sec")
            
    pool.close()
    pool.join()
    print("✓ Generation complete.")

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    main()
