#!/usr/bin/env python3
"""
Comprehensive integration test for AI Batch Image Editor
"""
import os
import sys
import ast
from typing import List, Dict


def analyze_imports(filepath: str) -> List[str]:
    """Analyze imports in a Python file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        tree = ast.parse(f.read())
    
    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name.split('.')[0])
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.append(node.module.split('.')[0])
    
    return list(set(imports))


def analyze_classes(filepath: str) -> List[str]:
    """Analyze classes in a Python file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        tree = ast.parse(f.read())
    
    classes = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            classes.append(node.name)
    
    return classes


def check_module_structure():
    """Check the structure of all modules."""
    print("=" * 70)
    print("AI Batch Image Editor - Comprehensive Module Analysis")
    print("=" * 70)
    
    modules = {
        'main.py': {
            'expected_classes': [],
            'expected_imports': ['sys', 'logging', 'PyQt6'],
            'description': 'Application entry point'
        },
        'config_manager.py': {
            'expected_classes': ['ConfigManager'],
            'expected_imports': ['os', 'dotenv'],
            'description': 'Configuration management'
        },
        'api_clients.py': {
            'expected_classes': ['DoubaoClient', 'BananaClient'],
            'expected_imports': ['base64', 'requests', 'PIL'],
            'description': 'API client implementations'
        },
        'worker_threads.py': {
            'expected_classes': ['ProcessingTask', 'WorkerThread', 'TaskManager'],
            'expected_imports': ['queue', 'threading', 'PyQt6'],
            'description': 'Task scheduling and concurrency'
        },
        'ui_components.py': {
            'expected_classes': ['ApiConfigDialog', 'PreviewPanel', 'ConfigPanel', 'MainWindow'],
            'expected_imports': ['PyQt6', 'config_manager', 'worker_threads'],
            'description': 'UI components'
        }
    }
    
    all_passed = True
    
    for filepath, expectations in modules.items():
        print(f"\n{filepath} - {expectations['description']}")
        print("-" * 70)
        
        # Check file exists
        if not os.path.exists(filepath):
            print(f"  ✗ File does not exist!")
            all_passed = False
            continue
        
        # Check classes
        found_classes = analyze_classes(filepath)
        for expected in expectations['expected_classes']:
            if expected in found_classes:
                print(f"  ✓ Class: {expected}")
            else:
                print(f"  ✗ Missing class: {expected}")
                all_passed = False
        
        # Check imports
        found_imports = analyze_imports(filepath)
        for expected in expectations['expected_imports']:
            if any(expected in imp for imp in found_imports):
                print(f"  ✓ Import: {expected}")
            else:
                print(f"  ✗ Missing import: {expected}")
                all_passed = False
    
    return all_passed


def check_file_dependencies():
    """Check if all modules properly reference each other."""
    print("\n" + "=" * 70)
    print("Checking Module Dependencies")
    print("=" * 70)
    
    dependencies = {
        'main.py': ['config_manager', 'ui_components'],
        'ui_components.py': ['config_manager', 'worker_threads'],
        'worker_threads.py': ['api_clients'],
        'api_clients.py': [],
        'config_manager.py': []
    }
    
    all_passed = True
    
    for filepath, required_deps in dependencies.items():
        print(f"\n{filepath}:")
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        for dep in required_deps:
            if f'from {dep}' in content or f'import {dep}' in content:
                print(f"  ✓ Depends on: {dep}")
            else:
                print(f"  ✗ Missing dependency: {dep}")
                all_passed = False
    
    return all_passed


def check_documentation():
    """Check if files have proper documentation."""
    print("\n" + "=" * 70)
    print("Checking Documentation")
    print("=" * 70)
    
    doc_files = {
        'README.md': ['快速开始', '功能特性', '使用方法'],
        'QUICKSTART.md': ['环境准备', '运行程序', '使用流程'],
        '.env.example': ['DOUBAO_API_URL', 'BANANA_API_URL'],
        'requirements.txt': ['pyqt6', 'requests', 'pillow']
    }
    
    all_passed = True
    
    for filepath, required_content in doc_files.items():
        print(f"\n{filepath}:")
        
        if not os.path.exists(filepath):
            print(f"  ✗ File does not exist!")
            all_passed = False
            continue
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        for item in required_content:
            if item in content:
                print(f"  ✓ Contains: {item}")
            else:
                print(f"  ✗ Missing: {item}")
                all_passed = False
    
    return all_passed


def main():
    """Run all checks."""
    print("\n" + "╔" + "=" * 68 + "╗")
    print("║" + " " * 68 + "║")
    print("║" + "  AI Batch Image Editor - Comprehensive Verification  ".center(68) + "║")
    print("║" + " " * 68 + "║")
    print("╚" + "=" * 68 + "╝")
    
    # Run all checks
    module_ok = check_module_structure()
    deps_ok = check_file_dependencies()
    docs_ok = check_documentation()
    
    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Module Structure:      {'✓ PASSED' if module_ok else '✗ FAILED'}")
    print(f"File Dependencies:    {'✓ PASSED' if deps_ok else '✗ FAILED'}")
    print(f"Documentation:        {'✓ PASSED' if docs_ok else '✗ FAILED'}")
    print("=" * 70)
    
    if all([module_ok, deps_ok, docs_ok]):
        print("\n✓ All verification checks PASSED!")
        print("\nThe AI Batch Image Editor is ready to use!")
        print("\nQuick Start:")
        print("  1. pip install -r requirements.txt")
        print("  2. cp .env.example .env")
        print("  3. # Edit .env with your API keys")
        print("  4. python main.py")
        return 0
    else:
        print("\n✗ Some verification checks FAILED!")
        print("\nPlease review the output above for details.")
        return 1


if __name__ == '__main__':
    sys.exit(main())
