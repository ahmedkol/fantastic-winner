#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ollama Tests (English only)
"""

import sys
try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

import subprocess
import time

def test_ollama_installation():
    """Verify that the ollama CLI is installed and accessible."""
    print("Checking Ollama installation...")
    try:
        result = subprocess.run(["ollama", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            version = result.stdout.strip()
            print(f"Ollama is installed: {version}")
            return True
        print("Ollama appears to be installed but not working correctly")
        return False
    except FileNotFoundError:
        print("Ollama is not installed")
        print("Install tips:\n - Windows: winget install Ollama.Ollama\n - macOS: brew install ollama\n - Linux: curl -fsSL https://ollama.ai/install.sh | sh")
        return False
    except Exception as e:
        print(f"Error while checking Ollama: {e}")
        return False

def test_ollama_service():
    """Check that the ollama service responds."""
    print("Checking Ollama service...")
    try:
        result = subprocess.run(["ollama", "list"], capture_output=True, text=True)
        if result.returncode == 0:
            print("Ollama service is running")
            return True
        print("Ollama service is not running. Start it with: ollama serve")
        return False
    except Exception as e:
        print(f"Error while checking Ollama service: {e}")
        return False

def test_available_models():
    """List models and check for mistral:7b."""
    print("Checking available Ollama models...")
    try:
        result = subprocess.run(["ollama", "list"], capture_output=True, text=True)
        if result.returncode == 0:
            models_output = result.stdout
            print("Available models:")
            lines = models_output.strip().split("\n")
            if len(lines) > 1:
                for line in lines[1:]:
                    if line.strip():
                        parts = line.split()
                        model_name = parts[0]
                        model_size = parts[1] if len(parts) > 1 else "N/A"
                        print(f" - {model_name} ({model_size})")
            if "mistral:7b" in models_output:
                print("Model mistral:7b is available")
                return True
            print("Model mistral:7b is not available. Pull it with: ollama pull mistral:7b")
            return False
        print("Could not list models")
        return False
    except Exception as e:
        print(f"Error while listing models: {e}")
        return False

def test_model_pull():
    """Ensure mistral:7b is pulled (if not, try to pull)."""
    print("Verifying model pull (mistral:7b)...")
    try:
        result = subprocess.run(["ollama", "list"], capture_output=True, text=True)
        if result.returncode == 0 and "mistral:7b" in result.stdout:
            print("mistral:7b already present")
            return True
        print("Pulling mistral:7b (this may take time)...")
        pull_result = subprocess.run(["ollama", "pull", "mistral:7b"], capture_output=True, text=True)
        if pull_result.returncode == 0:
            print("Model pulled successfully")
            return True
        print("Failed to pull model")
        if pull_result.stderr:
            print(pull_result.stderr)
        return False
    except Exception as e:
        print(f"Error while pulling model: {e}")
        return False

def test_chat_ollama():
    """Smoke test ChatOllama."""
    print("Testing ChatOllama...")
    try:
        from langchain_ollama import ChatOllama
        llm = ChatOllama(model="mistral:7b", temperature=0.1, num_gpu_layers=0, num_thread=4)
        print("ChatOllama initialized")
        try:
            response = llm.invoke("Say hello in English")
            print("Simple query ok")
            print(f"Response: {getattr(response, 'content', str(response))[:100]}...")
            return True
        except Exception as e:
            print(f"Query error: {str(e)[:100]}")
            return False
    except ImportError:
        print("langchain_ollama is not installed. Run: pip install langchain_ollama")
        return False
    except Exception as e:
        print(f"Error testing ChatOllama: {e}")
        return False

def test_embeddings_ollama():
    """Smoke test OllamaEmbeddings."""
    print("Testing OllamaEmbeddings...")
    try:
        from langchain_ollama import OllamaEmbeddings
        embeddings = OllamaEmbeddings(model="nomic-embed-text")
        print("OllamaEmbeddings initialized")
        try:
            embedding = embeddings.embed_query("Hello world")
            print(f"Embedding generated (len={len(embedding)})")
            return True
        except Exception as e:
            print(f"Embedding error: {str(e)[:100]}")
            return False
    except ImportError:
        print("langchain_ollama is not installed")
        return False
    except Exception as e:
        print(f"Error testing embeddings: {e}")
        return False

def test_ollama_performance():
    """Very simple timing test."""
    print("Testing Ollama performance...")
    try:
        from langchain_ollama import ChatOllama
        llm = ChatOllama(model="mistral:7b", temperature=0.1, num_gpu_layers=0, num_thread=4)
        start_time = time.time()
        try:
            _ = llm.invoke("What is 2+2?")
            dt = time.time() - start_time
            print(f"Response time: {dt:.2f}s")
            return dt < 10
        except Exception as e:
            print(f"Performance query error: {str(e)[:100]}")
            return False
    except Exception as e:
        print(f"Error in performance test: {e}")
        return False

def main():
    print("Starting Ollama tests...")
    tests = [
        ("Ollama installation", test_ollama_installation),
        ("Ollama service", test_ollama_service),
        ("Available models", test_available_models),
        ("Model pull", test_model_pull),
        ("ChatOllama", test_chat_ollama),
        ("Ollama embeddings", test_embeddings_ollama),
        ("Ollama performance", test_ollama_performance),
    ]
    passed = 0
    total = len(tests)
    for name, func in tests:
        try:
            ok = func()
            print(f"- {name}: {'PASS' if ok else 'FAIL'}")
            if ok:
                passed += 1
        except Exception as e:
            print(f"Unexpected error in {name}: {e}")
    print("\n" + "=" * 50)
    print(f"Results: {passed}/{total} passed")
    return passed == total

if __name__ == "__main__":
    sys.exit(0 if main() else 1)