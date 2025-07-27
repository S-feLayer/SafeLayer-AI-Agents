#!/usr/bin/env python3
"""
SecureAI Agent Protection System - AI Agent Demonstration
Shows how the system works specifically for AI agents with real-world examples.
"""

import json
import time
from secureai_agent_shield import SecureAIAgentShield, AgentType, ProtectionLevel

def demonstrate_customer_service_agent():
    """Demonstrate customer service AI agent protection."""
    print("\n" + "="*70)
    print("CUSTOMER SERVICE AI AGENT DEMONSTRATION")
    print("="*70)
    
    @SecureAIAgentShield(
        agent_type=AgentType.CUSTOMER_SERVICE,
        protection_level=ProtectionLevel.COMPREHENSIVE,
        debug_mode=True
    ).protect_agent
    def customer_service_agent(customer_inquiry):
        """
        This is a customer service AI agent that handles customer inquiries.
        It automatically gets PII protection applied to all inputs and outputs.
        """
        customer_name = customer_inquiry.get("name", "Unknown")
        customer_email = customer_inquiry.get("email", "unknown@example.com")
        customer_phone = customer_inquiry.get("phone", "555-0000")
        order_number = customer_inquiry.get("order_number", "N/A")
        
        # Simulate AI agent processing
        response = f"""
        Hello {customer_name}, thank you for contacting our customer service.
        
        I can see your order #{order_number} and will contact you at {customer_email} 
        or {customer_phone} to resolve your inquiry.
        
        Your account information has been retrieved and I'm working on your request.
        """
        
        return response
    
    # Test with sensitive customer data
    customer_data = {
        "name": "John Smith",
        "email": "john.smith@example.com", 
        "phone": "555-123-4567",
        "order_number": "ORD-2024-001234",
        "account_number": "1234567890"
    }
    
    print("Original Customer Data:")
    print(json.dumps(customer_data, indent=2))
    
    print("\nAI Agent Response (with PII protection):")
    result = customer_service_agent(customer_data)
    print(result)
    
    return result

def demonstrate_data_analysis_agent():
    """Demonstrate data analysis AI agent protection."""
    print("\n" + "="*70)
    print("DATA ANALYSIS AI AGENT DEMONSTRATION")
    print("="*70)
    
    @SecureAIAgentShield(
        agent_type=AgentType.DATA_ANALYSIS,
        protection_level=ProtectionLevel.ENTERPRISE,
        debug_mode=True
    ).protect_agent
    def data_analysis_agent(analysis_request):
        """
        This is a data analysis AI agent that processes business data.
        It automatically protects database credentials, API keys, and sensitive metrics.
        """
        database_connection = analysis_request.get("database_connection", "")
        api_key = analysis_request.get("api_key", "")
        query = analysis_request.get("query", "")
        
        # Simulate AI agent data analysis
        analysis_result = {
            "status": "analysis_completed",
            "database_used": database_connection,
            "api_key_used": api_key,
            "query_executed": query,
            "data_points_processed": 10000,
            "sensitive_metrics": {
                "revenue": "$1,234,567",
                "customer_count": 5432,
                "growth_rate": "15.7%"
            }
        }
        
        return analysis_result
    
    # Test with sensitive business data
    analysis_data = {
        "database_connection": "mysql://admin:password123@prod-db.company.com/analytics",
        "api_key": "sk-1234567890abcdefghijklmnopqrstuvwxyz",
        "query": "SELECT * FROM customers WHERE revenue > 100000"
    }
    
    print("Original Analysis Request:")
    print(json.dumps(analysis_data, indent=2))
    
    print("\nAI Agent Analysis Result (with PII protection):")
    result = data_analysis_agent(analysis_data)
    print(json.dumps(result, indent=2))
    
    return result

def demonstrate_financial_agent():
    """Demonstrate financial AI agent protection."""
    print("\n" + "="*70)
    print("FINANCIAL AI AGENT DEMONSTRATION")
    print("="*70)
    
    @SecureAIAgentShield(
        agent_type=AgentType.FINANCIAL,
        protection_level=ProtectionLevel.ENTERPRISE,
        debug_mode=True
    ).protect_agent
    def financial_agent(transaction_request):
        """
        This is a financial AI agent that processes transactions.
        It automatically protects account numbers, credit cards, and financial data.
        """
        account_number = transaction_request.get("account_number", "")
        credit_card = transaction_request.get("credit_card", "")
        amount = transaction_request.get("amount", 0)
        
        # Simulate AI agent transaction processing
        transaction_result = {
            "transaction_id": "TXN-2024-789012",
            "account_number": account_number,
            "credit_card": credit_card,
            "amount": amount,
            "status": "processed",
            "balance_after": 5432.10
        }
        
        return transaction_result
    
    # Test with sensitive financial data
    financial_data = {
        "account_number": "9876543210",
        "credit_card": "4111-1111-1111-1111",
        "amount": 299.99
    }
    
    print("Original Financial Request:")
    print(json.dumps(financial_data, indent=2))
    
    print("\nAI Agent Transaction Result (with PII protection):")
    result = financial_agent(financial_data)
    print(json.dumps(result, indent=2))
    
    return result

def demonstrate_multi_agent_workflow():
    """Demonstrate multi-agent workflow with consistent PII protection."""
    print("\n" + "="*70)
    print("MULTI-AGENT WORKFLOW DEMONSTRATION")
    print("="*70)
    
    # Create shields for different agent types
    customer_shield = SecureAIAgentShield(
        agent_type=AgentType.CUSTOMER_SERVICE,
        protection_level=ProtectionLevel.COMPREHENSIVE,
        persistence_enabled=True,
        debug_mode=True
    )
    
    data_shield = SecureAIAgentShield(
        agent_type=AgentType.DATA_ANALYSIS,
        protection_level=ProtectionLevel.ENTERPRISE,
        persistence_enabled=True,
        debug_mode=True
    )
    
    financial_shield = SecureAIAgentShield(
        agent_type=AgentType.FINANCIAL,
        protection_level=ProtectionLevel.ENTERPRISE,
        persistence_enabled=True,
        debug_mode=True
    )
    
    @customer_shield.protect_agent
    def customer_inquiry_agent(customer_data):
        """First agent: Customer inquiry processing"""
        return {
            "customer_id": customer_data.get("name"),
            "inquiry_type": "payment_issue",
            "priority": "high",
            "contact_info": customer_data.get("email")
        }
    
    @data_shield.protect_agent
    def data_analysis_agent(inquiry_data):
        """Second agent: Data analysis for the inquiry"""
        return {
            "analysis_id": "ANAL-001",
            "customer_id": inquiry_data.get("customer_id"),
            "risk_score": 0.15,
            "recommendation": "process_refund"
        }
    
    @financial_shield.protect_agent
    def financial_processing_agent(analysis_data):
        """Third agent: Financial processing based on analysis"""
        return {
            "transaction_id": "TXN-REFUND-001",
            "customer_id": analysis_data.get("customer_id"),
            "refund_amount": 299.99,
            "status": "approved"
        }
    
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
    
    print("\nStep 3: Financial Processing Agent")
    financial_result = financial_processing_agent(analysis_result)
    print(json.dumps(financial_result, indent=2))
    
    return financial_result

def demonstrate_analytics():
    """Demonstrate analytics and monitoring capabilities."""
    print("\n" + "="*70)
    print("ANALYTICS AND MONITORING DEMONSTRATION")
    print("="*70)
    
    # Create a shield for analytics
    shield = SecureAIAgentShield(
        agent_type=AgentType.CUSTOMER_SERVICE,
        protection_level=ProtectionLevel.COMPREHENSIVE,
        persistence_enabled=True,
        debug_mode=True
    )
    
    @shield.protect_agent
    def test_agent(data):
        """Test agent for analytics demonstration"""
        return f"Processed data for {data.get('name', 'Unknown')}"
    
    # Run multiple operations to generate analytics
    test_cases = [
        {"name": "John Doe", "email": "john@example.com", "phone": "555-111-1111"},
        {"name": "Jane Smith", "email": "jane@example.com", "phone": "555-222-2222"},
        {"name": "Bob Wilson", "email": "bob@example.com", "phone": "555-333-3333"},
        {"name": "Alice Brown", "email": "alice@example.com", "phone": "555-444-4444"}
    ]
    
    print("Running multiple agent operations...")
    for i, test_case in enumerate(test_cases, 1):
        print(f"\nOperation {i}:")
        result = test_agent(test_case)
        print(f"Result: {result}")
    
    # Get analytics
    print("\nAgent Analytics:")
    analytics = shield.get_agent_analytics()
    print(json.dumps(analytics, indent=2))
    
    return analytics

def main():
    """Run the complete AI agent demonstration."""
    print("SecureAI Agent Protection System - AI Agent Demonstration")
    print("="*80)
    print("This demonstration shows how SecureAI works specifically for AI agents")
    print("Each agent type gets different protection rules and configurations")
    print("="*80)
    
    start_time = time.time()
    
    try:
        # Run all demonstrations
        demonstrate_customer_service_agent()
        demonstrate_data_analysis_agent()
        demonstrate_financial_agent()
        demonstrate_multi_agent_workflow()
        demonstrate_analytics()
        
        total_time = time.time() - start_time
        
        print("\n" + "="*80)
        print("AI AGENT DEMONSTRATION COMPLETE")
        print("="*80)
        print(f"Total demonstration time: {total_time:.2f} seconds")
        print("All AI agents are now protected with SecureAI!")
        print("="*80)
        
    except Exception as e:
        print(f"\nDemonstration failed with error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 