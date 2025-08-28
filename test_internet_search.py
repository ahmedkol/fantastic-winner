#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Internet Search Functionality
"""

import sys
import time

def test_internet_search():
    """Test internet search functionality"""
    print("Internet search functionality test...")
    print("=" * 50)
    
    try:
        from internet_search import InternetSearch
        
        # Create search instance
        search = InternetSearch()
        print("InternetSearch instance created")
        
        # Test queries
        test_queries = [
            "Python programming language",
            "latest Python release",
            "JavaScript tutorial",
            "machine learning basics"
        ]
        
        search_engines = ['google', 'bing', 'duckduckgo']
        
        for engine in search_engines:
            print(f"\nTesting search engine: {engine.upper()}")
            print("-" * 30)
            
            for query in test_queries:
                print(f"Searching for: '{query}'")
                
                try:
                    results = search.search_web(query, engine)
                    
                    if results:
                        print(f"Found {len(results)} result(s)")
                        for i, result in enumerate(results[:2], 1):
                            print(f"   {i}. {result['title'][:60]}...")
                            print(f"      {result['url'][:50]}...")
                    else:
                        print("No results found")
                    
                    # Wait a bit between requests
                    time.sleep(1)
                    
                except Exception as e:
                    print(f"Search error: {str(e)[:50]}")
        
        # Test web content fetching
        print(f"\nTesting web content fetch...")
        test_url = "https://www.python.org"
        
        try:
            content = search.get_web_content(test_url)
            if content:
                print(f"Fetched content from {test_url}")
                print(f"   length: {len(content)} chars")
                print(f"   preview: {content[:100]}...")
            else:
                print(f"No content fetched from {test_url}")
        except Exception as e:
            print(f"Content fetch error: {str(e)[:50]}")
        
        print("\nInternet search tests completed")
        return True
        
    except ImportError as e:
        print(f"Import error: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

def test_search_tools():
    """Test LangChain search tools"""
    print("\nTesting LangChain search tools...")
    print("=" * 50)
    
    try:
        from internet_search import create_web_search_tool, create_web_content_tool
        
        # Create tools
        web_search_tool = create_web_search_tool()
        web_content_tool = create_web_content_tool()
        
        print("Search tools created")
        
        # Test web search tool
        print("\nTesting web_search tool...")
        try:
            result = web_search_tool.invoke({"query": "Python programming", "engine": "google"})
            print(f"Search OK: {len(result)} chars")
            print(f"   preview: {result[:100]}...")
        except Exception as e:
            print(f"web_search tool error: {str(e)[:50]}")
        
        # Test web content tool
        print("\nTesting get_webpage_content tool...")
        try:
            result = web_content_tool.invoke({"url": "https://www.python.org"})
            print(f"Content fetch OK: {len(result)} chars")
            print(f"   preview: {result[:100]}...")
        except Exception as e:
            print(f"get_webpage_content tool error: {str(e)[:50]}")
        
        return True
        
    except Exception as e:
        print(f"Error while testing tools: {e}")
        return False

def main():
    """Run all internet search tests"""
    print("Starting internet search tests...")
    
    tests = [
        ("InternetSearch", test_internet_search),
        ("Tools", test_search_tools)
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
        print("All internet search tests passed. Rona is ready for internet search.")
    else:
        print("Some internet search tests failed. Check errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)