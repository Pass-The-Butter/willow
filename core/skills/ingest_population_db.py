"""
Willow Skill: Ingest Population DB
Reads sample data from the Population DB (Postgres) and creates nodes in the Graph.
"""

import os
import psycopg2
from neo4j import GraphDatabase
from typing import Dict, Any

# Postgres Configuration (Xeon Server)
PG_HOST = os.getenv("POSTGRES_HOST", "bunny") # Default to bunny hostname
PG_PORT = os.getenv("POSTGRES_PORT", "5432")
PG_DB = os.getenv("POSTGRES_DB", "population")
PG_USER = os.getenv("POSTGRES_USER", "willow")
PG_PASS = os.getenv("POSTGRES_PASSWORD", "willowdev123")

# Neo4j Configuration
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "willowdev123")

def execute(limit: int = 10) -> Dict[str, Any]:
    """
    Ingest a sample of people and quotes from Postgres to Neo4j.
    
    Args:
        limit: Number of records to ingest (default: 10)
    """
    
    results = {
        "people_ingested": 0,
        "quotes_ingested": 0,
        "errors": []
    }

    try:
        # 1. Connect to Postgres
        pg_conn = psycopg2.connect(
            host=PG_HOST,
            port=PG_PORT,
            dbname=PG_DB,
            user=PG_USER,
            password=PG_PASS
        )
        pg_cur = pg_conn.cursor()

        # 2. Fetch Sample Data (People with Quotes)
        query = """
            SELECT p.id, p.first_name, p.last_name, p.risk_score, 
                   q.id, q.product_type, q.premium_amount, q.status
            FROM people p
            JOIN quotes q ON p.id = q.person_id
            WHERE q.status = 'ISSUED'
            LIMIT %s
        """
        pg_cur.execute(query, (limit,))
        rows = pg_cur.fetchall()
        
        pg_cur.close()
        pg_conn.close()

        if not rows:
            return {"success": True, "message": "No data found in Postgres yet. Is the generator running?", "data": results}

        # 3. Connect to Neo4j
        driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
        
        with driver.session() as session:
            for row in rows:
                p_id, p_first, p_last, p_risk, q_id, q_product, q_premium, q_status = row
                
                # Create Person and Quote nodes
                session.run("""
                    MERGE (p:Person {id: $p_id})
                    SET p.first_name = $p_first,
                        p.last_name = $p_last,
                        p.risk_score = $p_risk,
                        p.source = 'population_db'
                    
                    MERGE (q:Quote {id: $q_id})
                    SET q.product = $q_product,
                        q.premium = $q_premium,
                        q.status = $q_status,
                        q.ingested_at = datetime()
                    
                    MERGE (p)-[:HAS_QUOTE]->(q)
                """, {
                    "p_id": str(p_id), "p_first": p_first, "p_last": p_last, "p_risk": float(p_risk),
                    "q_id": str(q_id), "q_product": q_product, "q_premium": float(q_premium), "q_status": q_status
                })
                
                results["people_ingested"] += 1
                results["quotes_ingested"] += 1

        driver.close()
        return {"success": True, "message": "Ingestion complete", "data": results}

    except Exception as e:
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    # Local test
    print(execute())
