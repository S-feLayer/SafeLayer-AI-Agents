#!/usr/bin/env python3
"""
Example: AI Agent PII Protection
Demonstrates how to protect different types of AI agents from PII exposure.
"""

import json
from typing import Dict, List, Any
from ai_agent_pii_shield import create_agent_shield, AgentType, ProtectionLevel

def main():
    """Demonstrate AI agent PII protection with different agent types."""
    
    print("🤖 AI Agent PII Protection Examples")
    print("=" * 50)
    
    # Example 1: Customer Service Agent
    print("\n1. Customer Service Agent Protection")
    print("-" * 40)
    
    customer_shield = create_agent_shield(
        agent_type=AgentType.CUSTOMER_SERVICE,
        protection_level=ProtectionLevel.COMPREHENSIVE
    )
    
    @customer_shield.protect_agent
    def customer_service_agent(customer_data: Dict[str, Any]) -> str:
        """Customer service agent that handles customer inquiries."""
        name = customer_data.get('name', 'Customer')
        email = customer_data.get('email', '')
        phone = customer_data.get('phone', '')
        order_id = customer_data.get('order_id', '')
        
        response = f"""
        Hello {name}, thank you for contacting us!
        
        I can see your order {order_id} and will help you with your inquiry.
        I'll send updates to {email} and can call you at {phone} if needed.
        
        How can I assist you today?
        """
        return response
    
    # Test with sensitive customer data
    customer_data = {
        "name": "John Smith",
        "email": "john.smith@example.com",
        "phone": "555-123-4567",
        "order_id": "ORD-12345",
        "address": "123 Main St, Anytown, CA 90210",
        "credit_card": "4111-1111-1111-1111"
    }
    
    print("Original data:", json.dumps(customer_data, indent=2))
    result = customer_service_agent(customer_data)
    print("Protected response:", result)
    
    # Example 2: Data Analysis Agent
    print("\n2. Data Analysis Agent Protection")
    print("-" * 40)
    
    data_shield = create_agent_shield(
        agent_type=AgentType.DATA_ANALYSIS,
        protection_level=ProtectionLevel.ENTERPRISE
    )
    
    @data_shield.protect_agent
    def data_analysis_agent(analysis_request: Dict[str, Any]) -> Dict[str, Any]:
        """Data analysis agent that processes business data."""
        database_url = analysis_request.get('database_url', '')
        api_key = analysis_request.get('api_key', '')
        customer_data = analysis_request.get('customer_data', {})
        
        analysis_result = {
            "database_connection": f"Connected to {database_url}",
            "api_status": f"API key {api_key} is valid",
            "customer_analysis": f"Analyzed data for {customer_data.get('name', 'Customer')}",
            "metrics": {
                "total_customers": 1500,
                "revenue": "$50,000",
                "growth_rate": "15%"
            }
        }
        return analysis_result
    
    # Test with sensitive business data
    analysis_data = {
        "database_url": "postgresql://user:password123@localhost:5432/business_db",
        "api_key": "sk-1234567890abcdef",
        "customer_data": {
            "name": "Acme Corporation",
            "email": "contact@acme.com",
            "revenue": "$1,000,000"
        }
    }
    
    print("Original analysis data:", json.dumps(analysis_data, indent=2))
    result = data_analysis_agent(analysis_data)
    print("Protected analysis result:", json.dumps(result, indent=2))
    
    # Example 3: Chatbot Agent
    print("\n3. Chatbot Agent Protection")
    print("-" * 40)
    
    chatbot_shield = create_agent_shield(
        agent_type=AgentType.CHATBOT,
        protection_level=ProtectionLevel.STANDARD
    )
    
    @chatbot_shield.protect_agent
    def chatbot_agent(user_message: str, user_context: Dict[str, Any]) -> str:
        """Chatbot agent that handles user conversations."""
        user_name = user_context.get('name', 'User')
        user_email = user_context.get('email', '')
        user_preferences = user_context.get('preferences', {})
        
        response = f"""
        Hi {user_name}! 👋
        
        I understand you're interested in our services. 
        I'll send more information to {user_email}.
        
        Based on your preferences: {user_preferences}
        
        How can I help you today?
        """
        return response
    
    # Test with user conversation data
    user_message = "I need help with my account"
    user_context = {
        "name": "Sarah Johnson",
        "email": "sarah.johnson@email.com",
        "phone": "555-987-6543",
        "preferences": {
            "language": "English",
            "timezone": "PST",
            "notifications": "email"
        }
    }
    
    print("Original user context:", json.dumps(user_context, indent=2))
    result = chatbot_agent(user_message, user_context)
    print("Protected chatbot response:", result)
    
    # Example 4: Automation Agent
    print("\n4. Automation Agent Protection")
    print("-" * 40)
    
    automation_shield = create_agent_shield(
        agent_type=AgentType.AUTOMATION,
        protection_level=ProtectionLevel.BASIC
    )
    
    @automation_shield.protect_agent
    def automation_agent(automation_config: Dict[str, Any]) -> Dict[str, Any]:
        """Automation agent that handles system tasks."""
        system_credentials = automation_config.get('credentials', {})
        automation_paths = automation_config.get('paths', [])
        log_data = automation_config.get('logs', [])
        
        automation_result = {
            "status": "Automation completed successfully",
            "credentials_used": f"Used credentials for {system_credentials.get('username', 'user')}",
            "paths_processed": f"Processed {len(automation_paths)} paths",
            "logs_generated": f"Generated {len(log_data)} log entries",
            "execution_time": "2.5 seconds"
        }
        return automation_result
    
    # Test with automation configuration
    automation_config = {
        "credentials": {
            "username": "admin",
            "password": "secure_password_123",
            "api_key": "ak-9876543210fedcba"
        },
        "paths": [
            "/var/log/system.log",
            "/home/user/data/",
            "/etc/config/"
        ],
        "logs": [
            "System backup completed",
            "User authentication successful",
            "Database connection established"
        ]
    }
    
    print("Original automation config:", json.dumps(automation_config, indent=2))
    result = automation_agent(automation_config)
    print("Protected automation result:", json.dumps(result, indent=2))
    
    # Show statistics for all agents
    print("\n5. Agent Protection Statistics")
    print("-" * 40)
    
    agents = [
        ("Customer Service", customer_shield),
        ("Data Analysis", data_shield),
        ("Chatbot", chatbot_shield),
        ("Automation", automation_shield)
    ]
    
    for agent_name, shield in agents:
        stats = shield.get_agent_stats()
        print(f"{agent_name} Agent:")
        print(f"  - Total sessions: {stats['total_sessions']}")
        print(f"  - Protection level: {stats['protection_level']}")
        print(f"  - Agent type: {stats['agent_type']}")
        print()

if __name__ == "__main__":
    main() 