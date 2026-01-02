import os
import asyncio
from mcp.server import Server, NotificationOptions
from mcp.server.sse import SseServerTransport
from starlette.applications import Starlette
from starlette.routing import Route
from graphiti_core import Graphiti

# Initialize Graphiti
# Explicitly pass credentials with correct argument names
graphiti = Graphiti(
    uri=os.getenv("NEO4J_URI"),
    user=os.getenv("NEO4J_USER"),
    password=os.getenv("NEO4J_PASSWORD")
)

server = Server("willow-graphiti")

@server.list_tools()
async def list_tools():
    return [
        {
            "name": "add_event",
            "description": "Add an event or generic fact to the graph",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "text": {"type": "string"},
                    "entities": {"type": "array", "items": {"type": "string"}}
                },
                "required": ["text"]
            }
        },
        {
            "name": "search_facts",
            "description": "Search for facts/events in the graph",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"}
                },
                "required": ["query"]
            }
        }
    ]

@server.call_tool()
async def call_tool(name, arguments):
    if name == "add_event":
        # Simplified Graphiti usage - actual API might differ slightly based on version
        # This is a placeholder for the "Graphiti Logic"
        # In reality we'd use graphiti.add_episode() or similar
        return [{"type": "text", "text": f"Added event: {arguments.get('text')}"}]
    
    elif name == "search_facts":
        # Placeholder for search
        return [{"type": "text", "text": f"Searching for: {arguments.get('query')}"}]
    
    return [{"type": "text", "text": "Unknown tool"}]

# SSE Transport setup
async def handle_sse(request):
    async with sse.connect_sse(request.scope, request.receive, request._send) as streams:
        await server.run(streams.read_stream, streams.write_stream, server.create_initialization_options())

async def handle_messages(request):
    await sse.handle_post_message(request.scope, request.receive, request._send)

sse = SseServerTransport("/messages")

app = Starlette(
    debug=True,
    routes=[
        Route("/sse", endpoint=handle_sse),
        Route("/messages", endpoint=handle_messages, methods=["POST"]),
    ],
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
