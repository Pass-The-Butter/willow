
def classify_intent(messages: list) -> dict:
    """
    Analyzes the chat history to determine intent and research depth.
    Returns: dict {"depth": int [1-5], "intent": str}
    """
    if not messages:
        return {"depth": 1, "intent": "chat"}
        
    last_msg = messages[-1]['content'].lower()
    
    # 1. High Depth Indicators (Research/Governor)
    high_keywords = [
        "research", "deep dive", "policy", "governance", 
        "architecture", "audit", "long term", "comprehensive"
    ]
    if any(k in last_msg for k in high_keywords):
        return {"depth": 4, "intent": "research"}
        
    # 2. Medium Depth Indicators (Debugging/Validation)
    medium_keywords = [
        "debug", "fix", "why is", "error", "fail", "broken", 
        "validate", "verify"
    ]
    if any(k in last_msg for k in medium_keywords):
        return {"depth": 3, "intent": "debug"}
        
    # 3. Low Depth (Chat)
    return {"depth": 1, "intent": "chat"}
