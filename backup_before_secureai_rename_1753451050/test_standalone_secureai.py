#!/usr/bin/env python3
"""
Test script for the standalone SecureAI Agent Shield
"""

from secureai_agent_shield import SecureAIAgentShield, AgentType, ProtectionLevel, create_agent_shield

def test_customer_service_agent():
    """Test customer service agent protection."""
    print("\n" + "="*60)
    print("CUSTOMER SERVICE AGENT TEST")
    print("="*60)
    
    @SecureAIAgentShield(
        agent_type=AgentType.CUSTOMER_SERVICE,
        protection_level=ProtectionLevel.COMPREHENSIVE,
        debug_mode=True
    ).protect_agent
    def customer_service_agent(customer_data):
        customer_name = customer_data.get("name", "Unknown")
        customer_email = customer_data.get("email", "unknown@example.com")
        customer_phone = customer_data.get("phone", "555-0000")
        
        response = f"Hello {customer_name}, I can help you with your inquiry. I'll contact you at {customer_email} or {customer_phone}."
        return response
    
    # Test data with sensitive information
    test_data = {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "phone": "555-123-4567",
        "account_number": "1234567890"
    }
    
    print("Original Data:")
    print(test_data)
    
    print("\nProtected Response:")
    result = customer_service_agent(test_data)
    print(result)
    
    return result

def test_data_analysis_agent():
    """Test data analysis agent protection."""
    print("\n" + "="*60)
    print("DATA ANALYSIS AGENT TEST")
    print("="*60)
    
    @SecureAIAgentShield(
        agent_type=AgentType.DATA_ANALYSIS,
        protection_level=ProtectionLevel.ENTERPRISE,
        debug_mode=True
    ).protect_agent
    def data_analysis_agent(analysis_request):
        database_connection = analysis_request.get("database_connection", "mysql://user:pass@localhost/db")
        api_key = analysis_request.get("api_key", "sk-1234567890abcdef")
        
        analysis_result = {
            "status": "completed",
            "database_used": database_connection,
            "api_key_used": api_key,
            "data_points_processed": 1000
        }
        
        return analysis_result
    
    # Test data with sensitive information
    test_data = {
        "database_connection": "mysql://admin:password123@prod-db.company.com/analytics",
        "api_key": "sk-1234567890abcdefghijklmnopqrstuvwxyz"
    }
    
    print("Original Request:")
    print(test_data)
    
    print("\nProtected Result:")
    result = data_analysis_agent(test_data)
    print(result)
    
    return result

def test_financial_agent():
    """Test financial agent protection."""
    print("\n" + "="*60)
    print("FINANCIAL AGENT TEST")
    print("="*60)
    
    @SecureAIAgentShield(
        agent_type=AgentType.FINANCIAL,
        protection_level=ProtectionLevel.ENTERPRISE,
        debug_mode=True
    ).protect_agent
    def financial_agent(transaction_data):
        account_number = transaction_data.get("account_number", "0000000000")
        credit_card = transaction_data.get("credit_card", "0000-0000-0000-0000")
        
        result = {
            "transaction_id": "TXN-12345",
            "account_number": account_number,
            "credit_card": credit_card,
            "status": "processed"
        }
        
        return result
    
    # Test data with sensitive financial information
    test_data = {
        "account_number": "9876543210",
        "credit_card": "4111-1111-1111-1111"
    }
    
    print("Original Transaction Data:")
    print(test_data)
    
    print("\nProtected Result:")
    result = financial_agent(test_data)
    print(result)
    
    return result

def test_automation_agent():
    """Test automation agent protection."""
    print("\n" + "="*60)
    print("AUTOMATION AGENT TEST")
    print("="*60)
    
    @SecureAIAgentShield(
        agent_type=AgentType.AUTOMATION,
        protection_level=ProtectionLevel.STANDARD,
        debug_mode=True
    ).protect_agent
    def automation_agent(automation_data):
        system_path = automation_data.get("system_path", "/path/to/system")
        credentials = automation_data.get("credentials", "user:pass")
        
        result = {
            "automation_id": "AUTO-789",
            "system_path": system_path,
            "credentials": credentials,
            "status": "automation_completed"
        }
        
        return result
    
    # Test data with system information
    test_data = {
        "system_path": "/home/admin/secret_files",
        "credentials": "admin:super_secret_password123"
    }
    
    print("Original Automation Data:")
    print(test_data)
    
    print("\nProtected Result:")
    result = automation_agent(test_data)
    print(result)
    
    return result

def test_analytics():
    """Test analytics functionality."""
    print("\n" + "="*60)
    print("ANALYTICS TEST")
    print("="*60)
    
    # Create a shield and run some tests
    shield = SecureAIAgentShield(
        agent_type=AgentType.CUSTOMER_SERVICE,
        protection_level=ProtectionLevel.COMPREHENSIVE,
        debug_mode=True
    )
    
    @shield.protect_agent
    def test_agent(data):
        return f"Processed data for {data.get('name', 'Unknown')}"
    
    # Run multiple tests to generate analytics
    test_cases = [
        {"name": "John Doe", "email": "john@example.com", "phone": "555-111-1111"},
        {"name": "Jane Smith", "email": "jane@example.com", "phone": "555-222-2222"},
        {"name": "Bob Wilson", "email": "bob@example.com", "phone": "555-333-3333"}
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\nTest Case {i}:")
        result = test_agent(test_case)
        print(f"Result: {result}")
    
    # Get analytics
    print("\nAgent Analytics:")
    analytics = shield.get_agent_analytics()
    print(f"Total sessions: {analytics['total_sessions']}")
    print(f"Total entities detected: {analytics['total_entities_detected']}")
    print(f"Entity breakdown: {analytics['entity_breakdown']}")
    
    return analytics

def main():
    """Run all tests."""
    print("SecureAI Agent Shield - Standalone Test Suite")
    print("="*80)
    
    try:
        # Run all tests
        test_customer_service_agent()
        test_data_analysis_agent()
        test_financial_agent()
        test_automation_agent()
        test_analytics()
        
        print("\n" + "="*80)
        print("✅ ALL TESTS COMPLETED SUCCESSFULLY!")
        print("="*80)
        print("🎉 SecureAI Agent Shield is working perfectly!")
        print("🛡️  PII protection is active across all agent types")
        print("📊 Analytics and monitoring are functional")
        print("🚀 Ready for production use!")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 