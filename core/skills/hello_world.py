"""
Willow Skill: Hello World
First skill - proves the system works
"""

def execute(name: str = "World") -> dict:
    """
    Simple greeting skill to verify Willow is operational

    Args:
        name: Name to greet (default: "World")

    Returns:
        dict with greeting message and metadata
    """
    message = f"Hello, {name}! Willow is alive."

    return {
        "success": True,
        "message": message,
        "skill": "hello_world",
        "version": "0.1.0"
    }

if __name__ == "__main__":
    # Test the skill
    result = execute("Peter")
    print(result)
