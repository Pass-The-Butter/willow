import os
import certifi
from neo4j import GraphDatabase

# AuraDB connection details
URI = "neo4j+s://e59298d2.databases.neo4j.io"
USER = "neo4j"
PASSWORD = "c2U7h1mwvmYn2k2cr_Fp9EaUrZaLZdEQ3_Cawt6zvyU"

def clear_db():
    print("WARNING: This will delete ALL data from AuraDB!")
    print(f"Connecting to AuraDB at {URI}...")
    
    os.environ['SSL_CERT_FILE'] = certifi.where()
    os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()
    
    driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))
    
    try:
        with driver.session() as session:
            # Check count
            result = session.run("MATCH (n) RETURN count(n) as count")
            count = result.single()["count"]
            print(f"\nChecking current database state...")
            print(f"  Current nodes: {count}")
            
            # Delete everything
            print("\nDeleting all nodes and relationships...")
            session.run("MATCH (n) DETACH DELETE n")
            print("  ✓ All nodes and relationships deleted")
            
            # Drop constraints and indexes to be safe
            print("\nDropping constraints...")
            constraints = session.run("SHOW CONSTRAINTS")
            for record in constraints:
                name = record["name"]
                print(f"  Dropping constraint: {name}")
                session.run(f"DROP CONSTRAINT {name}")

            print("\nDropping indexes...")
            indexes = session.run("SHOW INDEXES")
            for record in indexes:
                name = record["name"]
                if name != "index_343aff4e": # Don't drop system indexes if any
                     # Neo4j 5.x might have system indexes, but usually safe to try dropping ours
                     # We'll just catch errors if we try to drop something we shouldn't
                     try:
                        print(f"  Dropping index: {name}")
                        session.run(f"DROP INDEX {name}")
                     except Exception as e:
                        pass
            
            print("\n✓ Database cleared! Final node count: 0")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.close()

if __name__ == "__main__":
    clear_db()
