#!/usr/bin/env python3
"""
SecureSecureSecureAI Agent PII Shield - AI Agent Protection System
Protect AI agents from PII exposure with easy-to-use decorators and comprehensive protection.
"""

import os
import json
import time
import uuid
import functools
from datetime import datetime
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass
from enum import Enum
import logging

# Import the core protection components
from src.secure_AI.ai_privacy_shield import SecureAIPrivacyShield
from src.secure_AI.enhanced_detection import EnhancedDetection
from src.secure_AI.advanced_masking import AdvancedMasking, MaskingStrategy

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AgentType(Enum):
    """Types of AI agents that can be protected."""
    CUSTOMER_SERVICE = "customer_service"
    DATA_ANALYSIS = "data_analysis"
    AUTOMATION = "automation"
    CHATBOT = "chatbot"
    RESEARCH = "research"
    MULTI_AGENT = "multi_agent"
    FINANCIAL = "financial"
    HEALTHCARE = "healthcare"
    AUTONOMOUS = "autonomous"
    DEBUGGING = "debugging"

class ProtectionLevel(Enum):
    """Protection levels for different use cases."""
    BASIC = "basic"           # Minimal protection
    STANDARD = "standard"     # Standard PII protection
    COMPREHENSIVE = "comprehensive"  # Full protection
    ENTERPRISE = "enterprise" # Maximum security

@dataclass
class AgentProtectionResult:
    """Result of agent protection operation."""
    original_input: Any
    protected_input: Any
    original_output: Any
    protected_output: Any
    detected_pii: List[Dict[str, Any]]
    processing_time_ms: float
    agent_id: str
    session_id: str
    protection_level: str

class SecureAIAgentPIIShield:
    """
    SecureSecureSecureAI Agent PII Shield - Protects AI agents from PII exposure.
    """
    
    def __init__(self,
                 agent_type: AgentType = AgentType.CUSTOMER_SERVICE,
                 protection_level: ProtectionLevel = ProtectionLevel.STANDARD,
                 tinfoil_api_key: str = None,
                 enable_persistence: bool = True):
        """
        Initialize the SecureSecureSecureAI Agent PII Shield.
        
        Args:
            agent_type: Type of agent being protected
            protection_level: Level of protection to apply
            tinfoil_api_key: Optional Tinfoil API key for advanced detection
            enable_persistence: Enable entity persistence across sessions
        """
        self.agent_type = agent_type
        self.protection_level = protection_level
        self.enable_persistence = enable_persistence
        
        # Initialize core protection components
        self.privacy_shield = SecureAIPrivacyShield(
            tinfoil_api_key=tinfoil_api_key,
            enable_persistence=enable_persistence
        )
        
        # Agent-specific configurations
        self.agent_configs = self._get_agent_config(agent_type, protection_level)
        
        # Session tracking
        self.agent_sessions = {}
        
        logger.info(f"SecureSecureSecureAI Agent PII Shield initialized for {agent_type.value} agent with {protection_level.value} protection")
    
    def _get_agent_config(self, agent_type: AgentType, protection_level: ProtectionLevel) -> Dict[str, Any]:
        """Get agent-specific configuration."""
        base_config = {
            "enable_customer_data": True,
            "enable_financial_data": True,
            "enable_personal_info": True,
            "enable_credentials": True,
            "enable_api_keys": True,
            "enable_addresses": True,
            "enable_phone_numbers": True,
            "enable_email_addresses": True,
            "enable_ssn": True,
            "enable_credit_cards": True,
            "enable_account_numbers": True,
            "enable_medical_data": False,
            "enable_tax_data": False,
            "enable_automation_paths": False,
            "enable_log_data": False
        }
        
        # Agent-specific overrides
        if agent_type == AgentType.CUSTOMER_SERVICE:
            base_config.update({
                "enable_customer_data": True,
                "enable_order_data": True,
                "enable_payment_info": True,
                "enable_contact_info": True
            })
        elif agent_type == AgentType.DATA_ANALYSIS:
            base_config.update({
                "enable_database_credentials": True,
                "enable_api_keys": True,
                "enable_business_data": True,
                "enable_sensitive_metrics": True
            })
        elif agent_type == AgentType.AUTOMATION:
            base_config.update({
                "enable_system_credentials": True,
                "enable_automation_paths": False,  # Allow automation paths
                "enable_api_endpoints": True,
                "enable_configuration_data": True,
                "enable_log_data": False  # Allow log data for automation
            })
        elif agent_type == AgentType.FINANCIAL:
            base_config.update({
                "enable_financial_data": True,
                "enable_account_numbers": True,
                "enable_transaction_data": True,
                "enable_balance_info": True,
                "enable_routing_numbers": True,
                "enable_tax_data": True
            })
        elif agent_type == AgentType.HEALTHCARE:
            base_config.update({
                "enable_medical_data": True,
                "enable_patient_identifiers": True,
                "enable_diagnosis_data": True,
                "enable_treatment_plans": True,
                "enable_insurance_info": True,
                "enable_pharmacy_data": True
            })
        elif agent_type == AgentType.CHATBOT:
            base_config.update({
                "enable_personal_info": True,
                "enable_contact_info": True,
                "enable_location_data": True,
                "enable_preferences": True
            })
        elif agent_type == AgentType.RESEARCH:
            base_config.update({
                "enable_personal_data": True,
                "enable_research_data": False,  # Allow research data
                "enable_publications": False,   # Allow publications
                "enable_methodologies": False   # Allow methodologies
            })
        
        # Protection level adjustments
        if protection_level == ProtectionLevel.BASIC:
            base_config.update({
                "enable_ssn": False,
                "enable_credit_cards": False,
                "enable_medical_data": False,
                "enable_tax_data": False
            })
        elif protection_level == ProtectionLevel.ENTERPRISE:
            base_config.update({
                "enable_all": True,
                "enable_advanced_detection": True,
                "enable_ai_enhanced_detection": True
            })
        
        return base_config

    def protect_agent(self, func: Callable) -> Callable:
        """
        Decorator to protect an AI agent function.
        
        Args:
            func: The function to protect
            
        Returns:
            Protected function wrapper
        """
        @functools.wraps(func)
        def protected_wrapper(*args, **kwargs):
            start_time = time.time()
            agent_id = str(uuid.uuid4())
            session_id = str(uuid.uuid4())
            
            # Store session info
            self.agent_sessions[session_id] = {
                "agent_id": agent_id,
                "agent_type": self.agent_type.value,
                "protection_level": self.protection_level.value,
                "start_time": datetime.now().isoformat(),
                "detected_pii": []
            }
            
            try:
                # Protect input data
                protected_args = self._protect_input(args, session_id)
                protected_kwargs = self._protect_input(kwargs, session_id)
                
                # Execute the original function
                original_output = func(*protected_args, **protected_kwargs)
                
                # Protect output data
                protected_output = self._protect_output(original_output, session_id)
                
                # Calculate processing time
                processing_time_ms = (time.time() - start_time) * 1000
                
                # Create protection result
                result = AgentProtectionResult(
                    original_input={"args": args, "kwargs": kwargs},
                    protected_input={"args": protected_args, "kwargs": protected_kwargs},
                    original_output=original_output,
                    protected_output=protected_output,
                    detected_pii=self._get_detected_pii(session_id),
                    processing_time_ms=processing_time_ms,
                    agent_id=agent_id,
                    session_id=session_id,
                    protection_level=self.protection_level.value
                )
                
                # Log protection result
                self._log_protection_result(result)
                
                return protected_output
                
            except Exception as e:
                logger.error(f"Error in protected agent {agent_id}: {str(e)}")
                raise
            finally:
                # Clean up session if not persisting
                if not self.enable_persistence:
                    self.agent_sessions.pop(session_id, None)
        
        return protected_wrapper

    def _protect_input(self, data: Any, session_id: str) -> Any:
        """Protect input data based on agent configuration."""
        if isinstance(data, str):
            return self._protect_text(data, session_id)
        elif isinstance(data, dict):
            return {k: self._protect_input(v, session_id) for k, v in data.items()}
        elif isinstance(data, list):
            return [self._protect_input(item, session_id) for item in data]
        elif isinstance(data, tuple):
            return tuple(self._protect_input(item, session_id) for item in data)
        else:
            return data

    def _protect_output(self, data: Any, session_id: str) -> Any:
        """Protect output data based on agent configuration."""
        return self._protect_input(data, session_id)

    def _protect_text(self, text: str, session_id: str) -> str:
        """Protect text content using the core privacy shield."""
        if not isinstance(text, str):
            return text
        
        # Use the core privacy shield for text protection
        protected_text, detected_entities = self.privacy_shield.protect_text(
            text, 
            agent_type=self.agent_type.value,
            protection_level=self.protection_level.value
        )
        
        # Store detected PII in session
        self.agent_sessions[session_id]["detected_pii"].extend(detected_entities)
        
        return protected_text

    def _get_detected_pii(self, session_id: str) -> List[Dict[str, Any]]:
        """Get detected PII for a session."""
        session = self.agent_sessions.get(session_id, {})
        return session.get("detected_pii", [])

    def _log_protection_result(self, result: AgentProtectionResult):
        """Log protection result for monitoring and analytics."""
        logger.info(f"SecureAI Agent Protection Result:")
        logger.info(f"  Agent ID: {result.agent_id}")
        logger.info(f"  Session ID: {result.session_id}")
        logger.info(f"  Agent Type: {self.agent_type.value}")
        logger.info(f"  Protection Level: {result.protection_level}")
        logger.info(f"  Processing Time: {result.processing_time_ms:.2f}ms")
        logger.info(f"  Detected PII: {len(result.detected_pii)}")
        
        for pii in result.detected_pii:
            logger.info(f"    - {pii['type']}: {pii['value']}")

    def get_agent_stats(self, agent_id: str = None) -> Dict[str, Any]:
        """Get statistics for agent protection."""
        stats = {
            "total_sessions": len(self.agent_sessions),
            "total_pii_detected": 0,
            "pii_breakdown": {},
            "agent_type": self.agent_type.value,
            "protection_level": self.protection_level.value
        }
        
        for session_data in self.agent_sessions.values():
            if agent_id and session_data.get("agent_id") != agent_id:
                continue
            
            pii_list = session_data.get("detected_pii", [])
            stats["total_pii_detected"] += len(pii_list)
            
            for pii in pii_list:
                pii_type = pii["type"]
                stats["pii_breakdown"][pii_type] = stats["pii_breakdown"].get(pii_type, 0) + 1
        
        return stats

def create_agent_shield(agent_type: AgentType = AgentType.CUSTOMER_SERVICE,
                       protection_level: ProtectionLevel = ProtectionLevel.STANDARD,
                       tinfoil_api_key: str = None) -> SecureAIAgentPIIShield:
    """
    Factory function to create an AI agent shield.
    
    Args:
        agent_type: Type of agent to protect
        protection_level: Level of protection to apply
        tinfoil_api_key: Optional Tinfoil API key for advanced detection
        
    Returns:
        Configured SecureSecureSecureAI Agent PII Shield
    """
    return SecureAIAgentPIIShield(
        agent_type=agent_type,
        protection_level=protection_level,
        tinfoil_api_key=tinfoil_api_key,
        enable_persistence=True
    )

# Example usage
if __name__ == "__main__":
    # Create a customer service agent shield
    customer_shield = create_agent_shield(
        agent_type=AgentType.CUSTOMER_SERVICE,
        protection_level=ProtectionLevel.COMPREHENSIVE
    )
    
    @customer_shield.protect_agent
    def customer_service_agent(customer_data: Dict[str, Any]) -> str:
        # This agent will automatically have PII protection
        customer_name = customer_data.get("name", "Unknown")
        customer_email = customer_data.get("email", "unknown@example.com")
        customer_phone = customer_data.get("phone", "555-0000")
        
        response = f"Hello {customer_name}, I can help you with your inquiry. I'll contact you at {customer_email} or {customer_phone}."
        return response
    
    # Test the protected agent
    test_data = {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "phone": "555-123-4567",
        "account_number": "1234567890"
    }
    
    result = customer_service_agent(test_data)
    print(f"Protected Response: {result}")
    
    # Get agent statistics
    stats = customer_shield.get_agent_stats()
    print(f"Agent Stats: {stats}") 