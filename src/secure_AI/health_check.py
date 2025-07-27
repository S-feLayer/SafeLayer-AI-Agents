"""
Health Check Module for SecureAI Privacy Shield
Provides comprehensive health monitoring and status reporting.
"""

import os
import time
import psutil
import logging
from typing import Dict, Any, List
from datetime import datetime, timedelta
import requests
from pathlib import Path

logger = logging.getLogger(__name__)

class HealthChecker:
    """Comprehensive health checker for SecureAI services."""
    
    def __init__(self):
        self.start_time = time.time()
        self.health_history: List[Dict[str, Any]] = []
        self.max_history_size = 100
        
    def check_health(self) -> Dict[str, Any]:
        """Perform comprehensive health check."""
        try:
            health_status = {
                "status": "healthy",
                "timestamp": datetime.now().isoformat(),
                "uptime": time.time() - self.start_time,
                "version": "1.0.0",
                "services": {},
                "system": self._check_system_health(),
                "dependencies": self._check_dependencies(),
                "performance": self._check_performance(),
                "errors": []
            }
            
            # Check individual services
            health_status["services"] = {
                "api": self._check_api_health(),
                "database": self._check_database_health(),
                "cache": self._check_cache_health(),
                "external_apis": self._check_external_apis()
            }
            
            # Determine overall status
            if any(service.get("status") == "unhealthy" for service in health_status["services"].values()):
                health_status["status"] = "degraded"
            
            if health_status["errors"]:
                health_status["status"] = "unhealthy"
            
            # Store in history
            self._store_health_status(health_status)
            
            return health_status
            
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return {
                "status": "unhealthy",
                "timestamp": datetime.now().isoformat(),
                "uptime": time.time() - self.start_time,
                "version": "1.0.0",
                "services": {},
                "system": {},
                "dependencies": {},
                "performance": {},
                "errors": [str(e)]
            }
    
    def _check_system_health(self) -> Dict[str, Any]:
        """Check system resources."""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            return {
                "cpu_usage": cpu_percent,
                "memory_usage": memory.percent,
                "memory_available": memory.available,
                "disk_usage": disk.percent,
                "disk_free": disk.free,
                "load_average": self._get_load_average()
            }
        except Exception as e:
            logger.error(f"System health check failed: {e}")
            return {"error": str(e)}
    
    def _check_dependencies(self) -> Dict[str, Any]:
        """Check external dependencies."""
        dependencies = {}
        
        # Check Tinfoil API
        tinfoil_api_key = os.getenv("TINFOIL_API_KEY")
        if tinfoil_api_key:
            dependencies["tinfoil_api"] = self._check_tinfoil_api()
        else:
            dependencies["tinfoil_api"] = {"status": "not_configured"}
        
        # Check database connectivity
        dependencies["database"] = self._check_database_connectivity()
        
        # Check Redis connectivity
        dependencies["redis"] = self._check_redis_connectivity()
        
        return dependencies
    
    def _check_performance(self) -> Dict[str, Any]:
        """Check performance metrics."""
        try:
            # Get recent health history for performance analysis
            recent_checks = self.health_history[-10:] if self.health_history else []
            
            avg_response_time = 0
            if recent_checks:
                response_times = [check.get("response_time", 0) for check in recent_checks]
                avg_response_time = sum(response_times) / len(response_times)
            
            return {
                "average_response_time": avg_response_time,
                "active_connections": self._get_active_connections(),
                "request_rate": self._calculate_request_rate()
            }
        except Exception as e:
            logger.error(f"Performance check failed: {e}")
            return {"error": str(e)}
    
    def _check_api_health(self) -> Dict[str, Any]:
        """Check internal API health."""
        try:
            # Check if main application is responding
            response = requests.get("http://localhost:8000/", timeout=5)
            return {
                "status": "healthy" if response.status_code == 200 else "unhealthy",
                "response_time": response.elapsed.total_seconds() * 1000,
                "status_code": response.status_code
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e)
            }
    
    def _check_database_health(self) -> Dict[str, Any]:
        """Check database health."""
        try:
            # This would check your actual database connection
            # For now, return a mock status
            return {
                "status": "healthy",
                "connection_pool": "active",
                "last_query_time": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e)
            }
    
    def _check_cache_health(self) -> Dict[str, Any]:
        """Check cache health."""
        try:
            # This would check your actual cache (Redis, etc.)
            # For now, return a mock status
            return {
                "status": "healthy",
                "hit_rate": 0.85,
                "memory_usage": "2.1MB"
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e)
            }
    
    def _check_external_apis(self) -> Dict[str, Any]:
        """Check external API health."""
        apis = {}
        
        # Check Tinfoil API
        tinfoil_api_key = os.getenv("TINFOIL_API_KEY")
        if tinfoil_api_key:
            apis["tinfoil"] = self._check_tinfoil_api()
        
        return apis
    
    def _check_tinfoil_api(self) -> Dict[str, Any]:
        """Check Tinfoil API connectivity."""
        try:
            # This would make an actual API call to Tinfoil
            # For now, return a mock status
            return {
                "status": "healthy",
                "response_time": 150,  # ms
                "last_check": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e)
            }
    
    def _check_database_connectivity(self) -> Dict[str, Any]:
        """Check database connectivity."""
        try:
            # This would check your actual database connection
            # For now, return a mock status
            return {
                "status": "healthy",
                "connection_pool": "active"
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e)
            }
    
    def _check_redis_connectivity(self) -> Dict[str, Any]:
        """Check Redis connectivity."""
        try:
            # This would check your actual Redis connection
            # For now, return a mock status
            return {
                "status": "healthy",
                "memory_usage": "2.1MB"
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e)
            }
    
    def _get_load_average(self) -> List[float]:
        """Get system load average."""
        try:
            return list(psutil.getloadavg())
        except Exception:
            return [0, 0, 0]
    
    def _get_active_connections(self) -> int:
        """Get number of active connections."""
        try:
            # This would count actual active connections
            # For now, return a mock value
            return 5
        except Exception:
            return 0
    
    def _calculate_request_rate(self) -> float:
        """Calculate requests per second."""
        try:
            # This would calculate actual request rate
            # For now, return a mock value
            return 10.5
        except Exception:
            return 0.0
    
    def _store_health_status(self, status: Dict[str, Any]):
        """Store health status in history."""
        self.health_history.append(status)
        
        # Keep only recent history
        if len(self.health_history) > self.max_history_size:
            self.health_history = self.health_history[-self.max_history_size:]
    
    def get_health_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent health history."""
        return self.health_history[-limit:] if self.health_history else []
    
    def get_uptime(self) -> float:
        """Get service uptime in seconds."""
        return time.time() - self.start_time
    
    def is_healthy(self) -> bool:
        """Check if service is healthy."""
        health = self.check_health()
        return health["status"] == "healthy"
    
    def get_status_summary(self) -> Dict[str, Any]:
        """Get a summary of current status."""
        health = self.check_health()
        return {
            "status": health["status"],
            "uptime": health["uptime"],
            "version": health["version"],
            "timestamp": health["timestamp"]
        }

class HealthMetrics:
    """Health metrics collector for Prometheus."""
    
    def __init__(self):
        self.metrics = {}
    
    def record_metric(self, name: str, value: float, labels: Dict[str, str] = None):
        """Record a metric."""
        if name not in self.metrics:
            self.metrics[name] = []
        
        metric = {
            "value": value,
            "timestamp": time.time(),
            "labels": labels or {}
        }
        self.metrics[name].append(metric)
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get all metrics."""
        return self.metrics
    
    def get_metric(self, name: str) -> List[Dict[str, Any]]:
        """Get specific metric."""
        return self.metrics.get(name, [])

# Global health checker instance
health_checker = HealthChecker()
metrics = HealthMetrics()
