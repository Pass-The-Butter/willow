"""
Willow Skill: Check Population Progress
Query the Postgres database on Bunny to check population generation progress
"""

import psycopg2
import os

DB_HOST = os.getenv("PG_HOST", "bunny")
DB_PORT = os.getenv("PG_PORT", "5432")
DB_NAME = os.getenv("PG_DB", "population")
DB_USER = os.getenv("PG_USER", "willow")
DB_PASS = os.getenv("PG_PASS", "willowdev123")

def execute() -> dict:
    """
    Check the population database for current entity counts
    
    Returns:
        dict with counts of people, quotes, and claims
    """
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASS
        )
        cur = conn.cursor()
        
        # Count people
        cur.execute("SELECT COUNT(*) FROM people")
        people_count = cur.fetchone()[0]
        
        # Count quotes
        cur.execute("SELECT COUNT(*) FROM quotes")
        quotes_count = cur.fetchone()[0]
        
        # Count claims
        cur.execute("SELECT COUNT(*) FROM claims")
        claims_count = cur.fetchone()[0]
        
        # Get latest person
        cur.execute("SELECT first_name, last_name, age FROM people ORDER BY policy_start_date DESC LIMIT 1")
        latest = cur.fetchone()
        
        cur.close()
        conn.close()
        
        return {
            "success": True,
            "people": people_count,
            "quotes": quotes_count,
            "claims": claims_count,
            "target": 100_000_000,
            "progress_pct": round((people_count / 100_000_000) * 100, 4),
            "latest_person": f"{latest[0]} {latest[1]}, age {latest[2]}" if latest else None
        }
        
    except Exception as e:
        return {"success": False, "error": str(e)}
