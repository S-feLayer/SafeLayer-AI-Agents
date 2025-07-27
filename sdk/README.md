# SecureAI Privacy Shield SDK

Comprehensive PII protection SDK for AI agents. Protect sensitive data with real-time detection and automatic redaction.

## Features

- **Real-time PII Detection**: Automatically detect emails, phone numbers, SSNs, addresses, and custom patterns
- **Automatic Redaction**: Intelligently redact sensitive information before processing
- **High Performance**: Process thousands of requests per second with sub-50ms response times
- **Compliance Ready**: Meet GDPR, CCPA, HIPAA, and other privacy regulations
- **Easy Integration**: Simple SDKs for Python, JavaScript, and direct API integration
- **Comprehensive Monitoring**: Track protection effectiveness with detailed metrics

## Quick Start

### Python SDK

```bash
pip install secureai-privacy-shield
```

```python
from secureai_sdk import SecureAIShield

# Initialize the shield
shield = SecureAIShield(
    api_key="your_secureai_api_key",
    endpoint="https://your-secureai-instance.com"
)

# Protect AI agent input
user_input = "My email is john.doe@company.com and my phone is 555-123-4567"
protected_input = shield.redact(user_input)

# Process with AI agent
ai_response = ai_agent.process(protected_input.redacted_content)

# Protect AI agent output
protected_response = shield.redact(ai_response)
```

### JavaScript SDK

```bash
npm install secureai-privacy-shield
```

```javascript
const { SecureAIShield } = require('secureai-privacy-shield');

// Initialize the shield
const shield = new SecureAIShield({
    apiKey: 'your_secureai_api_key',
    endpoint: 'https://your-secureai-instance.com'
});

// Protect AI agent processing
async function processWithProtection(userInput) {
    // Protect input
    const protectedInput = await shield.redact(userInput);
    
    // Process with AI agent
    const aiResponse = await aiAgent.process(protectedInput.redactedContent);
    
    // Protect output
    const protectedResponse = await shield.redact(aiResponse);
    
    return protectedResponse;
}
```

## Installation

### Python SDK

```bash
# Install from PyPI
pip install secureai-privacy-shield

# Or install from source
git clone https://github.com/secureai/privacy-shield-sdk
cd privacy-shield-sdk/python
pip install -e .
```

### JavaScript SDK

```bash
# Install from npm
npm install secureai-privacy-shield

# Or install from source
git clone https://github.com/secureai/privacy-shield-sdk
cd privacy-shield-sdk/javascript
npm install
```

## Usage Examples

### Basic Protection

```python
from secureai_sdk import SecureAIShield, RedactionLevel

# Create shield with basic redaction
shield = SecureAIShield(
    api_key="your_api_key",
    redaction_level=RedactionLevel.STANDARD
)

# Protect content
content = "Contact me at john.doe@email.com or call 555-123-4567"
result = shield.redact(content)

print(f"Original: {content}")
print(f"Protected: {result.redacted_content}")
# Output: "Contact me at [REDACTED] or call [REDACTED]"
```

### AI Agent Integration

```python
from secureai_sdk import protect_ai_agent, SecureAIShield

shield = SecureAIShield(api_key="your_api_key")

# Protect AI agent function
@protect_ai_agent(shield)
def ai_chat(message: str) -> str:
    # This function is automatically protected
    return f"AI response to: {message}"

# Usage
response = ai_chat("My SSN is 123-45-6789")
print(response)  # "AI response to: My SSN is [REDACTED]"
```

### Batch Processing

```python
# Process multiple inputs efficiently
contents = [
    "Email: user1@company.com",
    "Phone: 555-111-2222", 
    "SSN: 123-45-6789"
]

results = shield.redact_batch(contents)
for result in results:
    print(result.redacted_content)
```

### Async Processing

```python
import asyncio

async def process_multiple():
    contents = ["content1", "content2", "content3"]
    results = await shield.redact_batch_async(contents)
    return results

# Usage
results = asyncio.run(process_multiple())
```

### Custom Patterns

```python
# Define custom redaction patterns
custom_patterns = {
    "company_secrets": r"SECRET-\d{6}",
    "internal_codes": r"CODE-[A-Z]{3}-\d{4}"
}

shield = SecureAIShield(
    api_key="your_api_key",
    custom_patterns=custom_patterns
)

content = "The secret code is SECRET-123456 and internal code is CODE-ABC-1234"
result = shield.redact(content)
# Output: "The secret code is [REDACTED] and internal code is [REDACTED]"
```

## Configuration Options

### Redaction Levels

```python
from secureai_sdk import RedactionLevel

# Basic redaction (email, phone, SSN)
shield = SecureAIShield(redaction_level=RedactionLevel.BASIC)

# Standard redaction (includes addresses, names)
shield = SecureAIShield(redaction_level=RedactionLevel.STANDARD)

# Strict redaction (includes all PII types)
shield = SecureAIShield(redaction_level=RedactionLevel.STRICT)
```

### Caching Configuration

```python
# Enable caching for better performance
shield = SecureAIShield(
    enable_cache=True,
    cache_ttl=3600,  # 1 hour
    cache_size=10000  # 10k entries
)
```

### Performance Tuning

```python
shield = SecureAIShield(
    timeout=30,        # Request timeout in seconds
    max_retries=3,     # Maximum retry attempts
    enable_cache=True  # Enable caching
)
```

## Framework Integrations

### LangChain Integration

```python
from langchain.agents import AgentExecutor
from langchain.tools import BaseTool
from secureai_langchain import SecureAITool

# Create SecureAI protection tool
secureai_tool = SecureAITool(
    name="privacy_protection",
    description="Protects sensitive information in text",
    api_key="your_secureai_api_key"
)

# Add to agent tools
tools = [secureai_tool, other_tools...]

# Create protected agent
agent = AgentExecutor.from_agent_and_tools(
    agent=agent,
    tools=tools,
    verbose=True
)

# Agent will automatically use privacy protection
response = agent.run("Process this sensitive data: john.doe@email.com")
```

### OpenAI Function Calling

```python
import openai
from secureai_openai import SecureAIFunction

# Define SecureAI function
secureai_function = SecureAIFunction(
    name="protect_privacy",
    description="Protect sensitive information in text",
    parameters={
        "type": "object",
        "properties": {
            "text": {"type": "string", "description": "Text to protect"}
        },
        "required": ["text"]
    }
)

# Add to OpenAI function calling
response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Process: john.doe@email.com"}],
    functions=[secureai_function],
    function_call={"name": "protect_privacy"}
)
```

### FastAPI Middleware

```python
from fastapi import FastAPI, Request
from secureai_middleware import SecureAIMiddleware

app = FastAPI()

# Add SecureAI middleware
app.add_middleware(SecureAIMiddleware, 
    api_key="your_secureai_api_key",
    auto_redact=True
)

@app.post("/ai-agent/chat")
async def chat_endpoint(request: Request):
    # Input is automatically protected by middleware
    user_message = await request.json()
    
    # Process with AI agent
    response = ai_agent.chat(user_message)
    
    # Response is automatically protected before returning
    return {"response": response}
```

## API Reference

### SecureAIShield Class

#### Constructor

```python
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
```

#### Methods

- `redact(content, content_type, user_id, use_cache)` - Redact sensitive information
- `redact_async(content, content_type, user_id, use_cache)` - Async redaction
- `redact_batch(contents, content_type, user_id, use_cache)` - Batch redaction
- `redact_batch_async(contents, content_type, user_id, use_cache)` - Async batch redaction
- `contains_pii(content)` - Check if content contains PII
- `get_redaction_count(content)` - Get number of redactions
- `get_redaction_summary()` - Get protection metrics
- `health_check()` - Check service health
- `clear_cache()` - Clear the cache

### Utility Functions

- `create_shield(api_key, endpoint, redaction_level, **kwargs)` - Create shield with defaults
- `quick_redact(content, api_key, redaction_level)` - Quick redaction function
- `protect_ai_agent(shield, content_type)` - Decorator for automatic protection

## Error Handling

```python
from secureai_sdk import SecureAIError

try:
    result = shield.redact(content)
    print(result.redacted_content)
except SecureAIError as e:
    print(f"Protection failed: {e}")
    # Handle error appropriately
except Exception as e:
    print(f"Unexpected error: {e}")
    # Handle unexpected errors
```

## Monitoring and Metrics

```python
# Get protection metrics
summary = shield.get_redaction_summary()
print(f"Total requests: {summary['total_requests']}")
print(f"Success rate: {summary['successful_redactions'] / summary['total_requests']}")
print(f"Average response time: {summary['average_processing_time_ms']}ms")
print(f"Cache hit rate: {summary['cache_hit_rate']}")
```

## Best Practices

### 1. Always Protect Input and Output

```python
def safe_ai_processing(user_input):
    # ❌ Don't do this
    # response = ai_agent.process(user_input)
    # return response
    
    # ✅ Do this
    protected_input = shield.redact(user_input)
    ai_response = ai_agent.process(protected_input.redacted_content)
    protected_response = shield.redact(ai_response)
    return protected_response.redacted_content
```

### 2. Handle Errors Gracefully

```python
def robust_protection(content):
    try:
        return shield.redact(content)
    except SecureAIError as e:
        # Log error and return safe fallback
        logger.error(f"Protection failed: {e}")
        return "[CONTENT PROTECTION ERROR]"
    except Exception as e:
        # Handle unexpected errors
        logger.error(f"Unexpected error: {e}")
        return content  # Return original content as fallback
```

### 3. Monitor Protection Effectiveness

```python
class MonitoredProtectedAgent:
    def __init__(self):
        self.shield = SecureAIShield()
        self.metrics = ProtectionMetrics()
    
    def process(self, user_input):
        # Track protection metrics
        self.metrics.record_input_length(len(user_input))
        
        protected_input = self.shield.redact(user_input)
        
        # Track redaction effectiveness
        redacted_count = self.shield.get_redaction_count(protected_input.redacted_content)
        self.metrics.record_redactions(redacted_count)
        
        return protected_input
```

## Deployment

### Docker Deployment

```dockerfile
FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["python", "ai_agent_with_protection.py"]
```

### Kubernetes Deployment

```yaml
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
```

## Support

- **Documentation**: [https://docs.secureai.com](https://docs.secureai.com)
- **GitHub**: [https://github.com/secureai/privacy-shield-sdk](https://github.com/secureai/privacy-shield-sdk)
- **Email**: support@secureai.com
- **Discord**: [https://discord.gg/secureai](https://discord.gg/secureai)

## License

MIT License - see [LICENSE](LICENSE) file for details.

---

**SecureAI Privacy Shield** - Protecting AI agents with intelligent privacy protection. 