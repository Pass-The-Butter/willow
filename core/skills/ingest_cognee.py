"""
Willow Skill: Ingest Context via Cognee (Context Augmentation)
Uses local Cognee library to ingest documents and 'cognify' them into the Neo4j Graph.
"""

import os
import asyncio
import starlette.status
if not hasattr(starlette.status, "HTTP_422_UNPROCESSABLE_CONTENT"):
    starlette.status.HTTP_422_UNPROCESSABLE_CONTENT = starlette.status.HTTP_422_UNPROCESSABLE_ENTITY

import cognee
from cognee.api.v1.cognify.cognify import cognify
from core.utils.credentials import get_neo4j_auth
from dotenv import load_dotenv

load_dotenv()

async def execute_async(file_path: str, dataset_name: str = "willow_context"):
    """
    Ingest a file using Cognee and cognify it into the graph.
    """
    if not os.path.exists(file_path):
        return {"success": False, "error": f"File not found: {file_path}"}
    
    try:
        print(f"🧠 Cognee: Ingesting {file_path}...")
        
        # Add data to Cognee
        await cognee.add(file_path, dataset_name)
        
        # Cognify (Process) - this extracts entities and relations
        print("🧠 Cognee: Cognifying (Extracting Knowledge Graph)...")
        await cognify(dataset_name)
        
        return {
            "success": True, 
            "message": f"Successfully ingested {file_path}",
            "dataset": dataset_name
        }
        
    except Exception as e:
        return {"success": False, "error": str(e)}

def execute(file_path: str):
    return asyncio.run(execute_async(file_path))

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        print(execute(sys.argv[1]))
    else:
        # Test mode
        with open("test_context.txt", "w") as f:
            f.write("Willow is an advanced AI agent system. Peter is the Captain.")
        print(execute("test_context.txt"))
