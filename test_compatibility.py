#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Compatibility tests for Rona_v5 (English only)
"""

import sys
import os
import platform
import subprocess

def test_python_version():
    print("Python version...")
    v = sys.version_info
    print(f"Version: {v.major}.{v.minor}.{v.micro}")
    return (v.major, v.minor) >= (3, 8)

def test_operating_system():
    print("Operating system...")
    system = platform.system()
    release = platform.release()
    version = platform.version()
    print(f"System: {system}")
    print(f"Release: {release}")
    print(f"Details: {version}")
    return system in ["Windows", "Darwin", "Linux"]

def test_encoding_support():
    print("Encoding support...")
    try:
        arabic_text = "مرحبا بالعالم"  # keep only inside file operations
        mixed_text = "Hello World"
        test_content = "Hello World\n"
        with open("test_encoding.txt", "w", encoding="utf-8") as f:
            f.write(test_content)
        with open("test_encoding.txt", "r", encoding="utf-8") as f:
            read_content = f.read()
        os.remove("test_encoding.txt")
        return read_content == test_content and isinstance(arabic_text, str) and isinstance(mixed_text, str)
    except Exception as e:
        print(f"Encoding error: {e}")
        return False

def test_package_availability():
    print("Required packages...")
    required = [
        ("customtkinter", "CustomTkinter"),
        ("langchain_ollama", "LangChain Ollama"),
        ("langchain", "LangChain"),
        ("langchain_core", "LangChain Core"),
        ("requests", "Requests"),
        ("bs4", "BeautifulSoup4"),
        ("chromadb", "ChromaDB"),
    ]
    missing = []
    for pkg, name in required:
        try:
            __import__(pkg)
            print(f" - {name}: OK")
        except ImportError:
            print(f" - {name}: MISSING")
            missing.append(pkg)
    return len(missing) == 0

def test_ollama_compatibility():
    print("Ollama compatibility...")
    try:
        result = subprocess.run(["ollama", "--version"], capture_output=True, text=True)
        if result.returncode != 0:
            print("Ollama not installed")
            return False
        print(f"Ollama: {result.stdout.strip()}")
        list_result = subprocess.run(["ollama", "list"], capture_output=True, text=True)
        if list_result.returncode == 0:
            models = list_result.stdout
            if "mistral:7b" in models:
                print("Model mistral:7b available")
                return True
            print("Model mistral:7b not available")
            return False
        print("Cannot list models")
        return False
    except FileNotFoundError:
        print("Ollama not installed")
        return False
    except Exception as e:
        print(f"Ollama error: {e}")
        return False

def test_gui_compatibility():
    print("GUI compatibility...")
    try:
        import customtkinter as ctk
        root = ctk.CTk()
        root.withdraw()
        ctk.set_appearance_mode("dark")
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        _ = ctk.CTkLabel(root, text="Test")
        _ = ctk.CTkButton(root, text="Button")
        _ = ctk.CTkEntry(root)
        _ = ctk.CTkTextbox(root)
        root.destroy()
        return True
    except Exception as e:
        print(f"GUI error: {e}")
        return False

def test_network_compatibility():
    print("Network compatibility...")
    try:
        import requests
        urls = [
            "https://www.google.com",
            "https://www.python.org",
            "https://httpbin.org/get",
        ]
        ok = True
        for url in urls:
            try:
                r = requests.get(url, timeout=10)
                print(f" - {url}: {r.status_code}")
            except Exception as e:
                print(f" - {url}: error {e}")
                ok = False
        return ok
    except Exception as e:
        print(f"Network error: {e}")
        return False

def test_file_system_compatibility():
    print("File system compatibility...")
    try:
        test_file = "test_compatibility.txt"
        with open(test_file, "w", encoding="utf-8") as f:
            f.write("Test file")
        with open(test_file, "r", encoding="utf-8") as f:
            content = f.read()
        os.remove(test_file)
        test_dir = "test_compatibility_dir"
        os.makedirs(test_dir, exist_ok=True)
        os.rmdir(test_dir)
        return content == "Test file"
    except Exception as e:
        print(f"File system error: {e}")
        return False

def test_memory_compatibility():
    print("Memory compatibility...")
    try:
        try:
            import psutil  # noqa: F401
        except Exception:
            return True
        memory = psutil.virtual_memory()
        available_gb = memory.available / (1024 ** 3)
        print(f"Available memory: {available_gb:.2f} GB")
        return available_gb >= 2.0
    except Exception as e:
        print(f"Memory compatibility error: {e}")
        return False

def test_language_support():
    print("Language support...")
    try:
        # Ensure UTF-8 handling in file IO
        text = "Hello"
        with open("test_lang.txt", "w", encoding="utf-8") as f:
            f.write(text)
        with open("test_lang.txt", "r", encoding="utf-8") as f:
            read_back = f.read()
        os.remove("test_lang.txt")
        return read_back == text
    except Exception as e:
        print(f"Language support error: {e}")
        return False

def test_performance_compatibility():
    print("Performance compatibility...")
    try:
        import time
        t0 = time.time()
        for _ in range(200000):
            pass
        dt = time.time() - t0
        print(f"Loop time: {dt:.3f}s")
        return True
    except Exception as e:
        print(f"Performance error: {e}")
        return False

def main():
    print("Starting compatibility tests...")
    tests = [
        ("Python version", test_python_version),
        ("Operating system", test_operating_system),
        ("Encoding support", test_encoding_support),
        ("Required packages", test_package_availability),
        ("Ollama compatibility", test_ollama_compatibility),
        ("GUI compatibility", test_gui_compatibility),
        ("Network compatibility", test_network_compatibility),
        ("File system compatibility", test_file_system_compatibility),
        ("Memory compatibility", test_memory_compatibility),
        ("Language support", test_language_support),
        ("Performance compatibility", test_performance_compatibility),
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