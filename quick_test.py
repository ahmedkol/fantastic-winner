#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quick Test Script for Rona_v5
اختبار سريع لمكونات رونا
"""

import sys
import os
import subprocess

def test_imports():
    """Test if all required modules can be imported"""
    print("🔍 اختبار استيراد المكتبات...")
    
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
            print(f"✅ {module}")
        except ImportError as e:
            print(f"❌ {module}: {e}")
            failed_imports.append(module)
    
    if failed_imports:
        print(f"\n❌ فشل في استيراد {len(failed_imports)} مكتبة")
        return False
    else:
        print("✅ جميع المكتبات متاحة")
        return True

def test_ollama():
    """Test Ollama installation and model"""
    print("\n🤖 اختبار Ollama...")
    
    try:
        # Check if Ollama is installed
        result = subprocess.run(['ollama', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Ollama مثبت: {result.stdout.strip()}")
        else:
            print("❌ Ollama غير مثبت")
            return False
        
        # Check if model is available
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
        if result.returncode == 0:
            if 'mistral:7b' in result.stdout:
                print("✅ نموذج mistral:7b متاح")
                return True
            else:
                print("⚠️ نموذج mistral:7b غير متاح")
                print("💡 قم بتشغيل: ollama pull mistral:7b")
                return False
        else:
            print("❌ لا يمكن التحقق من النماذج")
            return False
            
    except FileNotFoundError:
        print("❌ Ollama غير مثبت")
        return False
    except Exception as e:
        print(f"❌ خطأ في اختبار Ollama: {e}")
        return False

def test_internet_search():
    """Test internet search functionality"""
    print("\n🌐 اختبار البحث في الإنترنت...")
    
    try:
        from internet_search import InternetSearch
        
        search = InternetSearch()
        results = search.search_web("Python programming", engine='google')
        
        if results:
            print(f"✅ نجح البحث في الإنترنت - تم العثور على {len(results)} نتيجة")
            return True
        else:
            print("⚠️ البحث في الإنترنت لم يعيد نتائج")
            return False
            
    except Exception as e:
        print(f"❌ خطأ في اختبار البحث في الإنترنت: {e}")
        return False

def test_vector_database():
    """Test vector database functionality"""
    print("\n📚 اختبار قاعدة البيانات المتجهة...")
    
    try:
        from langchain_ollama import OllamaEmbeddings
        from langchain_chroma import Chroma
        
        # Test embeddings
        embeddings = OllamaEmbeddings(model="nomic-embed-text")
        print("✅ تم تهيئة نموذج التضمين")
        
        # Test vector database
        vector_db = Chroma(
            persist_directory="./test_chroma_db",
            embedding_function=embeddings
        )
        print("✅ تم تهيئة قاعدة البيانات المتجهة")
        
        # Clean up test database
        import shutil
        if os.path.exists("./test_chroma_db"):
            shutil.rmtree("./test_chroma_db")
        
        return True
        
    except Exception as e:
        print(f"❌ خطأ في اختبار قاعدة البيانات المتجهة: {e}")
        return False

def test_gui():
    """Test GUI components"""
    print("\n🖥️ اختبار واجهة المستخدم...")
    
    try:
        import customtkinter as ctk
        
        # Test basic GUI creation
        root = ctk.CTk()
        root.withdraw()  # Hide the window
        
        label = ctk.CTkLabel(root, text="اختبار")
        print("✅ تم إنشاء عناصر واجهة المستخدم")
        
        root.destroy()
        return True
        
    except Exception as e:
        print(f"❌ خطأ في اختبار واجهة المستخدم: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 بدء الاختبار السريع لـ Rona_v5...")
    print("=" * 50)
    
    tests = [
        ("استيراد المكتبات", test_imports),
        ("Ollama", test_ollama),
        ("البحث في الإنترنت", test_internet_search),
        ("قاعدة البيانات المتجهة", test_vector_database),
        ("واجهة المستخدم", test_gui)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"❌ خطأ غير متوقع في {test_name}: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 نتائج الاختبار: {passed}/{total} نجح")
    
    if passed == total:
        print("🎉 جميع الاختبارات نجحت! رونا جاهز للاستخدام.")
        print("\n💡 لتشغيل رونا:")
        print("   python run_rona.py")
    else:
        print("⚠️ بعض الاختبارات فشلت. راجع الأخطاء أعلاه.")
        print("\n💡 للحصول على المساعدة:")
        print("   راجع ملف INSTALL.md")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)