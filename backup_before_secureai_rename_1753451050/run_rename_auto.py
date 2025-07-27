#!/usr/bin/env python3
"""
Automated runner for the SecureAI renaming script
"""

import sys
import os
from rename_to_secureai import SecureAIRenamer

def main():
    """Run the renaming process automatically."""
    print("SecureAI Renaming Script - Automated Run")
    print("=" * 50)
    print("Running automated renaming process...")
    print()
    
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
    print("All instances of 'secureai' have been renamed to 'SecureAI'")
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
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 