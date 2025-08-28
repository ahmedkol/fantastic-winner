#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Performance tests for Rona_v5 (English only)
"""

import sys
import time
import os
from datetime import datetime

try:
    import psutil
except Exception:
    psutil = None

def measure_memory_usage_mb():
    if not psutil:
        return 0.0
    process = psutil.Process(os.getpid())
    memory_info = process.memory_info()
    return memory_info.rss / 1024 / 1024

def test_import_performance():
    print("Import performance...")
    start_time = time.time()
    start_mem = measure_memory_usage_mb()
    try:
        import customtkinter as ctk  # noqa: F401
        import langchain_ollama  # noqa: F401
        import langchain  # noqa: F401
        import requests  # noqa: F401
        import chromadb  # noqa: F401
        dt = time.time() - start_time
        delta_mem = measure_memory_usage_mb() - start_mem
        print(f"Import time: {dt:.3f}s")
        print(f"Import memory: {delta_mem:.2f} MB")
        return dt < 5.0
    except Exception as e:
        print(f"Import performance error: {e}")
        return False

def test_ollama_performance():
    print("Ollama performance...")
    try:
        from langchain_ollama import ChatOllama
        start_time = time.time()
        start_mem = measure_memory_usage_mb()
        llm = ChatOllama(model="mistral:7b", temperature=0.1, num_gpu_layers=0, num_thread=4)
        init_dt = time.time() - start_time
        init_mem = measure_memory_usage_mb() - start_mem
        print(f"Init time: {init_dt:.3f}s")
        print(f"Init memory: {init_mem:.2f} MB")
        queries = ["Hello", "What is 2+2?", "Say hello in English"]
        total = 0.0
        count = 0
        for q in queries:
            try:
                t0 = time.time()
                _ = llm.invoke(q)
                t = time.time() - t0
                print(f" - '{q}': {t:.3f}s")
                total += t
                count += 1
            except Exception as e:
                print(f" - '{q}': FAIL ({e})")
        if count:
            avg = total / count
            print(f"Average response: {avg:.3f}s")
            return avg < 10.0
        print("No successful queries")
        return False
    except Exception as e:
        print(f"Ollama performance error: {e}")
        return False

def test_vector_db_performance():
    print("Vector DB performance...")
    try:
        from langchain_ollama import OllamaEmbeddings
        try:
            from langchain_chroma import Chroma
        except ImportError:
            from langchain_community.vectorstores import Chroma
        from langchain_core.documents import Document
        import tempfile
        import shutil
        temp_dir = tempfile.mkdtemp()
        try:
            t0 = time.time()
            m0 = measure_memory_usage_mb()
            embeddings = OllamaEmbeddings(model="nomic-embed-text")
            vector_db = Chroma(persist_directory=temp_dir, embedding_function=embeddings)
            init_dt = time.time() - t0
            init_mem = measure_memory_usage_mb() - m0
            print(f"Init time: {init_dt:.3f}s")
            print(f"Init memory: {init_mem:.2f} MB")
            docs = [Document(page_content=f"Test document {i}", metadata={"id": i}) for i in range(100)]
            add_t0 = time.time()
            vector_db.add_documents(docs)
            add_dt = time.time() - add_t0
            print(f"Add 100 docs: {add_dt:.3f}s")
            queries = ["test", "document", "content"]
            total = 0.0
            count = 0
            for q in queries:
                try:
                    s0 = time.time()
                    res = vector_db.similarity_search(q, k=5)
                    st = time.time() - s0
                    print(f" - search '{q}': {st:.3f}s ({len(res)} results)")
                    total += st
                    count += 1
                except Exception as e:
                    print(f" - search '{q}': FAIL ({e})")
            if count:
                avg = total / count
                print(f"Average search: {avg:.3f}s")
                return avg < 2.0
            print("No successful searches")
            return False
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)
    except Exception as e:
        print(f"Vector DB performance error: {e}")
        return False

def test_internet_search_performance():
    print("Internet search performance...")
    try:
        from internet_search import InternetSearch
        t0 = time.time()
        m0 = measure_memory_usage_mb()
        search = InternetSearch()
        init_dt = time.time() - t0
        init_mem = measure_memory_usage_mb() - m0
        print(f"Init time: {init_dt:.3f}s")
        print(f"Init memory: {init_mem:.2f} MB")
        queries = ["Python programming", "machine learning", "artificial intelligence"]
        engines = ["google", "bing", "duckduckgo"]
        total = 0.0
        count = 0
        for eng in engines:
            for q in queries:
                try:
                    s0 = time.time()
                    res = search.search_web(q, eng)
                    st = time.time() - s0
                    n = len(res) if res else 0
                    print(f" - {eng}: '{q}' -> {st:.3f}s ({n} results)")
                    total += st
                    count += 1
                    time.sleep(1)
                except Exception as e:
                    print(f" - {eng}: '{q}' -> FAIL ({e})")
        if count:
            avg = total / count
            print(f"Average internet search: {avg:.3f}s")
            return avg < 5.0
        print("No successful searches")
        return False
    except Exception as e:
        print(f"Internet search performance error: {e}")
        return False

def test_gui_performance():
    print("GUI performance...")
    try:
        import customtkinter as ctk
        t0 = time.time()
        m0 = measure_memory_usage_mb()
        root = ctk.CTk()
        root.withdraw()
        widgets = []
        for i in range(50):
            widgets.append(ctk.CTkLabel(root, text=f"Widget {i}"))
            widgets.append(ctk.CTkButton(root, text=f"Button {i}"))
            widgets.append(ctk.CTkEntry(root))
        create_dt = time.time() - t0
        create_mem = measure_memory_usage_mb() - m0
        print(f"Create 150 widgets: {create_dt:.3f}s")
        print(f"Create memory: {create_mem:.2f} MB")
        text = ctk.CTkTextbox(root)
        t1 = time.time()
        for i in range(1000):
            text.insert("end", f"Line {i}\n")
        text_dt = time.time() - t1
        print(f"Insert 1000 lines: {text_dt:.3f}s")
        root.destroy()
        return create_dt < 2.0 and text_dt < 3.0
    except Exception as e:
        print(f"GUI performance error: {e}")
        return False

def test_memory_leaks():
    print("Memory leak smoke test...")
    try:
        from rona_v5_updated import ConversationManager
        m0 = measure_memory_usage_mb()
        for _ in range(10):
            manager = ConversationManager()
            for j in range(100):
                manager.add_message("user", f"Message {j}")
                manager.add_message("assistant", f"Response {j}")
            manager.clear_history()
            del manager
        m1 = measure_memory_usage_mb()
        diff = m1 - m0
        print(f"Initial memory: {m0:.2f} MB")
        print(f"Final memory:   {m1:.2f} MB")
        print(f"Delta:          {diff:.2f} MB")
        return diff < 50.0
    except Exception as e:
        print(f"Memory leak test error: {e}")
        return False

def generate_report(results: dict):
    print("\n" + "=" * 60)
    print("Performance Report")
    print("=" * 60)
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    print(f"Results: {passed}/{total} passed")
    for name, ok in results.items():
        print(f" - {name}: {'PASS' if ok else 'FAIL'}")


def main():
    print("Starting performance tests...")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    tests = [
        ("Import performance", test_import_performance),
        ("Ollama performance", test_ollama_performance),
        ("Vector DB performance", test_vector_db_performance),
        ("Internet search performance", test_internet_search_performance),
        ("GUI performance", test_gui_performance),
        ("Memory leak", test_memory_leaks),
    ]
    results = {}
    for name, func in tests:
        try:
            results[name] = func()
        except Exception as e:
            print(f"Unexpected error in {name}: {e}")
            results[name] = False
    generate_report(results)
    return sum(1 for v in results.values() if v) >= int(len(results) * 0.8)

if __name__ == "__main__":
    sys.exit(0 if main() else 1)