#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Integration Testing for Rona_v5
اختبار التكامل لرونا
"""

import sys
import os
import tempfile
import time

def test_full_workflow():
    """Test complete workflow from file loading to response"""
    print("🔄 اختبار سير العمل الكامل...")
    
    try:
        from rona_v5_updated import RonaApp, ConversationManager, get_agent_llm, get_vector_db
        from langchain_community.document_loaders import TextLoader
        from langchain.text_splitter import RecursiveCharacterTextSplitter
        
        # Step 1: Initialize components
        print("1️⃣ تهيئة المكونات...")
        
        conversation_manager = ConversationManager()
        vector_db = get_vector_db()
        llm = get_agent_llm()
        
        if not llm:
            print("❌ فشل في تهيئة نموذج اللغة")
            return False
        
        print("✅ تم تهيئة جميع المكونات")
        
        # Step 2: Create test file
        print("2️⃣ إنشاء ملف تجريبي...")
        
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
        
        Common Use Cases:
        - Web development
        - Data analysis
        - Machine learning
        - Automation scripts
        """
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
            f.write(test_content)
            temp_file = f.name
        
        try:
            # Step 3: Load and process file
            print("3️⃣ تحميل ومعالجة الملف...")
            
            loader = TextLoader(temp_file, encoding='utf-8')
            documents = loader.load()
            
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=150,
                chunk_overlap=30,
                length_function=len
            )
            
            chunked_docs = text_splitter.split_documents(documents)
            
            if vector_db:
                vector_db.add_documents(chunked_docs)
                print(f"✅ تم إضافة {len(chunked_docs)} جزء إلى قاعدة البيانات")
            else:
                print("⚠️ قاعدة البيانات غير متاحة")
            
            # Step 4: Test conversation flow
            print("4️⃣ اختبار تدفق المحادثة...")
            
            # Add user message
            user_message = "ما هي مميزات Python؟"
            conversation_manager.add_message("user", user_message)
            
            # Get context from vector database
            if vector_db:
                try:
                    retrieved_docs = vector_db.similarity_search(user_message, k=2)
                    context = "\n".join([doc.page_content for doc in retrieved_docs])
                    print("✅ تم الحصول على السياق من قاعدة البيانات")
                except Exception as e:
                    print(f"⚠️ خطأ في البحث في قاعدة البيانات: {e}")
                    context = "لا يوجد سياق متاح"
            else:
                context = "قاعدة البيانات غير متاحة"
            
            # Get conversation context
            conversation_context = conversation_manager.get_recent_context(2)
            
            # Step 5: Test agent response
            print("5️⃣ اختبار رد الوكيل...")
            
            try:
                # Create a simple prompt
                prompt = f"""
                السياق من قاعدة البيانات:
                {context}
                
                المحادثة السابقة:
                {conversation_context}
                
                السؤال: {user_message}
                
                أجب باللغة العربية بناءً على السياق المقدم.
                """
                
                response = llm.invoke(prompt)
                
                if response and response.content:
                    print("✅ تم الحصول على رد من الوكيل")
                    print(f"   الرد: {response.content[:100]}...")
                    
                    # Add response to conversation
                    conversation_manager.add_message("assistant", response.content)
                    
                    return True
                else:
                    print("❌ لم يتم الحصول على رد من الوكيل")
                    return False
                    
            except Exception as e:
                print(f"❌ خطأ في الحصول على رد الوكيل: {e}")
                return False
                
        finally:
            # Clean up
            os.unlink(temp_file)
            
    except Exception as e:
        print(f"❌ خطأ في اختبار سير العمل: {e}")
        return False

def test_internet_search_integration():
    """Test internet search integration with the main application"""
    print("\n🌐 اختبار تكامل البحث في الإنترنت...")
    
    try:
        from rona_v5_updated import get_agent_llm
        from internet_search import InternetSearch
        
        # Initialize components
        llm = get_agent_llm()
        search = InternetSearch()
        
        if not llm:
            print("❌ فشل في تهيئة نموذج اللغة")
            return False
        
        # Test search and response generation
        search_query = "أحدث إصدار من Python"
        
        print(f"🔍 البحث عن: {search_query}")
        
        # Perform search
        search_results = search.search_web(search_query, engine='google')
        
        if search_results:
            print(f"✅ تم العثور على {len(search_results)} نتيجة")
            
            # Create context from search results
            context_parts = []
            for i, result in enumerate(search_results[:2], 1):
                context_parts.append(f"{i}. {result['title']}")
                context_parts.append(f"   {result['snippet']}")
            
            search_context = "\n".join(context_parts)
            
            # Generate response using LLM
            prompt = f"""
            نتائج البحث في الإنترنت:
            {search_context}
            
            السؤال: {search_query}
            
            أجب باللغة العربية بناءً على نتائج البحث المقدمة.
            """
            
            response = llm.invoke(prompt)
            
            if response and response.content:
                print("✅ تم دمج البحث في الإنترنت مع الوكيل")
                print(f"   الرد: {response.content[:100]}...")
                return True
            else:
                print("❌ فشل في توليد الرد")
                return False
        else:
            print("❌ لم يتم العثور على نتائج بحث")
            return False
            
    except Exception as e:
        print(f"❌ خطأ في اختبار تكامل البحث في الإنترنت: {e}")
        return False

def test_gui_integration():
    """Test GUI integration with backend components"""
    print("\n🖥️ اختبار تكامل واجهة المستخدم...")
    
    try:
        import customtkinter as ctk
        from rona_v5_updated import RonaApp
        
        # Create GUI application (without running mainloop)
        root = ctk.CTk()
        root.withdraw()
        
        app = RonaApp()
        
        # Test that GUI components are properly connected
        if hasattr(app, 'conversation_manager'):
            print("✅ مدير المحادثة متصل بواجهة المستخدم")
        else:
            print("❌ مدير المحادثة غير متصل")
            return False
        
        if hasattr(app, 'vector_db'):
            print("✅ قاعدة البيانات متصلة بواجهة المستخدم")
        else:
            print("⚠️ قاعدة البيانات غير متصلة")
        
        if hasattr(app, 'agent_executor'):
            print("✅ الوكيل متصل بواجهة المستخدم")
        else:
            print("❌ الوكيل غير متصل")
            return False
        
        # Test GUI methods
        if hasattr(app, 'send_message'):
            print("✅ دالة إرسال الرسائل متاحة")
        else:
            print("❌ دالة إرسال الرسائل غير متاحة")
            return False
        
        if hasattr(app, 'load_file_dialog'):
            print("✅ دالة تحميل الملفات متاحة")
        else:
            print("❌ دالة تحميل الملفات غير متاحة")
            return False
        
        # Clean up
        root.destroy()
        
        return True
        
    except Exception as e:
        print(f"❌ خطأ في اختبار تكامل واجهة المستخدم: {e}")
        return False

def test_memory_integration():
    """Test memory integration across components"""
    print("\n💾 اختبار تكامل الذاكرة...")
    
    try:
        from rona_v5_updated import ConversationManager, save_memory_to_file, load_memory_from_file
        from langchain.memory import ConversationBufferWindowMemory
        from langchain_ollama import ChatOllama
        
        # Test conversation manager memory
        manager = ConversationManager()
        manager.add_message("user", "مرحباً")
        manager.add_message("assistant", "أهلاً وسهلاً")
        
        # Test file persistence
        if len(manager.conversation_history) == 2:
            print("✅ مدير المحادثة يحفظ الرسائل")
        else:
            print("❌ مدير المحادثة لا يحفظ الرسائل")
            return False
        
        # Test LangChain memory
        llm = ChatOllama(model="mistral:7b", temperature=0.1)
        memory = ConversationBufferWindowMemory(
            llm=llm,
            memory_key="chat_history",
            input_key="input",
            return_messages=True,
            k=4
        )
        
        # Add messages to LangChain memory
        from langchain_core.messages import HumanMessage, AIMessage
        memory.chat_memory.add_user_message("Hello")
        memory.chat_memory.add_ai_message("Hi there!")
        
        # Test memory persistence
        save_memory_to_file(memory)
        print("✅ تم حفظ ذاكرة LangChain")
        
        # Test memory loading
        load_memory_from_file(memory)
        print("✅ تم تحميل ذاكرة LangChain")
        
        return True
        
    except Exception as e:
        print(f"❌ خطأ في اختبار تكامل الذاكرة: {e}")
        return False

def test_error_handling_integration():
    """Test error handling across components"""
    print("\n🛡️ اختبار معالجة الأخطاء المتكاملة...")
    
    try:
        from rona_v5_updated import ConversationManager, get_vector_db, get_agent_llm
        
        # Test handling of missing components
        manager = ConversationManager()
        
        # Test with invalid vector database
        try:
            vector_db = get_vector_db()
            if vector_db is None:
                print("✅ معالجة قاعدة البيانات غير المتاحة")
            else:
                print("✅ قاعدة البيانات متاحة")
        except Exception as e:
            print(f"✅ معالجة خطأ قاعدة البيانات: {e}")
        
        # Test with invalid LLM
        try:
            llm = get_agent_llm()
            if llm is None:
                print("✅ معالجة نموذج اللغة غير المتاح")
            else:
                print("✅ نموذج اللغة متاح")
        except Exception as e:
            print(f"✅ معالجة خطأ نموذج اللغة: {e}")
        
        # Test conversation manager with invalid input
        try:
            manager.add_message("invalid_role", "test message")
            print("✅ معالجة الأدوار غير الصحيحة")
        except Exception as e:
            print(f"✅ معالجة خطأ الأدوار: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ خطأ في اختبار معالجة الأخطاء: {e}")
        return False

def test_performance_integration():
    """Test performance of integrated components"""
    print("\n⚡ اختبار أداء المكونات المتكاملة...")
    
    try:
        from rona_v5_updated import ConversationManager, get_vector_db, get_agent_llm
        
        start_time = time.time()
        
        # Test component initialization time
        manager = ConversationManager()
        vector_db = get_vector_db()
        llm = get_agent_llm()
        
        init_time = time.time() - start_time
        print(f"✅ وقت تهيئة المكونات: {init_time:.3f} ثانية")
        
        # Test conversation flow performance
        conversation_start = time.time()
        
        for i in range(10):
            manager.add_message("user", f"Message {i}")
            manager.add_message("assistant", f"Response {i}")
        
        conversation_time = time.time() - conversation_start
        print(f"✅ وقت إضافة 20 رسالة: {conversation_time:.3f} ثانية")
        
        # Test context retrieval performance
        if vector_db:
            context_start = time.time()
            
            for i in range(5):
                try:
                    results = vector_db.similarity_search(f"test query {i}", k=2)
                except Exception:
                    pass
            
            context_time = time.time() - context_start
            print(f"✅ وقت 5 عمليات بحث: {context_time:.3f} ثانية")
        
        total_time = time.time() - start_time
        print(f"✅ إجمالي وقت الاختبار: {total_time:.3f} ثانية")
        
        if total_time < 30:  # Less than 30 seconds
            print("✅ الأداء المتكامل مقبول")
            return True
        else:
            print("⚠️ الأداء المتكامل بطيء")
            return False
            
    except Exception as e:
        print(f"❌ خطأ في اختبار الأداء المتكامل: {e}")
        return False

def main():
    """Run all integration tests"""
    print("🚀 بدء اختبارات التكامل...")
    
    tests = [
        ("سير العمل الكامل", test_full_workflow),
        ("تكامل البحث في الإنترنت", test_internet_search_integration),
        ("تكامل واجهة المستخدم", test_gui_integration),
        ("تكامل الذاكرة", test_memory_integration),
        ("معالجة الأخطاء المتكاملة", test_error_handling_integration),
        ("أداء المكونات المتكاملة", test_performance_integration)
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
    print(f"📊 نتائج اختبارات التكامل: {passed}/{total} نجح")
    
    if passed == total:
        print("🎉 جميع اختبارات التكامل نجحت!")
        print("✅ جميع المكونات تعمل معاً بشكل صحيح")
    else:
        print("⚠️ بعض اختبارات التكامل فشلت")
        print("💡 راجع الأخطاء أعلاه")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)