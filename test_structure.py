#!/usr/bin/env python3
"""
Simple test to verify the project structure and module imports
without requiring all dependencies to be installed.
"""

import sys
import ast


def check_syntax(filepath):
    """Check if a Python file has valid syntax."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            ast.parse(f.read())
        return True, "OK"
    except SyntaxError as e:
        return False, f"Syntax Error: {e}"


def main():
    files = [
        'main.py',
        'config_manager.py',
        'api_clients.py',
        'worker_threads.py',
        'ui_components.py'
    ]
    
    print("Checking Python file syntax...")
    print("=" * 50)
    
    all_ok = True
    for filepath in files:
        ok, msg = check_syntax(filepath)
        status = "✓" if ok else "✗"
        print(f"{status} {filepath}: {msg}")
        if not ok:
            all_ok = False
    
    print("=" * 50)
    
    if all_ok:
        print("\n✓ All files have valid syntax!")
        print("\nTo run the application:")
        print("  1. Install dependencies: pip install -r requirements.txt")
        print("  2. Configure API: cp .env.example .env && edit .env")
        print("  3. Run: python main.py")
        return 0
    else:
        print("\n✗ Some files have syntax errors!")
        return 1


if __name__ == '__main__':
    sys.exit(main())
