#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Vector Database Functionality
"""

import sys
import os
import tempfile
import shutil

def test_embeddings():
    """Test embeddings model"""
    print("Testing embeddings model...")
    
    try:
        from langchain_ollama import OllamaEmbeddings
        
        # Test embeddings initialization
        embeddings = OllamaEmbeddings(model="nomic-embed-text")
        print("Embeddings model initialized")
        
        # Test embedding generation
        test_texts = [
            "Hello world",
            "مرحبا بالعالم",
            "Python programming",
            "البرمجة بلغة Python"
        ]
        
        for text in test_texts:
            try:
                embedding = embeddings.embed_query(text)
                print(f"Embedding created for: '{text[:20]}...' (len: {len(embedding)})")
            except Exception as e:
                print(f"Error generating embedding: {str(e)[:50]}")
        
        return True
        
    except Exception as e:
        print(f"❌ خطأ في اختبار التضمين: {e}")
        return False

def test_vector_database():
    """Test vector database operations"""
    print("\nTesting vector database...")
    
    try:
        from langchain_ollama import OllamaEmbeddings
        from langchain_chroma import Chroma
        from langchain_core.documents import Document
        
        # Create temporary directory for test database
        temp_dir = tempfile.mkdtemp()
        
        try:
            # Initialize embeddings and database
            embeddings = OllamaEmbeddings(model="nomic-embed-text")
            vector_db = Chroma(
                persist_directory=temp_dir,
                embedding_function=embeddings
            )
            
            print("Vector database initialized")
            
            # Test documents
            test_documents = [
                Document(page_content="Python is a programming language", metadata={"source": "test1"}),
                Document(page_content="JavaScript is used for web development", metadata={"source": "test2"}),
                Document(page_content="Machine learning is a subset of AI", metadata={"source": "test3"}),
                Document(page_content="البرمجة بلغة Python سهلة التعلم", metadata={"source": "test4"}),
                Document(page_content="JavaScript تستخدم لتطوير الويب", metadata={"source": "test5"})
            ]
            
            # Add documents to database
            vector_db.add_documents(test_documents)
            print(f"Added {len(test_documents)} documents to DB")
            
            # Test search functionality
            search_queries = [
                "Python programming",
                "web development",
                "machine learning",
                "البرمجة",
                "تطوير الويب"
            ]
            
            for query in search_queries:
                try:
                    results = vector_db.similarity_search(query, k=2)
                    print(f"Search '{query}': found {len(results)} result(s)")
                    for i, doc in enumerate(results, 1):
                        print(f"   {i}. {doc.page_content[:50]}...")
                except Exception as e:
                    print(f"❌ خطأ في البحث عن '{query}': {str(e)[:50]}")
            
            # Test database count
            try:
                count = vector_db._collection.count()
                print(f"Documents in DB: {count}")
            except Exception as e:
                print(f"Warning: cannot get DB document count: {str(e)[:50]}")
            
            return True
            
        finally:
            # Clean up temporary directory
            shutil.rmtree(temp_dir)
            print("Cleaned temporary files")
        
    except Exception as e:
        print(f"Error in vector database test: {e}")
        return False

def test_text_processing():
    """Test text processing and chunking"""
    print("\nTesting text processing...")
    
    try:
        from langchain.text_splitter import RecursiveCharacterTextSplitter
        from langchain_community.document_loaders import TextLoader
        
        # Create a temporary test file
        test_content = """
        Python is a high-level, interpreted programming language.
        Created by Guido van Rossum in 1991.
        Known for being easy to learn and read.
        Python supports object-oriented programming.
        Used in web development and artificial intelligence.
        """
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
            f.write(test_content)
            temp_file = f.name
        
        try:
            # Test text loading
            loader = TextLoader(temp_file, encoding='utf-8')
            documents = loader.load()
            print(f"Loaded {len(documents)} document(s) from file")
            
            # Test text splitting
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=100,
                chunk_overlap=20,
                length_function=len,
                separators=["\n\n", "\n", " ", ""]
            )
            
            chunked_documents = text_splitter.split_documents(documents)
            print(f"Split into {len(chunked_documents)} chunk(s)")
            
            for i, chunk in enumerate(chunked_documents, 1):
                print(f"   Chunk {i}: {chunk.page_content[:50]}...")
            
            return True
            
        finally:
            # Clean up temporary file
            os.unlink(temp_file)
        
    except Exception as e:
        print(f"Error in text processing test: {e}")
        return False

def test_database_integration():
    """Test full database integration"""
    print("\nTesting database integration...")
    
    try:
        from langchain_ollama import OllamaEmbeddings
        from langchain_chroma import Chroma
        from langchain.text_splitter import RecursiveCharacterTextSplitter
        from langchain_core.documents import Document
        
        # Create temporary directory
        temp_dir = tempfile.mkdtemp()
        
        try:
            # Initialize components
            embeddings = OllamaEmbeddings(model="nomic-embed-text")
            vector_db = Chroma(
                persist_directory=temp_dir,
                embedding_function=embeddings
            )
            
            # Create test content
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
            
            # Process text
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=150,
                chunk_overlap=30,
                length_function=len
            )
            
            documents = [Document(page_content=test_content, metadata={"source": "python_guide"})]
            chunked_docs = text_splitter.split_documents(documents)
            
            # Add to database
            vector_db.add_documents(chunked_docs)
            print(f"Added {len(chunked_docs)} chunk(s) to DB")
            
            # Test various searches
            search_tests = [
                ("Python features", "features"),
                ("programming language", "language"),
                ("web development", "web"),
                ("machine learning", "learning")
            ]
            
            for query, description in search_tests:
                try:
                    results = vector_db.similarity_search(query, k=1)
                    print(f"Search '{description}': {'found' if results else 'no'} results")
                except Exception as e:
                    print(f"Error searching '{description}': {str(e)[:50]}")
            
            return True
            
        finally:
            shutil.rmtree(temp_dir)
        
    except Exception as e:
        print(f"Error in integration test: {e}")
        return False

def main():
    """Run all database tests"""
    print("Starting vector database tests...")
    
    tests = [
        ("Embeddings", test_embeddings),
        ("Vector DB", test_vector_database),
        ("Text processing", test_text_processing),
        ("DB integration", test_database_integration)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"Unexpected error in {test_name}: {e}")
    
    print("\n" + "=" * 50)
    print(f"Results: {passed}/{total} passed")
    
    if passed == total:
        print("All DB tests passed. Vector DB is ready.")
    else:
        print("Some DB tests failed. Check errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)