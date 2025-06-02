#!/usr/bin/env python3
"""
Repository cleanup script for MyFS project
Prepares the repository for GitHub by removing temporary files and organizing structure
"""

import os
import shutil
import sys
from pathlib import Path

def cleanup_repository():
    """Clean up repository for GitHub push"""
    
    base_path = Path(__file__).parent
    print(f"Cleaning repository at: {base_path}")
    
    # Files and directories to remove
    cleanup_items = [
        # Backup files
        "backup",
        "old_files_backup", 
        "src/filesystem/core/volume_operations.py.backup",
        "src/filesystem/core/volume_operations_fixed.py",
        "src/filesystem/core/myfs.py",  # duplicate file
        
        # Development/debug files
        "replace_debug_prints.py",
        "test_file_listing_fix.py", 
        "emergency_recovery.py",
        "FIX_SUMMARY.md",
        
        # Runtime files
        "logs",
        "system_integrity.json",
        
        # Demo/test directories (optional - comment out if you want to keep)
        # "demo",
        # "tests",
        
        # Python cache
        "__pycache__",
    ]
    
    # Remove __pycache__ directories recursively
    for pycache_dir in base_path.rglob("__pycache__"):
        if pycache_dir.is_dir():
            print(f"Removing: {pycache_dir}")
            shutil.rmtree(pycache_dir, ignore_errors=True)
    
    # Remove other cleanup items
    for item in cleanup_items:
        item_path = base_path / item
        if item_path.exists():
            if item_path.is_dir():
                print(f"Removing directory: {item_path}")
                shutil.rmtree(item_path, ignore_errors=True)
            else:
                print(f"Removing file: {item_path}")
                item_path.unlink(missing_ok=True)
    
    # Remove .pyc files
    for pyc_file in base_path.rglob("*.pyc"):
        print(f"Removing: {pyc_file}")
        pyc_file.unlink(missing_ok=True)
    
    # Remove .pyo files  
    for pyo_file in base_path.rglob("*.pyo"):
        print(f"Removing: {pyo_file}")
        pyo_file.unlink(missing_ok=True)
    
    print("\n✅ Repository cleanup completed!")
    
    # Show final structure
    print("\n📁 Final repository structure:")
    show_structure(base_path)

def show_structure(path, prefix="", max_depth=3, current_depth=0):
    """Display directory structure"""
    if current_depth >= max_depth:
        return
        
    items = sorted(path.iterdir())
    for i, item in enumerate(items):
        if item.name.startswith('.') and item.name not in ['.gitignore', '.github']:
            continue
            
        is_last = i == len(items) - 1
        current_prefix = "└── " if is_last else "├── "
        print(f"{prefix}{current_prefix}{item.name}")
        
        if item.is_dir() and current_depth < max_depth - 1:
            extension = "    " if is_last else "│   "
            show_structure(item, prefix + extension, max_depth, current_depth + 1)

def verify_essential_files():
    """Verify all essential files are present"""
    base_path = Path(__file__).parent
    
    essential_files = [
        "README.md",
        "README_EN.md", 
        "README_VI.md",
        "requirements.txt",
        "setup.py",
        ".gitignore",
        "src/main.py",
        "src/__init__.py",
        "src/filesystem/myfs.py",
        "src/filesystem/core/volume_operations.py",
        "src/filesystem/operations/security_operations.py",
        "src/security/encryption.py",
        "src/ui/cli.py",
        "src/utils/logger.py",
    ]
    
    print("\n🔍 Verifying essential files:")
    missing_files = []
    
    for file_path in essential_files:
        full_path = base_path / file_path
        if full_path.exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path}")
            missing_files.append(file_path)
    
    if missing_files:
        print(f"\n⚠️  Missing {len(missing_files)} essential files!")
        return False
    else:
        print(f"\n✅ All {len(essential_files)} essential files present!")
        return True

if __name__ == "__main__":
    print("🧹 MyFS Repository Cleanup Tool")
    print("=" * 40)
    
    # Ask for confirmation
    response = input("\nDo you want to clean up the repository? (y/N): ")
    if response.lower() not in ['y', 'yes']:
        print("Cleanup cancelled.")
        sys.exit(0)
    
    cleanup_repository()
    verify_essential_files()
    
    print("\n" + "=" * 40)
    print("🚀 Repository is ready for GitHub!")
    print("\nNext steps:")
    print("1. git add .")
    print("2. git commit -m 'Initial commit: MyFS secure file system'")
    print("3. git push origin main")
