#!/usr/bin/env python3
"""
SecureAI Agent Protection System - Setup Script
Installs and configures the SecureAI Agent Protection System for AI agents.
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def create_config_file():
    """Create SecureAI configuration file."""
    config = {
        "secureai_agents": {
            "default_agent_type": "customer_service",
            "default_protection_level": "comprehensive",
            "enable_persistence": True,
            "enable_debug_mode": False,
            "redis_url": "redis://localhost:6379",
            "postgres_url": None,
            "tinfoil_api_key": None
        },
        "agent_types": {
            "customer_service": {
                "protection_level": "comprehensive",
                "enable_customer_data": True,
                "enable_payment_info": True,
                "enable_contact_info": True
            },
            "data_analysis": {
                "protection_level": "enterprise",
                "enable_database_credentials": True,
                "enable_api_keys": True,
                "enable_business_data": True
            },
            "automation": {
                "protection_level": "standard",
                "enable_system_credentials": True,
                "enable_automation_paths": False
            },
            "financial": {
                "protection_level": "enterprise",
                "enable_financial_data": True,
                "enable_account_numbers": True,
                "enable_transaction_data": True
            },
            "healthcare": {
                "protection_level": "enterprise",
                "enable_medical_data": True,
                "enable_patient_identifiers": True,
                "enable_diagnosis_data": True
            }
        }
    }
    
    config_path = Path("secureai_agents_config.json")
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"✅ Configuration file created: {config_path}")
    return config_path

def create_example_agents():
    """Create example AI agent files."""
    examples_dir = Path("examples")
    examples_dir.mkdir(exist_ok=True)
    
    # Customer Service Agent Example
    customer_agent = '''#!/usr/bin/env python3
"""
Example Customer Service Agent with SecureAI Protection
"""

from agent_privacy_shield import SecureAIAgentPrivacyShield, AgentType, ProtectionLevel

@SecureAIAgentPrivacyShield(
    agent_type=AgentType.CUSTOMER_SERVICE,
    protection_level=ProtectionLevel.COMPREHENSIVE,
    persistence_enabled=True,
    debug_mode=True
).protect_agent
def customer_service_agent(customer_data):
    """Protected customer service agent."""
    customer_name = customer_data.get("name", "Unknown")
    customer_email = customer_data.get("email", "unknown@example.com")
    customer_phone = customer_data.get("phone", "555-0000")
    
    response = f"Hello {customer_name}, I can help you with your inquiry. I'll contact you at {customer_email} or {customer_phone}."
    return response

if __name__ == "__main__":
    # Test the protected agent
    test_data = {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "phone": "555-123-4567",
        "account_number": "1234567890"
    }
    
    result = customer_service_agent(test_data)
    print(f"Protected Response: {result}")
'''
    
    with open(examples_dir / "customer_service_agent.py", 'w') as f:
        f.write(customer_agent)
    
    # Data Analysis Agent Example
    data_agent = '''#!/usr/bin/env python3
"""
Example Data Analysis Agent with SecureAI Protection
"""

from agent_privacy_shield import SecureAIAgentPrivacyShield, AgentType, ProtectionLevel

@SecureAIAgentPrivacyShield(
    agent_type=AgentType.DATA_ANALYSIS,
    protection_level=ProtectionLevel.ENTERPRISE,
    persistence_enabled=True,
    debug_mode=True
).protect_agent
def data_analysis_agent(analysis_request):
    """Protected data analysis agent."""
    database_connection = analysis_request.get("database_connection", "mysql://user:pass@localhost/db")
    api_key = analysis_request.get("api_key", "sk-1234567890abcdef")
    
    # Simulate analysis
    analysis_result = {
        "status": "completed",
        "database_used": database_connection,
        "api_key_used": api_key,
        "data_points_processed": 1000
    }
    
    return analysis_result

if __name__ == "__main__":
    # Test the protected agent
    test_data = {
        "database_connection": "mysql://admin:password123@prod-db.company.com/analytics",
        "api_key": "sk-1234567890abcdefghijklmnopqrstuvwxyz"
    }
    
    result = data_analysis_agent(test_data)
    print(f"Protected Result: {result}")
'''
    
    with open(examples_dir / "data_analysis_agent.py", 'w') as f:
        f.write(data_agent)
    
    print(f"✅ Example agents created in {examples_dir}/")

def create_environment_file():
    """Create .env file with SecureAI configuration."""
    env_content = """# SecureAI Agent Protection System - Environment Configuration

# Tinfoil API key for advanced AI detection (optional)
TINFOIL_API_KEY=your_tinfoil_api_key_here

# Redis configuration for entity persistence
REDIS_URL=redis://localhost:6379

# PostgreSQL configuration for enterprise features (optional)
POSTGRES_URL=postgresql://user:password@localhost/secureai_db

# SecureAI Agent Protection settings
SECUREAI_DEFAULT_AGENT_TYPE=customer_service
SECUREAI_DEFAULT_PROTECTION_LEVEL=comprehensive
SECUREAI_ENABLE_PERSISTENCE=true
SECUREAI_ENABLE_DEBUG=false

# Logging configuration
SECUREAI_LOG_LEVEL=INFO
SECUREAI_LOG_FILE=secureai_agents.log
"""
    
    with open(".env", 'w') as f:
        f.write(env_content)
    
    print("✅ Environment file created: .env")

def main():
    """Main setup function."""
    print("SecureAI Agent Protection System - Setup")
    print("=" * 50)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)
    
    print(f"✅ Python version: {sys.version}")
    
    # Install dependencies
    if not run_command("pip install -r requirements.txt", "Installing dependencies"):
        print("❌ Failed to install dependencies")
        sys.exit(1)
    
    # Create configuration files
    create_config_file()
    create_environment_file()
    create_example_agents()
    
    # Test installation
    print("\n🔄 Testing SecureAI Agent Protection System...")
    try:
        from agent_privacy_shield import SecureAIAgentPrivacyShield, AgentType, ProtectionLevel
        from ai_agent_pii_shield import create_agent_shield
        
        # Create a test shield
        shield = SecureAIAgentPrivacyShield(
            agent_type=AgentType.CUSTOMER_SERVICE,
            protection_level=ProtectionLevel.BASIC,
            debug_mode=True
        )
        
        print("✅ SecureAI Agent Protection System imported successfully")
        
        # Test basic functionality
        @shield.protect_agent
        def test_agent(data):
            return f"Hello {data.get('name', 'Unknown')}"
        
        result = test_agent({"name": "John Doe", "email": "john@example.com"})
        print(f"✅ Test agent executed successfully: {result}")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Test failed: {e}")
        sys.exit(1)
    
    print("\n" + "=" * 50)
    print("🎉 SecureAI Agent Protection System Setup Complete!")
    print("=" * 50)
    
    print("\n📋 Next Steps:")
    print("1. Configure your .env file with your API keys")
    print("2. Review the examples in the examples/ directory")
    print("3. Run the test script: python test_secureai_agents.py")
    print("4. Start protecting your AI agents!")
    
    print("\n📚 Documentation:")
    print("- README_SECUREAI_AGENTS.md - Complete guide")
    print("- examples/ - Example implementations")
    print("- test_secureai_agents.py - Comprehensive test suite")
    
    print("\n🔧 Configuration:")
    print("- secureai_agents_config.json - System configuration")
    print("- .env - Environment variables")
    
    print("\n🚀 Quick Start:")
    print("from agent_privacy_shield import SecureAIAgentPrivacyShield, AgentType, ProtectionLevel")
    print("@SecureAIAgentPrivacyShield(agent_type=AgentType.CUSTOMER_SERVICE).protect_agent")
    print("def your_agent(data):")
    print("    return 'Protected response'")

if __name__ == "__main__":
    main() 