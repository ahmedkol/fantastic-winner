#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quick Test Script for Rona_v5
"""

import sys
import os
import subprocess

def test_imports():
    """Test if all required modules can be imported"""
    print("Checking required Python packages...")
    
    modules = [
        'customtkinter',
        'langchain_ollama',
        'langchain',
        'langchain_core',
        'requests',
        'bs4',
        'chromadb'
    ]
    
    failed_imports = []
    
    for module in modules:
        try:
            __import__(module)
            print(f"OK  {module}")
        except ImportError as e:
            print(f"FAIL {module}: {e}")
            failed_imports.append(module)
    
    if failed_imports:
        print(f"\nFAIL: could not import {len(failed_imports)} package(s)")
        return False
    else:
        print("All required packages are available")
        return True

def test_ollama():
    """Test Ollama installation and model"""
    print("\nOllama check...")
    
    try:
        # Check if Ollama is installed
        result = subprocess.run(['ollama', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"Ollama found: {result.stdout.strip()}")
        else:
            print("Ollama is not installed or not in PATH")
            return False
        
        # Check if model is available
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
        if result.returncode == 0:
            if 'mistral:7b' in result.stdout:
                print("Model mistral:7b is available")
                return True
            else:
                print("Model mistral:7b not available")
                print("Hint: run 'ollama pull mistral:7b'")
                return False
        else:
            print("Cannot list models")
            return False
            
    except FileNotFoundError:
        print("Ollama not installed")
        return False
    except Exception as e:
        print(f"Error while checking Ollama: {e}")
        return False

def test_internet_search():
    """Test internet search functionality"""
    print("\nInternet search quick test...")
    
    try:
        from internet_search import InternetSearch
        
        search = InternetSearch()
        results = search.search_web("Python programming", engine='google')
        
        if results:
            print(f"Internet search OK - found {len(results)} results")
            return True
        else:
            print("Internet search returned no results")
            return False
            
    except Exception as e:
        print(f"Error during internet search test: {e}")
        return False

def test_vector_database():
    """Test vector database functionality"""
    print("\nVector database quick test...")
    
    try:
        from langchain_ollama import OllamaEmbeddings
        from langchain_chroma import Chroma
        import tempfile
        import shutil
        import time as _qt_time
        import gc as _qt_gc
        
        # Test embeddings
        embeddings = OllamaEmbeddings(model="nomic-embed-text")
        print("Embeddings model initialized")
        
        # Use a unique temp directory to avoid file locks
        temp_dir = tempfile.mkdtemp(prefix="test_chroma_db_")
        vector_db = None
        try:
            vector_db = Chroma(
                persist_directory=temp_dir,
                embedding_function=embeddings
            )
            print("Vector database initialized")
            return True
        finally:
            # Best-effort cleanup on Windows (release file locks first)
            try:
                if vector_db is not None:
                    try:
                        # Some versions expose _client.reset(); ignore if not
                        vector_db._client.reset()  # type: ignore[attr-defined]
                    except Exception:
                        pass
                    try:
                        vector_db._collection = None  # type: ignore[attr-defined]
                    except Exception:
                        pass
                del vector_db
                _qt_gc.collect()
                _qt_time.sleep(0.2)
            except Exception:
                pass
            
            def _onerror(func, path, exc_info):
                try:
                    os.chmod(path, 0o777)
                    func(path)
                except Exception:
                    pass
            
            if os.path.exists(temp_dir):
                try:
                    shutil.rmtree(temp_dir, onerror=_onerror)
                except Exception as _e:
                    print(f"Warning: could not remove temp DB dir: {_e}")
        
    except Exception as e:
        print(f"Error during vector database test: {e}")
        return False

def test_gui():
    """Test GUI components"""
    print("\nGUI quick test...")
    
    try:
        import customtkinter as ctk
        
        # Test basic GUI creation
        root = ctk.CTk()
        root.withdraw()  # Hide the window
        
        label = ctk.CTkLabel(root, text="GUI test")
        print("GUI components created")
        
        root.destroy()
        return True
        
    except Exception as e:
        print(f"Error during GUI test: {e}")
        return False

def main():
    """Run all tests"""
    print("Starting quick test for Rona_v5...")
    print("=" * 50)
    
    tests = [
        ("Imports", test_imports),
        ("Ollama", test_ollama),
        ("InternetSearch", test_internet_search),
        ("VectorDB", test_vector_database),
        ("GUI", test_gui)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"Unexpected error in {test_name}: {e}")
    
    print("\n" + "=" * 50)
    print(f"Results: {passed}/{total} passed")
    
    if passed == total:
        print("All quick tests passed. Rona is ready.")
        print("\nTo run Rona:")
        print("   python run_rona.py")
    else:
        print("Some tests failed. Check errors above.")
        print("\nFor help:")
        print("   See INSTALL.md")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)