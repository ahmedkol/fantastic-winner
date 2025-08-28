# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
import time
import re
from langchain.tools import tool

class InternetSearch:
    """Manages internet search functionality for Rona"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.search_engines = {
            'google': 'https://www.google.com/search?q={}',
            'bing': 'https://www.bing.com/search?q={}',
            'duckduckgo': 'https://duckduckgo.com/html/?q={}'
        }
        self.max_results = 3
        self.timeout = 10
    
    def search_web(self, query, engine='google'):
        """
        Search the web using the specified search engine
        """
        try:
            if engine not in self.search_engines:
                engine = 'google'
            
            # Encode the query for URL
            encoded_query = quote_plus(query)
            search_url = self.search_engines[engine].format(encoded_query)
            
            print(f"🔍 Searching web for: {query}")
            
            # Make the request
            response = self.session.get(search_url, timeout=self.timeout)
            response.raise_for_status()
            
            # Parse the results
            soup = BeautifulSoup(response.text, 'html.parser')
            
            if engine == 'google':
                return self._parse_google_results(soup)
            elif engine == 'bing':
                return self._parse_bing_results(soup)
            elif engine == 'duckduckgo':
                return self._parse_duckduckgo_results(soup)
            else:
                return self._parse_google_results(soup)
                
        except requests.RequestException as e:
            print(f"❌ Search request failed: {str(e)[:50]}")
            return []
        except Exception as e:
            print(f"❌ Search parsing failed: {str(e)[:50]}")
            return []
    
    def _parse_google_results(self, soup):
        """Parse Google search results"""
        results = []
        try:
            # Find search result containers
            search_results = soup.find_all('div', class_='g')
            
            for result in search_results[:self.max_results]:
                title_elem = result.find('h3')
                link_elem = result.find('a')
                snippet_elem = result.find('div', class_='VwiC3b')
                
                if title_elem and link_elem:
                    title = title_elem.get_text(strip=True)
                    link = link_elem.get('href', '')
                    snippet = snippet_elem.get_text(strip=True) if snippet_elem else ''
                    
                    if link.startswith('/url?q='):
                        link = link.split('/url?q=')[1].split('&')[0]
                    
                    results.append({
                        'title': title,
                        'url': link,
                        'snippet': snippet[:200] + '...' if len(snippet) > 200 else snippet
                    })
        except Exception as e:
            print(f"⚠️ Google parsing error: {str(e)[:50]}")
        
        return results
    
    def _parse_bing_results(self, soup):
        """Parse Bing search results"""
        results = []
        try:
            search_results = soup.find_all('li', class_='b_algo')
            
            for result in search_results[:self.max_results]:
                title_elem = result.find('h2')
                link_elem = result.find('a')
                snippet_elem = result.find('p')
                
                if title_elem and link_elem:
                    title = title_elem.get_text(strip=True)
                    link = link_elem.get('href', '')
                    snippet = snippet_elem.get_text(strip=True) if snippet_elem else ''
                    
                    results.append({
                        'title': title,
                        'url': link,
                        'snippet': snippet[:200] + '...' if len(snippet) > 200 else snippet
                    })
        except Exception as e:
            print(f"⚠️ Bing parsing error: {str(e)[:50]}")
        
        return results
    
    def _parse_duckduckgo_results(self, soup):
        """Parse DuckDuckGo search results"""
        results = []
        try:
            search_results = soup.find_all('div', class_='result')
            
            for result in search_results[:self.max_results]:
                title_elem = result.find('a', class_='result__a')
                snippet_elem = result.find('a', class_='result__snippet')
                
                if title_elem:
                    title = title_elem.get_text(strip=True)
                    link = title_elem.get('href', '')
                    snippet = snippet_elem.get_text(strip=True) if snippet_elem else ''
                    
                    results.append({
                        'title': title,
                        'url': link,
                        'snippet': snippet[:200] + '...' if len(snippet) > 200 else snippet
                    })
        except Exception as e:
            print(f"⚠️ DuckDuckGo parsing error: {str(e)[:50]}")
        
        return results
    
    def get_web_content(self, url):
        """
        Get content from a specific URL
        """
        try:
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Get text content
            text = soup.get_text()
            
            # Clean up whitespace
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            return text[:1000] + '...' if len(text) > 1000 else text
            
        except Exception as e:
            print(f"❌ Failed to get content from {url}: {str(e)[:50]}")
            return ""

def create_web_search_tool():
    """
    Create a web search tool for LangChain
    """
    internet_search = InternetSearch()
    
    @tool
    def web_search(query: str, engine: str = "google") -> str:
        """
        Search the internet for information. Use this when you need current information 
        that's not in the local database.
        
        Args:
            query: The search query
            engine: Search engine to use (google, bing, duckduckgo)
        
        Returns:
            Search results as formatted text
        """
        try:
            results = internet_search.search_web(query, engine)
            
            if not results:
                return "لم يتم العثور على نتائج بحث في الإنترنت."
            
            formatted_results = f"نتائج البحث عن '{query}':\n\n"
            
            for i, result in enumerate(results, 1):
                formatted_results += f"{i}. {result['title']}\n"
                formatted_results += f"   الرابط: {result['url']}\n"
                formatted_results += f"   الملخص: {result['snippet']}\n\n"
            
            return formatted_results
            
        except Exception as e:
            return f"حدث خطأ أثناء البحث في الإنترنت: {str(e)[:100]}"
    
    return web_search

def create_web_content_tool():
    """
    Create a tool to get content from specific URLs
    """
    internet_search = InternetSearch()
    
    @tool
    def get_webpage_content(url: str) -> str:
        """
        Get the content of a specific webpage. Use this when you need detailed 
        information from a specific website.
        
        Args:
            url: The URL to fetch content from
        
        Returns:
            The webpage content as text
        """
        try:
            content = internet_search.get_web_content(url)
            
            if not content:
                return "لم يتم العثور على محتوى من الرابط المحدد."
            
            return f"محتوى الصفحة من {url}:\n\n{content}"
            
        except Exception as e:
            return f"حدث خطأ أثناء جلب محتوى الصفحة: {str(e)[:100]}"
    
    return get_webpage_content