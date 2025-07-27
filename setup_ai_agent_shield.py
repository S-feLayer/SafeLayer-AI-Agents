#!/usr/bin/env python3
"""
Setup Script for SecureSecureAI Agent PII Shield
Quick setup and configuration for protecting AI agents from PII exposure.
"""

import os
import json
import sys
from pathlib import Path

def create_config_file():
    """Create a configuration file for the SecureSecureAI Agent PII Shield."""
    config = {
        "agent_types": {
            "customer_service": {
                "protection_level": "comprehensive",
                "enable_persistence": True,
                "custom_rules": {
                    "customer_data": True,
                    "order_details": True,
                    "payment_info": True,
                    "contact_info": True
                }
            },
            "data_analysis": {
                "protection_level": "enterprise",
                "enable_persistence": True,
                "custom_rules": {
                    "database_credentials": True,
                    "api_keys": True,
                    "sensitive_metrics": True,
                    "business_data": True
                }
            },
            "automation": {
                "protection_level": "basic",
                "enable_persistence": False,
                "custom_rules": {
                    "system_credentials": True,
                    "automation_paths": False,
                    "log_data": False
                }
            },
            "chatbot": {
                "protection_level": "standard",
                "enable_persistence": True,
                "custom_rules": {
                    "conversation_context": True,
                    "user_preferences": True,
                    "personal_info": True
                }
            }
        },
        "global_settings": {
            "tinfoil_api_key": "",
            "enable_audit_logging": True,
            "log_level": "INFO",
            "cache_enabled": True,
            "max_file_size": "100MB"
        }
    }
    
    with open("ai_agent_shield_config.json", "w") as f:
        json.dump(config, f, indent=2)
    
    print("✅ Created ai_agent_shield_config.json")

def create_example_agents():
    """Create example AI agent implementations."""
    
    # Example 1: Customer Service Agent
    customer_agent_code = '''#!/usr/bin/env python3
"""
Example Customer Service Agent
Protected with SecureSecureAI Agent PII Shield
"""

from ai_agent_pii_shield import create_agent_shield, AgentType, ProtectionLevel
from typing import Dict, Any

# Create shield for customer service
customer_shield = create_agent_shield(
    agent_type=AgentType.CUSTOMER_SERVICE,
    protection_level=ProtectionLevel.COMPREHENSIVE
)

@customer_shield.protect_agent
def handle_customer_inquiry(customer_data: Dict[str, Any]) -> str:
    """Handle customer service inquiries with automatic PII protection."""
    name = customer_data.get('name', 'Customer')
    email = customer_data.get('email', '')
    order_id = customer_data.get('order_id', '')
    
    response = f"""
    Hello {name}, thank you for contacting us!
    
    I can see your order {order_id} and will help you with your inquiry.
    I'll send updates to {email}.
    
    How can I assist you today?
    """
    return response

# Example usage
if __name__ == "__main__":
    test_data = {
        "name": "John Smith",
        "email": "john.smith@example.com",
        "phone": "555-123-4567",
        "order_id": "ORD-12345"
    }
    
    result = handle_customer_inquiry(test_data)
    print("Protected response:", result)
'''
    
    with open("example_customer_agent.py", "w") as f:
        f.write(customer_agent_code)
    
    # Example 2: Data Analysis Agent
    data_agent_code = '''#!/usr/bin/env python3
"""
Example Data Analysis Agent
Protected with SecureSecureAI Agent PII Shield
"""

from ai_agent_pii_shield import create_agent_shield, AgentType, ProtectionLevel
from typing import Dict, Any

# Create shield for data analysis
data_shield = create_agent_shield(
    agent_type=AgentType.DATA_ANALYSIS,
    protection_level=ProtectionLevel.ENTERPRISE
)

@data_shield.protect_agent
def analyze_business_data(analysis_request: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze business data with automatic PII protection."""
    database_url = analysis_request.get('database_url', '')
    customer_data = analysis_request.get('customer_data', {})
    
    analysis_result = {
        "database_connection": f"Connected to {database_url}",
        "customer_analysis": f"Analyzed data for {customer_data.get('name', 'Customer')}",
        "metrics": {
            "total_customers": 1500,
            "revenue": "$50,000",
            "growth_rate": "15%"
        }
    }
    return analysis_result

# Example usage
if __name__ == "__main__":
    test_data = {
        "database_url": "postgresql://user:password123@localhost:5432/business_db",
        "customer_data": {
            "name": "Acme Corporation",
            "email": "contact@acme.com"
        }
    }
    
    result = analyze_business_data(test_data)
    print("Protected analysis result:", result)
'''
    
    with open("example_data_agent.py", "w") as f:
        f.write(data_agent_code)
    
    print("✅ Created example agent files:")
    print("   - example_customer_agent.py")
    print("   - example_data_agent.py")

def create_requirements_file():
    """Create requirements.txt for the SecureSecureAI Agent PII Shield."""
    requirements = [
        "fastmcp==0.4.1",
        "mcp==1.3.0",
        "PyMuPDF>=1.26.0",
        "tinfoil",
        "psutil>=5.8.0",
        "requests>=2.31.0",
        "python-dotenv>=1.0.0",
        "redis>=4.0.0",
        "psycopg2-binary>=2.9.0"
    ]
    
    with open("requirements_ai_agent.txt", "w") as f:
        for req in requirements:
            f.write(req + "\n")
    
    print("✅ Created requirements_ai_agent.txt")

def create_readme():
    """Create a README file for the SecureSecureAI Agent PII Shield."""
    readme_content = """# SecureSecureAI Agent PII Shield

Protect your AI agents from PII exposure with easy-to-use decorators.

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements_ai_agent.txt
   ```

2. **Set up your Tinfoil API key (optional):**
   ```bash
   export TINFOIL_API_KEY="your_api_key_here"
   ```

3. **Protect your AI agent:**
   ```python
   from ai_agent_pii_shield import create_agent_shield, AgentType, ProtectionLevel
   
   # Create a shield
   shield = create_agent_shield(
       agent_type=AgentType.CUSTOMER_SERVICE,
       protection_level=ProtectionLevel.COMPREHENSIVE
   )
   
   # Protect your agent function
   @shield.protect_agent
   def my_ai_agent(customer_data):
       return "Agent response"
   ```

## Agent Types

- **CUSTOMER_SERVICE**: Protects customer data, orders, payments
- **DATA_ANALYSIS**: Protects database credentials, API keys, business data
- **AUTOMATION**: Protects system credentials while allowing automation paths
- **CHATBOT**: Protects conversation context and user preferences

## Protection Levels

- **BASIC**: Minimal protection, fast processing
- **STANDARD**: Standard PII protection
- **COMPREHENSIVE**: Full protection with persistence
- **ENTERPRISE**: Maximum security with audit logging

## Examples

Run the example files to see how it works:
```bash
python example_customer_agent.py
python example_data_agent.py
```

## Configuration

Edit `ai_agent_shield_config.json` to customize protection rules for your use case.

## Features

- ✅ Automatic PII detection and masking
- ✅ Agent-specific protection rules
- ✅ Session persistence across conversations
- ✅ Audit logging for compliance
- ✅ Easy-to-use decorator syntax
- ✅ Support for multiple agent types
- ✅ Configurable protection levels
"""
    
    with open("README_AI_AGENT_SHIELD.md", "w") as f:
        f.write(readme_content)
    
    print("✅ Created README_AI_AGENT_SHIELD.md")

def main():
    """Main setup function."""
    print("🚀 Setting up SecureSecureAI Agent PII Shield")
    print("=" * 40)
    
    # Create necessary files
    create_config_file()
    create_example_agents()
    create_requirements_file()
    create_readme()
    
    print("\n🎉 Setup complete!")
    print("\nNext steps:")
    print("1. Install dependencies: pip install -r requirements_ai_agent.txt")
    print("2. Set your Tinfoil API key: export TINFOIL_API_KEY='your_key'")
    print("3. Run examples: python example_customer_agent.py")
    print("4. Start protecting your AI agents!")
    
    print("\n📁 Files created:")
    print("   - ai_agent_shield_config.json (configuration)")
    print("   - example_customer_agent.py (customer service example)")
    print("   - example_data_agent.py (data analysis example)")
    print("   - requirements_ai_agent.txt (dependencies)")
    print("   - README_AI_AGENT_SHIELD.md (documentation)")

if __name__ == "__main__":
    main() 