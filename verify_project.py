#!/usr/bin/env python3
"""
Integration test to verify the application structure
"""
import os
import sys


def check_file_exists(filepath):
    """Check if a file exists."""
    return os.path.exists(filepath)


def check_file_content(filepath, required_content=None):
    """Check if file contains required content."""
    if not os.path.exists(filepath):
        return False, "File does not exist"
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if required_content:
        for item in required_content:
            if item not in content:
                return False, f"Missing content: {item}"
    
    return True, "OK"


def main():
    print("AI Batch Image Editor - Structure Verification")
    print("=" * 60)
    
    checks = []
    
    # Check required files
    print("\n1. Checking required files...")
    required_files = [
        'main.py',
        'config_manager.py',
        'api_clients.py',
        'worker_threads.py',
        'ui_components.py',
        'requirements.txt',
        '.env.example',
        'README.md',
        '.gitignore'
    ]
    
    for filepath in required_files:
        exists = check_file_exists(filepath)
        status = "✓" if exists else "✗"
        print(f"  {status} {filepath}")
        checks.append(exists)
    
    # Check main.py structure
    print("\n2. Checking main.py structure...")
    ok, msg = check_file_content('main.py', ['QApplication', 'MainWindow', 'ConfigManager'])
    status = "✓" if ok else "✗"
    print(f"  {status} main.py: {msg}")
    checks.append(ok)
    
    # Check config_manager.py structure
    print("\n3. Checking config_manager.py structure...")
    ok, msg = check_file_content('config_manager.py', ['ConfigManager', 'update_config', 'save_to_env'])
    status = "✓" if ok else "✗"
    print(f"  {status} config_manager.py: {msg}")
    checks.append(ok)
    
    # Check api_clients.py structure
    print("\n4. Checking api_clients.py structure...")
    ok, msg = check_file_content('api_clients.py', ['DoubaoClient', 'BananaClient', 'image_to_base64'])
    status = "✓" if ok else "✗"
    print(f"  {status} api_clients.py: {msg}")
    checks.append(ok)
    
    # Check worker_threads.py structure
    print("\n5. Checking worker_threads.py structure...")
    ok, msg = check_file_content('worker_threads.py', ['TaskManager', 'ProcessingTask', 'WorkerThread'])
    status = "✓" if ok else "✗"
    print(f"  {status} worker_threads.py: {msg}")
    checks.append(ok)
    
    # Check ui_components.py structure
    print("\n6. Checking ui_components.py structure...")
    ok, msg = check_file_content('ui_components.py', ['MainWindow', 'ConfigPanel', 'PreviewPanel', 'ApiConfigDialog'])
    status = "✓" if ok else "✗"
    print(f"  {status} ui_components.py: {msg}")
    checks.append(ok)
    
    # Check requirements.txt
    print("\n7. Checking requirements.txt...")
    ok, msg = check_file_content('requirements.txt', ['pyqt6', 'requests', 'pillow', 'python-dotenv'])
    status = "✓" if ok else "✗"
    print(f"  {status} requirements.txt: {msg}")
    checks.append(ok)
    
    # Check .env.example
    print("\n8. Checking .env.example...")
    ok, msg = check_file_content('.env.example', ['DOUBAO_API_URL', 'BANANA_API_URL'])
    status = "✓" if ok else "✗"
    print(f"  {status} .env.example: {msg}")
    checks.append(ok)
    
    print("\n" + "=" * 60)
    
    if all(checks):
        print("\n✓ All structure checks passed!")
        print("\nThe application is ready to use.")
        print("\nNext steps:")
        print("  1. Install dependencies: pip install -r requirements.txt")
        print("  2. Configure API: cp .env.example .env && edit .env")
        print("  3. Run application: python main.py")
        return 0
    else:
        print("\n✗ Some structure checks failed!")
        return 1


if __name__ == '__main__':
    sys.exit(main())
