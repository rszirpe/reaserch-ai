from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
try:
    from ddgs import DDGS
except ImportError:
    from duckduckgo_search import DDGS
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import re

app = Flask(__name__, static_folder='static')
CORS(app)

# Configure Gemini API
GEMINI_API_KEY = "AIzaSyD1A1JWBvL2AZ4e4y3vYGffUbqyJBauBWs"
genai.configure(api_key=GEMINI_API_KEY)

def search_duckduckgo(query, max_results=8):
    """Search DuckDuckGo and return top results"""
    try:
        # Use DuckDuckGo HTML search (no SSL/TLS 1.3 required)
        url = "https://html.duckduckgo.com/html/"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        data = {'q': query}
        
        response = requests.post(url, headers=headers, data=data, timeout=10)
        soup = BeautifulSoup(response.content, 'lxml')
        
        results = []
        result_divs = soup.find_all('div', class_='result')
        
        for div in result_divs[:max_results]:
            title_tag = div.find('a', class_='result__a')
            snippet_tag = div.find('a', class_='result__snippet')
            
            if title_tag:
                title = title_tag.get_text(strip=True)
                url = title_tag.get('href', '')
                snippet = snippet_tag.get_text(strip=True) if snippet_tag else ''
                
                print(f"Found result: {title}")
                results.append({
                    'title': title,
                    'url': url,
                    'snippet': snippet
                })
        
        print(f"Total results found: {len(results)}")
        return results
    except Exception as e:
        print(f"Error searching DuckDuckGo: {e}")
        import traceback
        traceback.print_exc()
        return []

def scrape_website(url, timeout=5):
    """Scrape content from a website"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=timeout, allow_redirects=True)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'lxml')
        
        # Remove script and style elements
        for script in soup(["script", "style", "nav", "footer", "header"]):
            script.decompose()
        
        # Get text
        text = soup.get_text()
        
        # Clean up text
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        # Limit text length to prevent token overflow
        max_chars = 3000
        if len(text) > max_chars:
            text = text[:max_chars] + "..."
        
        return text
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None

def scrape_multiple_sites(urls, max_workers=5):
    """Scrape multiple sites concurrently"""
    scraped_data = []
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_url = {executor.submit(scrape_website, url): url for url in urls}
        
        for future in as_completed(future_to_url):
            url = future_to_url[future]
            try:
                content = future.result()
                if content:
                    scraped_data.append({
                        'url': url,
                        'content': content
                    })
            except Exception as e:
                print(f"Exception for {url}: {e}")
    
    return scraped_data

def generate_answer_with_gemini(query, scraped_data):
    """Use Gemini API to generate a concise answer from scraped data"""
    try:
        # Prepare the context from scraped data
        context = ""
        for i, data in enumerate(scraped_data, 1):
            context += f"\n\n--- Source {i} ({data['url']}) ---\n{data['content']}\n"
        
        # Create the prompt
        prompt = f"""You are a research assistant. Based on the following information gathered from multiple websites, provide a clear, concise, and comprehensive answer to the user's question.

User's Question: {query}

Information from websites:
{context}

Please synthesize this information and provide:
1. A clear, well-structured answer to the question
2. Key facts and insights
3. If there are conflicting information, mention it

Make your response informative but easy to understand. Use bullet points or numbered lists where appropriate."""

        # Generate response using Gemini
        # Use the latest flash model
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content(prompt)
        
        return response.text
    except Exception as e:
        print(f"Error generating answer with Gemini: {e}")
        return f"Error generating answer: {str(e)}"

@app.route('/')
def index():
    """Serve the main page"""
    return send_from_directory('static', 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    """Serve static files"""
    return send_from_directory('static', filename)

@app.route('/search', methods=['POST'])
def search():
    """Handle search requests"""
    try:
        data = request.get_json()
        query = data.get('query', '').strip()
        
        if not query:
            return jsonify({'error': 'Query is required'}), 400
        
        # Step 1: Search DuckDuckGo
        print(f"Searching DuckDuckGo for: {query}")
        search_results = search_duckduckgo(query, max_results=8)
        
        if not search_results:
            return jsonify({'error': 'No search results found'}), 404
        
        # Step 2: Scrape websites
        print(f"Found {len(search_results)} results. Starting to scrape...")
        urls = [result['url'] for result in search_results]
        scraped_data = scrape_multiple_sites(urls, max_workers=5)
        
        if not scraped_data:
            return jsonify({'error': 'Could not scrape any websites'}), 500
        
        print(f"Successfully scraped {len(scraped_data)} websites")
        
        # Step 3: Generate answer with Gemini
        print("Generating answer with Gemini...")
        answer = generate_answer_with_gemini(query, scraped_data)
        
        # Prepare response
        sources = [{'title': result['title'], 'url': result['url']} for result in search_results]
        
        return jsonify({
            'answer': answer,
            'sources': sources,
            'scraped_count': len(scraped_data)
        })
    
    except Exception as e:
        print(f"Error in search endpoint: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=8080)

