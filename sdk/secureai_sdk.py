"""
SecureAI Privacy Shield SDK
Comprehensive Python SDK for integrating privacy protection with AI agents.
"""

import requests
import json
import time
import logging
from typing import Dict, List, Optional, Union, Any
from dataclasses import dataclass
from enum import Enum
import asyncio
import aiohttp
from functools import wraps

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RedactionLevel(Enum):
    """Redaction levels for different privacy requirements."""
    BASIC = "basic"      # Email, phone, SSN
    STANDARD = "standard"  # Includes addresses, names
    STRICT = "strict"    # All PII types

class ContentType(Enum):
    """Supported content types for redaction."""
    TEXT = "text"
    CODE = "code"
    JSON = "json"
    PDF = "pdf"
    EMAIL = "email"

@dataclass
class RedactionResult:
    """Result of a redaction operation."""
    redacted_content: str
    original_content: str
    redaction_summary: Dict[str, Any]
    processing_time_ms: float
    cached: bool = False
    error: Optional[str] = None

@dataclass
class ProtectionMetrics:
    """Metrics for protection operations."""
    total_requests: int = 0
    successful_redactions: int = 0
    failed_redactions: int = 0
    total_processing_time_ms: float = 0.0
    cache_hits: int = 0
    cache_misses: int = 0

class SecureAIError(Exception):
    """Base exception for SecureAI SDK errors."""
    pass

class SecureAIShield:
    """
    Main SecureAI Privacy Shield client for protecting AI agent data.
    
    This SDK provides comprehensive PII protection for AI agents, including
    real-time detection, automatic redaction, and compliance features.
    """
    
    def __init__(
        self,
        api_key: str,
        endpoint: str = "https://api.secureai.com",
        redaction_level: RedactionLevel = RedactionLevel.STANDARD,
        enable_cache: bool = True,
        cache_ttl: int = 3600,
        timeout: int = 30,
        max_retries: int = 3,
        custom_patterns: Optional[Dict[str, str]] = None
    ):
        """
        Initialize the SecureAI Shield.
        
        Args:
            api_key: Your SecureAI API key
            endpoint: SecureAI API endpoint
            redaction_level: Level of redaction to apply
            enable_cache: Enable caching for better performance
            cache_ttl: Cache time-to-live in seconds
            timeout: Request timeout in seconds
            max_retries: Maximum retry attempts
            custom_patterns: Custom redaction patterns
        """
        self.api_key = api_key
        self.endpoint = endpoint.rstrip('/')
        self.redaction_level = redaction_level
        self.enable_cache = enable_cache
        self.cache_ttl = cache_ttl
        self.timeout = timeout
        self.max_retries = max_retries
        self.custom_patterns = custom_patterns or {}
        
        # Initialize cache
        self._cache = {}
        self._cache_timestamps = {}
        
        # Initialize metrics
        self.metrics = ProtectionMetrics()
        
        # Session for connection pooling
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
            'User-Agent': 'SecureAI-SDK/1.0.0'
        })
        
        logger.info(f"SecureAI Shield initialized with endpoint: {endpoint}")
    
    def redact(
        self,
        content: str,
        content_type: ContentType = ContentType.TEXT,
        user_id: Optional[str] = None,
        use_cache: bool = True
    ) -> RedactionResult:
        """
        Redact sensitive information from content.
        
        Args:
            content: Content to redact
            content_type: Type of content being processed
            user_id: User identifier for tracking
            use_cache: Whether to use caching
            
        Returns:
            RedactionResult with redacted content and metadata
        """
        start_time = time.time()
        
        try:
            # Check cache first
            if use_cache and self.enable_cache:
                cache_key = self._generate_cache_key(content, content_type)
                cached_result = self._get_from_cache(cache_key)
                if cached_result:
                    self.metrics.cache_hits += 1
                    return cached_result
            
            # Prepare request
            payload = {
                "content": content,
                "content_type": content_type.value,
                "redaction_level": self.redaction_level.value,
                "user_id": user_id or "anonymous",
                "use_cache": use_cache
            }
            
            # Add custom patterns if provided
            if self.custom_patterns:
                payload["custom_patterns"] = self.custom_patterns
            
            # Make API request
            response = self._make_request("/api/redact", payload)
            
            # Process response
            processing_time = (time.time() - start_time) * 1000
            
            result = RedactionResult(
                redacted_content=response.get("redacted_content", content),
                original_content=content,
                redaction_summary=response.get("redaction_summary", {}),
                processing_time_ms=processing_time,
                cached=response.get("cached", False)
            )
            
            # Cache result
            if use_cache and self.enable_cache:
                cache_key = self._generate_cache_key(content, content_type)
                self._add_to_cache(cache_key, result)
            
            # Update metrics
            self.metrics.total_requests += 1
            self.metrics.successful_redactions += 1
            self.metrics.total_processing_time_ms += processing_time
            
            return result
            
        except Exception as e:
            # Update metrics
            self.metrics.total_requests += 1
            self.metrics.failed_redactions += 1
            
            logger.error(f"Redaction failed: {e}")
            return RedactionResult(
                redacted_content=content,  # Return original content on error
                original_content=content,
                redaction_summary={},
                processing_time_ms=(time.time() - start_time) * 1000,
                error=str(e)
            )
    
    async def redact_async(
        self,
        content: str,
        content_type: ContentType = ContentType.TEXT,
        user_id: Optional[str] = None,
        use_cache: bool = True
    ) -> RedactionResult:
        """
        Asynchronously redact sensitive information from content.
        
        Args:
            content: Content to redact
            content_type: Type of content being processed
            user_id: User identifier for tracking
            use_cache: Whether to use caching
            
        Returns:
            RedactionResult with redacted content and metadata
        """
        start_time = time.time()
        
        try:
            # Check cache first
            if use_cache and self.enable_cache:
                cache_key = self._generate_cache_key(content, content_type)
                cached_result = self._get_from_cache(cache_key)
                if cached_result:
                    self.metrics.cache_hits += 1
                    return cached_result
            
            # Prepare request
            payload = {
                "content": content,
                "content_type": content_type.value,
                "redaction_level": self.redaction_level.value,
                "user_id": user_id or "anonymous",
                "use_cache": use_cache
            }
            
            # Add custom patterns if provided
            if self.custom_patterns:
                payload["custom_patterns"] = self.custom_patterns
            
            # Make async API request
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.endpoint}/api/redact",
                    json=payload,
                    headers={
                        'Authorization': f'Bearer {self.api_key}',
                        'Content-Type': 'application/json'
                    },
                    timeout=aiohttp.ClientTimeout(total=self.timeout)
                ) as response:
                    response_data = await response.json()
            
            # Process response
            processing_time = (time.time() - start_time) * 1000
            
            result = RedactionResult(
                redacted_content=response_data.get("redacted_content", content),
                original_content=content,
                redaction_summary=response_data.get("redaction_summary", {}),
                processing_time_ms=processing_time,
                cached=response_data.get("cached", False)
            )
            
            # Cache result
            if use_cache and self.enable_cache:
                cache_key = self._generate_cache_key(content, content_type)
                self._add_to_cache(cache_key, result)
            
            # Update metrics
            self.metrics.total_requests += 1
            self.metrics.successful_redactions += 1
            self.metrics.total_processing_time_ms += processing_time
            
            return result
            
        except Exception as e:
            # Update metrics
            self.metrics.total_requests += 1
            self.metrics.failed_redactions += 1
            
            logger.error(f"Async redaction failed: {e}")
            return RedactionResult(
                redacted_content=content,
                original_content=content,
                redaction_summary={},
                processing_time_ms=(time.time() - start_time) * 1000,
                error=str(e)
            )
    
    def redact_batch(
        self,
        contents: List[str],
        content_type: ContentType = ContentType.TEXT,
        user_id: Optional[str] = None,
        use_cache: bool = True
    ) -> List[RedactionResult]:
        """
        Redact multiple content items efficiently.
        
        Args:
            contents: List of content to redact
            content_type: Type of content being processed
            user_id: User identifier for tracking
            use_cache: Whether to use caching
            
        Returns:
            List of RedactionResult objects
        """
        results = []
        
        for content in contents:
            result = self.redact(content, content_type, user_id, use_cache)
            results.append(result)
        
        return results
    
    async def redact_batch_async(
        self,
        contents: List[str],
        content_type: ContentType = ContentType.TEXT,
        user_id: Optional[str] = None,
        use_cache: bool = True
    ) -> List[RedactionResult]:
        """
        Asynchronously redact multiple content items efficiently.
        
        Args:
            contents: List of content to redact
            content_type: Type of content being processed
            user_id: User identifier for tracking
            use_cache: Whether to use caching
            
        Returns:
            List of RedactionResult objects
        """
        tasks = [
            self.redact_async(content, content_type, user_id, use_cache)
            for content in contents
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Handle exceptions
        processed_results = []
        for result in results:
            if isinstance(result, Exception):
                logger.error(f"Batch redaction failed: {result}")
                processed_results.append(RedactionResult(
                    redacted_content="",
                    original_content="",
                    redaction_summary={},
                    processing_time_ms=0,
                    error=str(result)
                ))
            else:
                processed_results.append(result)
        
        return processed_results
    
    def contains_pii(self, content: str) -> bool:
        """
        Check if content contains PII without redacting.
        
        Args:
            content: Content to check
            
        Returns:
            True if PII is detected, False otherwise
        """
        try:
            payload = {
                "content": content,
                "content_type": ContentType.TEXT.value,
                "check_only": True
            }
            
            response = self._make_request("/api/check", payload)
            return response.get("contains_pii", False)
            
        except Exception as e:
            logger.error(f"PII check failed: {e}")
            return True  # Assume PII present on error for safety
    
    def get_redaction_count(self, content: str) -> int:
        """
        Get the number of redactions performed on content.
        
        Args:
            content: Content to analyze
            
        Returns:
            Number of redactions performed
        """
        try:
            payload = {
                "content": content,
                "content_type": ContentType.TEXT.value,
                "analyze_only": True
            }
            
            response = self._make_request("/api/analyze", payload)
            return response.get("redaction_count", 0)
            
        except Exception as e:
            logger.error(f"Redaction count analysis failed: {e}")
            return 0
    
    def get_redaction_summary(self) -> Dict[str, Any]:
        """
        Get a summary of redaction operations.
        
        Returns:
            Dictionary with redaction summary
        """
        return {
            "total_requests": self.metrics.total_requests,
            "successful_redactions": self.metrics.successful_redactions,
            "failed_redactions": self.metrics.failed_redactions,
            "average_processing_time_ms": (
                self.metrics.total_processing_time_ms / max(self.metrics.total_requests, 1)
            ),
            "cache_hit_rate": (
                self.metrics.cache_hits / max(self.metrics.total_requests, 1)
            ),
            "redaction_level": self.redaction_level.value
        }
    
    def health_check(self) -> bool:
        """
        Check if the SecureAI service is healthy.
        
        Returns:
            True if service is healthy, False otherwise
        """
        try:
            response = self._make_request("/health", {})
            return response.get("status") == "healthy"
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return False
    
    def _make_request(self, endpoint: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Make HTTP request to SecureAI API."""
        url = f"{self.endpoint}{endpoint}"
        
        for attempt in range(self.max_retries):
            try:
                response = self.session.post(
                    url,
                    json=payload,
                    timeout=self.timeout
                )
                response.raise_for_status()
                return response.json()
                
            except requests.exceptions.RequestException as e:
                if attempt == self.max_retries - 1:
                    raise SecureAIError(f"API request failed: {e}")
                
                logger.warning(f"Request failed, retrying ({attempt + 1}/{self.max_retries}): {e}")
                time.sleep(2 ** attempt)  # Exponential backoff
    
    def _generate_cache_key(self, content: str, content_type: ContentType) -> str:
        """Generate cache key for content."""
        import hashlib
        key_data = f"{content}:{content_type.value}:{self.redaction_level.value}"
        return hashlib.md5(key_data.encode()).hexdigest()
    
    def _get_from_cache(self, cache_key: str) -> Optional[RedactionResult]:
        """Get result from cache if valid."""
        if cache_key in self._cache:
            timestamp = self._cache_timestamps.get(cache_key, 0)
            if time.time() - timestamp < self.cache_ttl:
                self.metrics.cache_hits += 1
                return self._cache[cache_key]
            else:
                # Remove expired cache entry
                del self._cache[cache_key]
                del self._cache_timestamps[cache_key]
        
        self.metrics.cache_misses += 1
        return None
    
    def _add_to_cache(self, cache_key: str, result: RedactionResult):
        """Add result to cache."""
        self._cache[cache_key] = result
        self._cache_timestamps[cache_key] = time.time()
        
        # Clean up old cache entries
        current_time = time.time()
        expired_keys = [
            key for key, timestamp in self._cache_timestamps.items()
            if current_time - timestamp > self.cache_ttl
        ]
        
        for key in expired_keys:
            del self._cache[key]
            del self._cache_timestamps[key]
    
    def clear_cache(self):
        """Clear the cache."""
        self._cache.clear()
        self._cache_timestamps.clear()
        logger.info("Cache cleared")
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.session.close()


# Decorator for automatic protection
def protect_ai_agent(shield: SecureAIShield, content_type: ContentType = ContentType.TEXT):
    """
    Decorator to automatically protect AI agent functions.
    
    Args:
        shield: SecureAI Shield instance
        content_type: Type of content being processed
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Extract content from arguments
            content = None
            if args:
                content = args[0]
            elif 'content' in kwargs:
                content = kwargs['content']
            elif 'message' in kwargs:
                content = kwargs['message']
            elif 'input' in kwargs:
                content = kwargs['input']
            
            if content and isinstance(content, str):
                # Protect input
                protected_content = shield.redact(content, content_type)
                
                # Update arguments with protected content
                if args:
                    args = (protected_content.redacted_content,) + args[1:]
                else:
                    kwargs['content'] = protected_content.redacted_content
                
                # Call original function
                result = func(*args, **kwargs)
                
                # Protect output if it's a string
                if isinstance(result, str):
                    protected_result = shield.redact(result, content_type)
                    return protected_result.redacted_content
                
                return result
            
            return func(*args, **kwargs)
        
        return wrapper
    return decorator


# Utility functions
def create_shield(
    api_key: str,
    endpoint: Optional[str] = None,
    redaction_level: RedactionLevel = RedactionLevel.STANDARD,
    **kwargs
) -> SecureAIShield:
    """
    Create a SecureAI Shield instance with default settings.
    
    Args:
        api_key: Your SecureAI API key
        endpoint: SecureAI API endpoint (optional)
        redaction_level: Level of redaction to apply
        **kwargs: Additional configuration options
        
    Returns:
        Configured SecureAIShield instance
    """
    return SecureAIShield(
        api_key=api_key,
        endpoint=endpoint or "https://api.secureai.com",
        redaction_level=redaction_level,
        **kwargs
    )


def quick_redact(
    content: str,
    api_key: str,
    redaction_level: RedactionLevel = RedactionLevel.STANDARD
) -> str:
    """
    Quick redaction function for simple use cases.
    
    Args:
        content: Content to redact
        api_key: Your SecureAI API key
        redaction_level: Level of redaction to apply
        
    Returns:
        Redacted content
    """
    with create_shield(api_key, redaction_level=redaction_level) as shield:
        result = shield.redact(content)
        return result.redacted_content


# Example usage
if __name__ == "__main__":
    # Example 1: Basic usage
    shield = SecureAIShield(api_key="your_api_key_here")
    
    content = "My email is john.doe@company.com and my phone is 555-123-4567"
    result = shield.redact(content)
    print(f"Original: {content}")
    print(f"Redacted: {result.redacted_content}")
    print(f"Summary: {result.redaction_summary}")
    
    # Example 2: With decorator
    @protect_ai_agent(shield)
    def ai_chat(message: str) -> str:
        # Simulate AI processing
        return f"AI response to: {message}"
    
    response = ai_chat("My SSN is 123-45-6789")
    print(f"Protected AI response: {response}")
    
    # Example 3: Quick redaction
    quick_result = quick_redact(
        "Contact me at jane.smith@email.com",
        api_key="your_api_key_here"
    )
    print(f"Quick redaction: {quick_result}") 