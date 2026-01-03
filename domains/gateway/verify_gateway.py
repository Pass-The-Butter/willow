"""
Gateway Verification Script
===========================
Tests the Gateway components locally (Mocking the server if not running, or testing Logic).
"""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.parent
sys.path.append(str(REPO_ROOT))

from domains.gateway.policy import PolicyEnforcer

def test_policy_logic():
    print("🧪 Testing Policy Logic...")
    enforcer = PolicyEnforcer()
    
    # Test 1: Allowed Query
    q1 = "MATCH (n) RETURN n"
    check1 = enforcer.check_query(q1)
    if check1['allowed']:
        print("  ✅ Access Query allowed")
    else:
        print(f"  ❌ Access Query blocked: {check1['reason']}")

    # Test 2: Forbidden Query
    q2 = "MATCH (n) DETACH DELETE n"
    check2 = enforcer.check_query(q2)
    if not check2['allowed']:
        print("  ✅ DELETE Query correctly blocked")
    else:
        print("  ❌ DELETE Query wrongly allowed!")

    # Test 3: Drop
    q3 = "CALL dbms.functions()"
    check3 = enforcer.check_query(q3)
    if not check3['allowed']:
        print("  ✅ CALL dbms blocked")
    else:
        print("  ❌ CALL dbms allowed!")

if __name__ == "__main__":
    test_policy_logic()
