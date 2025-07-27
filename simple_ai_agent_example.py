#!/usr/bin/env python3
"""
Simple AI Agent Example with SecureAI Protection
This shows the basic usage for protecting AI agents.
"""

from secureai_agent_shield import SecureAIAgentShield, AgentType, ProtectionLevel

# Example 1: Customer Service AI Agent
@SecureAIAgentShield(
    agent_type=AgentType.CUSTOMER_SERVICE,
    protection_level=ProtectionLevel.COMPREHENSIVE
).protect_agent
def customer_service_agent(customer_data):
    """This AI agent handles customer inquiries with automatic PII protection."""
    name = customer_data.get("name", "Unknown")
    email = customer_data.get("email", "unknown@example.com")
    phone = customer_data.get("phone", "555-0000")
    
    response = f"Hello {name}, I'll contact you at {email} or {phone} to help with your inquiry."
    return response

# Example 2: Data Analysis AI Agent
@SecureAIAgentShield(
    agent_type=AgentType.DATA_ANALYSIS,
    protection_level=ProtectionLevel.ENTERPRISE
).protect_agent
def data_analysis_agent(analysis_data):
    """This AI agent analyzes data with automatic protection of sensitive information."""
    database_url = analysis_data.get("database_url", "")
    api_key = analysis_data.get("api_key", "")
    
    result = {
        "status": "completed",
        "database_used": database_url,
        "api_key_used": api_key,
        "data_points": 1000
    }
    return result

# Example 3: Financial AI Agent
@SecureAIAgentShield(
    agent_type=AgentType.FINANCIAL,
    protection_level=ProtectionLevel.ENTERPRISE
).protect_agent
def financial_agent(transaction_data):
    """This AI agent processes financial transactions with automatic protection."""
    account = transaction_data.get("account_number", "")
    credit_card = transaction_data.get("credit_card", "")
    
    result = {
        "transaction_id": "TXN-12345",
        "account_number": account,
        "credit_card": credit_card,
        "status": "processed"
    }
    return result

def main():
    """Run the simple AI agent examples."""
    print("SecureAI Agent Protection - Simple Examples")
    print("="*50)
    
    # Test Customer Service Agent
    print("\n1. Customer Service AI Agent:")
    customer_data = {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "phone": "555-123-4567"
    }
    print("Input:", customer_data)
    result = customer_service_agent(customer_data)
    print("Output:", result)
    
    # Test Data Analysis Agent
    print("\n2. Data Analysis AI Agent:")
    analysis_data = {
        "database_url": "mysql://admin:password123@prod-db.company.com/analytics",
        "api_key": "sk-1234567890abcdefghijklmnopqrstuvwxyz"
    }
    print("Input:", analysis_data)
    result = data_analysis_agent(analysis_data)
    print("Output:", result)
    
    # Test Financial Agent
    print("\n3. Financial AI Agent:")
    transaction_data = {
        "account_number": "9876543210",
        "credit_card": "4111-1111-1111-1111"
    }
    print("Input:", transaction_data)
    result = financial_agent(transaction_data)
    print("Output:", result)
    
    print("\n" + "="*50)
    print("All AI agents are now protected with SecureAI!")
    print("Notice how sensitive data is automatically masked in the outputs.")

if __name__ == "__main__":
    main() 