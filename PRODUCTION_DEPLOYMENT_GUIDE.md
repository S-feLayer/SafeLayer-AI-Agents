# SecureAI Privacy Shield - Production Deployment Guide

## Overview

This guide provides comprehensive instructions for deploying the SecureAI Privacy Shield to production environments. The system is designed to be scalable, secure, and maintainable with full monitoring and health checking capabilities.

## Prerequisites

### System Requirements

- **Operating System**: Linux (Ubuntu 20.04+ recommended) or Windows Server 2019+
- **Docker**: Version 20.10+ with Docker Compose
- **Memory**: Minimum 4GB RAM, 8GB+ recommended
- **Storage**: 20GB+ available disk space
- **Network**: Stable internet connection for API calls

### Software Dependencies

- Docker Engine 20.10+
- Docker Compose 2.0+
- Git (for code deployment)
- curl (for health checks)

## Quick Start Deployment

### 1. Clone and Setup

```bash
# Clone the repository
git clone <repository-url>
cd secureai-dataloss-AI-Agents

# Make deployment script executable
chmod +x deployment/deploy.sh
```

### 2. Configure Environment

```bash
# Run the deployment script
./deployment/deploy.sh
```

The script will:
- Check prerequisites
- Create necessary directories
- Generate environment configuration
- Build Docker images
- Start all services
- Verify deployment

### 3. Verify Deployment

```bash
# Check service status
docker-compose ps

# View logs
docker-compose logs -f secureai-privacy-shield

# Test health endpoint
curl http://localhost:8000/health
```

## Manual Deployment Steps

### 1. Environment Configuration

Create a `.env` file in the project root:

```bash
# API Configuration
TINFOIL_API_KEY=your_actual_tinfoil_api_key_here
MASQUERADE_ENV=production

# Server Configuration
HOST=0.0.0.0
PORT=8000
WORKERS=4

# Logging Configuration
LOG_LEVEL=INFO
LOG_FILE=logs/secureai.log

# Security Configuration
SECRET_KEY=your_secret_key_here
ALLOWED_HOSTS=localhost,127.0.0.1,your-domain.com

# Rate Limiting
RATE_LIMIT_PER_HOUR=1000
RATE_LIMIT_PER_MINUTE=60

# Cache Configuration
CACHE_ENABLED=true
CACHE_TTL=3600

# Monitoring Configuration
PROMETHEUS_ENABLED=true
GRAFANA_ENABLED=true
```

### 2. Build and Deploy

```bash
# Build Docker images
docker-compose build --no-cache

# Start services
docker-compose up -d

# Verify deployment
docker-compose ps
```

### 3. Service Verification

```bash
# Test main service
curl http://localhost:8000/

# Test health endpoint
curl http://localhost:8000/health

# Test API documentation
curl http://localhost:8000/docs

# Test redaction endpoint
curl -X POST http://localhost:8000/api/redact \
  -H "Content-Type: application/json" \
  -d '{"content": "My email is john.doe@example.com", "content_type": "text"}'
```

## Production Configuration

### Security Hardening

#### 1. SSL/TLS Configuration

Create SSL certificates and configure Nginx:

```bash
# Generate self-signed certificate (for testing)
mkdir -p nginx/ssl
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout nginx/ssl/nginx.key \
  -out nginx/ssl/nginx.crt
```

#### 2. Firewall Configuration

```bash
# Allow only necessary ports
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw enable
```

#### 3. Environment Security

```bash
# Set secure file permissions
chmod 600 .env
chmod 700 logs/
chmod 700 cache/
```

### Performance Optimization

#### 1. Resource Limits

Update `docker-compose.yml` with resource limits:

```yaml
services:
  secureai-privacy-shield:
    # ... existing configuration ...
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 4G
        reservations:
          cpus: '1.0'
          memory: 2G
```

#### 2. Database Optimization

For production databases, consider:

- PostgreSQL for persistent storage
- Redis cluster for high-availability caching
- Connection pooling configuration

#### 3. Load Balancing

For high-traffic deployments:

```yaml
# Add load balancer service
  nginx-lb:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/load-balancer.conf:/etc/nginx/nginx.conf
    depends_on:
      - secureai-privacy-shield-1
      - secureai-privacy-shield-2
```

## Monitoring and Observability

### 1. Prometheus Metrics

Access Prometheus at `http://localhost:9090` to view:

- Request rates and response times
- Error rates and status codes
- System resource usage
- Custom business metrics

### 2. Grafana Dashboards

Access Grafana at `http://localhost:3000` (admin/admin):

- Pre-configured dashboards for:
  - Service health and performance
  - System resource monitoring
  - API usage analytics
  - Error tracking

### 3. Log Management

```bash
# View application logs
docker-compose logs -f secureai-privacy-shield

# View all service logs
docker-compose logs -f

# Export logs for analysis
docker-compose logs > production-logs.txt
```

### 4. Health Monitoring

```bash
# Automated health checks
curl -f http://localhost:8000/health

# Detailed health status
curl http://localhost:8000/health | jq
```

## Backup and Recovery

### 1. Data Backup

```bash
# Backup configuration
tar -czf backup-config-$(date +%Y%m%d).tar.gz config/ .env

# Backup logs
tar -czf backup-logs-$(date +%Y%m%d).tar.gz logs/

# Backup Docker volumes
docker run --rm -v secureai-privacy-shield_redis-data:/data -v $(pwd):/backup alpine tar czf /backup/redis-backup-$(date +%Y%m%d).tar.gz -C /data .
```

### 2. Recovery Procedures

```bash
# Restore from backup
docker-compose down
tar -xzf backup-config-$(date +%Y%m%d).tar.gz
docker-compose up -d
```

## Scaling and High Availability

### 1. Horizontal Scaling

```bash
# Scale the main service
docker-compose up -d --scale secureai-privacy-shield=3

# Update load balancer configuration
# (See nginx/load-balancer.conf example)
```

### 2. Database Scaling

For high-availability databases:

```yaml
services:
  postgres-primary:
    image: postgres:15
    environment:
      POSTGRES_DB: secureai
      POSTGRES_USER: secureai
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres-primary-data:/var/lib/postgresql/data

  postgres-replica:
    image: postgres:15
    environment:
      POSTGRES_DB: secureai
      POSTGRES_USER: secureai
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres-replica-data:/var/lib/postgresql/data
    depends_on:
      - postgres-primary
```

## Troubleshooting

### Common Issues

#### 1. Service Won't Start

```bash
# Check logs
docker-compose logs secureai-privacy-shield

# Check resource usage
docker stats

# Verify environment variables
docker-compose config
```

#### 2. API Key Issues

```bash
# Verify API key is set
echo $TINFOIL_API_KEY

# Test API connectivity
curl -H "Authorization: Bearer $TINFOIL_API_KEY" \
  https://api.tinfoil.ai/v1/health
```

#### 3. Performance Issues

```bash
# Monitor resource usage
docker stats

# Check application metrics
curl http://localhost:8000/api/stats

# Analyze logs for bottlenecks
docker-compose logs secureai-privacy-shield | grep "ERROR\|WARNING"
```

### Debug Mode

Enable debug logging:

```bash
# Update .env file
LOG_LEVEL=DEBUG

# Restart services
docker-compose restart secureai-privacy-shield
```

## Maintenance

### 1. Regular Updates

```bash
# Update code
git pull origin main

# Rebuild and restart
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### 2. Log Rotation

```bash
# Configure log rotation in docker-compose.yml
services:
  secureai-privacy-shield:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

### 3. Security Updates

```bash
# Update base images
docker-compose pull
docker-compose build --no-cache
docker-compose up -d
```

## API Usage Examples

### 1. Basic Redaction

```bash
curl -X POST http://localhost:8000/api/redact \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Contact me at john.doe@example.com or call 555-123-4567",
    "content_type": "text",
    "user_id": "user123"
  }'
```

### 2. Advanced AI Redaction

```bash
curl -X POST http://localhost:8000/api/redact/advanced \
  -H "Content-Type: application/json" \
  -d '{
    "content": "My SSN is 123-45-6789 and I live at 123 Main St",
    "content_type": "text",
    "redaction_level": "strict"
  }'
```

### 3. Get Statistics

```bash
# Service statistics
curl http://localhost:8000/api/stats

# User-specific statistics
curl http://localhost:8000/api/stats/user123
```

## Support and Documentation

### Useful Commands

```bash
# Service management
docker-compose start/stop/restart
docker-compose ps
docker-compose logs -f

# Health monitoring
curl http://localhost:8000/health
curl http://localhost:8000/api/stats

# Configuration
docker-compose config
docker-compose exec secureai-privacy-shield env
```

### Documentation URLs

- API Documentation: http://localhost:8000/docs
- ReDoc Documentation: http://localhost:8000/redoc
- Prometheus Metrics: http://localhost:9090
- Grafana Dashboards: http://localhost:3000

### Getting Help

1. Check the logs: `docker-compose logs -f`
2. Verify configuration: `docker-compose config`
3. Test endpoints: Use the health check and stats endpoints
4. Review this guide for common issues
5. Check the troubleshooting section above

## Security Checklist

- [ ] SSL/TLS certificates configured
- [ ] Firewall rules applied
- [ ] Environment variables secured
- [ ] API keys properly configured
- [ ] Regular security updates scheduled
- [ ] Monitoring and alerting configured
- [ ] Backup procedures tested
- [ ] Access controls implemented

## Performance Checklist

- [ ] Resource limits configured
- [ ] Load balancing implemented (if needed)
- [ ] Caching enabled and optimized
- [ ] Database connections pooled
- [ ] Monitoring dashboards configured
- [ ] Performance baselines established
- [ ] Scaling procedures documented

---

**Note**: This deployment guide covers the essential aspects of production deployment. For enterprise environments, additional considerations such as compliance, audit logging, and advanced security measures may be required. 