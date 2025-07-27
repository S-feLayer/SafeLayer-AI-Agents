#!/usr/bin/env python3
"""
Complete SecureAI Renaming Script
Finishes the transformation from secureai to SecureAI throughout the codebase.
"""

import os
import re
import glob
from pathlib import Path

def replace_in_file(file_path, replacements):
    """Replace patterns in a single file."""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        original_content = content
        modified = False
        
        for pattern, replacement in replacements:
            if re.search(pattern, content, re.IGNORECASE):
                content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
                modified = True
        
        if modified:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Modified: {file_path}")
            return True
        
        return False
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def main():
    """Main renaming function."""
    print("Completing SecureAI Renaming Process...")
    print("=" * 50)
    
    # Define all replacement patterns
    replacements = [
        # Import statements
        (r'from secureai\.', 'from secureai.'),
        (r'import secureai', 'import secureai'),
        (r'from secureai import', 'from secureai import'),
        
        # Class names
        (r'\bAIPrivacyShield\b', 'SecureAIPrivacyShield'),
        (r'\bEnterprisePrivacyAPI\b', 'SecureAIEnterprisePrivacyAPI'),
        (r'\bAgentPrivacyShield\b', 'SecureAIAgentPrivacyShield'),
        (r'\bAIAgentPIIShield\b', 'SecureAIAgentPIIShield'),
        
        # Function names
        (r'\bdemonstrate_ai_privacy_shield\b', 'demonstrate_secureai_privacy_shield'),
        (r'\bdemonstrate_masquerade\b', 'demonstrate_secureai'),
        
        # Comments and strings
        (r'# SecureAI', '# SecureAI'),
        (r'# SecureAI Privacy Shield', '# SecureAI Privacy Shield'),
        (r'# SecureAI MCP', '# SecureAI MCP'),
        (r'Masquerade\s+Windows\s+Setup', 'SecureAI Windows Setup'),
        (r'Masquerade\s+Environment\s+Variables', 'SecureAI Environment Variables'),
        (r'Masquerade\s+imports\s+work', 'SecureAI imports work'),
        (r'Masquerade\s+imports\s+failed', 'SecureAI imports failed'),
        (r'Masquerade\s+Configuration', 'SecureAI Configuration'),
        (r'Masquerade\s+Environment\s+Configuration', 'SecureAI Environment Configuration'),
        
        # Documentation references
        (r'Comprehensive test suite for SecureAI', 'Comprehensive test suite for SecureAI'),
        (r'Performance benchmarking script for SecureAI', 'Performance benchmarking script for SecureAI'),
        (r'Integration test script for SecureAI', 'Integration test script for SecureAI'),
        (r'Example usage of SecureAI', 'Example usage of SecureAI'),
        (r'This script demonstrates SecureAI', 'This script demonstrates SecureAI'),
        (r'This script demonstrates how to use SecureAI', 'This script demonstrates how to use SecureAI'),
        (r'Test script for SecureAI', 'Test script for SecureAI'),
        (r'SecureAI prevents data leakage', 'SecureAI prevents data leakage'),
        (r'SECUREAI PII DETECTION DEMONSTRATION', 'SECUREAI PII DETECTION DEMONSTRATION'),
        (r'SecureAI Universal Redaction Demo', 'SecureAI Universal Redaction Demo'),
        (r'Running SecureAI Universal Redaction Tests', 'Running SecureAI Universal Redaction Tests'),
        
        # Error messages
        (r'No module named \'masquerade\'', 'No module named \'secureai\''),
        (r'Can\'t import secureai modules', 'Can\'t import secureai modules'),
        
        # Setup and installation references
        (r'pip install git\+https://github\.com/postralai/masquerade', 'pip install git+https://github.com/your-org/secureai'),
        (r'python -m pip install git\+https://github\.com/postralai/masquerade', 'python -m pip install git+https://github.com/your-org/secureai'),
        
        # Version references
        (r'importlib\.metadata\.version\("masquerade"\)', 'importlib.metadata.version("secureai")'),
        
        # Log messages
        (r'SecureAI Privacy Shield initialized', 'SecureSecureAI Privacy Shield initialized'),
        (r'SECUREAI PRIVACY SHIELD DEMONSTRATION', 'SECURESECUREAI PRIVACY SHIELD DEMONSTRATION'),
        (r'SecureAI Agent Privacy Shield', 'SecureAI SecureAI Agent Privacy Shield'),
        (r'SecureAI Agent PII Shield', 'SecureSecureAI Agent PII Shield'),
        
        # Module references in code
        (r'import secureai as m', 'import secureai as m'),
        (r'from secureai\.ai_privacy_shield import', 'from secureai.ai_privacy_shield import'),
        (r'from secureai\.enhanced_detection import', 'from secureai.enhanced_detection import'),
        (r'from secureai\.advanced_masking import', 'from secureai.advanced_masking import'),
        (r'from secureai\.smart_model_selection import', 'from secureai.smart_model_selection import'),
        (r'from secureai\.tinfoil_llm import', 'from secureai.tinfoil_llm import'),
        (r'from secureai\.redact_content import', 'from secureai.redact_content import'),
        (r'from secureai\.redact_code import', 'from secureai.redact_code import'),
        (r'from secureai\.redact_pdf import', 'from secureai.redact_pdf import'),
        (r'from secureai\.redact_text import', 'from secureai.redact_text import'),
        (r'from secureai\.get_pdf_text import', 'from secureai.get_pdf_text import'),
        (r'from secureai\.get_sensitive_data import', 'from secureai.get_sensitive_data import'),
        (r'from secureai\.remove_values import', 'from secureai.remove_values import'),
        (r'from secureai\.assign_new_values import', 'from secureai.assign_new_values import'),
        (r'from secureai\.replace_text_pdf_spire import', 'from secureai.replace_text_pdf_spire import'),
        (r'from secureai\.proxy_redaction_service import', 'from secureai.proxy_redaction_service import'),
        (r'from secureai\.redact_per_pdf import', 'from secureai.redact_per_pdf import'),
        (r'from secureai\.mcp_universal_redaction import', 'from secureai.mcp_universal_redaction import'),
        (r'from secureai\.mcp_pdf_redaction import', 'from secureai.mcp_pdf_redaction import'),
        (r'from secureai\.configure_claude import', 'from secureai.configure_claude import'),
        (r'from secureai\.health_check import', 'from secureai.health_check import'),
    ]
    
    # Find all Python files
    python_files = []
    for pattern in ['*.py', '*.md', '*.txt', '*.json', '*.yml', '*.yaml']:
        python_files.extend(glob.glob(pattern, recursive=True))
        python_files.extend(glob.glob(f'src/**/{pattern}', recursive=True))
    
    # Remove duplicates and filter out backup and cache directories
    python_files = list(set(python_files))
    python_files = [f for f in python_files if 'backup' not in f and '__pycache__' not in f and '.git' not in f]
    
    print(f"Found {len(python_files)} files to process...")
    
    modified_count = 0
    for file_path in python_files:
        if replace_in_file(file_path, replacements):
            modified_count += 1
    
    print(f"\n" + "=" * 50)
    print(f"RENAMING COMPLETED!")
    print(f"Files processed: {len(python_files)}")
    print(f"Files modified: {modified_count}")
    print("=" * 50)
    
    # Check for remaining masquerade references
    print("\n🔍 Checking for remaining 'masquerade' references...")
    remaining_files = []
    
    for file_path in python_files:
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            if 'masquerade' in content.lower():
                remaining_files.append(file_path)
        except:
            pass
    
    if remaining_files:
        print(f"Found {len(remaining_files)} files with remaining 'masquerade' references:")
        for file_path in remaining_files[:10]:  # Show first 10
            print(f"  • {file_path}")
        if len(remaining_files) > 10:
            print(f"  ... and {len(remaining_files) - 10} more")
    else:
        print("No remaining 'masquerade' references found!")
    
    print("\nNext steps:")
    print("1. Test your codebase: python test_standalone_secureai.py")
    print("2. Run the full test suite: python test_secureai_agents.py")
    print("3. Commit your changes to version control")

if __name__ == "__main__":
    main() 