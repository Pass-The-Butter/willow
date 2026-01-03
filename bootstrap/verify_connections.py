import os
import sys
import socket
import psycopg2
from neo4j import GraphDatabase
import requests
import certifi
from dotenv import load_dotenv

# Load environment
load_dotenv()

# Colors
GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"

def check_neo4j():
    uri = os.getenv("NEO4J_URI")
    user = os.getenv("NEO4J_USER")
    password = os.getenv("NEO4J_PASSWORD")
    
    print(f"Checking AuraDB ({uri})...", end=" ")
    try:
        os.environ['SSL_CERT_FILE'] = certifi.where()
        driver = GraphDatabase.driver(uri, auth=(user, password))
        with driver.session() as session:
            result = session.run("RETURN 1 AS num")
            record = result.single()
            if record['num'] == 1:
                print(f"{GREEN}OK{RESET}")
                return True
    except Exception as e:
        print(f"{RED}FAIL{RESET} - {e}")
        return False
    finally:
        if 'driver' in locals():
            driver.close()

def check_postgres():
    host = "bunny"
    port = 5432
    user = "willow" 
    # Try getting pass from env, fallback to redated placeholder (which will fail)
    # The user didn't give me the postgres password in the chat, but it might be in .env
    # valid password is required. 
    password = os.getenv("PG_PASS") or os.getenv("POSTGRES_PASSWORD")
    dbname = "population"
    
    print(f"Checking Postgres (@{host}:{port})...", end=" ")
    
    if not password:
         print(f"{RED}SKIPPED (No Password in env){RESET}")
         return False

    try:
        conn = psycopg2.connect(
            host=host,
            port=port,
            database=dbname,
            user=user,
            password=password,
            connect_timeout=3
        )
        conn.close()
        print(f"{GREEN}OK{RESET}")
        return True
    except Exception as e:
        print(f"{RED}FAIL{RESET} - {e}")
        return False

def check_http_service(name, url):
    print(f"Checking {name} ({url})...", end=" ")
    try:
        response = requests.get(url, timeout=3)
        if response.status_code < 500: # Any non-server-error is "alive"
            print(f"{GREEN}OK ({response.status_code}){RESET}")
            return True
        else:
            print(f"{RED}FAIL (Status {response.status_code}){RESET}")
            return False
    except requests.exceptions.ConnectionError:
        print(f"{RED}FAIL (Connection Refused){RESET}")
        return False
    except Exception as e:
        print(f"{RED}FAIL{RESET} - {e}")
        return False

def check_ping(host):
    print(f"Pinging {host}...", end=" ")
    response = os.system(f"ping -c 1 -W 1 {host} > /dev/null 2>&1")
    if response == 0:
        print(f"{GREEN}OK{RESET}")
        return True
    else:
        print(f"{RED}FAIL{RESET}")
        return False

def main():
    print("--- 🕵️‍♀️ WILLOW CONNECTION DIAGNOSTIC ---")
    
    # 1. Host Reachability
    check_ping("bunny")
    check_ping("frank")
    
    # 2. Database Connectivity
    check_neo4j()
    check_postgres()
    
    # 3. Service Connectivity
    # Graphiti on Bunny port 8002
    check_http_service("Graphiti", "http://bunny:8002/")
    
    # N8N on Bunny port 5678
    check_http_service("N8N", "http://bunny:5678/")
    
    # Dashboard (if running)
    check_http_service("Dashboard", "http://localhost:5001/board")

if __name__ == "__main__":
    main()
