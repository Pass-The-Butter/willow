"""
Willow Neo4j MCP Server
Exposes Neo4j graph operations as MCP tools for Claude
"""

import os
import json
from datetime import datetime
from typing import Any, Dict, List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from neo4j import GraphDatabase
import uvicorn

# Environment configuration
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "willowdev123")
MCP_PORT = int(os.getenv("MCP_PORT", "3001"))

# Initialize FastAPI app
app = FastAPI(title="Willow Neo4j MCP Server", version="0.1.0")

# Neo4j driver
driver = None

def get_driver():
    global driver
    if driver is None:
        driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    return driver

# Pydantic models for request/response
class CypherRequest(BaseModel):
    query: str
    parameters: Optional[Dict[str, Any]] = {}
    log_execution: bool = True

class SkillExecutionRequest(BaseModel):
    name: str
    parameters: Optional[Dict[str, Any]] = {}

class Response(BaseModel):
    success: bool
    data: Optional[Any] = None
    error: Optional[str] = None

# Helper to log executions to graph
def log_query_execution(query: str, parameters: dict, result_count: int):
    """Log query execution as :ExecutionLog node in graph"""
    try:
        log_query = """
        CREATE (log:ExecutionLog {
            query: $query,
            parameters: $parameters,
            result_count: $result_count,
            executed_at: datetime(),
            executed_by: 'claude-mcp'
        })
        RETURN log
        """
        with get_driver().session() as session:
            session.run(log_query, {
                "query": query,
                "parameters": json.dumps(parameters),
                "result_count": result_count
            })
    except Exception as e:
        print(f"Failed to log execution: {e}")

@app.get("/")
def root():
    return {"service": "Willow Neo4j MCP Server", "status": "running", "version": "0.1.0"}

@app.get("/health")
def health_check():
    """Health check endpoint"""
    try:
        with get_driver().session() as session:
            result = session.run("RETURN 1 as num")
            result.single()
        return {"status": "healthy", "neo4j": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "neo4j": str(e)}

@app.post("/tools/run_cypher", response_model=Response)
def run_cypher(request: CypherRequest):
    """
    Execute arbitrary Cypher query against Neo4j
    Returns results as list of dictionaries
    """
    try:
        with get_driver().session() as session:
            result = session.run(request.query, request.parameters)
            records = [dict(record) for record in result]

            if request.log_execution:
                log_query_execution(request.query, request.parameters, len(records))

            return Response(success=True, data=records)
    except Exception as e:
        return Response(success=False, error=str(e))

@app.post("/tools/get_skills", response_model=Response)
def get_skills():
    """
    Query all available skills from the graph
    Returns skill nodes with their metadata
    """
    query = """
    MATCH (s:Skill)
    RETURN s.name as name,
           s.language as language,
           s.description as description,
           s.code_path as code_path,
           s.query_template as query_template,
           s.mcp_compatible as mcp_compatible
    ORDER BY s.name
    """
    try:
        with get_driver().session() as session:
            result = session.run(query)
            skills = [dict(record) for record in result]
            log_query_execution(query, {}, len(skills))
            return Response(success=True, data=skills)
    except Exception as e:
        return Response(success=False, error=str(e))

@app.post("/tools/execute_skill", response_model=Response)
def execute_skill(request: SkillExecutionRequest):
    """
    Execute a skill by name
    For Cypher skills: runs the query template with provided parameters
    For Python skills: delegates to willow-api service
    """
    try:
        # First, fetch the skill from graph
        skill_query = """
        MATCH (s:Skill {name: $name})
        RETURN s.language as language,
               s.query_template as query_template,
               s.code_path as code_path
        """
        with get_driver().session() as session:
            result = session.run(skill_query, {"name": request.name})
            skill = result.single()

            if not skill:
                return Response(success=False, error=f"Skill '{request.name}' not found")

            # Handle Cypher skills
            if skill["language"] == "cypher":
                query_template = skill["query_template"]
                result = session.run(query_template, request.parameters)
                records = [dict(record) for record in result]
                log_query_execution(query_template, request.parameters, len(records))
                return Response(success=True, data=records)

            # Handle Python skills (would delegate to willow-api)
            elif skill["language"] == "python":
                return Response(
                    success=False,
                    error="Python skill execution not yet implemented - use willow-api service"
                )

            else:
                return Response(success=False, error=f"Unsupported skill language: {skill['language']}")

    except Exception as e:
        return Response(success=False, error=str(e))

@app.post("/tools/get_brand_assets", response_model=Response)
def get_brand_assets(season: Optional[str] = None, active_only: bool = True):
    """
    Retrieve brand assets from graph
    Optionally filter by season and active status
    """
    query_parts = ["MATCH (b:BrandAsset)"]
    params = {}

    if active_only:
        query_parts.append("WHERE b.active = true")

    if season:
        if active_only:
            query_parts.append("AND b.season = $season")
        else:
            query_parts.append("WHERE b.season = $season")
        params["season"] = season

    query_parts.append("RETURN b")
    query = " ".join(query_parts)

    try:
        with get_driver().session() as session:
            result = session.run(query, params)
            assets = [dict(record["b"]) for record in result]
            log_query_execution(query, params, len(assets))
            return Response(success=True, data=assets)
    except Exception as e:
        return Response(success=False, error=str(e))

@app.on_event("shutdown")
def shutdown_event():
    """Close Neo4j driver on shutdown"""
    global driver
    if driver:
        driver.close()

if __name__ == "__main__":
    print(f"Starting Willow Neo4j MCP Server on port {MCP_PORT}")
    print(f"Connecting to Neo4j at {NEO4J_URI}")
    uvicorn.run(app, host="0.0.0.0", port=MCP_PORT)
