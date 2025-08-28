#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Integration tests for Rona_v5 (English only)
"""

import sys
import os
import tempfile
import time

def test_full_workflow():
    print("Full workflow test...")
    try:
        from rona_v5_updated import RonaApp, ConversationManager, get_agent_llm, get_vector_db
        from langchain_community.document_loaders import TextLoader
        from langchain.text_splitter import RecursiveCharacterTextSplitter
        print("1) Initializing components...")
        conversation_manager = ConversationManager()
        vector_db = get_vector_db()
        llm = get_agent_llm()
        if not llm:
            print("Failed to initialize LLM")
            return False
        print("Components initialized")
        print("2) Creating temporary file...")
        test_content = (
            "Python Programming Guide\n\n"
            "Python is a high-level programming language.\n"
            "It was created by Guido van Rossum in 1991.\n"
            "Python is known for its simplicity and readability.\n\n"
            "Key Features:\n"
            "- Easy to learn and use\n"
            "- Extensive library support\n"
            "- Cross-platform compatibility\n"
            "- Object-oriented programming support\n\n"
            "Common Use Cases:\n"
            "- Web development\n"
            "- Data analysis\n"
            "- Machine learning\n"
            "- Automation scripts\n"
        )
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
            f.write(test_content)
            temp_file = f.name
        try:
            print("3) Loading and processing file...")
            loader = TextLoader(temp_file, encoding='utf-8')
            documents = loader.load()
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=150, chunk_overlap=30, length_function=len)
            chunked_docs = text_splitter.split_documents(documents)
            if vector_db:
                vector_db.add_documents(chunked_docs)
                print(f"Added {len(chunked_docs)} chunks to the vector DB")
            else:
                print("Vector DB not available")
            print("4) Conversation flow test...")
            user_message = "What are Python features?"
            conversation_manager.add_message("user", user_message)
            if vector_db:
                try:
                    retrieved_docs = vector_db.similarity_search(user_message, k=2)
                    context = "\n".join([doc.page_content for doc in retrieved_docs])
                    print("Context retrieved from vector DB")
                except Exception as e:
                    print(f"Vector DB search error: {e}")
                    context = ""
            else:
                context = ""
            conversation_context = conversation_manager.get_recent_context(2)
            prompt = (
                f"Context from vector DB:\n{context}\n\n"
                f"Conversation history:\n{conversation_context}\n\n"
                f"Question: {user_message}\n\n"
                f"Answer in English based on the provided context."
            )
            try:
                response = llm.invoke(prompt)
                content = getattr(response, 'content', str(response))
                if content:
                    print("LLM responded")
                    print(f"Sample: {content[:100]}...")
                    conversation_manager.add_message("assistant", content)
                    return True
                print("No response from LLM")
                return False
            except Exception as e:
                print(f"Error getting LLM response: {e}")
                return False
        finally:
            os.unlink(temp_file)
    except Exception as e:
        print(f"Workflow test error: {e}")
        return False

def test_internet_search_integration():
    print("Internet search integration...")
    try:
        from rona_v5_updated import get_agent_llm
        from internet_search import InternetSearch
        llm = get_agent_llm()
        search = InternetSearch()
        if not llm:
            print("Failed to initialize LLM")
            return False
        query = "Latest Python version"
        print(f"Searching: {query}")
        results = search.search_web(query, engine='google')
        if results:
            print(f"Found {len(results)} results")
            parts = []
            for i, r in enumerate(results[:2], 1):
                parts.append(f"{i}. {r['title']}")
                parts.append(f"   {r['snippet']}")
            ctx = "\n".join(parts)
            prompt = (
                f"Internet search results:\n{ctx}\n\n"
                f"Question: {query}\n\n"
                f"Answer in English based on the results."
            )
            resp = llm.invoke(prompt)
            content = getattr(resp, 'content', str(resp))
            if content:
                print("LLM integrated with internet search")
                print(f"Sample: {content[:100]}...")
                return True
            print("Failed to generate response")
            return False
        print("No internet search results")
        return False
    except Exception as e:
        print(f"Internet search integration error: {e}")
        return False

def test_gui_integration():
    print("GUI integration...")
    try:
        import customtkinter as ctk
        from rona_v5_updated import RonaApp
        root = ctk.CTk()
        root.withdraw()
        app = RonaApp()
        if not hasattr(app, 'conversation_manager'):
            print("Conversation manager not attached")
            return False
        if not hasattr(app, 'vector_db'):
            print("Vector DB not attached (warning only)")
        if not hasattr(app, 'agent_executor'):
            print("Agent executor not attached")
            return False
        if not hasattr(app, 'send_message'):
            print("send_message method missing")
            return False
        if not hasattr(app, 'load_file_dialog'):
            print("load_file_dialog method missing")
            return False
        root.destroy()
        return True
    except Exception as e:
        print(f"GUI integration error: {e}")
        return False

def test_memory_integration():
    print("Memory integration...")
    try:
        from rona_v5_updated import ConversationManager, save_memory_to_file, load_memory_from_file
        from langchain.memory import ConversationBufferWindowMemory
        from langchain_ollama import ChatOllama
        manager = ConversationManager()
        manager.add_message("user", "Hello")
        manager.add_message("assistant", "Hi")
        if len(manager.conversation_history) != 2:
            print("Conversation manager did not store messages")
            return False
        llm = ChatOllama(model="mistral:7b", temperature=0.1)
        memory = ConversationBufferWindowMemory(llm=llm, memory_key="chat_history", input_key="input", return_messages=True, k=4)
        memory.chat_memory.add_user_message("Hello")
        memory.chat_memory.add_ai_message("Hi there!")
        save_memory_to_file(memory)
        load_memory_from_file(memory)
        print("Memory saved and loaded")
        return True
    except Exception as e:
        print(f"Memory integration error: {e}")
        return False

def test_error_handling_integration():
    print("Error handling integration...")
    try:
        from rona_v5_updated import ConversationManager, get_vector_db, get_agent_llm
        manager = ConversationManager()
        try:
            vector_db = get_vector_db()
            print("Vector DB available" if vector_db else "Vector DB not available (handled)")
        except Exception as e:
            print(f"Vector DB exception handled: {e}")
        try:
            llm = get_agent_llm()
            print("LLM available" if llm else "LLM not available (handled)")
        except Exception as e:
            print(f"LLM exception handled: {e}")
        try:
            manager.add_message("invalid_role", "test message")
            print("Invalid role handled")
        except Exception as e:
            print(f"Role error handled: {e}")
        return True
    except Exception as e:
        print(f"Error handling integration error: {e}")
        return False

def test_performance_integration():
    print("Integrated performance...")
    try:
        from rona_v5_updated import ConversationManager, get_vector_db, get_agent_llm
        t0 = time.time()
        manager = ConversationManager()
        vector_db = get_vector_db()
        llm = get_agent_llm()
        init_dt = time.time() - t0
        print(f"Init time: {init_dt:.3f}s")
        t1 = time.time()
        for i in range(10):
            manager.add_message("user", f"Message {i}")
            manager.add_message("assistant", f"Response {i}")
        conv_dt = time.time() - t1
        print(f"Add 20 messages: {conv_dt:.3f}s")
        if vector_db:
            t2 = time.time()
            for i in range(5):
                try:
                    _ = vector_db.similarity_search(f"test query {i}", k=2)
                except Exception:
                    pass
            search_dt = time.time() - t2
            print(f"5 vector searches: {search_dt:.3f}s")
        total_dt = time.time() - t0
        print(f"Total test time: {total_dt:.3f}s")
        return total_dt < 30.0
    except Exception as e:
        print(f"Integrated performance error: {e}")
        return False

def main():
    print("Starting integration tests...")
    tests = [
        ("Full workflow", test_full_workflow),
        ("Internet search integration", test_internet_search_integration),
        ("GUI integration", test_gui_integration),
        ("Memory integration", test_memory_integration),
        ("Error handling integration", test_error_handling_integration),
        ("Integrated performance", test_performance_integration),
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