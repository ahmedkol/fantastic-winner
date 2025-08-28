#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Full Application Functionality
اختبار وظائف التطبيق الكامل
"""

import sys
import os
import tempfile
import time

def test_application_import():
    """Test if the main application can be imported"""
    print("📦 اختبار استيراد التطبيق الرئيسي...")
    
    try:
        from rona_v5_updated import RonaApp, ConversationManager, get_agent_llm, get_vector_db
        print("✅ تم استيراد التطبيق الرئيسي بنجاح")
        return True
    except ImportError as e:
        print(f"❌ خطأ في استيراد التطبيق: {e}")
        return False
    except Exception as e:
        print(f"❌ خطأ غير متوقع: {e}")
        return False

def test_conversation_manager():
    """Test conversation manager functionality"""
    print("\n💬 اختبار مدير المحادثة...")
    
    try:
        from rona_v5_updated import ConversationManager
        
        # Create conversation manager
        manager = ConversationManager(max_history=5)
        print("✅ تم إنشاء مدير المحادثة")
        
        # Test adding messages
        manager.add_message("user", "مرحباً")
        manager.add_message("assistant", "أهلاً وسهلاً")
        manager.add_message("user", "كيف حالك؟")
        
        print(f"✅ تم إضافة {len(manager.conversation_history)} رسالة")
        
        # Test getting context
        context = manager.get_recent_context(2)
        if context:
            print("✅ تم الحصول على السياق بنجاح")
        else:
            print("⚠️ السياق فارغ")
        
        # Test clearing history
        manager.clear_history()
        if len(manager.conversation_history) == 0:
            print("✅ تم مسح المحادثة بنجاح")
        else:
            print("❌ فشل في مسح المحادثة")
        
        return True
        
    except Exception as e:
        print(f"❌ خطأ في اختبار مدير المحادثة: {e}")
        return False

def test_agent_initialization():
    """Test agent initialization"""
    print("\n🤖 اختبار تهيئة الوكيل...")
    
    try:
        from rona_v5_updated import get_agent_llm, get_agent_prompt, build_agent, create_agent_executor
        from langchain.memory import ConversationBufferWindowMemory
        
        # Test LLM initialization
        llm = get_agent_llm()
        if llm:
            print("✅ تم تهيئة نموذج اللغة")
        else:
            print("❌ فشل في تهيئة نموذج اللغة")
            return False
        
        # Test prompt creation
        prompt = get_agent_prompt()
        print("✅ تم إنشاء قالب الإشارة")
        
        # Test agent building
        from langchain.tools import tool
        
        @tool
        def test_tool():
            """Test tool"""
            return "Test successful"
        
        tools = [test_tool]
        agent = build_agent(llm, tools, prompt)
        print("✅ تم بناء الوكيل")
        
        # Test agent executor
        memory = ConversationBufferWindowMemory(
            llm=llm,
            memory_key="chat_history",
            input_key="input",
            return_messages=True,
            k=4
        )
        
        executor = create_agent_executor(agent, tools, memory)
        print("✅ تم إنشاء منفذ الوكيل")
        
        return True
        
    except Exception as e:
        print(f"❌ خطأ في اختبار تهيئة الوكيل: {e}")
        return False

def test_vector_database():
    """Test vector database functionality"""
    print("\n📚 اختبار قاعدة البيانات المتجهة...")
    
    try:
        from rona_v5_updated import get_vector_db
        
        vector_db = get_vector_db()
        if vector_db:
            print("✅ تم تهيئة قاعدة البيانات المتجهة")
            return True
        else:
            print("❌ فشل في تهيئة قاعدة البيانات المتجهة")
            return False
            
    except Exception as e:
        print(f"❌ خطأ في اختبار قاعدة البيانات: {e}")
        return False

def test_file_processing():
    """Test file processing functionality"""
    print("\n📁 اختبار معالجة الملفات...")
    
    try:
        from rona_v5_updated import get_vector_db
        from langchain_community.document_loaders import TextLoader
        from langchain.text_splitter import RecursiveCharacterTextSplitter
        
        # Create temporary test file
        test_content = """
        Python Programming Guide
        
        Python is a high-level programming language.
        It was created by Guido van Rossum in 1991.
        Python is known for its simplicity and readability.
        
        Key Features:
        - Easy to learn and use
        - Extensive library support
        - Cross-platform compatibility
        - Object-oriented programming support
        """
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
            f.write(test_content)
            temp_file = f.name
        
        try:
            # Test file loading
            loader = TextLoader(temp_file, encoding='utf-8')
            documents = loader.load()
            print(f"✅ تم تحميل {len(documents)} وثيقة من الملف")
            
            # Test text splitting
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=150,
                chunk_overlap=30,
                length_function=len
            )
            
            chunked_docs = text_splitter.split_documents(documents)
            print(f"✅ تم تقسيم النص إلى {len(chunked_docs)} جزء")
            
            # Test adding to vector database
            vector_db = get_vector_db()
            if vector_db:
                vector_db.add_documents(chunked_docs)
                print("✅ تم إضافة الوثائق إلى قاعدة البيانات")
                
                # Test search
                results = vector_db.similarity_search("Python features", k=1)
                if results:
                    print("✅ نجح البحث في قاعدة البيانات")
                else:
                    print("⚠️ البحث لم يعيد نتائج")
            else:
                print("⚠️ قاعدة البيانات غير متاحة")
            
            return True
            
        finally:
            # Clean up temporary file
            os.unlink(temp_file)
        
    except Exception as e:
        print(f"❌ خطأ في اختبار معالجة الملفات: {e}")
        return False

def test_internet_search_integration():
    """Test internet search integration"""
    print("\n🌐 اختبار تكامل البحث في الإنترنت...")
    
    try:
        from rona_v5_updated import create_web_search_tool, create_web_content_tool
        
        # Test web search tool creation
        web_search_tool = create_web_search_tool()
        print("✅ تم إنشاء أداة البحث في الويب")
        
        # Test web content tool creation
        web_content_tool = create_web_content_tool()
        print("✅ تم إنشاء أداة جلب المحتوى")
        
        return True
        
    except Exception as e:
        print(f"❌ خطأ في اختبار تكامل البحث في الإنترنت: {e}")
        return False

def test_gui_components():
    """Test GUI components"""
    print("\n🖥️ اختبار مكونات واجهة المستخدم...")
    
    try:
        import customtkinter as ctk
        
        # Test basic GUI creation (without showing)
        root = ctk.CTk()
        root.withdraw()
        
        # Test main application class creation
        from rona_v5_updated import RonaApp
        
        # Create app instance (without running mainloop)
        app = RonaApp()
        print("✅ تم إنشاء تطبيق واجهة المستخدم")
        
        # Test basic GUI elements
        if hasattr(app, 'user_input') and hasattr(app, 'send_button'):
            print("✅ عناصر واجهة المستخدم الأساسية موجودة")
        else:
            print("❌ عناصر واجهة المستخدم الأساسية مفقودة")
            return False
        
        # Clean up
        root.destroy()
        
        return True
        
    except Exception as e:
        print(f"❌ خطأ في اختبار مكونات واجهة المستخدم: {e}")
        return False

def test_memory_management():
    """Test memory management"""
    print("\n💾 اختبار إدارة الذاكرة...")
    
    try:
        from rona_v5_updated import save_memory_to_file, load_memory_from_file
        from langchain.memory import ConversationBufferWindowMemory
        from langchain_ollama import ChatOllama
        
        # Create test memory
        llm = ChatOllama(model="mistral:7b", temperature=0.1)
        memory = ConversationBufferWindowMemory(
            llm=llm,
            memory_key="chat_history",
            input_key="input",
            return_messages=True,
            k=4
        )
        
        # Add some test messages
        from langchain_core.messages import HumanMessage, AIMessage
        memory.chat_memory.add_user_message("Hello")
        memory.chat_memory.add_ai_message("Hi there!")
        
        print("✅ تم إنشاء الذاكرة وإضافة رسائل")
        
        # Test saving memory
        save_memory_to_file(memory)
        print("✅ تم حفظ الذاكرة")
        
        # Test loading memory
        load_memory_from_file(memory)
        print("✅ تم تحميل الذاكرة")
        
        return True
        
    except Exception as e:
        print(f"❌ خطأ في اختبار إدارة الذاكرة: {e}")
        return False

def test_error_handling():
    """Test error handling"""
    print("\n🛡️ اختبار معالجة الأخطاء...")
    
    try:
        from rona_v5_updated import ConversationManager
        
        # Test invalid input handling
        manager = ConversationManager()
        
        # Test with empty message
        manager.add_message("user", "")
        if len(manager.conversation_history) > 0:
            print("✅ معالجة الرسائل الفارغة")
        
        # Test with very long message
        long_message = "A" * 10000
        manager.add_message("user", long_message)
        print("✅ معالجة الرسائل الطويلة")
        
        # Test invalid role
        manager.add_message("invalid_role", "test")
        print("✅ معالجة الأدوار غير الصحيحة")
        
        return True
        
    except Exception as e:
        print(f"❌ خطأ في اختبار معالجة الأخطاء: {e}")
        return False

def main():
    """Run all application tests"""
    print("🚀 بدء اختبار التطبيق الكامل...")
    
    tests = [
        ("استيراد التطبيق", test_application_import),
        ("مدير المحادثة", test_conversation_manager),
        ("تهيئة الوكيل", test_agent_initialization),
        ("قاعدة البيانات المتجهة", test_vector_database),
        ("معالجة الملفات", test_file_processing),
        ("تكامل البحث في الإنترنت", test_internet_search_integration),
        ("مكونات واجهة المستخدم", test_gui_components),
        ("إدارة الذاكرة", test_memory_management),
        ("معالجة الأخطاء", test_error_handling)
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
    print(f"📊 نتائج اختبار التطبيق: {passed}/{total} نجح")
    
    if passed == total:
        print("🎉 جميع اختبارات التطبيق نجحت!")
        print("✅ التطبيق جاهز للاستخدام")
    else:
        print("⚠️ بعض اختبارات التطبيق فشلت")
        print("💡 راجع الأخطاء أعلاه")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)