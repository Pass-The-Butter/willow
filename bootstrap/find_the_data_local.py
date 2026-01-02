import psycopg2
import sys

USER = "willow"
PASS = "willowdev123"
DB = "population"
HOST = "127.0.0.1"

def check_port(port):
    print(f"Checking Port {port}...")
    try:
        conn = psycopg2.connect(host=HOST, port=port, dbname=DB, user=USER, password=PASS, connect_timeout=3)
        cur = conn.cursor()
        cur.execute("SELECT count(*) FROM people;")
        count = cur.fetchone()[0]
        print(f"✅ FOUND DB on Port {port}! Count: {count}")
        conn.close()
        return count
    except Exception as e:
        print(f"❌ Port {port} failed: {e}")
        return -1

# Check mapped ports
for p in [5434, 5435]:
    check_port(p)
