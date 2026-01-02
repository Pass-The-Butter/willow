FROM python:3.11-slim

WORKDIR /app

# Install git (often needed for pip installing from git)
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Install Graphiti and dependencies
# Note: Graphiti is often installed via git as pypi release might lag
RUN pip install "graphiti-core" "mcp" "neo4j" "openai"

# Copy custom server script
COPY server.py /app/server.py

# Expose MCP port (if running via SSE/HTTP)
ENV PORT=8000
EXPOSE 8000

# Run the server
CMD ["python", "server.py"]
