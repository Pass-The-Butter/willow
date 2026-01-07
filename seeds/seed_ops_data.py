from core.clients.graph_client import GraphClient
import random
from datetime import datetime

client = GraphClient(agent_id="Seeder")

def seed_stock():
    print("🌱 Seeding Stock data for Robin...")
    
    # Add some Pending claims
    for i in range(5):
        ref = f"CLM-STOCK-P-{random.randint(1000, 9999)}"
        client.run("""
            CREATE (c:Claim {
                reference_number: $ref,
                status: 'Pending',
                incident_date: date(),
                amount: $amount,
                description: 'Initial assessment required'
            })
        """, parameters={"ref": ref, "amount": random.randint(100, 2000)})
    
    # Add some Under Review claims
    for i in range(3):
        ref = f"CLM-STOCK-R-{random.randint(1000, 9999)}"
        client.run("""
            CREATE (c:Claim {
                reference_number: $ref,
                status: 'Under Review',
                incident_date: date(),
                amount: $amount,
                description: 'Awaiting vet records'
            })
        """, parameters={"ref": ref, "amount": random.randint(100, 2000)})

    print("✅ Seeded 8 new 'Stock' items.")

if __name__ == "__main__":
    seed_stock()
