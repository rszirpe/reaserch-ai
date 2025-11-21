"""
Autonomous Web Learner - Continuously scrapes web and learns
Runs 24/7 in background, generating training data
"""
import requests
from bs4 import BeautifulSoup
import random
import time
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from model.data_manager import DataManager
import config

class AutonomousLearner:
    """Agent that autonomously browses web and learns"""
    
    # MASSIVE topic list for maximum learning diversity 🚀
    TOPICS = [
        # Science
        "photosynthesis", "black holes", "DNA", "evolution", "atoms", "gravity",
        "quantum physics", "chemistry", "astronomy", "biology", "neurons", "cells",
        "molecules", "ecosystems", "fossils", "plate tectonics", "thermodynamics",
        
        # Technology
        "artificial intelligence", "machine learning", "blockchain", "robotics",
        "internet", "computers", "programming", "databases", "cloud computing",
        "cybersecurity", "5G networks", "IoT", "algorithms", "data science",
        
        # History
        "World War 2", "Renaissance", "Ancient Egypt", "Roman Empire",
        "Industrial Revolution", "Cold War", "Space Race", "Medieval times",
        "Vikings", "Ancient Greece", "Silk Road", "Colonization",
        
        # General Knowledge
        "climate change", "renewable energy", "medicine", "psychology",
        "economics", "philosophy", "mathematics", "geography", "languages",
        "music theory", "architecture", "painting", "sculpture", "literature",
        
        # Current
        "cryptocurrency", "electric vehicles", "space exploration", "vaccines",
        "social media", "virtual reality", "quantum computing", "gene editing",
        "3D printing", "drones", "solar panels", "wind turbines", "batteries"
    ]
    
    QUESTION_TEMPLATES = [
        "What is {}?",
        "How does {} work?",
        "Explain {} in simple terms",
        "What are the benefits of {}?",
        "Tell me about {}",
        "What is the history of {}?",
        "Why is {} important?",
        "What are the key facts about {}?"
    ]
    
    def __init__(self, data_manager):
        self.data_manager = data_manager
        
    def generate_random_question(self):
        """Generate a random question from topics"""
        topic = random.choice(self.TOPICS)
        template = random.choice(self.QUESTION_TEMPLATES)
        question = template.format(topic)
        return question, topic
    
    def search_and_scrape(self, query):
        """Search DuckDuckGo and scrape content"""
        try:
            url = "https://html.duckduckgo.com/html/"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            data = {'q': query}
            
            response = requests.post(url, headers=headers, data=data, timeout=5)  # Faster timeout
            soup = BeautifulSoup(response.content, 'lxml')
            
            results = []
            result_divs = soup.find_all('div', class_='result')[:3]  # Take top 3
            
            for div in result_divs:
                title_tag = div.find('a', class_='result__a')
                if title_tag:
                    result_url = title_tag.get('href', '')
                    results.append(result_url)
            
            # Scrape content from results
            all_text = ""
            for result_url in results:
                try:
                    page_response = requests.get(result_url, headers=headers, timeout=3)  # Fast scraping!
                    page_soup = BeautifulSoup(page_response.content, 'lxml')
                    
                    # Remove unwanted tags
                    for tag in page_soup(["script", "style", "nav", "footer"]):
                        tag.decompose()
                    
                    text = page_soup.get_text()
                    lines = (line.strip() for line in text.splitlines())
                    text = ' '.join(line for line in lines if line)
                    
                    all_text += text[:2000] + " "  # Take first 2000 chars from each
                except:
                    continue
            
            return all_text[:5000] if all_text else None  # Limit total context
            
        except Exception as e:
            print(f"Error in search_and_scrape: {e}")
            return None
    
    def create_simple_answer(self, context, question):
        """Create a simple answer from context (for initial training)"""
        # Extract first few sentences as answer
        sentences = context.split('.')[:3]
        answer = '. '.join(sentences).strip() + '.'
        
        # Keep it concise (max 200 words)
        words = answer.split()
        if len(words) > 200:
            answer = ' '.join(words[:200]) + '...'
        
        return answer
    
    def learn_one_topic(self):
        """Learn one topic: search, scrape, create training example"""
        question, topic = self.generate_random_question()
        
        # Display question prominently
        print(f"\n" + "="*70)
        print(f"❓ QUESTION: {question}")
        print(f"🔍 TOPIC: {topic}")
        print("="*70)
        
        # Search and scrape
        context = self.search_and_scrape(topic)
        
        if context:
            # Create simple answer from context
            answer = self.create_simple_answer(context, question)
            
            # Save to database
            self.data_manager.add_example(
                question=question,
                context=context,
                answer=answer,
                quality_score=0.5  # Initial quality estimate
            )
            
            total = self.data_manager.get_total_examples()
            print(f"✅ Saved example #{total}")
            print(f"📝 Answer preview: {answer[:150]}...")
            
            return True
        else:
            print(f"[AUTONOMOUS LEARNING] Failed to scrape content for: {topic}")
            return False
    
    def run_forever(self, interval=30):
        """
        Run autonomous learning forever
        Scrapes web and creates training data continuously
        """
        print("\n" + "="*60)
        print("🧠 AUTONOMOUS LEARNER STARTED - TRAINING 24/7")
        print("="*60)
        
        iteration = 0
        while True:
            try:
                iteration += 1
                print(f"\n[Iteration {iteration}] Starting autonomous learning cycle...")
                
                success = self.learn_one_topic()
                
                if success:
                    print(f"[Iteration {iteration}] ✅ Success! Waiting {interval}s...")
                else:
                    print(f"[Iteration {iteration}] ⚠️ Failed. Retrying in {interval}s...")
                
                time.sleep(interval)
                
            except KeyboardInterrupt:
                print("\n\n[AUTONOMOUS LEARNING] Stopped by user")
                break
            except Exception as e:
                print(f"\n[AUTONOMOUS LEARNING] Error: {e}")
                print(f"Retrying in {interval}s...")
                time.sleep(interval)


if __name__ == "__main__":
    # Test autonomous learner
    from data_manager import DataManager
    
    db_path = "training_data.db"
    dm = DataManager(db_path)
    learner = AutonomousLearner(dm)
    
    print("Testing autonomous learner...")
    learner.learn_one_topic()
    
    print(f"\nTotal examples in database: {dm.get_total_examples()}")

