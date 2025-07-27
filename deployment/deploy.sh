#!/bin/bash

# SecureAI Privacy Shield - Production Deployment Script
# This script handles complete production deployment setup

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_NAME="secureai-privacy-shield"
DOCKER_COMPOSE_FILE="docker-compose.yml"
ENV_FILE=".env"
LOG_DIR="logs"
CACHE_DIR="cache"
CONFIG_DIR="config"

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check prerequisites
check_prerequisites() {
    print_status "Checking prerequisites..."
    
    # Check Docker
    if ! command_exists docker; then
        print_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    # Check Docker Compose
    if ! command_exists docker-compose; then
        print_error "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi
    
    # Check if Docker daemon is running
    if ! docker info >/dev/null 2>&1; then
        print_error "Docker daemon is not running. Please start Docker first."
        exit 1
    fi
    
    print_success "All prerequisites are satisfied"
}

# Function to create necessary directories
create_directories() {
    print_status "Creating necessary directories..."
    
    mkdir -p "$LOG_DIR"
    mkdir -p "$CACHE_DIR"
    mkdir -p "$CONFIG_DIR"
    mkdir -p "test_files"
    
    print_success "Directories created"
}

# Function to setup environment file
setup_environment() {
    print_status "Setting up environment configuration..."
    
    if [ ! -f "$ENV_FILE" ]; then
        cat > "$ENV_FILE" << EOF
# SecureAI Privacy Shield Environment Configuration
# Production Environment Variables

# API Configuration
TINFOIL_API_KEY=your_tinfoil_api_key_here
SECUREAI_ENV=production

# Server Configuration
HOST=0.0.0.0
PORT=8000
WORKERS=4

# Database Configuration (if using)
DATABASE_URL=sqlite:///secureai.db

# Redis Configuration (if using)
REDIS_URL=redis://localhost:6379

# Logging Configuration
LOG_LEVEL=INFO
LOG_FILE=logs/secureai.log

# Security Configuration
SECRET_KEY=$(openssl rand -hex 32)
ALLOWED_HOSTS=localhost,127.0.0.1

# Rate Limiting
RATE_LIMIT_PER_HOUR=1000
RATE_LIMIT_PER_MINUTE=60

# Cache Configuration
CACHE_ENABLED=true
CACHE_TTL=3600

# Monitoring Configuration
PROMETHEUS_ENABLED=true
GRAFANA_ENABLED=true
EOF
        print_warning "Environment file created. Please update TINFOIL_API_KEY with your actual API key."
    else
        print_status "Environment file already exists"
    fi
}

# Function to validate configuration
validate_configuration() {
    print_status "Validating configuration..."
    
    # Check if TINFOIL_API_KEY is set
    if [ -f "$ENV_FILE" ]; then
        if grep -q "TINFOIL_API_KEY=your_tinfoil_api_key_here" "$ENV_FILE"; then
            print_warning "TINFOIL_API_KEY is not set. Please update the .env file with your actual API key."
        fi
    fi
    
    # Check if required files exist
    if [ ! -f "requirements.txt" ]; then
        print_error "requirements.txt not found"
        exit 1
    fi
    
    if [ ! -f "Dockerfile" ]; then
        print_error "Dockerfile not found"
        exit 1
    fi
    
    if [ ! -f "$DOCKER_COMPOSE_FILE" ]; then
        print_error "docker-compose.yml not found"
        exit 1
    fi
    
    print_success "Configuration validation completed"
}

# Function to build Docker images
build_images() {
    print_status "Building Docker images..."
    
    docker-compose build --no-cache
    
    print_success "Docker images built successfully"
}

# Function to start services
start_services() {
    print_status "Starting services..."
    
    # Start services in detached mode
    docker-compose up -d
    
    print_success "Services started successfully"
}

# Function to check service health
check_health() {
    print_status "Checking service health..."
    
    # Wait for services to start
    sleep 10
    
    # Check if main service is running
    if docker-compose ps | grep -q "Up"; then
        print_success "Services are running"
        
        # Check health endpoint if available
        if command_exists curl; then
            if curl -f http://localhost:8000/health >/dev/null 2>&1; then
                print_success "Health check passed"
            else
                print_warning "Health check failed - service may still be starting"
            fi
        fi
    else
        print_error "Services failed to start"
        docker-compose logs
        exit 1
    fi
}

# Function to display deployment information
display_info() {
    print_success "Deployment completed successfully!"
    echo
    echo "Service Information:"
    echo "==================="
    echo "Main Service: http://localhost:8000"
    echo "API Documentation: http://localhost:8000/docs"
    echo "Health Check: http://localhost:8000/health"
    echo "Prometheus: http://localhost:9090"
    echo "Grafana: http://localhost:3000 (admin/admin)"
    echo
    echo "Useful Commands:"
    echo "==============="
    echo "View logs: docker-compose logs -f"
    echo "Stop services: docker-compose down"
    echo "Restart services: docker-compose restart"
    echo "Update services: docker-compose pull && docker-compose up -d"
    echo
    echo "Monitoring:"
    echo "==========="
    echo "Check service status: docker-compose ps"
    echo "View resource usage: docker stats"
    echo
}

# Function to handle cleanup on script exit
cleanup() {
    if [ $? -ne 0 ]; then
        print_error "Deployment failed. Cleaning up..."
        docker-compose down
    fi
}

# Main deployment function
main() {
    echo "SecureAI Privacy Shield - Production Deployment"
    echo "=============================================="
    echo
    
    # Set up cleanup trap
    trap cleanup EXIT
    
    # Run deployment steps
    check_prerequisites
    create_directories
    setup_environment
    validate_configuration
    build_images
    start_services
    check_health
    display_info
}

# Run main function
main "$@"
