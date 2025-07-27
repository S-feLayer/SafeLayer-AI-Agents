/**
 * SecureAI Privacy Shield SDK
 * Comprehensive JavaScript/Node.js SDK for integrating privacy protection with AI agents.
 */

const https = require('https');
const http = require('http');
const { URL } = require('url');

/**
 * Redaction levels for different privacy requirements
 */
const RedactionLevel = {
    BASIC: 'basic',      // Email, phone, SSN
    STANDARD: 'standard', // Includes addresses, names
    STRICT: 'strict'      // All PII types
};

/**
 * Supported content types for redaction
 */
const ContentType = {
    TEXT: 'text',
    CODE: 'code',
    JSON: 'json',
    PDF: 'pdf',
    EMAIL: 'email'
};

/**
 * Result of a redaction operation
 */
class RedactionResult {
    constructor(redactedContent, originalContent, redactionSummary, processingTimeMs, cached = false, error = null) {
        this.redactedContent = redactedContent;
        this.originalContent = originalContent;
        this.redactionSummary = redactionSummary;
        this.processingTimeMs = processingTimeMs;
        this.cached = cached;
        this.error = error;
    }
}

/**
 * Metrics for protection operations
 */
class ProtectionMetrics {
    constructor() {
        this.totalRequests = 0;
        this.successfulRedactions = 0;
        this.failedRedactions = 0;
        this.totalProcessingTimeMs = 0;
        this.cacheHits = 0;
        this.cacheMisses = 0;
    }

    getAverageProcessingTime() {
        return this.totalRequests > 0 ? this.totalProcessingTimeMs / this.totalRequests : 0;
    }

    getCacheHitRate() {
        return this.totalRequests > 0 ? this.cacheHits / this.totalRequests : 0;
    }
}

/**
 * Base exception for SecureAI SDK errors
 */
class SecureAIError extends Error {
    constructor(message) {
        super(message);
        this.name = 'SecureAIError';
    }
}

/**
 * Main SecureAI Privacy Shield client for protecting AI agent data
 */
class SecureAIShield {
    /**
     * Initialize the SecureAI Shield
     * @param {Object} config - Configuration object
     * @param {string} config.apiKey - Your SecureAI API key
     * @param {string} config.endpoint - SecureAI API endpoint (default: https://api.secureai.com)
     * @param {string} config.redactionLevel - Level of redaction to apply (default: STANDARD)
     * @param {boolean} config.enableCache - Enable caching for better performance (default: true)
     * @param {number} config.cacheTtl - Cache time-to-live in seconds (default: 3600)
     * @param {number} config.timeout - Request timeout in seconds (default: 30)
     * @param {number} config.maxRetries - Maximum retry attempts (default: 3)
     * @param {Object} config.customPatterns - Custom redaction patterns
     */
    constructor(config) {
        this.apiKey = config.apiKey;
        this.endpoint = config.endpoint || 'https://api.secureai.com';
        this.redactionLevel = config.redactionLevel || RedactionLevel.STANDARD;
        this.enableCache = config.enableCache !== false;
        this.cacheTtl = config.cacheTtl || 3600;
        this.timeout = config.timeout || 30000;
        this.maxRetries = config.maxRetries || 3;
        this.customPatterns = config.customPatterns || {};

        // Initialize cache
        this._cache = new Map();
        this._cacheTimestamps = new Map();

        // Initialize metrics
        this.metrics = new ProtectionMetrics();

        // Parse endpoint URL
        this.url = new URL(this.endpoint);

        console.log(`SecureAI Shield initialized with endpoint: ${this.endpoint}`);
    }

    /**
     * Redact sensitive information from content
     * @param {string} content - Content to redact
     * @param {string} contentType - Type of content being processed (default: TEXT)
     * @param {string} userId - User identifier for tracking
     * @param {boolean} useCache - Whether to use caching (default: true)
     * @returns {Promise<RedactionResult>} RedactionResult with redacted content and metadata
     */
    async redact(content, contentType = ContentType.TEXT, userId = null, useCache = true) {
        const startTime = Date.now();

        try {
            // Check cache first
            if (useCache && this.enableCache) {
                const cacheKey = this._generateCacheKey(content, contentType);
                const cachedResult = this._getFromCache(cacheKey);
                if (cachedResult) {
                    this.metrics.cacheHits++;
                    return cachedResult;
                }
            }

            // Prepare request payload
            const payload = {
                content: content,
                content_type: contentType,
                redaction_level: this.redactionLevel,
                user_id: userId || 'anonymous',
                use_cache: useCache
            };

            // Add custom patterns if provided
            if (Object.keys(this.customPatterns).length > 0) {
                payload.custom_patterns = this.customPatterns;
            }

            // Make API request
            const response = await this._makeRequest('/api/redact', payload);

            // Process response
            const processingTime = Date.now() - startTime;

            const result = new RedactionResult(
                response.redacted_content || content,
                content,
                response.redaction_summary || {},
                processingTime,
                response.cached || false
            );

            // Cache result
            if (useCache && this.enableCache) {
                const cacheKey = this._generateCacheKey(content, contentType);
                this._addToCache(cacheKey, result);
            }

            // Update metrics
            this.metrics.totalRequests++;
            this.metrics.successfulRedactions++;
            this.metrics.totalProcessingTimeMs += processingTime;

            return result;

        } catch (error) {
            // Update metrics
            this.metrics.totalRequests++;
            this.metrics.failedRedactions++;

            console.error(`Redaction failed: ${error.message}`);
            return new RedactionResult(
                content, // Return original content on error
                content,
                {},
                Date.now() - startTime,
                false,
                error.message
            );
        }
    }

    /**
     * Redact multiple content items efficiently
     * @param {string[]} contents - List of content to redact
     * @param {string} contentType - Type of content being processed (default: TEXT)
     * @param {string} userId - User identifier for tracking
     * @param {boolean} useCache - Whether to use caching (default: true)
     * @returns {Promise<RedactionResult[]>} List of RedactionResult objects
     */
    async redactBatch(contents, contentType = ContentType.TEXT, userId = null, useCache = true) {
        const results = [];

        for (const content of contents) {
            const result = await this.redact(content, contentType, userId, useCache);
            results.push(result);
        }

        return results;
    }

    /**
     * Check if content contains PII without redacting
     * @param {string} content - Content to check
     * @returns {Promise<boolean>} True if PII is detected, False otherwise
     */
    async containsPII(content) {
        try {
            const payload = {
                content: content,
                content_type: ContentType.TEXT,
                check_only: true
            };

            const response = await this._makeRequest('/api/check', payload);
            return response.contains_pii || false;

        } catch (error) {
            console.error(`PII check failed: ${error.message}`);
            return true; // Assume PII present on error for safety
        }
    }

    /**
     * Get the number of redactions performed on content
     * @param {string} content - Content to analyze
     * @returns {Promise<number>} Number of redactions performed
     */
    async getRedactionCount(content) {
        try {
            const payload = {
                content: content,
                content_type: ContentType.TEXT,
                analyze_only: true
            };

            const response = await this._makeRequest('/api/analyze', payload);
            return response.redaction_count || 0;

        } catch (error) {
            console.error(`Redaction count analysis failed: ${error.message}`);
            return 0;
        }
    }

    /**
     * Get a summary of redaction operations
     * @returns {Object} Dictionary with redaction summary
     */
    getRedactionSummary() {
        return {
            total_requests: this.metrics.totalRequests,
            successful_redactions: this.metrics.successfulRedactions,
            failed_redactions: this.metrics.failedRedactions,
            average_processing_time_ms: this.metrics.getAverageProcessingTime(),
            cache_hit_rate: this.metrics.getCacheHitRate(),
            redaction_level: this.redactionLevel
        };
    }

    /**
     * Check if the SecureAI service is healthy
     * @returns {Promise<boolean>} True if service is healthy, False otherwise
     */
    async healthCheck() {
        try {
            const response = await this._makeRequest('/health', {});
            return response.status === 'healthy';
        } catch (error) {
            console.error(`Health check failed: ${error.message}`);
            return false;
        }
    }

    /**
     * Make HTTP request to SecureAI API
     * @param {string} endpoint - API endpoint
     * @param {Object} payload - Request payload
     * @returns {Promise<Object>} API response
     */
    async _makeRequest(endpoint, payload) {
        const url = `${this.endpoint}${endpoint}`;
        const urlObj = new URL(url);

        for (let attempt = 0; attempt < this.maxRetries; attempt++) {
            try {
                const result = await this._makeHttpRequest(urlObj, payload);
                return result;
            } catch (error) {
                if (attempt === this.maxRetries - 1) {
                    throw new SecureAIError(`API request failed: ${error.message}`);
                }

                console.warn(`Request failed, retrying (${attempt + 1}/${this.maxRetries}): ${error.message}`);
                await this._sleep(Math.pow(2, attempt) * 1000); // Exponential backoff
            }
        }
    }

    /**
     * Make HTTP request with proper error handling
     * @param {URL} urlObj - Parsed URL object
     * @param {Object} payload - Request payload
     * @returns {Promise<Object>} API response
     */
    _makeHttpRequest(urlObj, payload) {
        return new Promise((resolve, reject) => {
            const postData = JSON.stringify(payload);

            const options = {
                hostname: urlObj.hostname,
                port: urlObj.port || (urlObj.protocol === 'https:' ? 443 : 80),
                path: urlObj.pathname + urlObj.search,
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${this.apiKey}`,
                    'Content-Type': 'application/json',
                    'User-Agent': 'SecureAI-SDK/1.0.0',
                    'Content-Length': Buffer.byteLength(postData)
                },
                timeout: this.timeout
            };

            const client = urlObj.protocol === 'https:' ? https : http;

            const req = client.request(options, (res) => {
                let data = '';

                res.on('data', (chunk) => {
                    data += chunk;
                });

                res.on('end', () => {
                    try {
                        if (res.statusCode >= 200 && res.statusCode < 300) {
                            const response = JSON.parse(data);
                            resolve(response);
                        } else {
                            reject(new Error(`HTTP ${res.statusCode}: ${data}`));
                        }
                    } catch (error) {
                        reject(new Error(`Failed to parse response: ${error.message}`));
                    }
                });
            });

            req.on('error', (error) => {
                reject(error);
            });

            req.on('timeout', () => {
                req.destroy();
                reject(new Error('Request timeout'));
            });

            req.write(postData);
            req.end();
        });
    }

    /**
     * Generate cache key for content
     * @param {string} content - Content to cache
     * @param {string} contentType - Type of content
     * @returns {string} Cache key
     */
    _generateCacheKey(content, contentType) {
        const crypto = require('crypto');
        const keyData = `${content}:${contentType}:${this.redactionLevel}`;
        return crypto.createHash('md5').update(keyData).digest('hex');
    }

    /**
     * Get result from cache if valid
     * @param {string} cacheKey - Cache key
     * @returns {RedactionResult|null} Cached result or null
     */
    _getFromCache(cacheKey) {
        if (this._cache.has(cacheKey)) {
            const timestamp = this._cacheTimestamps.get(cacheKey) || 0;
            if (Date.now() - timestamp < this.cacheTtl * 1000) {
                this.metrics.cacheHits++;
                return this._cache.get(cacheKey);
            } else {
                // Remove expired cache entry
                this._cache.delete(cacheKey);
                this._cacheTimestamps.delete(cacheKey);
            }
        }

        this.metrics.cacheMisses++;
        return null;
    }

    /**
     * Add result to cache
     * @param {string} cacheKey - Cache key
     * @param {RedactionResult} result - Result to cache
     */
    _addToCache(cacheKey, result) {
        this._cache.set(cacheKey, result);
        this._cacheTimestamps.set(cacheKey, Date.now());

        // Clean up old cache entries
        const currentTime = Date.now();
        for (const [key, timestamp] of this._cacheTimestamps.entries()) {
            if (currentTime - timestamp > this.cacheTtl * 1000) {
                this._cache.delete(key);
                this._cacheTimestamps.delete(key);
            }
        }
    }

    /**
     * Clear the cache
     */
    clearCache() {
        this._cache.clear();
        this._cacheTimestamps.clear();
        console.log('Cache cleared');
    }

    /**
     * Sleep utility function
     * @param {number} ms - Milliseconds to sleep
     * @returns {Promise} Promise that resolves after sleep
     */
    _sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
}

/**
 * Decorator to automatically protect AI agent functions
 * @param {SecureAIShield} shield - SecureAI Shield instance
 * @param {string} contentType - Type of content being processed
 * @returns {Function} Decorated function
 */
function protectAIAgent(shield, contentType = ContentType.TEXT) {
    return function(target, propertyKey, descriptor) {
        const originalMethod = descriptor.value;

        descriptor.value = async function(...args) {
            // Extract content from arguments
            let content = null;
            if (args.length > 0) {
                content = args[0];
            } else if (this.content) {
                content = this.content;
            } else if (this.message) {
                content = this.message;
            } else if (this.input) {
                content = this.input;
            }

            if (content && typeof content === 'string') {
                // Protect input
                const protectedContent = await shield.redact(content, contentType);

                // Update arguments with protected content
                if (args.length > 0) {
                    args[0] = protectedContent.redactedContent;
                } else {
                    this.content = protectedContent.redactedContent;
                }

                // Call original function
                const result = await originalMethod.apply(this, args);

                // Protect output if it's a string
                if (typeof result === 'string') {
                    const protectedResult = await shield.redact(result, contentType);
                    return protectedResult.redactedContent;
                }

                return result;
            }

            return originalMethod.apply(this, args);
        };

        return descriptor;
    };
}

/**
 * Create a SecureAI Shield instance with default settings
 * @param {string} apiKey - Your SecureAI API key
 * @param {Object} config - Additional configuration options
 * @returns {SecureAIShield} Configured SecureAIShield instance
 */
function createShield(apiKey, config = {}) {
    return new SecureAIShield({
        apiKey,
        endpoint: config.endpoint || 'https://api.secureai.com',
        redactionLevel: config.redactionLevel || RedactionLevel.STANDARD,
        ...config
    });
}

/**
 * Quick redaction function for simple use cases
 * @param {string} content - Content to redact
 * @param {string} apiKey - Your SecureAI API key
 * @param {string} redactionLevel - Level of redaction to apply (default: STANDARD)
 * @returns {Promise<string>} Redacted content
 */
async function quickRedact(content, apiKey, redactionLevel = RedactionLevel.STANDARD) {
    const shield = createShield(apiKey, { redactionLevel });
    const result = await shield.redact(content);
    return result.redactedContent;
}

// Export classes and functions
module.exports = {
    SecureAIShield,
    RedactionResult,
    ProtectionMetrics,
    SecureAIError,
    RedactionLevel,
    ContentType,
    protectAIAgent,
    createShield,
    quickRedact
};

// Example usage
if (require.main === module) {
    (async () => {
        // Example 1: Basic usage
        const shield = new SecureAIShield({ apiKey: 'your_api_key_here' });

        const content = 'My email is john.doe@company.com and my phone is 555-123-4567';
        const result = await shield.redact(content);
        console.log(`Original: ${content}`);
        console.log(`Redacted: ${result.redactedContent}`);
        console.log(`Summary: ${JSON.stringify(result.redactionSummary)}`);

        // Example 2: With decorator
        class AIAgent {
            constructor(shield) {
                this.shield = shield;
            }

            @protectAIAgent(shield)
            async chat(message) {
                // Simulate AI processing
                return `AI response to: ${message}`;
            }
        }

        const aiAgent = new AIAgent(shield);
        const response = await aiAgent.chat('My SSN is 123-45-6789');
        console.log(`Protected AI response: ${response}`);

        // Example 3: Quick redaction
        const quickResult = await quickRedact(
            'Contact me at jane.smith@email.com',
            'your_api_key_here'
        );
        console.log(`Quick redaction: ${quickResult}`);
    })().catch(console.error);
} 