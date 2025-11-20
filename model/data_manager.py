"""
Data Manager - SQLite database for storing training examples
"""
import sqlite3
import json
import os
from datetime import datetime

class DataManager:
    """Manages training data in SQLite database"""
    
    def __init__(self, db_path):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize database with tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Training examples table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS training_examples (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question TEXT NOT NULL,
                context TEXT NOT NULL,
                answer TEXT NOT NULL,
                corrected_answer TEXT,
                quality_score REAL DEFAULT 0.0,
                grammar_score REAL DEFAULT 0.0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                used_for_training BOOLEAN DEFAULT FALSE
            )
        ''')
        
        # Model performance table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS model_performance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                total_examples INTEGER,
                quality_score REAL,
                grammar_score REAL,
                status TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        print(f"Database initialized at {self.db_path}")
    
    def add_example(self, question, context, answer, corrected_answer=None, quality_score=0.0):
        """Add a training example"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO training_examples 
            (question, context, answer, corrected_answer, quality_score)
            VALUES (?, ?, ?, ?, ?)
        ''', (question, context, answer, corrected_answer, quality_score))
        
        conn.commit()
        conn.close()
    
    def get_untrained_examples(self, limit=32):
        """Get examples that haven't been used for training yet"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, question, context, answer, corrected_answer
            FROM training_examples
            WHERE used_for_training = FALSE
            ORDER BY created_at ASC
            LIMIT ?
        ''', (limit,))
        
        examples = cursor.fetchall()
        conn.close()
        
        return examples
    
    def mark_as_trained(self, example_ids):
        """Mark examples as used for training"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        placeholders = ','.join('?' * len(example_ids))
        cursor.execute(f'''
            UPDATE training_examples
            SET used_for_training = TRUE
            WHERE id IN ({placeholders})
        ''', example_ids)
        
        conn.commit()
        conn.close()
    
    def get_total_examples(self):
        """Get total number of training examples"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM training_examples')
        count = cursor.fetchone()[0]
        
        conn.close()
        return count
    
    def save_performance(self, total_examples, quality_score, grammar_score, status):
        """Save model performance metrics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO model_performance 
            (total_examples, quality_score, grammar_score, status)
            VALUES (?, ?, ?, ?)
        ''', (total_examples, quality_score, grammar_score, status))
        
        conn.commit()
        conn.close()
    
    def get_latest_performance(self):
        """Get most recent performance metrics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT total_examples, quality_score, grammar_score, status
            FROM model_performance
            ORDER BY timestamp DESC
            LIMIT 1
        ''')
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                'total_examples': result[0],
                'quality_score': result[1],
                'grammar_score': result[2],
                'status': result[3]
            }
        return None
    
    def get_random_examples(self, limit=10):
        """Get random examples for validation"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT question, context, answer
            FROM training_examples
            ORDER BY RANDOM()
            LIMIT ?
        ''', (limit,))
        
        examples = cursor.fetchall()
        conn.close()
        
        return examples
    
    def get_all_examples_for_vocab(self, limit=None):
        """Get all examples for vocabulary building"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if limit:
            cursor.execute('''
                SELECT question, context, answer
                FROM training_examples
                ORDER BY id ASC
                LIMIT ?
            ''', (limit,))
        else:
            cursor.execute('''
                SELECT question, context, answer
                FROM training_examples
                ORDER BY id ASC
            ''')
        
        examples = cursor.fetchall()
        conn.close()
        
        return examples


if __name__ == "__main__":
    # Test data manager
    db_path = "../model/training_data.db"
    dm = DataManager(db_path)
    
    # Add test example
    dm.add_example(
        question="What is AI?",
        context="AI is artificial intelligence...",
        answer="AI is the simulation of human intelligence.",
        quality_score=0.5
    )
    
    print(f"Total examples: {dm.get_total_examples()}")
    print("Data manager test successful!")

