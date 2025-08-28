#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Performance Testing for Rona_v5
اختبار الأداء لرونا
"""

import sys
import time
import psutil
import os
from datetime import datetime

def measure_memory_usage():
    """Measure memory usage"""
    process = psutil.Process(os.getpid())
    memory_info = process.memory_info()
    return memory_info.rss / 1024 / 1024  # Convert to MB

def test_import_performance():
    """Test import performance"""
    print("📦 اختبار أداء الاستيراد...")
    
    start_time = time.time()
    start_memory = measure_memory_usage()
    
    try:
        # Test importing main modules
        import customtkinter as ctk
        import langchain_ollama
        import langchain
        import requests
        import chromadb
        
        end_time = time.time()
        end_memory = measure_memory_usage()
        
        import_time = end_time - start_time
        memory_used = end_memory - start_memory
        
        print(f"✅ وقت الاستيراد: {import_time:.3f} ثانية")
        print(f"✅ استخدام الذاكرة: {memory_used:.2f} MB")
        
        if import_time < 5.0:
            print("✅ أداء الاستيراد مقبول")
            return True
        else:
            print("⚠️ أداء الاستيراد بطيء")
            return False
            
    except Exception as e:
        print(f"❌ خطأ في اختبار الاستيراد: {e}")
        return False

def test_ollama_performance():
    """Test Ollama performance"""
    print("\n🤖 اختبار أداء Ollama...")
    
    try:
        from langchain_ollama import ChatOllama
        
        start_time = time.time()
        start_memory = measure_memory_usage()
        
        # Initialize LLM
        llm = ChatOllama(
            model="mistral:7b",
            temperature=0.1,
            num_gpu_layers=0,  # Use CPU for testing
            num_thread=4
        )
        
        init_time = time.time() - start_time
        init_memory = measure_memory_usage() - start_memory
        
        print(f"✅ وقت التهيئة: {init_time:.3f} ثانية")
        print(f"✅ ذاكرة التهيئة: {init_memory:.2f} MB")
        
        # Test response time
        test_queries = [
            "Hello",
            "What is 2+2?",
            "Say hello in Arabic"
        ]
        
        total_response_time = 0
        successful_queries = 0
        
        for query in test_queries:
            try:
                query_start = time.time()
                response = llm.invoke(query)
                query_time = time.time() - query_start
                
                total_response_time += query_time
                successful_queries += 1
                
                print(f"   '{query}': {query_time:.3f}s")
                
            except Exception as e:
                print(f"   '{query}': فشل - {e}")
        
        if successful_queries > 0:
            avg_response_time = total_response_time / successful_queries
            print(f"✅ متوسط وقت الاستجابة: {avg_response_time:.3f} ثانية")
            
            if avg_response_time < 10.0:
                print("✅ أداء Ollama مقبول")
                return True
            else:
                print("⚠️ أداء Ollama بطيء")
                return False
        else:
            print("❌ جميع الاستعلامات فشلت")
            return False
            
    except Exception as e:
        print(f"❌ خطأ في اختبار أداء Ollama: {e}")
        return False

def test_vector_database_performance():
    """Test vector database performance"""
    print("\n📚 اختبار أداء قاعدة البيانات المتجهة...")
    
    try:
        from langchain_ollama import OllamaEmbeddings
        from langchain_chroma import Chroma
        from langchain_core.documents import Document
        import tempfile
        import shutil
        
        # Create temporary directory
        temp_dir = tempfile.mkdtemp()
        
        try:
            start_time = time.time()
            start_memory = measure_memory_usage()
            
            # Initialize embeddings and database
            embeddings = OllamaEmbeddings(model="nomic-embed-text")
            vector_db = Chroma(
                persist_directory=temp_dir,
                embedding_function=embeddings
            )
            
            init_time = time.time() - start_time
            init_memory = measure_memory_usage() - start_memory
            
            print(f"✅ وقت التهيئة: {init_time:.3f} ثانية")
            print(f"✅ ذاكرة التهيئة: {init_memory:.2f} MB")
            
            # Test document addition
            test_docs = [
                Document(page_content=f"Test document {i}", metadata={"id": i})
                for i in range(100)
            ]
            
            add_start = time.time()
            vector_db.add_documents(test_docs)
            add_time = time.time() - add_start
            
            print(f"✅ إضافة 100 وثيقة: {add_time:.3f} ثانية")
            
            # Test search performance
            search_queries = ["test", "document", "content"]
            total_search_time = 0
            successful_searches = 0
            
            for query in search_queries:
                try:
                    search_start = time.time()
                    results = vector_db.similarity_search(query, k=5)
                    search_time = time.time() - search_start
                    
                    total_search_time += search_time
                    successful_searches += 1
                    
                    print(f"   البحث عن '{query}': {search_time:.3f}s ({len(results)} نتائج)")
                    
                except Exception as e:
                    print(f"   البحث عن '{query}': فشل - {e}")
            
            if successful_searches > 0:
                avg_search_time = total_search_time / successful_searches
                print(f"✅ متوسط وقت البحث: {avg_search_time:.3f} ثانية")
                
                if avg_search_time < 2.0:
                    print("✅ أداء قاعدة البيانات مقبول")
                    return True
                else:
                    print("⚠️ أداء قاعدة البيانات بطيء")
                    return False
            else:
                print("❌ جميع عمليات البحث فشلت")
                return False
                
        finally:
            # Clean up
            shutil.rmtree(temp_dir)
            
    except Exception as e:
        print(f"❌ خطأ في اختبار أداء قاعدة البيانات: {e}")
        return False

def test_internet_search_performance():
    """Test internet search performance"""
    print("\n🌐 اختبار أداء البحث في الإنترنت...")
    
    try:
        from internet_search import InternetSearch
        
        start_time = time.time()
        start_memory = measure_memory_usage()
        
        # Initialize search
        search = InternetSearch()
        
        init_time = time.time() - start_time
        init_memory = measure_memory_usage() - start_memory
        
        print(f"✅ وقت التهيئة: {init_time:.3f} ثانية")
        print(f"✅ ذاكرة التهيئة: {init_memory:.2f} MB")
        
        # Test search performance
        test_queries = [
            "Python programming",
            "machine learning",
            "artificial intelligence"
        ]
        
        search_engines = ['google', 'bing', 'duckduckgo']
        total_search_time = 0
        successful_searches = 0
        
        for engine in search_engines:
            for query in test_queries:
                try:
                    search_start = time.time()
                    results = search.search_web(query, engine)
                    search_time = time.time() - search_start
                    
                    total_search_time += search_time
                    successful_searches += 1
                    
                    print(f"   {engine}: '{query}' - {search_time:.3f}s ({len(results)} نتائج)")
                    
                    # Add delay to avoid rate limiting
                    time.sleep(1)
                    
                except Exception as e:
                    print(f"   {engine}: '{query}' - فشل: {e}")
        
        if successful_searches > 0:
            avg_search_time = total_search_time / successful_searches
            print(f"✅ متوسط وقت البحث: {avg_search_time:.3f} ثانية")
            
            if avg_search_time < 5.0:
                print("✅ أداء البحث في الإنترنت مقبول")
                return True
            else:
                print("⚠️ أداء البحث في الإنترنت بطيء")
                return False
        else:
            print("❌ جميع عمليات البحث فشلت")
            return False
            
    except Exception as e:
        print(f"❌ خطأ في اختبار أداء البحث في الإنترنت: {e}")
        return False

def test_gui_performance():
    """Test GUI performance"""
    print("\n🖥️ اختبار أداء واجهة المستخدم...")
    
    try:
        import customtkinter as ctk
        
        start_time = time.time()
        start_memory = measure_memory_usage()
        
        # Test GUI creation
        root = ctk.CTk()
        root.withdraw()
        
        # Create multiple widgets
        widgets = []
        for i in range(50):
            label = ctk.CTkLabel(root, text=f"Widget {i}")
            button = ctk.CTkButton(root, text=f"Button {i}")
            entry = ctk.CTkEntry(root)
            widgets.extend([label, button, entry])
        
        creation_time = time.time() - start_time
        creation_memory = measure_memory_usage() - start_memory
        
        print(f"✅ إنشاء 150 عنصر: {creation_time:.3f} ثانية")
        print(f"✅ ذاكرة الإنشاء: {creation_memory:.2f} MB")
        
        # Test text widget performance
        text_widget = ctk.CTkTextbox(root)
        
        text_start = time.time()
        for i in range(1000):
            text_widget.insert("end", f"Line {i}\n")
        text_time = time.time() - text_start
        
        print(f"✅ إدراج 1000 سطر: {text_time:.3f} ثانية")
        
        # Clean up
        root.destroy()
        
        if creation_time < 2.0 and text_time < 3.0:
            print("✅ أداء واجهة المستخدم مقبول")
            return True
        else:
            print("⚠️ أداء واجهة المستخدم بطيء")
            return False
            
    except Exception as e:
        print(f"❌ خطأ في اختبار أداء واجهة المستخدم: {e}")
        return False

def test_memory_leaks():
    """Test for memory leaks"""
    print("\n💾 اختبار تسرب الذاكرة...")
    
    try:
        from rona_v5_updated import ConversationManager
        
        initial_memory = measure_memory_usage()
        
        # Create and destroy multiple conversation managers
        for i in range(10):
            manager = ConversationManager()
            
            # Add some messages
            for j in range(100):
                manager.add_message("user", f"Message {j}")
                manager.add_message("assistant", f"Response {j}")
            
            # Clear and recreate
            manager.clear_history()
            del manager
        
        final_memory = measure_memory_usage()
        memory_diff = final_memory - initial_memory
        
        print(f"✅ استخدام الذاكرة الأولي: {initial_memory:.2f} MB")
        print(f"✅ استخدام الذاكرة النهائي: {final_memory:.2f} MB")
        print(f"✅ فرق الذاكرة: {memory_diff:.2f} MB")
        
        if memory_diff < 50:  # Less than 50MB increase
            print("✅ لا يوجد تسرب واضح في الذاكرة")
            return True
        else:
            print("⚠️ قد يكون هناك تسرب في الذاكرة")
            return False
            
    except Exception as e:
        print(f"❌ خطأ في اختبار تسرب الذاكرة: {e}")
        return False

def generate_performance_report(results):
    """Generate performance report"""
    print("\n" + "=" * 60)
    print("📊 تقرير الأداء")
    print("=" * 60)
    
    passed = sum(results.values())
    total = len(results)
    
    print(f"📈 النتائج: {passed}/{total} نجح")
    print(f"📊 نسبة النجاح: {(passed/total)*100:.1f}%")
    
    print("\n🔍 تفاصيل النتائج:")
    for test_name, success in results.items():
        status = "✅ نجح" if success else "❌ فشل"
        print(f"   {test_name}: {status}")
    
    # System information
    print(f"\n💻 معلومات النظام:")
    print(f"   المعالج: {psutil.cpu_count()} نواة")
    print(f"   الذاكرة: {psutil.virtual_memory().total / 1024 / 1024 / 1024:.1f} GB")
    print(f"   استخدام الذاكرة الحالي: {measure_memory_usage():.2f} MB")
    
    # Recommendations
    print(f"\n💡 التوصيات:")
    if passed == total:
        print("✅ الأداء ممتاز! رونا جاهز للاستخدام")
    elif passed >= total * 0.8:
        print("⚠️ الأداء مقبول مع بعض التحسينات المطلوبة")
    else:
        print("❌ الأداء ضعيف، يلزم التحسين")

def main():
    """Run all performance tests"""
    print("🚀 بدء اختبارات الأداء...")
    print(f"📅 التاريخ: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    tests = [
        ("أداء الاستيراد", test_import_performance),
        ("أداء Ollama", test_ollama_performance),
        ("أداء قاعدة البيانات", test_vector_database_performance),
        ("أداء البحث في الإنترنت", test_internet_search_performance),
        ("أداء واجهة المستخدم", test_gui_performance),
        ("اختبار تسرب الذاكرة", test_memory_leaks)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            success = test_func()
            results[test_name] = success
        except Exception as e:
            print(f"❌ خطأ غير متوقع في {test_name}: {e}")
            results[test_name] = False
    
    # Generate report
    generate_performance_report(results)
    
    # Overall success
    overall_success = sum(results.values()) >= len(results) * 0.8
    
    return overall_success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)