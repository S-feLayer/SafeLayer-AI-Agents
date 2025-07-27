#!/usr/bin/env python3
"""
SecureAI Privacy Shield SDK Demo
Comprehensive demonstration of PII protection for AI agents
"""

import os
import sys
import time
from typing import List, Dict, Any

# Add the current directory to Python path for local development
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from secureai_sdk import (
        SecureAIShield, 
        RedactionLevel, 
        ContentType,
        protect_ai_agent,
        create_shield,
        quick_redact
    )
    print("✓ SecureAI SDK imported successfully")
except ImportError as e:
    print(f"✗ Failed to import SecureAI SDK: {e}")
    print("Please install the SDK first: pip install secureai-privacy-shield")
    sys.exit(1)

class DemoAIAgent:
    """Demo AI agent that simulates processing user input"""
    
    def __init__(self, name: str = "DemoAgent"):
        self.name = name
        self.conversation_history = []
    
    def process_message(self, message: str) -> str:
        """Simulate AI agent processing a message"""
        # Simulate some processing time
        time.sleep(0.1)
        
        # Simulate AI response (this is where PII could leak)
        response = f"{self.name}: I understand you said '{message}'. Let me help you with that."
        
        # Store in conversation history (this could also leak PII)
        self.conversation_history.append({
            "user": message,
            "agent": response,
            "timestamp": time.time()
        })
        
        return response
    
    def get_conversation_summary(self) -> str:
        """Get a summary of the conversation (could leak PII)"""
        if not self.conversation_history:
            return "No conversation history"
        
        summary = f"Conversation summary ({len(self.conversation_history)} messages):\n"
        for i, conv in enumerate(self.conversation_history[-3:], 1):  # Last 3 messages
            summary += f"{i}. User: {conv['user']}\n"
            summary += f"   Agent: {conv['agent']}\n"
        
        return summary

class ProtectedAIAgent:
    """AI agent with built-in privacy protection"""
    
    def __init__(self, shield: SecureAIShield, name: str = "ProtectedAgent"):
        self.shield = shield
        self.name = name
        self.conversation_history = []
    
    def process_message(self, message: str) -> str:
        """Process message with automatic privacy protection"""
        # Protect input
        protected_input = self.shield.redact(message)
        
        # Process with AI (simulated)
        time.sleep(0.1)
        response = f"{self.name}: I understand you said '{protected_input.redacted_content}'. Let me help you with that."
        
        # Protect output
        protected_response = self.shield.redact(response)
        
        # Store protected conversation
        self.conversation_history.append({
            "user": protected_input.redacted_content,
            "agent": protected_response.redacted_content,
            "timestamp": time.time(),
            "redaction_summary": protected_input.redaction_summary
        })
        
        return protected_response.redacted_content
    
    def get_conversation_summary(self) -> str:
        """Get protected conversation summary"""
        if not self.conversation_history:
            return "No conversation history"
        
        summary = f"Protected conversation summary ({len(self.conversation_history)} messages):\n"
        for i, conv in enumerate(self.conversation_history[-3:], 1):
            summary += f"{i}. User: {conv['user']}\n"
            summary += f"   Agent: {conv['agent']}\n"
            if conv.get('redaction_summary'):
                summary += f"   Redactions: {len(conv['redaction_summary'])} items\n"
        
        return summary

def demo_basic_protection():
    """Demonstrate basic PII protection"""
    print("\n" + "="*60)
    print("DEMO 1: Basic PII Protection")
    print("="*60)
    
    # Initialize shield
    shield = SecureAIShield(
        api_key="demo_key",  # Replace with actual API key
        endpoint="https://demo.secureai.com",  # Replace with actual endpoint
        redaction_level=RedactionLevel.STANDARD
    )
    
    # Test content with various PII types
    test_contents = [
        "My email is john.doe@company.com",
        "Call me at 555-123-4567",
        "My SSN is 123-45-6789",
        "I live at 123 Main Street, Anytown, CA 90210",
        "My credit card is 4111-1111-1111-1111",
        "Contact me at john.doe@company.com or call 555-123-4567"
    ]
    
    for content in test_contents:
        print(f"\nOriginal: {content}")
        
        # Protect content
        result = shield.redact(content)
        
        print(f"Protected: {result.redacted_content}")
        print(f"Processing time: {result.processing_time_ms:.2f}ms")
        
        if result.redaction_summary:
            print(f"Redactions: {result.redaction_summary}")

def demo_ai_agent_comparison():
    """Compare unprotected vs protected AI agents"""
    print("\n" + "="*60)
    print("DEMO 2: AI Agent Protection Comparison")
    print("="*60)
    
    # Initialize shield
    shield = SecureAIShield(
        api_key="demo_key",
        endpoint="https://demo.secureai.com",
        redaction_level=RedactionLevel.STANDARD
    )
    
    # Create both agents
    unprotected_agent = DemoAIAgent("UnprotectedAgent")
    protected_agent = ProtectedAIAgent(shield, "ProtectedAgent")
    
    # Test messages with PII
    test_messages = [
        "My email is user@company.com, can you help me?",
        "Call me at 555-987-6543 for urgent matters",
        "My SSN is 987-65-4321, please keep it secure"
    ]
    
    print("\n--- UNPROTECTED AGENT ---")
    for message in test_messages:
        print(f"\nUser: {message}")
        response = unprotected_agent.process_message(message)
        print(f"Agent: {response}")
    
    print("\n--- PROTECTED AGENT ---")
    for message in test_messages:
        print(f"\nUser: {message}")
        response = protected_agent.process_message(message)
        print(f"Agent: {response}")
    
    # Show conversation summaries
    print("\n--- CONVERSATION SUMMARIES ---")
    print("\nUnprotected Agent Summary:")
    print(unprotected_agent.get_conversation_summary())
    
    print("\nProtected Agent Summary:")
    print(protected_agent.get_conversation_summary())

def demo_decorator_usage():
    """Demonstrate the @protect_ai_agent decorator"""
    print("\n" + "="*60)
    print("DEMO 3: Decorator-Based Protection")
    print("="*60)
    
    # Initialize shield
    shield = SecureAIShield(
        api_key="demo_key",
        endpoint="https://demo.secureai.com",
        redaction_level=RedactionLevel.STANDARD
    )
    
    # Create protected function using decorator
    @protect_ai_agent(shield)
    def ai_chat(message: str) -> str:
        """AI chat function with automatic protection"""
        # Simulate AI processing
        time.sleep(0.1)
        return f"AI: I understand you said '{message}'. Here's my response."
    
    @protect_ai_agent(shield)
    def ai_analyze(text: str) -> str:
        """AI analysis function with automatic protection"""
        # Simulate AI analysis
        time.sleep(0.1)
        return f"Analysis: The text '{text}' contains important information."
    
    # Test the protected functions
    test_messages = [
        "My email is test@example.com",
        "Call 555-111-2222 for support",
        "SSN: 111-22-3333"
    ]
    
    for message in test_messages:
        print(f"\nInput: {message}")
        
        chat_response = ai_chat(message)
        print(f"Chat: {chat_response}")
        
        analysis_response = ai_analyze(message)
        print(f"Analysis: {analysis_response}")

def demo_batch_processing():
    """Demonstrate batch processing capabilities"""
    print("\n" + "="*60)
    print("DEMO 4: Batch Processing")
    print("="*60)
    
    # Initialize shield
    shield = SecureAIShield(
        api_key="demo_key",
        endpoint="https://demo.secureai.com",
        redaction_level=RedactionLevel.STANDARD
    )
    
    # Test batch of content
    batch_contents = [
        "Email: user1@company.com",
        "Phone: 555-111-2222",
        "SSN: 111-22-3333",
        "Address: 123 Main St, City, State 12345",
        "Credit Card: 4111-1111-1111-1111",
        "No sensitive data here",
        "Another email: user2@company.com"
    ]
    
    print(f"Processing batch of {len(batch_contents)} items...")
    
    # Process batch
    start_time = time.time()
    results = shield.redact_batch(batch_contents)
    total_time = time.time() - start_time
    
    print(f"Batch processing completed in {total_time:.2f} seconds")
    print(f"Average time per item: {(total_time/len(batch_contents))*1000:.2f}ms")
    
    # Show results
    for i, result in enumerate(results, 1):
        print(f"\n{i}. Original: {result.original_content}")
        print(f"   Protected: {result.redacted_content}")
        print(f"   Processing time: {result.processing_time_ms:.2f}ms")

def demo_custom_patterns():
    """Demonstrate custom redaction patterns"""
    print("\n" + "="*60)
    print("DEMO 5: Custom Redaction Patterns")
    print("="*60)
    
    # Define custom patterns
    custom_patterns = {
        "company_secrets": r"SECRET-\d{6}",
        "internal_codes": r"CODE-[A-Z]{3}-\d{4}",
        "project_ids": r"PROJ-\d{4}-[A-Z]{2}",
        "api_keys": r"API-[A-Z0-9]{32}"
    }
    
    # Initialize shield with custom patterns
    shield = SecureAIShield(
        api_key="demo_key",
        endpoint="https://demo.secureai.com",
        redaction_level=RedactionLevel.STANDARD,
        custom_patterns=custom_patterns
    )
    
    # Test content with custom patterns
    test_content = """
    Here's some sensitive information:
    - Company secret: SECRET-123456
    - Internal code: CODE-ABC-1234
    - Project ID: PROJ-2024-AI
    - API key: API-1234567890ABCDEF1234567890ABCDEF
    - Regular email: user@company.com
    - Regular phone: 555-123-4567
    """
    
    print("Original content:")
    print(test_content)
    
    # Protect content
    result = shield.redact(test_content)
    
    print("Protected content:")
    print(result.redacted_content)
    
    print(f"\nProcessing time: {result.processing_time_ms:.2f}ms")
    if result.redaction_summary:
        print(f"Redaction summary: {result.redaction_summary}")

def demo_performance_metrics():
    """Demonstrate performance monitoring"""
    print("\n" + "="*60)
    print("DEMO 6: Performance Monitoring")
    print("="*60)
    
    # Initialize shield
    shield = SecureAIShield(
        api_key="demo_key",
        endpoint="https://demo.secureai.com",
        redaction_level=RedactionLevel.STANDARD,
        enable_cache=True
    )
    
    # Process multiple requests to generate metrics
    test_contents = [
        "Email: user1@company.com",
        "Phone: 555-111-2222",
        "Email: user2@company.com",  # Should hit cache
        "SSN: 111-22-3333",
        "Email: user1@company.com",  # Should hit cache
    ]
    
    print("Processing test requests...")
    for content in test_contents:
        result = shield.redact(content)
        print(f"Processed: {content[:30]}... (cached: {result.cached})")
    
    # Get performance metrics
    metrics = shield.get_redaction_summary()
    
    print(f"\nPerformance Metrics:")
    print(f"Total requests: {metrics['total_requests']}")
    print(f"Successful redactions: {metrics['successful_redactions']}")
    print(f"Failed redactions: {metrics['failed_redactions']}")
    print(f"Average processing time: {metrics['average_processing_time_ms']:.2f}ms")
    print(f"Cache hit rate: {metrics['cache_hit_rate']:.2%}")
    print(f"Redaction level: {metrics['redaction_level']}")

def demo_quick_redact():
    """Demonstrate quick redaction utility"""
    print("\n" + "="*60)
    print("DEMO 7: Quick Redaction Utility")
    print("="*60)
    
    # Test content
    content = "Contact me at quick@example.com or call 555-999-8888"
    
    print(f"Original: {content}")
    
    # Quick redaction
    protected = quick_redact(
        content=content,
        api_key="demo_key",
        redaction_level=RedactionLevel.STANDARD
    )
    
    print(f"Protected: {protected}")

def main():
    """Run all demos"""
    print("SecureAI Privacy Shield SDK Demo")
    print("Comprehensive demonstration of PII protection for AI agents")
    print("="*80)
    
    # Check if API key is provided
    api_key = os.getenv("SECUREAI_API_KEY", "demo_key")
    if api_key == "demo_key":
        print("\n⚠️  WARNING: Using demo API key. For real testing, set SECUREAI_API_KEY environment variable.")
        print("   Example: export SECUREAI_API_KEY=your_actual_api_key")
    
    # Run demos
    try:
        demo_basic_protection()
        demo_ai_agent_comparison()
        demo_decorator_usage()
        demo_batch_processing()
        demo_custom_patterns()
        demo_performance_metrics()
        demo_quick_redact()
        
        print("\n" + "="*80)
        print("✓ All demos completed successfully!")
        print("\nNext steps:")
        print("1. Set your actual SECUREAI_API_KEY")
        print("2. Integrate the SDK with your AI agents")
        print("3. Check the documentation for more examples")
        print("4. Contact support@secureai.com for help")
        
    except Exception as e:
        print(f"\n✗ Demo failed: {e}")
        print("This might be due to:")
        print("- Invalid API key")
        print("- Network connectivity issues")
        print("- Service unavailability")
        print("\nPlease check your configuration and try again.")

if __name__ == "__main__":
    main() 