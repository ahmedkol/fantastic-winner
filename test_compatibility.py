#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Compatibility Testing for Rona_v5
اختبار التوافق لرونا
"""

import sys
import os
import platform
import subprocess

def test_python_version():
    """Test Python version compatibility"""
    print("🐍 اختبار إصدار Python...")
    
    version = sys.version_info
    print(f"   الإصدار: {version.major}.{version.minor}.{version.micro}")
    
    if version >= (3, 8):
        print("✅ إصدار Python مقبول")
        return True
    else:
        print("❌ إصدار Python قديم جداً (مطلوب 3.8+)")
        return False

def test_operating_system():
    """Test operating system compatibility"""
    print("\n💻 اختبار نظام التشغيل...")
    
    system = platform.system()
    release = platform.release()
    version = platform.version()
    
    print(f"   النظام: {system}")
    print(f"   الإصدار: {release}")
    print(f"   التفاصيل: {version}")
    
    # Test compatibility
    if system in ["Windows", "Darwin", "Linux"]:
        print("✅ نظام التشغيل مدعوم")
        return True
    else:
        print("⚠️ نظام التشغيل غير معروف")
        return True  # Still pass as it might work

def test_encoding_support():
    """Test Unicode and encoding support"""
    print("\n🌐 اختبار دعم الترميز...")
    
    try:
        # Test Arabic text
        arabic_text = "مرحبا بالعالم"
        print(f"   النص العربي: {arabic_text}")
        
        # Test Unicode characters
        unicode_text = "Hello World 🌍 مرحبا"
        print(f"   النص المختلط: {unicode_text}")
        
        # Test file encoding
        test_content = "مرحبا بالعالم\nHello World\n🌍"
        
        with open("test_encoding.txt", "w", encoding="utf-8") as f:
            f.write(test_content)
        
        with open("test_encoding.txt", "r", encoding="utf-8") as f:
            read_content = f.read()
        
        if read_content == test_content:
            print("✅ دعم الترميز يعمل")
            os.remove("test_encoding.txt")
            return True
        else:
            print("❌ مشكلة في دعم الترميز")
            return False
            
    except Exception as e:
        print(f"❌ خطأ في اختبار الترميز: {e}")
        return False

def test_package_availability():
    """Test required package availability"""
    print("\n📦 اختبار توفر الحزم...")
    
    required_packages = [
        ("customtkinter", "CustomTkinter"),
        ("langchain_ollama", "LangChain Ollama"),
        ("langchain", "LangChain"),
        ("langchain_core", "LangChain Core"),
        ("requests", "Requests"),
        ("bs4", "BeautifulSoup4"),
        ("chromadb", "ChromaDB")
    ]
    
    missing_packages = []
    
    for package, display_name in required_packages:
        try:
            __import__(package)
            print(f"   ✅ {display_name}")
        except ImportError:
            print(f"   ❌ {display_name}")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ الحزم المفقودة: {', '.join(missing_packages)}")
        return False
    else:
        print("✅ جميع الحزم متاحة")
        return True

def test_ollama_compatibility():
    """Test Ollama compatibility"""
    print("\n🤖 اختبار توافق Ollama...")
    
    try:
        # Check if ollama is installed
        result = subprocess.run(['ollama', '--version'], capture_output=True, text=True)
        
        if result.returncode == 0:
            version = result.stdout.strip()
            print(f"   إصدار Ollama: {version}")
            
            # Check available models
            list_result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
            
            if list_result.returncode == 0:
                models = list_result.stdout
                if 'mistral:7b' in models:
                    print("   ✅ نموذج mistral:7b متاح")
                    return True
                else:
                    print("   ⚠️ نموذج mistral:7b غير متاح")
                    return False
            else:
                print("   ❌ لا يمكن الحصول على قائمة النماذج")
                return False
        else:
            print("   ❌ Ollama غير مثبت")
            return False
            
    except FileNotFoundError:
        print("   ❌ Ollama غير مثبت")
        return False
    except Exception as e:
        print(f"   ❌ خطأ في اختبار Ollama: {e}")
        return False

def test_gui_compatibility():
    """Test GUI compatibility"""
    print("\n🖥️ اختبار توافق واجهة المستخدم...")
    
    try:
        import customtkinter as ctk
        
        # Test basic GUI creation
        root = ctk.CTk()
        root.withdraw()
        
        # Test appearance modes
        ctk.set_appearance_mode("dark")
        ctk.set_appearance_mode("light")
        
        # Test color themes
        ctk.set_default_color_theme("blue")
        
        # Test basic widgets
        label = ctk.CTkLabel(root, text="اختبار")
        button = ctk.CTkButton(root, text="زر")
        entry = ctk.CTkEntry(root)
        textbox = ctk.CTkTextbox(root)
        
        # Test Arabic text in widgets
        arabic_label = ctk.CTkLabel(root, text="مرحبا بالعالم")
        
        root.destroy()
        
        print("   ✅ واجهة المستخدم تعمل")
        return True
        
    except Exception as e:
        print(f"   ❌ خطأ في واجهة المستخدم: {e}")
        return False

def test_network_compatibility():
    """Test network connectivity and compatibility"""
    print("\n🌐 اختبار توافق الشبكة...")
    
    try:
        import requests
        
        # Test basic HTTP requests
        test_urls = [
            "https://www.google.com",
            "https://www.python.org",
            "https://httpbin.org/get"
        ]
        
        for url in test_urls:
            try:
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    print(f"   ✅ {url}")
                else:
                    print(f"   ⚠️ {url} - رمز الحالة: {response.status_code}")
            except Exception as e:
                print(f"   ❌ {url} - {e}")
        
        print("   ✅ اختبار الشبكة مكتمل")
        return True
        
    except Exception as e:
        print(f"   ❌ خطأ في اختبار الشبكة: {e}")
        return False

def test_file_system_compatibility():
    """Test file system compatibility"""
    print("\n📁 اختبار توافق نظام الملفات...")
    
    try:
        # Test file creation and deletion
        test_file = "test_compatibility.txt"
        
        with open(test_file, "w", encoding="utf-8") as f:
            f.write("اختبار التوافق")
        
        with open(test_file, "r", encoding="utf-8") as f:
            content = f.read()
        
        if content == "اختبار التوافق":
            print("   ✅ إنشاء وقراءة الملفات")
        else:
            print("   ❌ مشكلة في الملفات")
            return False
        
        # Test directory creation
        test_dir = "test_compatibility_dir"
        os.makedirs(test_dir, exist_ok=True)
        
        if os.path.exists(test_dir):
            print("   ✅ إنشاء المجلدات")
        else:
            print("   ❌ مشكلة في المجلدات")
            return False
        
        # Clean up
        os.remove(test_file)
        os.rmdir(test_dir)
        
        print("   ✅ نظام الملفات يعمل")
        return True
        
    except Exception as e:
        print(f"   ❌ خطأ في نظام الملفات: {e}")
        return False

def test_memory_compatibility():
    """Test memory and resource compatibility"""
    print("\n💾 اختبار توافق الذاكرة...")
    
    try:
        import psutil
        
        # Check available memory
        memory = psutil.virtual_memory()
        available_gb = memory.available / (1024**3)
        
        print(f"   الذاكرة المتاحة: {available_gb:.2f} GB")
        
        if available_gb >= 4:  # At least 4GB
            print("   ✅ ذاكرة كافية")
        else:
            print("   ⚠️ ذاكرة محدودة")
        
        # Check CPU
        cpu_count = psutil.cpu_count()
        print(f"   عدد النوى: {cpu_count}")
        
        if cpu_count >= 2:
            print("   ✅ معالج كافي")
        else:
            print("   ⚠️ معالج محدود")
        
        return True
        
    except ImportError:
        print("   ⚠️ psutil غير متاح - لا يمكن فحص الموارد")
        return True
    except Exception as e:
        print(f"   ❌ خطأ في فحص الموارد: {e}")
        return False

def test_language_support():
    """Test language and locale support"""
    print("\n🌍 اختبار دعم اللغة...")
    
    try:
        import locale
        
        # Check current locale
        current_locale = locale.getlocale()
        print(f"   اللغة الحالية: {current_locale}")
        
        # Test Arabic text handling
        arabic_texts = [
            "مرحبا بالعالم",
            "البرمجة بلغة Python",
            "الذكاء الاصطناعي",
            "🌍 مرحبا بالعالم 🌍"
        ]
        
        for text in arabic_texts:
            try:
                # Test encoding/decoding
                encoded = text.encode('utf-8')
                decoded = encoded.decode('utf-8')
                
                if decoded == text:
                    print(f"   ✅ {text}")
                else:
                    print(f"   ❌ {text}")
                    return False
            except Exception as e:
                print(f"   ❌ خطأ في {text}: {e}")
                return False
        
        print("   ✅ دعم اللغة يعمل")
        return True
        
    except Exception as e:
        print(f"   ❌ خطأ في اختبار اللغة: {e}")
        return False

def test_performance_compatibility():
    """Test performance compatibility"""
    print("\n⚡ اختبار توافق الأداء...")
    
    try:
        import time
        
        # Test basic performance
        start_time = time.time()
        
        # Simulate some work
        for i in range(1000000):
            pass
        
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"   وقت الحلقة: {duration:.3f} ثانية")
        
        if duration < 1.0:
            print("   ✅ الأداء مقبول")
        else:
            print("   ⚠️ الأداء بطيء")
        
        # Test memory allocation
        import gc
        
        gc.collect()
        initial_memory = len(gc.get_objects())
        
        # Allocate some memory
        test_list = [i for i in range(10000)]
        
        gc.collect()
        final_memory = len(gc.get_objects())
        
        memory_diff = final_memory - initial_memory
        
        if memory_diff < 1000:
            print("   ✅ إدارة الذاكرة جيدة")
        else:
            print("   ⚠️ إدارة الذاكرة ضعيفة")
        
        return True
        
    except Exception as e:
        print(f"   ❌ خطأ في اختبار الأداء: {e}")
        return False

def main():
    """Run all compatibility tests"""
    print("🚀 بدء اختبارات التوافق...")
    
    tests = [
        ("إصدار Python", test_python_version),
        ("نظام التشغيل", test_operating_system),
        ("دعم الترميز", test_encoding_support),
        ("توفر الحزم", test_package_availability),
        ("توافق Ollama", test_ollama_compatibility),
        ("توافق واجهة المستخدم", test_gui_compatibility),
        ("توافق الشبكة", test_network_compatibility),
        ("توافق نظام الملفات", test_file_system_compatibility),
        ("توافق الذاكرة", test_memory_compatibility),
        ("دعم اللغة", test_language_support),
        ("توافق الأداء", test_performance_compatibility)
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
    print(f"📊 نتائج اختبارات التوافق: {passed}/{total} نجح")
    
    if passed == total:
        print("🎉 جميع اختبارات التوافق نجحت!")
        print("✅ النظام متوافق مع رونا")
    else:
        print("⚠️ بعض اختبارات التوافق فشلت")
        print("💡 راجع الأخطاء أعلاه")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)