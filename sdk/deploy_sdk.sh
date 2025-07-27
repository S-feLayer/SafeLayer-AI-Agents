#!/bin/bash

# SecureAI Privacy Shield SDK Deployment Script
# This script packages and prepares the SDK for distribution to companies

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Print functions
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

# Configuration
SDK_VERSION="1.0.0"
BUILD_DIR="build"
DIST_DIR="dist"
PYTHON_SDK_DIR="python"
JS_SDK_DIR="javascript"

print_status "SecureAI Privacy Shield SDK Deployment"
print_status "Version: $SDK_VERSION"
echo "=============================================="

# Create build directories
print_status "Creating build directories..."
mkdir -p "$BUILD_DIR" "$DIST_DIR"

# Package Python SDK
package_python_sdk() {
    print_status "Packaging Python SDK..."
    
    PYTHON_PACKAGE_DIR="$BUILD_DIR/secureai-privacy-shield-python"
    mkdir -p "$PYTHON_PACKAGE_DIR"
    
    # Copy Python SDK files
    cp secureai_sdk.py "$PYTHON_PACKAGE_DIR/"
    cp requirements.txt "$PYTHON_PACKAGE_DIR/"
    cp README.md "$PYTHON_PACKAGE_DIR/"
    
    # Create setup.py for Python package
    cat > "$PYTHON_PACKAGE_DIR/setup.py" << EOF
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="secureai-privacy-shield",
    version="$SDK_VERSION",
    author="SecureAI",
    author_email="support@secureai.com",
    description="Comprehensive PII protection SDK for AI agents",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/secureai/privacy-shield-sdk",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Security",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    keywords="privacy, pii, ai, security, redaction, gdpr, compliance",
    project_urls={
        "Bug Reports": "https://github.com/secureai/privacy-shield-sdk/issues",
        "Source": "https://github.com/secureai/privacy-shield-sdk",
        "Documentation": "https://docs.secureai.com",
    },
)
EOF

    # Create __init__.py for package
    cat > "$PYTHON_PACKAGE_DIR/__init__.py" << EOF
"""
SecureAI Privacy Shield SDK
Comprehensive PII protection for AI agents.
"""

from .secureai_sdk import (
    SecureAIShield,
    RedactionResult,
    ProtectionMetrics,
    SecureAIError,
    RedactionLevel,
    ContentType,
    protect_ai_agent,
    create_shield,
    quick_redact
)

__version__ = "$SDK_VERSION"
__author__ = "SecureAI"
__email__ = "support@secureai.com"

__all__ = [
    "SecureAIShield",
    "RedactionResult", 
    "ProtectionMetrics",
    "SecureAIError",
    "RedactionLevel",
    "ContentType",
    "protect_ai_agent",
    "create_shield",
    "quick_redact"
]
EOF

    # Create MANIFEST.in
    cat > "$PYTHON_PACKAGE_DIR/MANIFEST.in" << EOF
include README.md
include requirements.txt
include LICENSE
recursive-include docs *
recursive-include examples *
EOF

    # Create LICENSE file
    cat > "$PYTHON_PACKAGE_DIR/LICENSE" << EOF
MIT License

Copyright (c) 2024 SecureAI

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
EOF

    # Create examples directory
    mkdir -p "$PYTHON_PACKAGE_DIR/examples"
    
    # Create basic example
    cat > "$PYTHON_PACKAGE_DIR/examples/basic_usage.py" << EOF
#!/usr/bin/env python3
"""
Basic usage example for SecureAI Privacy Shield SDK
"""

from secureai_sdk import SecureAIShield, RedactionLevel

def main():
    # Initialize the shield
    shield = SecureAIShield(
        api_key="your_secureai_api_key",
        redaction_level=RedactionLevel.STANDARD
    )
    
    # Example content with PII
    content = "Contact me at john.doe@company.com or call 555-123-4567"
    
    # Protect the content
    result = shield.redact(content)
    
    print(f"Original: {content}")
    print(f"Protected: {result.redacted_content}")
    print(f"Processing time: {result.processing_time_ms}ms")
    print(f"Redaction summary: {result.redaction_summary}")

if __name__ == "__main__":
    main()
EOF

    # Create AI agent example
    cat > "$PYTHON_PACKAGE_DIR/examples/ai_agent_integration.py" << EOF
#!/usr/bin/env python3
"""
AI Agent integration example for SecureAI Privacy Shield SDK
"""

from secureai_sdk import protect_ai_agent, SecureAIShield

# Initialize the shield
shield = SecureAIShield(api_key="your_secureai_api_key")

# Example AI agent function
@protect_ai_agent(shield)
def ai_chat(message: str) -> str:
    """Example AI agent that processes user messages"""
    # Simulate AI processing
    return f"AI response to: {message}"

def main():
    # Test with sensitive data
    test_messages = [
        "My email is user@company.com",
        "Call me at 555-123-4567",
        "My SSN is 123-45-6789"
    ]
    
    for message in test_messages:
        response = ai_chat(message)
        print(f"Input: {message}")
        print(f"Output: {response}")
        print("-" * 50)

if __name__ == "__main__":
    main()
EOF

    # Create batch processing example
    cat > "$PYTHON_PACKAGE_DIR/examples/batch_processing.py" << EOF
#!/usr/bin/env python3
"""
Batch processing example for SecureAI Privacy Shield SDK
"""

import asyncio
from secureai_sdk import SecureAIShield

async def main():
    # Initialize the shield
    shield = SecureAIShield(api_key="your_secureai_api_key")
    
    # Example batch of content
    contents = [
        "Email: user1@company.com",
        "Phone: 555-111-2222",
        "SSN: 123-45-6789",
        "Address: 123 Main St, City, State 12345"
    ]
    
    # Process batch
    results = await shield.redact_batch_async(contents)
    
    for i, result in enumerate(results):
        print(f"Item {i+1}:")
        print(f"  Original: {result.original_content}")
        print(f"  Protected: {result.redacted_content}")
        print(f"  Processing time: {result.processing_time_ms}ms")
        print()

if __name__ == "__main__":
    asyncio.run(main())
EOF

    # Create zip file
    cd "$BUILD_DIR"
    zip -r "../$DIST_DIR/secureai-privacy-shield-python-$SDK_VERSION.zip" secureai-privacy-shield-python/
    cd ..
    
    print_success "Python SDK packaged successfully"
}

# Package JavaScript SDK
package_javascript_sdk() {
    print_status "Packaging JavaScript SDK..."
    
    JS_PACKAGE_DIR="$BUILD_DIR/secureai-privacy-shield-js"
    mkdir -p "$JS_PACKAGE_DIR"
    
    # Copy JavaScript SDK files
    cp secureai-sdk.js "$JS_PACKAGE_DIR/"
    cp package.json "$JS_PACKAGE_DIR/"
    cp README.md "$JS_PACKAGE_DIR/"
    
    # Create LICENSE file
    cp "$PYTHON_PACKAGE_DIR/LICENSE" "$JS_PACKAGE_DIR/"
    
    # Create examples directory
    mkdir -p "$JS_PACKAGE_DIR/examples"
    
    # Create basic example
    cat > "$JS_PACKAGE_DIR/examples/basic_usage.js" << EOF
/**
 * Basic usage example for SecureAI Privacy Shield SDK
 */

const { SecureAIShield, RedactionLevel } = require('../secureai-sdk.js');

async function main() {
    // Initialize the shield
    const shield = new SecureAIShield({
        apiKey: 'your_secureai_api_key',
        redactionLevel: RedactionLevel.STANDARD
    });
    
    // Example content with PII
    const content = 'Contact me at john.doe@company.com or call 555-123-4567';
    
    // Protect the content
    const result = await shield.redact(content);
    
    console.log(\`Original: \${content}\`);
    console.log(\`Protected: \${result.redactedContent}\`);
    console.log(\`Processing time: \${result.processingTimeMs}ms\`);
    console.log(\`Redaction summary: \${JSON.stringify(result.redactionSummary)}\`);
}

main().catch(console.error);
EOF

    # Create AI agent example
    cat > "$JS_PACKAGE_DIR/examples/ai_agent_integration.js" << EOF
/**
 * AI Agent integration example for SecureAI Privacy Shield SDK
 */

const { SecureAIShield, protectAIAgent } = require('../secureai-sdk.js');

// Initialize the shield
const shield = new SecureAIShield({ apiKey: 'your_secureai_api_key' });

// Example AI agent class
class AIAgent {
    constructor(shield) {
        this.shield = shield;
    }
    
    @protectAIAgent(shield)
    async chat(message) {
        // Simulate AI processing
        return \`AI response to: \${message}\`;
    }
}

async function main() {
    const aiAgent = new AIAgent(shield);
    
    // Test with sensitive data
    const testMessages = [
        'My email is user@company.com',
        'Call me at 555-123-4567',
        'My SSN is 123-45-6789'
    ];
    
    for (const message of testMessages) {
        const response = await aiAgent.chat(message);
        console.log(\`Input: \${message}\`);
        console.log(\`Output: \${response}\`);
        console.log('-'.repeat(50));
    }
}

main().catch(console.error);
EOF

    # Create batch processing example
    cat > "$JS_PACKAGE_DIR/examples/batch_processing.js" << EOF
/**
 * Batch processing example for SecureAI Privacy Shield SDK
 */

const { SecureAIShield } = require('../secureai-sdk.js');

async function main() {
    // Initialize the shield
    const shield = new SecureAIShield({ apiKey: 'your_secureai_api_key' });
    
    // Example batch of content
    const contents = [
        'Email: user1@company.com',
        'Phone: 555-111-2222',
        'SSN: 123-45-6789',
        'Address: 123 Main St, City, State 12345'
    ];
    
    // Process batch
    const results = await shield.redactBatch(contents);
    
    results.forEach((result, i) => {
        console.log(\`Item \${i+1}:\`);
        console.log(\`  Original: \${result.originalContent}\`);
        console.log(\`  Protected: \${result.redactedContent}\`);
        console.log(\`  Processing time: \${result.processingTimeMs}ms\`);
        console.log();
    });
}

main().catch(console.error);
EOF

    # Create zip file
    cd "$BUILD_DIR"
    zip -r "../$DIST_DIR/secureai-privacy-shield-js-$SDK_VERSION.zip" secureai-privacy-shield-js/
    cd ..
    
    print_success "JavaScript SDK packaged successfully"
}

# Create comprehensive documentation
create_documentation() {
    print_status "Creating comprehensive documentation..."
    
    DOCS_DIR="$BUILD_DIR/docs"
    mkdir -p "$DOCS_DIR"
    
    # Copy integration guide
    cp ../docs/ai_agent_integration_guide.md "$DOCS_DIR/"
    
    # Create API reference
    cat > "$DOCS_DIR/api_reference.md" << EOF
# SecureAI Privacy Shield API Reference

## Python SDK

### SecureAIShield Class

The main class for interacting with SecureAI Privacy Shield.

#### Constructor

\`\`\`python
SecureAIShield(
    api_key: str,
    endpoint: str = "https://api.secureai.com",
    redaction_level: RedactionLevel = RedactionLevel.STANDARD,
    enable_cache: bool = True,
    cache_ttl: int = 3600,
    timeout: int = 30,
    max_retries: int = 3,
    custom_patterns: Optional[Dict[str, str]] = None
)
\`\`\`

#### Methods

- \`redact(content, content_type, user_id, use_cache)\` - Redact sensitive information
- \`redact_async(content, content_type, user_id, use_cache)\` - Async redaction
- \`redact_batch(contents, content_type, user_id, use_cache)\` - Batch redaction
- \`redact_batch_async(contents, content_type, user_id, use_cache)\` - Async batch redaction
- \`contains_pii(content)\` - Check if content contains PII
- \`get_redaction_count(content)\` - Get number of redactions
- \`get_redaction_summary()\` - Get protection metrics
- \`health_check()\` - Check service health
- \`clear_cache()\` - Clear the cache

## JavaScript SDK

### SecureAIShield Class

The main class for interacting with SecureAI Privacy Shield.

#### Constructor

\`\`\`javascript
new SecureAIShield({
    apiKey: string,
    endpoint?: string,
    redactionLevel?: RedactionLevel,
    enableCache?: boolean,
    cacheTtl?: number,
    timeout?: number,
    maxRetries?: number,
    customPatterns?: object
})
\`\`\`

#### Methods

- \`redact(content, contentType, userId, useCache)\` - Redact sensitive information
- \`redactBatch(contents, contentType, userId, useCache)\` - Batch redaction
- \`containsPII(content)\` - Check if content contains PII
- \`getRedactionCount(content)\` - Get number of redactions
- \`getRedactionSummary()\` - Get protection metrics
- \`healthCheck()\` - Check service health
- \`clearCache()\` - Clear the cache
EOF

    # Create deployment guide
    cat > "$DOCS_DIR/deployment_guide.md" << EOF
# SecureAI Privacy Shield Deployment Guide

## Production Deployment

### Docker Deployment

\`\`\`dockerfile
FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["python", "ai_agent_with_protection.py"]
\`\`\`

### Kubernetes Deployment

\`\`\`yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: protected-ai-agent
spec:
  replicas: 3
  selector:
    matchLabels:
      app: protected-ai-agent
  template:
    metadata:
      labels:
        app: protected-ai-agent
    spec:
      containers:
      - name: ai-agent
        image: your-registry/protected-ai-agent:latest
        env:
        - name: SECUREAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: secureai-secret
              key: api-key
\`\`\`

## Configuration

### Environment Variables

- \`SECUREAI_API_KEY\` - Your SecureAI API key
- \`SECUREAI_ENDPOINT\` - SecureAI API endpoint (optional)
- \`SECUREAI_REDACTION_LEVEL\` - Redaction level (basic/standard/strict)
- \`SECUREAI_ENABLE_CACHE\` - Enable caching (true/false)
- \`SECUREAI_CACHE_TTL\` - Cache TTL in seconds

### Security Best Practices

1. Store API keys in environment variables or secrets
2. Use HTTPS for all API communications
3. Implement proper error handling
4. Monitor API usage and performance
5. Regular security audits
EOF

    # Create zip file
    cd "$BUILD_DIR"
    zip -r "../$DIST_DIR/secureai-documentation-$SDK_VERSION.zip" docs/
    cd ..
    
    print_success "Documentation created successfully"
}

# Create installation script
create_install_script() {
    print_status "Creating installation script..."
    
    cat > "$DIST_DIR/install_sdk.sh" << 'EOF'
#!/bin/bash

# SecureAI Privacy Shield SDK Installation Script
# This script installs the SDK for companies

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

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

print_status "SecureAI Privacy Shield SDK Installation"
echo "=============================================="

# Check if Python is installed
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    print_error "Python is not installed. Please install Python 3.8+ first."
    exit 1
fi

print_status "Python version: $($PYTHON_CMD --version)"

# Check if pip is installed
if ! command -v pip3 &> /dev/null && ! command -v pip &> /dev/null; then
    print_error "pip is not installed. Please install pip first."
    exit 1
fi

# Install Python SDK
print_status "Installing Python SDK..."
if command -v pip3 &> /dev/null; then
    pip3 install secureai-privacy-shield
else
    pip install secureai-privacy-shield
fi

# Check if Node.js is installed
if command -v node &> /dev/null; then
    print_status "Node.js version: $(node --version)"
    
    # Install JavaScript SDK
    print_status "Installing JavaScript SDK..."
    npm install secureai-privacy-shield
else
    print_warning "Node.js is not installed. JavaScript SDK will not be installed."
fi

print_success "SDK installation completed successfully!"
print_status "Next steps:"
echo "1. Get your API key from https://secureai.com"
echo "2. Check the documentation in the docs/ directory"
echo "3. Run the examples to test the installation"
echo "4. Integrate with your AI agents"

EOF

    chmod +x "$DIST_DIR/install_sdk.sh"
    print_success "Installation script created"
}

# Create test script
create_test_script() {
    print_status "Creating test script..."
    
    cat > "$DIST_DIR/test_sdk.py" << 'EOF'
#!/usr/bin/env python3
"""
Test script for SecureAI Privacy Shield SDK
"""

import sys
import os

def test_import():
    """Test if the SDK can be imported"""
    try:
        from secureai_sdk import SecureAIShield, RedactionLevel, ContentType
        print("✓ SDK import successful")
        return True
    except ImportError as e:
        print(f"✗ SDK import failed: {e}")
        return False

def test_basic_functionality():
    """Test basic SDK functionality"""
    try:
        from secureai_sdk import SecureAIShield, RedactionLevel
        
        # Create shield instance (without API key for testing)
        shield = SecureAIShield(
            api_key="test_key",
            endpoint="https://test.secureai.com",
            redaction_level=RedactionLevel.STANDARD
        )
        
        print("✓ Shield instance created successfully")
        return True
    except Exception as e:
        print(f"✗ Basic functionality test failed: {e}")
        return False

def test_redaction_levels():
    """Test redaction level enums"""
    try:
        from secureai_sdk import RedactionLevel
        
        levels = [RedactionLevel.BASIC, RedactionLevel.STANDARD, RedactionLevel.STRICT]
        for level in levels:
            print(f"✓ Redaction level: {level.value}")
        
        return True
    except Exception as e:
        print(f"✗ Redaction levels test failed: {e}")
        return False

def test_content_types():
    """Test content type enums"""
    try:
        from secureai_sdk import ContentType
        
        types = [ContentType.TEXT, ContentType.CODE, ContentType.JSON, ContentType.PDF, ContentType.EMAIL]
        for content_type in types:
            print(f"✓ Content type: {content_type.value}")
        
        return True
    except Exception as e:
        print(f"✗ Content types test failed: {e}")
        return False

def main():
    print("SecureAI Privacy Shield SDK Test")
    print("================================")
    
    tests = [
        ("Import Test", test_import),
        ("Basic Functionality", test_basic_functionality),
        ("Redaction Levels", test_redaction_levels),
        ("Content Types", test_content_types)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\nRunning {test_name}...")
        if test_func():
            passed += 1
        else:
            print(f"✗ {test_name} failed")
    
    print(f"\nTest Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("✓ All tests passed! SDK is ready to use.")
        return 0
    else:
        print("✗ Some tests failed. Please check the installation.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
EOF

    chmod +x "$DIST_DIR/test_sdk.py"
    print_success "Test script created"
}

# Main execution
main() {
    print_status "Starting SDK deployment process..."
    
    # Package SDKs
    package_python_sdk
    package_javascript_sdk
    
    # Create documentation
    create_documentation
    
    # Create installation and test scripts
    create_install_script
    create_test_script
    
    # Create final distribution summary
    cat > "$DIST_DIR/README.txt" << EOF
SecureAI Privacy Shield SDK - Distribution Package
==================================================

Version: $SDK_VERSION
Date: $(date)

This package contains everything needed to integrate SecureAI Privacy Shield 
with your AI agents and applications.

Contents:
- secureai-privacy-shield-python-$SDK_VERSION.zip: Python SDK package
- secureai-privacy-shield-js-$SDK_VERSION.zip: JavaScript SDK package  
- secureai-documentation-$SDK_VERSION.zip: Comprehensive documentation
- install_sdk.sh: Installation script
- test_sdk.py: Test script to verify installation

Quick Start:
1. Run: chmod +x install_sdk.sh && ./install_sdk.sh
2. Run: python test_sdk.py
3. Check the documentation for integration examples

For support: support@secureai.com
Documentation: https://docs.secureai.com
GitHub: https://github.com/secureai/privacy-shield-sdk

EOF

    print_success "SDK deployment completed successfully!"
    print_status "Distribution files created in $DIST_DIR/:"
    ls -la "$DIST_DIR/"
    
    print_status "Next steps:"
    echo "1. Test the SDK packages"
    echo "2. Upload to package repositories (PyPI, npm)"
    echo "3. Distribute to companies"
    echo "4. Update documentation website"
}

# Run main function
main "$@" 