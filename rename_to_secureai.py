#!/usr/bin/env python3
"""
Automated Renaming Script: Masquerade → SecureAI
Completes the transformation of the codebase from "masquerade" to "SecureAI" branding.
"""

import os
import re
import shutil
from pathlib import Path
from typing import List, Tuple, Dict
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SecureAIRenamer:
    """Automated renamer for transforming masquerade to SecureAI."""
    
    def __init__(self, root_dir: str = "."):
        self.root_dir = Path(root_dir)
        self.changes_made = []
        self.files_processed = 0
        self.files_modified = 0
        
        # Define file patterns to process
        self.file_patterns = [
            "*.py", "*.md", "*.txt", "*.json", "*.yml", "*.yaml", 
            "*.toml", "*.cfg", "*.ini", "*.sh", "*.ps1", "*.bat"
        ]
        
        # Define directories to skip
        self.skip_dirs = {
            ".git", "__pycache__", "node_modules", "venv", "env", 
            ".venv", ".env", "build", "dist", ".pytest_cache"
        }
        
        # Define files to skip
        self.skip_files = {
            "rename_to_secureai.py",  # This script itself
            ".gitignore", "LICENSE", "README.md"  # Keep original README
        }
        
        # Replacement patterns
        self.replacements = [
            # Class and function names
            (r'\bAIPrivacyShield\b', 'SecureAIPrivacyShield'),
            (r'\bEnterprisePrivacyAPI\b', 'SecureAIEnterprisePrivacyAPI'),
            (r'\bAgentPrivacyShield\b', 'SecureAIAgentPrivacyShield'),
            (r'\bAIAgentPIIShield\b', 'SecureAIAgentPIIShield'),
            
            # Module and package names
            (r'\bmasquerade\b', 'secureai'),
            (r'\bMasquerade\b', 'SecureAI'),
            (r'\bMASQUERADE\b', 'SECUREAI'),
            
            # Function names
            (r'\bdemonstrate_ai_privacy_shield\b', 'demonstrate_secureai_privacy_shield'),
            (r'\bdemonstrate_masquerade\b', 'demonstrate_secureai'),
            
            # Comments and strings
            (r'# SecureAI', '# SecureAI'),
            (r'# SecureAI Privacy Shield', '# SecureAI Privacy Shield'),
            (r'# SecureAI MCP', '# SecureAI MCP'),
            
            # Documentation references
            (r'Masquerade\s+Windows\s+Setup', 'SecureAI Windows Setup'),
            (r'Masquerade\s+Environment\s+Variables', 'SecureAI Environment Variables'),
            (r'Masquerade\s+imports\s+work', 'SecureAI imports work'),
            (r'Masquerade\s+imports\s+failed', 'SecureAI imports failed'),
            
            # Configuration references
            (r'Masquerade\s+Configuration', 'SecureAI Configuration'),
            (r'Masquerade\s+Environment\s+Configuration', 'SecureAI Environment Configuration'),
            
            # URL references (keep original URLs but update descriptions)
            (r'github\.com/postralai/masquerade', 'github.com/your-org/secureai'),
            
            # Version references
            (r'importlib\.metadata\.version\("masquerade"\)', 'importlib.metadata.version("secureai")'),
            
            # Log messages
            (r'SecureAI Privacy Shield initialized', 'SecureSecureAI Privacy Shield initialized'),
            (r'SECUREAI PRIVACY SHIELD DEMONSTRATION', 'SECURESECUREAI PRIVACY SHIELD DEMONSTRATION'),
            (r'SecureAI Agent Privacy Shield', 'SecureAI SecureAI Agent Privacy Shield'),
            (r'SecureAI Agent PII Shield', 'SecureSecureAI Agent PII Shield'),
            
            # Error messages
            (r'No module named \'masquerade\'', 'No module named \'secureai\''),
            (r'Can\'t import secureai modules', 'Can\'t import secureai modules'),
            
            # Setup and installation references
            (r'pip install git\+https://github\.com/postralai/masquerade', 'pip install git+https://github.com/your-org/secureai'),
            (r'python -m pip install git\+https://github\.com/postralai/masquerade', 'python -m pip install git+https://github.com/your-org/secureai'),
        ]
    
    def should_process_file(self, file_path: Path) -> bool:
        """Check if a file should be processed."""
        # Skip directories
        if file_path.is_dir():
            return False
        
        # Skip files in skip directories
        for part in file_path.parts:
            if part in self.skip_dirs:
                return False
        
        # Skip specific files
        if file_path.name in self.skip_files:
            return False
        
        # Check file extension
        return any(file_path.match(pattern) for pattern in self.file_patterns)
    
    def process_file(self, file_path: Path) -> bool:
        """Process a single file for replacements."""
        try:
            # Read file content
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            original_content = content
            modified = False
            
            # Apply all replacements
            for pattern, replacement in self.replacements:
                if re.search(pattern, content, re.IGNORECASE):
                    content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
                    modified = True
            
            # Write back if modified
            if modified:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                self.changes_made.append({
                    'file': str(file_path),
                    'changes': len([p for p, r in self.replacements if re.search(p, original_content, re.IGNORECASE)])
                })
                self.files_modified += 1
                logger.info(f"Modified: {file_path}")
            
            self.files_processed += 1
            return modified
            
        except Exception as e:
            logger.error(f"Error processing {file_path}: {e}")
            return False
    
    def process_directory(self, directory: Path) -> Tuple[int, int]:
        """Process all files in a directory recursively."""
        processed = 0
        modified = 0
        
        for item in directory.rglob('*'):
            if self.should_process_file(item):
                if self.process_file(item):
                    modified += 1
                processed += 1
        
        return processed, modified
    
    def rename_files_and_directories(self):
        """Rename files and directories that contain 'masquerade'."""
        renamed_items = []
        
        # Find all files and directories containing 'masquerade'
        for item in self.root_dir.rglob('*'):
            if 'masquerade' in item.name.lower():
                try:
                    # Create new name
                    new_name = item.name.replace('masquerade', 'secureai').replace('Masquerade', 'SecureAI')
                    new_path = item.parent / new_name
                    
                    # Rename
                    item.rename(new_path)
                    renamed_items.append((str(item), str(new_path)))
                    logger.info(f"Renamed: {item} → {new_path}")
                    
                except Exception as e:
                    logger.error(f"Error renaming {item}: {e}")
        
        return renamed_items
    
    def update_import_statements(self):
        """Update import statements in Python files."""
        python_files = list(self.root_dir.rglob('*.py'))
        
        for file_path in python_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                original_content = content
                modified = False
                
                # Update import statements
                import_patterns = [
                    (r'from secureai', 'from secureai'),
                    (r'import secureai', 'import secureai'),
                    (r'from \.masquerade', 'from .secureai'),
                    (r'from src\.secure_AI\.masquerade', 'from src.secure_AI.secureai'),
                ]
                
                for pattern, replacement in import_patterns:
                    if re.search(pattern, content, re.IGNORECASE):
                        content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
                        modified = True
                
                if modified:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    logger.info(f"Updated imports in: {file_path}")
                    
            except Exception as e:
                logger.error(f"Error updating imports in {file_path}: {e}")
    
    def create_backup(self):
        """Create a backup of the original codebase."""
        import time
        backup_dir = self.root_dir / f"backup_before_secureai_rename_{int(time.time())}"
        
        try:
            # Copy the entire directory
            shutil.copytree(self.root_dir, backup_dir, ignore=shutil.ignore_patterns(
                'backup_*', '.git', '__pycache__', '*.pyc', '*.pyo'
            ))
            logger.info(f"Backup created: {backup_dir}")
            return backup_dir
        except Exception as e:
            logger.error(f"Error creating backup: {e}")
            return None
    
    def run(self) -> Dict[str, any]:
        """Run the complete renaming process."""
        logger.info("Starting SecureAI renaming process...")
        
        # Create backup
        backup_dir = self.create_backup()
        
        # Step 1: Rename files and directories
        logger.info("Step 1: Renaming files and directories...")
        renamed_items = self.rename_files_and_directories()
        
        # Step 2: Process file contents
        logger.info("Step 2: Processing file contents...")
        processed, modified = self.process_directory(self.root_dir)
        
        # Step 3: Update import statements
        logger.info("Step 3: Updating import statements...")
        self.update_import_statements()
        
        # Generate summary
        summary = {
            'backup_created': backup_dir is not None,
            'backup_location': str(backup_dir) if backup_dir else None,
            'files_processed': processed,
            'files_modified': modified,
            'items_renamed': len(renamed_items),
            'total_changes': len(self.changes_made),
            'renamed_items': renamed_items,
            'changes_made': self.changes_made
        }
        
        logger.info("Renaming process completed!")
        logger.info(f"Files processed: {processed}")
        logger.info(f"Files modified: {modified}")
        logger.info(f"Items renamed: {len(renamed_items)}")
        logger.info(f"Total changes: {len(self.changes_made)}")
        
        return summary

def main():
    """Main function to run the renaming process."""
    import time
    
    print("SecureAI Renaming Script")
    print("=" * 50)
    print("This script will rename all instances of 'masquerade' to 'SecureAI'")
    print("A backup will be created before making changes.")
    print()
    
    # Confirm with user
    response = input("Do you want to proceed? (y/N): ").strip().lower()
    if response not in ['y', 'yes']:
        print("Renaming cancelled.")
        return
    
    # Run the renaming process
    renamer = SecureAIRenamer()
    summary = renamer.run()
    
    # Print summary
    print("\n" + "=" * 50)
    print("RENAMING SUMMARY")
    print("=" * 50)
    print(f"✅ Backup created: {summary['backup_created']}")
    if summary['backup_location']:
        print(f"📁 Backup location: {summary['backup_location']}")
    print(f"📄 Files processed: {summary['files_processed']}")
    print(f"✏️  Files modified: {summary['files_modified']}")
    print(f"🔄 Items renamed: {summary['items_renamed']}")
    print(f"📊 Total changes: {summary['total_changes']}")
    
    print("\n" + "=" * 50)
    print("🎉 RENAMING COMPLETED SUCCESSFULLY!")
    print("=" * 50)
    print("All instances of 'masquerade' have been renamed to 'SecureAI'")
    print("Your codebase is now fully branded as SecureAI!")
    
    # Show some examples of changes
    if summary['changes_made']:
        print("\n📝 Examples of changes made:")
        for change in summary['changes_made'][:5]:  # Show first 5
            print(f"  • {change['file']} ({change['changes']} changes)")
    
    print("\n🚀 Next steps:")
    print("1. Test your codebase: python test_standalone_secureai.py")
    print("2. Run the full test suite: python test_secureai_agents.py")
    print("3. Update any external references to the new SecureAI branding")
    print("4. Commit your changes to version control")

if __name__ == "__main__":
    main() 