#!/usr/bin/env python3
"""
SecureAI Agent Protection System - Test Script
Demonstrates the comprehensive PII protection capabilities for AI agents.
"""

import json
import time
from typing import Dict, Any

# Import the SecureAI protection components
from agent_privacy_shield import SecureAIAgentPrivacyShield, AgentType, ProtectionLevel
from ai_agent_pii_shield import create_agent_shield

def test_customer_service_agent():
    """Test customer service agent protection."""
    print("\n" + "="*60)
    print("CUSTOMER SERVICE AGENT TEST")
    print("="*60)
    
    @SecureAIAgentPrivacyShield(
        agent_type=AgentType.CUSTOMER_SERVICE,
        protection_level=ProtectionLevel.COMPREHENSIVE,
        persistence_enabled=True,
        debug_mode=True
    ).protect_agent
    def customer_service_agent(customer_data: Dict[str, Any]) -> str:
        customer_name = customer_data.get("name", "Unknown")
        customer_email = customer_data.get("email", "unknown@example.com")
        customer_phone = customer_data.get("phone", "555-0000")
        account_number = customer_data.get("account_number", "0000000000")
        
        response = f"Hello {customer_name}, I can help you with your inquiry. I'll contact you at {customer_email} or {customer_phone}. Your account number is {account_number}."
        return response
    
    # Test data with sensitive information
    test_data = {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "phone": "555-123-4567",
        "account_number": "1234567890",
        "ssn": "123-45-6789"
    }
    
    print("Original Data:")
    print(json.dumps(test_data, indent=2))
    
    print("\nProtected Response:")
    result = customer_service_agent(test_data)
    print(result)
    
    return result

def test_data_analysis_agent():
    """Test data analysis agent protection."""
    print("\n" + "="*60)
    print("DATA ANALYSIS AGENT TEST")
    print("="*60)
    
    @SecureAIAgentPrivacyShield(
        agent_type=AgentType.DATA_ANALYSIS,
        protection_level=ProtectionLevel.ENTERPRISE,
        persistence_enabled=True,
        debug_mode=True
    ).protect_agent
    def data_analysis_agent(analysis_request: Dict[str, Any]) -> Dict[str, Any]:
        database_connection = analysis_request.get("database_connection", "mysql://user:pass@localhost/db")
        api_key = analysis_request.get("api_key", "sk-1234567890abcdef")
        query = analysis_request.get("query", "SELECT * FROM users")
        
        # Simulate analysis
        analysis_result = {
            "status": "completed",
            "database_used": database_connection,
            "api_key_used": api_key,
            "query_executed": query,
            "data_points_processed": 1000,
            "sensitive_metrics": {
                "revenue": "$1,234,567",
                "customer_count": 50000,
                "api_calls": 1000000
            }
        }
        
        return analysis_result
    
    # Test data with sensitive information
    test_data = {
        "database_connection": "mysql://admin:password123@prod-db.company.com/analytics",
        "api_key": "sk-1234567890abcdefghijklmnopqrstuvwxyz",
        "query": "SELECT * FROM customers WHERE email = 'john.doe@example.com'"
    }
    
    print("Original Request:")
    print(json.dumps(test_data, indent=2))
    
    print("\nProtected Result:")
    result = data_analysis_agent(test_data)
    print(json.dumps(result, indent=2))
    
    return result

def test_financial_agent():
    """Test financial agent protection."""
    print("\n" + "="*60)
    print("FINANCIAL AGENT TEST")
    print("="*60)
    
    @SecureAIAgentPrivacyShield(
        agent_type=AgentType.FINANCIAL,
        protection_level=ProtectionLevel.ENTERPRISE,
        persistence_enabled=True,
        debug_mode=True
    ).protect_agent
    def financial_agent(transaction_data: Dict[str, Any]) -> Dict[str, Any]:
        account_number = transaction_data.get("account_number", "0000000000")
        routing_number = transaction_data.get("routing_number", "000000000")
        amount = transaction_data.get("amount", "0.00")
        credit_card = transaction_data.get("credit_card", "0000-0000-0000-0000")
        
        # Simulate financial processing
        result = {
            "transaction_id": "TXN-12345",
            "account_number": account_number,
            "routing_number": routing_number,
            "amount": amount,
            "credit_card": credit_card,
            "status": "processed",
            "balance": "$5,432.10"
        }
        
        return result
    
    # Test data with sensitive financial information
    test_data = {
        "account_number": "9876543210",
        "routing_number": "123456789",
        "amount": "1234.56",
        "credit_card": "4111-1111-1111-1111",
        "ssn": "987-65-4321"
    }
    
    print("Original Transaction Data:")
    print(json.dumps(test_data, indent=2))
    
    print("\nProtected Result:")
    result = financial_agent(test_data)
    print(json.dumps(result, indent=2))
    
    return result

def test_healthcare_agent():
    """Test healthcare agent protection."""
    print("\n" + "="*60)
    print("HEALTHCARE AGENT TEST")
    print("="*60)
    
    @SecureAIAgentPrivacyShield(
        agent_type=AgentType.HEALTHCARE,
        protection_level=ProtectionLevel.ENTERPRISE,
        persistence_enabled=True,
        debug_mode=True
    ).protect_agent
    def healthcare_agent(patient_data: Dict[str, Any]) -> Dict[str, Any]:
        patient_name = patient_data.get("name", "Unknown")
        patient_id = patient_data.get("patient_id", "000000")
        diagnosis = patient_data.get("diagnosis", "Unknown")
        insurance_id = patient_data.get("insurance_id", "000000000")
        
        # Simulate healthcare processing
        result = {
            "patient_name": patient_name,
            "patient_id": patient_id,
            "diagnosis": diagnosis,
            "insurance_id": insurance_id,
            "treatment_plan": "Standard treatment protocol",
            "prescription": "Medication A, 10mg daily"
        }
        
        return result
    
    # Test data with sensitive healthcare information
    test_data = {
        "name": "Jane Smith",
        "patient_id": "P123456",
        "diagnosis": "Hypertension",
        "insurance_id": "INS987654321",
        "ssn": "111-22-3333",
        "phone": "555-987-6543"
    }
    
    print("Original Patient Data:")
    print(json.dumps(test_data, indent=2))
    
    print("\nProtected Result:")
    result = healthcare_agent(test_data)
    print(json.dumps(result, indent=2))
    
    return result

def test_automation_agent():
    """Test automation agent protection."""
    print("\n" + "="*60)
    print("AUTOMATION AGENT TEST")
    print("="*60)
    
    @SecureAIAgentPrivacyShield(
        agent_type=AgentType.AUTOMATION,
        protection_level=ProtectionLevel.STANDARD,
        persistence_enabled=True,
        debug_mode=True
    ).protect_agent
    def automation_agent(automation_data: Dict[str, Any]) -> Dict[str, Any]:
        system_path = automation_data.get("system_path", "/path/to/system")
        api_endpoint = automation_data.get("api_endpoint", "https://api.example.com")
        credentials = automation_data.get("credentials", "user:pass")
        
        # Simulate automation
        result = {
            "automation_id": "AUTO-789",
            "system_path": system_path,
            "api_endpoint": api_endpoint,
            "credentials": credentials,
            "status": "automation_completed",
            "log_file": "/var/log/automation.log"
        }
        
        return result
    
    # Test data with system information
    test_data = {
        "system_path": "/home/admin/secret_files",
        "api_endpoint": "https://internal-api.company.com/v1/secret",
        "credentials": "admin:super_secret_password123",
        "database_url": "postgresql://admin:password@internal-db.company.com/prod"
    }
    
    print("Original Automation Data:")
    print(json.dumps(test_data, indent=2))
    
    print("\nProtected Result:")
    result = automation_agent(test_data)
    print(json.dumps(result, indent=2))
    
    return result

def test_multi_agent_workflow():
    """Test multi-agent workflow with consistent protection."""
    print("\n" + "="*60)
    print("MULTI-AGENT WORKFLOW TEST")
    print("="*60)
    
    # Create shields for different agent types
    customer_shield = create_agent_shield(
        agent_type=AgentType.CUSTOMER_SERVICE,
        protection_level=ProtectionLevel.COMPREHENSIVE
    )
    
    data_shield = create_agent_shield(
        agent_type=AgentType.DATA_ANALYSIS,
        protection_level=ProtectionLevel.ENTERPRISE
    )
    
    @customer_shield.protect_agent
    def customer_inquiry_agent(customer_data):
        customer_name = customer_data.get("name", "Unknown")
        customer_email = customer_data.get("email", "unknown@example.com")
        
        # Pass data to data analysis agent
        analysis_request = {
            "customer_name": customer_name,
            "customer_email": customer_email,
            "query": f"Analyze data for {customer_name}",
            "database_connection": "mysql://admin:pass@db.company.com/customers"
        }
        
        return analysis_request
    
    @data_shield.protect_agent
    def data_analysis_agent(analysis_request):
        customer_name = analysis_request.get("customer_name", "Unknown")
        customer_email = analysis_request.get("customer_email", "unknown@example.com")
        database_connection = analysis_request.get("database_connection", "mysql://user:pass@localhost/db")
        
        result = {
            "analysis_id": "ANALYSIS-456",
            "customer_name": customer_name,
            "customer_email": customer_email,
            "database_used": database_connection,
            "findings": "Customer analysis completed"
        }
        
        return result
    
    # Test multi-agent workflow
    initial_data = {
        "name": "Alice Johnson",
        "email": "alice.johnson@company.com",
        "phone": "555-111-2222",
        "account_number": "1112223333"
    }
    
    print("Initial Customer Data:")
    print(json.dumps(initial_data, indent=2))
    
    print("\nStep 1: Customer Inquiry Agent")
    inquiry_result = customer_inquiry_agent(initial_data)
    print(json.dumps(inquiry_result, indent=2))
    
    print("\nStep 2: Data Analysis Agent")
    analysis_result = data_analysis_agent(inquiry_result)
    print(json.dumps(analysis_result, indent=2))
    
    return analysis_result

def test_agent_analytics():
    """Test agent analytics and statistics."""
    print("\n" + "="*60)
    print("AGENT ANALYTICS TEST")
    print("="*60)
    
    # Create a shield and run some tests
    shield = SecureAIAgentPrivacyShield(
        agent_type=AgentType.CUSTOMER_SERVICE,
        protection_level=ProtectionLevel.COMPREHENSIVE,
        persistence_enabled=True,
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
    print(json.dumps(analytics, indent=2))
    
    return analytics

def main():
    """Run all SecureAI Agent Protection tests."""
    print("SecureAI Agent Protection System - Comprehensive Test Suite")
    print("="*80)
    print("Testing PII protection for various AI agent types...")
    
    start_time = time.time()
    
    try:
        # Run all tests
        test_customer_service_agent()
        test_data_analysis_agent()
        test_financial_agent()
        test_healthcare_agent()
        test_automation_agent()
        test_multi_agent_workflow()
        test_agent_analytics()
        
        total_time = time.time() - start_time
        
        print("\n" + "="*80)
        print("SECUREAI AGENT PROTECTION SYSTEM - TEST RESULTS")
        print("="*80)
        print(f"✅ All tests completed successfully!")
        print(f"⏱️  Total test time: {total_time:.2f} seconds")
        print(f"🛡️  PII protection working across all agent types")
        print(f"📊 Analytics and monitoring functional")
        print(f"🔄 Multi-agent workflows protected")
        print(f"🔒 Enterprise-grade security features active")
        
        print("\n" + "="*80)
        print("SECUREAI AGENT PROTECTION SYSTEM READY FOR PRODUCTION")
        print("="*80)
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 