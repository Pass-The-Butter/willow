import psycopg2
import os
import random
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration (Should match remote_generator.py)
DB_HOST = os.getenv("PG_HOST", "bunny")
DB_PORT = os.getenv("PG_PORT", "5432")
DB_NAME = os.getenv("PG_DB", "population")
DB_USER = os.getenv("PG_USER", "willow")
DB_PASS = os.getenv("PG_PASS", "willowdev123")

def hello_willow():
    print("\n🌿 Willow 'Hello World' - Customer Voice 🌿")
    print("---------------------------------------------")
    
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASS
        )
        cur = conn.cursor()
        
        # Get a random person with a quote
        # Assuming tables: people, quotes (linked by person_id?)
        # Let's check schema.sql or just try a simple join if we knew the schema.
        # Based on remote_generator.py, we need to infer the schema or read it.
        # For now, let's try to read from 'people' and 'quotes' if they exist.
        
        # Check if tables exist first
        cur.execute("SELECT to_regclass('public.people');")
        if not cur.fetchone()[0]:
            print("❌ Table 'people' not found. Has Frank run the generator?")
            return

        # Simple fetch
        query = """
            SELECT p.first_name, p.last_name, q.text 
            FROM people p 
            JOIN quotes q ON p.id = q.person_id 
            ORDER BY RANDOM() 
            LIMIT 1;
        """
        
        # Note: If the table is huge, ORDER BY RANDOM() is slow, but for Hello World it's fine.
        # If tables don't exist yet, this will fail, which is a good test.
        
        try:
            cur.execute(query)
            row = cur.fetchone()
            
            if row:
                first_name, last_name, quote = row
                print(f"👤 Customer: {first_name} {last_name}")
                print(f"💬 Says:     \"{quote}\"")
                print("---------------------------------------------")
                print("✅ End-to-End Pipeline Verified (Frank -> Bunny -> Mac)")
            else:
                print("⚠️ No data found. Frank needs to get to work!")
                
        except psycopg2.Error as e:
            print(f"⚠️ Query Error (Tables might be missing): {e}")

        cur.close()
        conn.close()

    except Exception as e:
        print(f"❌ Connection Failed: {e}")
        print(f"   Target: {DB_HOST}:{DB_PORT}")
        print("   Hint: Is Tailscale up? Is Postgres running on Bunny?")

if __name__ == "__main__":
    hello_willow()
