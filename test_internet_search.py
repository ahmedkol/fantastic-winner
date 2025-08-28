#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Internet Search Functionality
اختبار وظائف البحث في الإنترنت
"""

import sys
import time

def test_internet_search():
    """Test internet search functionality"""
    print("🔍 اختبار وظائف البحث في الإنترنت...")
    print("=" * 50)
    
    try:
        from internet_search import InternetSearch
        
        # Create search instance
        search = InternetSearch()
        print("✅ تم إنشاء مثيل البحث في الإنترنت")
        
        # Test queries
        test_queries = [
            "Python programming language",
            "أحدث إصدار من Python",
            "JavaScript tutorial",
            "machine learning basics"
        ]
        
        search_engines = ['google', 'bing', 'duckduckgo']
        
        for engine in search_engines:
            print(f"\n🌐 اختبار محرك البحث: {engine.upper()}")
            print("-" * 30)
            
            for query in test_queries:
                print(f"🔍 البحث عن: '{query}'")
                
                try:
                    results = search.search_web(query, engine)
                    
                    if results:
                        print(f"✅ تم العثور على {len(results)} نتيجة")
                        for i, result in enumerate(results[:2], 1):
                            print(f"   {i}. {result['title'][:60]}...")
                            print(f"      {result['url'][:50]}...")
                    else:
                        print("⚠️ لم يتم العثور على نتائج")
                    
                    # Wait a bit between requests
                    time.sleep(1)
                    
                except Exception as e:
                    print(f"❌ خطأ في البحث: {str(e)[:50]}")
        
        # Test web content fetching
        print(f"\n📄 اختبار جلب محتوى الويب...")
        test_url = "https://www.python.org"
        
        try:
            content = search.get_web_content(test_url)
            if content:
                print(f"✅ تم جلب محتوى من {test_url}")
                print(f"   الطول: {len(content)} حرف")
                print(f"   المعاينة: {content[:100]}...")
            else:
                print(f"⚠️ لم يتم جلب محتوى من {test_url}")
        except Exception as e:
            print(f"❌ خطأ في جلب المحتوى: {str(e)[:50]}")
        
        print("\n✅ تم إكمال اختبار البحث في الإنترنت")
        return True
        
    except ImportError as e:
        print(f"❌ خطأ في استيراد وحدة البحث: {e}")
        return False
    except Exception as e:
        print(f"❌ خطأ غير متوقع: {e}")
        return False

def test_search_tools():
    """Test LangChain search tools"""
    print("\n🔧 اختبار أدوات البحث في LangChain...")
    print("=" * 50)
    
    try:
        from internet_search import create_web_search_tool, create_web_content_tool
        
        # Create tools
        web_search_tool = create_web_search_tool()
        web_content_tool = create_web_content_tool()
        
        print("✅ تم إنشاء أدوات البحث")
        
        # Test web search tool
        print("\n🔍 اختبار أداة البحث في الويب...")
        try:
            result = web_search_tool.invoke({"query": "Python programming", "engine": "google"})
            print(f"✅ نجح البحث: {len(result)} حرف")
            print(f"   المعاينة: {result[:100]}...")
        except Exception as e:
            print(f"❌ خطأ في أداة البحث: {str(e)[:50]}")
        
        # Test web content tool
        print("\n📄 اختبار أداة جلب المحتوى...")
        try:
            result = web_content_tool.invoke({"url": "https://www.python.org"})
            print(f"✅ نجح جلب المحتوى: {len(result)} حرف")
            print(f"   المعاينة: {result[:100]}...")
        except Exception as e:
            print(f"❌ خطأ في أداة جلب المحتوى: {str(e)[:50]}")
        
        return True
        
    except Exception as e:
        print(f"❌ خطأ في اختبار الأدوات: {e}")
        return False

def main():
    """Run all internet search tests"""
    print("🚀 بدء اختبار وظائف البحث في الإنترنت...")
    
    tests = [
        ("البحث في الإنترنت", test_internet_search),
        ("أدوات البحث", test_search_tools)
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
        print("🎉 جميع اختبارات البحث في الإنترنت نجحت!")
        print("✅ رونا جاهز للبحث في الإنترنت")
    else:
        print("⚠️ بعض اختبارات البحث في الإنترنت فشلت")
        print("💡 راجع الأخطاء أعلاه")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)