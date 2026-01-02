"""
Willow Skill: Client for Graphiti Service
Connects to the Graphiti Service running on port 8002 via MCP (SSE).
"""

import aiohttp
import asyncio
import os
import json

GRAPHITI_URL = os.getenv("GRAPHITI_URL", "http://localhost:8002")

async def add_event_async(event_text: str, entities: list = []):
    """
    Async implementation of adding an event via Graphiti MCP.
    """
    async with aiohttp.ClientSession() as session:
        # Standard MCP JSON-RPC 2.0 via HTTP Post (if supported by server.py)
        # Note: My server.py set up /messages for POST.
        
        payload = {
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {
                "name": "add_event",
                "arguments": {
                    "text": event_text,
                    "entities": entities
                }
            },
            "id": 1
        }
        
        async with session.post(f"{GRAPHITI_URL}/messages", json=payload) as resp:
            return await resp.json()

def add_event(event_text: str, entities: list = []) -> dict:
    """
    Synchronous wrapper for adding an event.
    """
    try:
        return asyncio.run(add_event_async(event_text, entities))
    except Exception as e:
        return {"success": False, "error": str(e)}

async def search_facts_async(query: str):
    async with aiohttp.ClientSession() as session:
        payload = {
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {
                "name": "search_facts",
                "arguments": {
                    "query": query
                }
            },
            "id": 2
        }
        async with session.post(f"{GRAPHITI_URL}/messages", json=payload) as resp:
            return await resp.json()

def search_facts(query: str) -> dict:
    try:
        return asyncio.run(search_facts_async(query))
    except Exception as e:
        return {"success": False, "error": str(e)}
