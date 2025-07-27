#!/usr/bin/env python3
"""
SecureAI Agent Shield - Standalone Version
A comprehensive PII protection solution for AI agents with no external dependencies.
"""

import os
import json
import time
import uuid
import functools
import re
from datetime import datetime
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass
from enum import Enum
import logging

# Configure logging
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
    BASIC = "basic"
    STANDARD = "standard"
    COMPREHENSIVE = "comprehensive"
    ENTERPRISE = "enterprise"

@dataclass
class ProtectionResult:
    """Result of agent protection operation."""
    original_input: Any
    protected_input: Any
    original_output: Any
    protected_output: Any
    detected_entities: List[Dict[str, Any]]
    processing_time_ms: float
    agent_id: str
    session_id: str

class SecureAIAgentShield:
    """
    SecureAI Agent Shield - Standalone PII protection for AI agents.
    """
    
    def __init__(self,
                 agent_type: AgentType = AgentType.CUSTOMER_SERVICE,
                 protection_level: ProtectionLevel = ProtectionLevel.COMPREHENSIVE,
                 persistence_enabled: bool = True,
                 debug_mode: bool = False):
        """
        Initialize the SecureAI Agent Shield.
        
        Args:
            agent_type: Type of agent being protected
            protection_level: Level of protection to apply
            persistence_enabled: Enable entity persistence across sessions
            debug_mode: Enable debug mode for development
        """
        self.agent_type = agent_type
        self.protection_level = protection_level
        self.persistence_enabled = persistence_enabled
        self.debug_mode = debug_mode
        
        # Entity persistence storage
        self.entity_mappings = {}
        self.agent_sessions = {}
        
        # Agent-specific configurations
        self.agent_configs = self._initialize_agent_configs()
        
        logger.info(f"SecureAI Agent Shield initialized for {agent_type.value} agent with {protection_level.value} protection")
    
    def _initialize_agent_configs(self) -> Dict[AgentType, Dict[str, Any]]:
        """Initialize agent-specific configurations."""
        configs = {}
        
        for agent_type in AgentType:
            if agent_type == AgentType.CUSTOMER_SERVICE:
                configs[agent_type] = {
                    "protect_customer_data": True,
                    "protect_payment_info": True,
                    "protect_addresses": True,
                    "protect_phone_numbers": True,
                    "protect_email_addresses": True,
                    "protect_order_numbers": True,
                    "protect_account_numbers": True
                }
            elif agent_type == AgentType.DATA_ANALYSIS:
                configs[agent_type] = {
                    "protect_database_credentials": True,
                    "protect_api_keys": True,
                    "protect_business_data": True,
                    "protect_financial_data": True,
                    "protect_personal_identifiers": True,
                    "protect_sensitive_metrics": True
                }
            elif agent_type == AgentType.AUTOMATION:
                configs[agent_type] = {
                    "protect_system_credentials": True,
                    "protect_automation_paths": False,  # Allow automation paths
                    "protect_api_endpoints": True,
                    "protect_configuration_data": True,
                    "protect_log_data": True
                }
            elif agent_type == AgentType.FINANCIAL:
                configs[agent_type] = {
                    "protect_account_numbers": True,
                    "protect_transaction_data": True,
                    "protect_balance_info": True,
                    "protect_routing_numbers": True,
                    "protect_credit_card_data": True,
                    "protect_tax_identifiers": True
                }
            elif agent_type == AgentType.HEALTHCARE:
                configs[agent_type] = {
                    "protect_medical_records": True,
                    "protect_patient_identifiers": True,
                    "protect_diagnosis_data": True,
                    "protect_treatment_plans": True,
                    "protect_insurance_info": True,
                    "protect_pharmacy_data": True
                }
            else:
                configs[agent_type] = {
                    "protect_personal_data": True,
                    "protect_credentials": True,
                    "protect_financial_data": True,
                    "protect_addresses": True
                }
        
        return configs

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
                "detected_entities": []
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
                result = ProtectionResult(
                    original_input={"args": args, "kwargs": kwargs},
                    protected_input={"args": protected_args, "kwargs": protected_kwargs},
                    original_output=original_output,
                    protected_output=protected_output,
                    detected_entities=self._get_detected_entities(session_id),
                    processing_time_ms=processing_time_ms,
                    agent_id=agent_id,
                    session_id=session_id
                )
                
                # Log protection result
                self._log_protection_result(result)
                
                return protected_output
                
            except Exception as e:
                logger.error(f"Error in protected agent {agent_id}: {str(e)}")
                raise
            finally:
                # Clean up session if not persisting
                if not self.persistence_enabled:
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
        """Protect text content by detecting and masking sensitive entities."""
        if not isinstance(text, str):
            return text
        
        # Detect entities based on agent type and protection level
        entities = self._detect_entities(text)
        
        # Store detected entities in session
        self.agent_sessions[session_id]["detected_entities"].extend(entities)
        
        # Apply masking based on protection level
        protected_text = text
        for entity in entities:
            original_value = entity["value"]
            entity_type = entity["type"]
            
            # Get persistent mapping if enabled
            if self.persistence_enabled:
                masked_value = self._get_persistent_mapping(original_value, entity_type, session_id)
            else:
                masked_value = self._get_masked_value(original_value, entity_type)
            
            # Replace in text
            protected_text = protected_text.replace(original_value, masked_value)
        
        return protected_text

    def _detect_entities(self, text: str) -> List[Dict[str, Any]]:
        """Detect sensitive entities in text based on agent configuration."""
        entities = []
        
        # Get agent-specific rules
        agent_config = self.agent_configs.get(self.agent_type, {})
        
        # Email addresses
        if agent_config.get("protect_email_addresses", True):
            email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            for match in re.finditer(email_pattern, text):
                entities.append({
                    "type": "email",
                    "value": match.group(),
                    "start": match.start(),
                    "end": match.end()
                })
        
        # Phone numbers
        if agent_config.get("protect_phone_numbers", True):
            phone_pattern = r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'
            for match in re.finditer(phone_pattern, text):
                entities.append({
                    "type": "phone",
                    "value": match.group(),
                    "start": match.start(),
                    "end": match.end()
                })
        
        # Credit card numbers
        if agent_config.get("protect_credit_card_data", True) or agent_config.get("protect_payment_info", True):
            cc_pattern = r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b'
            for match in re.finditer(cc_pattern, text):
                entities.append({
                    "type": "credit_card",
                    "value": match.group(),
                    "start": match.start(),
                    "end": match.end()
                })
        
        # Social Security Numbers
        ssn_pattern = r'\b\d{3}-\d{2}-\d{4}\b'
        for match in re.finditer(ssn_pattern, text):
            entities.append({
                "type": "ssn",
                "value": match.group(),
                "start": match.start(),
                "end": match.end()
            })
        
        # Account numbers (basic pattern)
        if agent_config.get("protect_account_numbers", True):
            account_pattern = r'\b\d{8,12}\b'
            for match in re.finditer(account_pattern, text):
                # Avoid matching phone numbers and other patterns
                if not re.match(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', match.group()):
                    entities.append({
                        "type": "account_number",
                        "value": match.group(),
                        "start": match.start(),
                        "end": match.end()
                    })
        
        # API Keys
        if agent_config.get("protect_api_keys", True):
            api_key_pattern = r'sk-[a-zA-Z0-9]{32,}'
            for match in re.finditer(api_key_pattern, text):
                entities.append({
                    "type": "api_key",
                    "value": match.group(),
                    "start": match.start(),
                    "end": match.end()
                })
        
        # Database URLs
        if agent_config.get("protect_database_credentials", True):
            db_url_pattern = r'[a-zA-Z]+://[^/\\s]+:[^/\\s]+@[^/\\s]+'
            for match in re.finditer(db_url_pattern, text):
                entities.append({
                    "type": "database_url",
                    "value": match.group(),
                    "start": match.start(),
                    "end": match.end()
                })
        
        return entities

    def _get_persistent_mapping(self, original_value: str, entity_type: str, session_id: str) -> str:
        """Get or create persistent mapping for an entity."""
        mapping_key = f"{entity_type}_{original_value}"
        
        if mapping_key not in self.entity_mappings:
            self.entity_mappings[mapping_key] = self._get_masked_value(original_value, entity_type)
        
        return self.entity_mappings[mapping_key]

    def _get_masked_value(self, original_value: str, entity_type: str) -> str:
        """Generate masked value for an entity."""
        if entity_type == "email":
            parts = original_value.split("@")
            if len(parts) == 2:
                username = parts[0]
                domain = parts[1]
                masked_username = username[0] + "*" * (len(username) - 2) + username[-1] if len(username) > 2 else username
                return f"{masked_username}@{domain}"
        
        elif entity_type == "phone":
            return f"***-***-{original_value[-4:]}"
        
        elif entity_type == "credit_card":
            return f"****-****-****-{original_value[-4:]}"
        
        elif entity_type == "ssn":
            return f"***-**-{original_value[-4:]}"
        
        elif entity_type == "account_number":
            return f"****{original_value[-4:]}"
        
        elif entity_type == "api_key":
            return f"sk-{original_value[3:7]}...{original_value[-4:]}"
        
        elif entity_type == "database_url":
            return "***://***:***@***"
        
        # Default masking
        if len(original_value) <= 4:
            return "*" * len(original_value)
        else:
            return original_value[0] + "*" * (len(original_value) - 2) + original_value[-1]

    def _get_detected_entities(self, session_id: str) -> List[Dict[str, Any]]:
        """Get detected entities for a session."""
        session = self.agent_sessions.get(session_id, {})
        return session.get("detected_entities", [])

    def _log_protection_result(self, result: ProtectionResult):
        """Log protection result for monitoring and analytics."""
        if self.debug_mode:
            logger.info(f"SecureAI Protection Result:")
            logger.info(f"  Agent ID: {result.agent_id}")
            logger.info(f"  Session ID: {result.session_id}")
            logger.info(f"  Processing Time: {result.processing_time_ms:.2f}ms")
            logger.info(f"  Detected Entities: {len(result.detected_entities)}")
            
            for entity in result.detected_entities:
                logger.info(f"    - {entity['type']}: {entity['value']}")

    def get_agent_analytics(self, agent_id: str = None, session_id: str = None) -> Dict[str, Any]:
        """Get analytics for agent protection."""
        analytics = {
            "total_sessions": len(self.agent_sessions),
            "total_entities_detected": 0,
            "entity_breakdown": {},
            "protection_level": self.protection_level.value,
            "agent_type": self.agent_type.value
        }
        
        # Calculate entity breakdown
        for session_data in self.agent_sessions.values():
            if agent_id and session_data.get("agent_id") != agent_id:
                continue
            if session_id and session_data.get("session_id") != session_id:
                continue
            
            entities = session_data.get("detected_entities", [])
            analytics["total_entities_detected"] += len(entities)
            
            for entity in entities:
                entity_type = entity["type"]
                analytics["entity_breakdown"][entity_type] = analytics["entity_breakdown"].get(entity_type, 0) + 1
        
        return analytics

def create_agent_shield(agent_type: AgentType = AgentType.CUSTOMER_SERVICE,
                       protection_level: ProtectionLevel = ProtectionLevel.STANDARD) -> SecureAIAgentShield:
    """
    Factory function to create an AI agent shield.
    
    Args:
        agent_type: Type of agent to protect
        protection_level: Level of protection to apply
        
    Returns:
        Configured SecureAI Agent Shield
    """
    return SecureAIAgentShield(
        agent_type=agent_type,
        protection_level=protection_level,
        persistence_enabled=True
    )

# Example usage
if __name__ == "__main__":
    # Create a customer service agent shield
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
    
    # Test the protected agent
    test_data = {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "phone": "555-123-4567",
        "account_number": "1234567890"
    }
    
    result = customer_service_agent(test_data)
    print(f"Protected Response: {result}") 