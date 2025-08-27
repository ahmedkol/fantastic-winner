#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Ollama Functionality
اختبار وظائف Ollama
"""

import sys
import subprocess
import time

def test_ollama_installation():
    """Test if Ollama is installed and accessible"""
    print("🔧 اختبار تثبيت Ollama...")
    
    try:
        # Check if ollama command is available
        result = subprocess.run(['ollama', '--version'], capture_output=True, text=True)
        
        if result.returncode == 0:
            version = result.stdout.strip()
            print(f"✅ Ollama مثبت: {version}")
            return True
        else:
            print("❌ Ollama مثبت ولكن لا يعمل بشكل صحيح")
            return False
            
    except FileNotFoundError:
        print("❌ Ollama غير مثبت")
        print("💡 لتثبيت Ollama:")
        print("   Windows: winget install Ollama.Ollama")
        print("   macOS: brew install ollama")
        print("   Linux: curl -fsSL https://ollama.ai/install.sh | sh")
        return False
    except Exception as e:
        print(f"❌ خطأ في اختبار Ollama: {e}")
        return False

def test_ollama_service():
    """Test if Ollama service is running"""
    print("\n🚀 اختبار خدمة Ollama...")
    
    try:
        # Check if ollama service is responding
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ خدمة Ollama تعمل")
            return True
        else:
            print("❌ خدمة Ollama لا تعمل")
            print("💡 لبدء خدمة Ollama:")
            print("   ollama serve")
            return False
            
    except Exception as e:
        print(f"❌ خطأ في اختبار خدمة Ollama: {e}")
        return False

def test_available_models():
    """Test available models"""
    print("\n🤖 اختبار النماذج المتاحة...")
    
    try:
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
        
        if result.returncode == 0:
            models_output = result.stdout
            print("✅ النماذج المتاحة:")
            
            # Parse and display models
            lines = models_output.strip().split('\n')
            if len(lines) > 1:  # Skip header line
                for line in lines[1:]:
                    if line.strip():
                        parts = line.split()
                        if len(parts) >= 2:
                            model_name = parts[0]
                            model_size = parts[1] if len(parts) > 1 else "N/A"
                            print(f"   📦 {model_name} ({model_size})")
            
            # Check for required model
            if 'mistral:7b' in models_output:
                print("✅ نموذج mistral:7b متاح")
                return True
            else:
                print("⚠️ نموذج mistral:7b غير متاح")
                print("💡 لتحميل النموذج:")
                print("   ollama pull mistral:7b")
                return False
        else:
            print("❌ لا يمكن الحصول على قائمة النماذج")
            return False
            
    except Exception as e:
        print(f"❌ خطأ في اختبار النماذج: {e}")
        return False

def test_model_pull():
    """Test model pulling functionality"""
    print("\n📥 اختبار تحميل النموذج...")
    
    try:
        # Check if model already exists
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
        
        if result.returncode == 0 and 'mistral:7b' in result.stdout:
            print("✅ نموذج mistral:7b موجود بالفعل")
            return True
        
        # Try to pull the model
        print("📥 تحميل نموذج mistral:7b...")
        print("⚠️ هذا قد يستغرق وقتاً طويلاً...")
        
        pull_result = subprocess.run(['ollama', 'pull', 'mistral:7b'], 
                                   capture_output=True, text=True)
        
        if pull_result.returncode == 0:
            print("✅ تم تحميل نموذج mistral:7b بنجاح")
            return True
        else:
            print("❌ فشل في تحميل النموذج")
            print(f"خطأ: {pull_result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ خطأ في تحميل النموذج: {e}")
        return False

def test_chat_ollama():
    """Test ChatOllama functionality"""
    print("\n💬 اختبار ChatOllama...")
    
    try:
        from langchain_ollama import ChatOllama
        
        # Test ChatOllama initialization
        llm = ChatOllama(
            model="mistral:7b",
            temperature=0.1,
            num_gpu_layers=0,  # Use CPU for testing
            num_thread=4
        )
        
        print("✅ تم تهيئة ChatOllama")
        
        # Test simple query
        try:
            response = llm.invoke("Say hello in Arabic")
            print("✅ نجح الاستعلام البسيط")
            print(f"   الرد: {response.content[:100]}...")
            return True
        except Exception as e:
            print(f"❌ خطأ في الاستعلام: {str(e)[:100]}")
            return False
            
    except ImportError:
        print("❌ langchain_ollama غير مثبت")
        print("💡 قم بتشغيل: pip install langchain_ollama")
        return False
    except Exception as e:
        print(f"❌ خطأ في اختبار ChatOllama: {e}")
        return False

def test_embeddings_ollama():
    """Test Ollama embeddings"""
    print("\n🔤 اختبار Ollama Embeddings...")
    
    try:
        from langchain_ollama import OllamaEmbeddings
        
        # Test embeddings initialization
        embeddings = OllamaEmbeddings(model="nomic-embed-text")
        print("✅ تم تهيئة Ollama Embeddings")
        
        # Test embedding generation
        test_text = "Hello world"
        try:
            embedding = embeddings.embed_query(test_text)
            print(f"✅ تم إنشاء التضمين (الطول: {len(embedding)})")
            return True
        except Exception as e:
            print(f"❌ خطأ في إنشاء التضمين: {str(e)[:100]}")
            return False
            
    except ImportError:
        print("❌ langchain_ollama غير مثبت")
        return False
    except Exception as e:
        print(f"❌ خطأ في اختبار Embeddings: {e}")
        return False

def test_ollama_performance():
    """Test Ollama performance"""
    print("\n⚡ اختبار أداء Ollama...")
    
    try:
        from langchain_ollama import ChatOllama
        
        llm = ChatOllama(
            model="mistral:7b",
            temperature=0.1,
            num_gpu_layers=0,
            num_thread=4
        )
        
        # Test response time
        start_time = time.time()
        
        try:
            response = llm.invoke("What is 2+2?")
            end_time = time.time()
            
            response_time = end_time - start_time
            print(f"✅ وقت الاستجابة: {response_time:.2f} ثانية")
            
            if response_time < 10:
                print("✅ الأداء مقبول")
                return True
            else:
                print("⚠️ الأداء بطيء")
                return False
                
        except Exception as e:
            print(f"❌ خطأ في اختبار الأداء: {str(e)[:100]}")
            return False
            
    except Exception as e:
        print(f"❌ خطأ في اختبار الأداء: {e}")
        return False

def main():
    """Run all Ollama tests"""
    print("🚀 بدء اختبار Ollama...")
    
    tests = [
        ("تثبيت Ollama", test_ollama_installation),
        ("خدمة Ollama", test_ollama_service),
        ("النماذج المتاحة", test_available_models),
        ("تحميل النموذج", test_model_pull),
        ("ChatOllama", test_chat_ollama),
        ("Ollama Embeddings", test_embeddings_ollama),
        ("أداء Ollama", test_ollama_performance)
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
        print("🎉 جميع اختبارات Ollama نجحت!")
        print("✅ Ollama جاهز للاستخدام مع رونا")
    else:
        print("⚠️ بعض اختبارات Ollama فشلت")
        print("💡 راجع الأخطاء أعلاه")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)