#!/usr/bin/env python3
"""
SecureAI Privacy Shield - Main Application Entry Point
Production-ready FastAPI server with comprehensive PII protection capabilities.
"""

import os
import sys
import logging
from pathlib import Path
from typing import Dict, Any, Optional
from contextlib import asynccontextmanager

# Add src directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from fastapi import FastAPI, HTTPException, Depends, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
import uvicorn
from dotenv import load_dotenv

# Import SecureAI components
from secure_AI.proxy_redaction_service import ProxyRedactionService
from secure_AI.ai_privacy_shield import AIPrivacyShield
from secure_AI.advanced_masking import AdvancedMasking
from secure_AI.health_check import HealthChecker

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=getattr(logging, os.getenv("LOG_LEVEL", "INFO")),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(os.getenv("LOG_FILE", "logs/secureai.log")),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Security
security = HTTPBearer(auto_error=False)

# Global service instances
proxy_service: Optional[ProxyRedactionService] = None
ai_shield: Optional[AIPrivacyShield] = None
health_checker: Optional[HealthChecker] = None

# Pydantic models
class RedactRequest(BaseModel):
    content: str = Field(..., description="Content to redact")
    content_type: str = Field(default="text", description="Type of content (text, code, json, etc.)")
    user_id: str = Field(default="anonymous", description="User identifier")
    use_cache: bool = Field(default=True, description="Whether to use caching")
    redaction_level: str = Field(default="standard", description="Redaction level (basic, standard, strict)")

class RedactResponse(BaseModel):
    success: bool
    redacted_content: str
    redaction_summary: Dict[str, Any]
    processing_time_ms: float
    cached: bool = False
    error: Optional[str] = None

class HealthResponse(BaseModel):
    status: str
    services: Dict[str, str]
    version: str
    uptime: float

class StatsResponse(BaseModel):
    total_requests: int
    successful_requests: int
    failed_requests: int
    average_processing_time: float
    cache_hit_rate: float
    active_users: int

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager for startup and shutdown."""
    global proxy_service, ai_shield, health_checker
    
    # Startup
    logger.info("Starting SecureAI Privacy Shield...")
    
    try:
        # Initialize services
        tinfoil_api_key = os.getenv("TINFOIL_API_KEY")
        if not tinfoil_api_key:
            logger.warning("TINFOIL_API_KEY not set. Some features may be limited.")
        
        proxy_service = ProxyRedactionService(
            tinfoil_api_key=tinfoil_api_key,
            rate_limit_per_hour=int(os.getenv("RATE_LIMIT_PER_HOUR", "1000"))
        )
        
        ai_shield = AIPrivacyShield(
            api_key=tinfoil_api_key,
            model_name=os.getenv("AI_MODEL", "llama-3.3-70b")
        )
        
        health_checker = HealthChecker()
        
        logger.info("SecureAI Privacy Shield started successfully")
        
    except Exception as e:
        logger.error(f"Failed to start SecureAI Privacy Shield: {e}")
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down SecureAI Privacy Shield...")
    if proxy_service:
        proxy_service.cleanup()
    logger.info("SecureAI Privacy Shield shutdown complete")

# Create FastAPI app
app = FastAPI(
    title="SecureAI Privacy Shield",
    description="Production-ready PII protection and redaction service with AI-powered detection",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")
)

# Rate limiting middleware
class RateLimiter:
    def __init__(self):
        self.requests = {}
    
    def is_allowed(self, user_id: str) -> bool:
        import time
        current_time = time.time()
        minute_ago = current_time - 60
        
        if user_id not in self.requests:
            self.requests[user_id] = []
        
        # Clean old requests
        self.requests[user_id] = [req for req in self.requests[user_id] if req > minute_ago]
        
        # Check rate limit
        max_requests = int(os.getenv("RATE_LIMIT_PER_MINUTE", "60"))
        if len(self.requests[user_id]) >= max_requests:
            return False
        
        self.requests[user_id].append(current_time)
        return True

rate_limiter = RateLimiter()

# Dependency for authentication
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """Simple authentication - can be enhanced with proper JWT validation."""
    if not credentials:
        return "anonymous"
    
    # In production, validate JWT token here
    # For now, just return the token as user_id
    return credentials.credentials

# Dependency for rate limiting
async def check_rate_limit(user_id: str = Depends(get_current_user)):
    """Check rate limiting for the user."""
    if not rate_limiter.is_allowed(user_id):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded. Please try again later."
        )
    return user_id

@app.get("/", response_model=Dict[str, str])
async def root():
    """Root endpoint with service information."""
    return {
        "service": "SecureAI Privacy Shield",
        "version": "1.0.0",
        "status": "operational",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    if not health_checker:
        raise HTTPException(status_code=503, detail="Service not initialized")
    
    health_status = health_checker.check_health()
    return HealthResponse(**health_status)

@app.post("/api/redact", response_model=RedactResponse)
async def redact_content(
    request: RedactRequest,
    user_id: str = Depends(check_rate_limit)
):
    """Main redaction endpoint."""
    if not proxy_service:
        raise HTTPException(status_code=503, detail="Service not available")
    
    try:
        import time
        start_time = time.time()
        
        # Perform redaction
        result = proxy_service.redact_content(
            content=request.content,
            content_type=request.content_type,
            user_identifier=user_id,
            use_cache=request.use_cache
        )
        
        processing_time = (time.time() - start_time) * 1000
        
        return RedactResponse(
            success=True,
            redacted_content=result.get("redacted_content", request.content),
            redaction_summary=result.get("summary", {}),
            processing_time_ms=processing_time,
            cached=result.get("cached", False)
        )
        
    except Exception as e:
        logger.error(f"Redaction failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/redact/advanced", response_model=RedactResponse)
async def advanced_redact(
    request: RedactRequest,
    user_id: str = Depends(check_rate_limit)
):
    """Advanced redaction with AI-powered detection."""
    if not ai_shield:
        raise HTTPException(status_code=503, detail="AI service not available")
    
    try:
        import time
        start_time = time.time()
        
        # Use AI shield for advanced redaction
        result = ai_shield.redact_content(
            content=request.content,
            content_type=request.content_type,
            redaction_level=request.redaction_level
        )
        
        processing_time = (time.time() - start_time) * 1000
        
        return RedactResponse(
            success=True,
            redacted_content=result.get("redacted_content", request.content),
            redaction_summary=result.get("summary", {}),
            processing_time_ms=processing_time,
            cached=False
        )
        
    except Exception as e:
        logger.error(f"Advanced redaction failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/stats", response_model=StatsResponse)
async def get_service_stats():
    """Get service statistics."""
    if not proxy_service:
        raise HTTPException(status_code=503, detail="Service not available")
    
    try:
        stats = proxy_service.get_service_stats()
        return StatsResponse(**stats)
    except Exception as e:
        logger.error(f"Failed to get stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/stats/{user_id}")
async def get_user_stats(user_id: str):
    """Get user-specific statistics."""
    if not proxy_service:
        raise HTTPException(status_code=503, detail="Service not available")
    
    try:
        return proxy_service.get_user_stats(user_id)
    except Exception as e:
        logger.error(f"Failed to get user stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler."""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "detail": str(exc)}
    )

if __name__ == "__main__":
    # Production server configuration
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    workers = int(os.getenv("WORKERS", "4"))
    
    logger.info(f"Starting SecureAI Privacy Shield on {host}:{port}")
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        workers=workers,
        log_level=os.getenv("LOG_LEVEL", "info").lower(),
        access_log=True,
        reload=False  # Disable reload in production
    ) 