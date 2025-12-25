"""
Willow API
Skill execution environment for Python-based skills
"""

import os
import sys
import importlib.util
from typing import Any, Dict, Optional
from pathlib import Path
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

# Add skills directory to Python path
SKILLS_DIR = Path("/app/skills")
sys.path.insert(0, str(SKILLS_DIR))

# Initialize FastAPI app
app = FastAPI(title="Willow API", version="0.1.0")

# Request/Response models
class SkillExecutionRequest(BaseModel):
    skill_name: str
    parameters: Optional[Dict[str, Any]] = {}

class SkillExecutionResponse(BaseModel):
    success: bool
    result: Optional[Any] = None
    error: Optional[str] = None
    skill_name: str

def load_skill(skill_name: str):
    """
    Dynamically load a Python skill module

    Args:
        skill_name: Name of the skill (e.g., 'hello_world')

    Returns:
        Loaded module
    """
    skill_path = SKILLS_DIR / f"{skill_name}.py"

    if not skill_path.exists():
        raise FileNotFoundError(f"Skill '{skill_name}' not found at {skill_path}")

    spec = importlib.util.spec_from_file_location(skill_name, skill_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load skill '{skill_name}'")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return module

@app.get("/")
def root():
    return {
        "service": "Willow API",
        "version": "0.1.0",
        "description": "Skill execution environment"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/skills")
def list_skills():
    """
    List all available Python skills
    """
    if not SKILLS_DIR.exists():
        return {"skills": []}

    skills = []
    for skill_file in SKILLS_DIR.glob("*.py"):
        if skill_file.name.startswith("__"):
            continue
        skills.append(skill_file.stem)

    return {"skills": sorted(skills)}

@app.post("/execute", response_model=SkillExecutionResponse)
def execute_skill(request: SkillExecutionRequest):
    """
    Execute a Python skill by name

    Args:
        request: SkillExecutionRequest with skill_name and parameters

    Returns:
        SkillExecutionResponse with result or error
    """
    try:
        # Load the skill module
        skill_module = load_skill(request.skill_name)

        # Check if execute function exists
        if not hasattr(skill_module, 'execute'):
            raise AttributeError(f"Skill '{request.skill_name}' does not have an 'execute' function")

        # Execute the skill
        result = skill_module.execute(**request.parameters)

        return SkillExecutionResponse(
            success=True,
            result=result,
            skill_name=request.skill_name
        )

    except FileNotFoundError as e:
        return SkillExecutionResponse(
            success=False,
            error=str(e),
            skill_name=request.skill_name
        )

    except Exception as e:
        return SkillExecutionResponse(
            success=False,
            error=f"{type(e).__name__}: {str(e)}",
            skill_name=request.skill_name
        )

@app.post("/execute/{skill_name}")
def execute_skill_by_path(skill_name: str, parameters: Optional[Dict[str, Any]] = None):
    """
    Execute a skill via path parameter (alternative endpoint)

    Args:
        skill_name: Name of the skill to execute
        parameters: Optional parameters dict

    Returns:
        Skill execution result
    """
    request = SkillExecutionRequest(
        skill_name=skill_name,
        parameters=parameters or {}
    )
    return execute_skill(request)

if __name__ == "__main__":
    print("Starting Willow API on port 8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)
