#!/usr/bin/env python3
"""
Simple test for DataGuard components
"""

from dataguard_agent_shield import DataGuardAgentShield, AgentType, ProtectionLevel

def test_dataguard_agent_shield():
    """Test the DataGuard Agent Shield functionality."""
    print("Testing DataGuard Agent Shield...")
    
    @DataGuardAgentShield(
        agent_type=AgentType.CUSTOMER_SERVICE,
        protection_level=ProtectionLevel.STANDARD
    ).protect_agent
    def test_agent(text):
        return f"Processed: {text}"
    
    test_text = "My email is john.doe@company.com and my phone is 555-123-4567"
    result = test_agent(test_text)
    
    print(f"Original: {test_text}")
    print(f"Protected: {result}")
    
    # Check if protection worked
    if "john.doe@company.com" not in result and "555-123-4567" not in result:
        print("✓ DataGuard protection works correctly!")
        return True
    else:
        print("✗ DataGuard protection failed")
        return False

if __name__ == "__main__":
    print("DataGuard Test")
    print("=" * 30)
    test_dataguard_agent_shield() 