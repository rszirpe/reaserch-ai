"""
Custom Tokenizer for the Neural Network
Handles text encoding/decoding with vocabulary management
"""
import pickle
import re
from collections import Counter
import os

class SimpleTokenizer:
    """Word-level tokenizer with special tokens"""
    
    # Special tokens
    PAD_TOKEN = '<PAD>'
    UNK_TOKEN = '<UNK>'
    START_TOKEN = '<START>'
    END_TOKEN = '<END>'
    
    PAD_IDX = 0
    UNK_IDX = 1
    START_IDX = 2
    END_IDX = 3
    
    def __init__(self, vocab_size=30000):
        self.vocab_size = vocab_size
        self.word2idx = {
            self.PAD_TOKEN: self.PAD_IDX,
            self.UNK_TOKEN: self.UNK_IDX,
            self.START_TOKEN: self.START_IDX,
            self.END_TOKEN: self.END_IDX
        }
        self.idx2word = {v: k for k, v in self.word2idx.items()}
        self.word_counts = Counter()
        
    def tokenize(self, text):
        """Convert text to list of tokens"""
        # Lowercase and clean
        text = text.lower()
        # Keep letters, numbers, basic punctuation
        text = re.sub(r'[^a-z0-9\s\.\,\?\!\-]', '', text)
        # Split into words
        tokens = text.split()
        return tokens
    
    def build_vocab(self, texts, min_freq=2):
        """Build vocabulary from list of texts"""
        print(f"Building vocabulary from {len(texts)} texts...")
        
        # Count all words
        for text in texts:
            tokens = self.tokenize(text)
            self.word_counts.update(tokens)
        
        # Take most common words (up to vocab_size - 4 special tokens)
        most_common = self.word_counts.most_common(self.vocab_size - 4)
        
        # Add to vocabulary (only words with freq >= min_freq)
        for word, count in most_common:
            if count >= min_freq and word not in self.word2idx:
                idx = len(self.word2idx)
                self.word2idx[word] = idx
                self.idx2word[idx] = word
        
        print(f"Vocabulary built with {len(self.word2idx)} words")
        
    def encode(self, text, max_length=None, add_special_tokens=True):
        """Convert text to list of indices"""
        tokens = self.tokenize(text)
        
        if add_special_tokens:
            tokens = [self.START_TOKEN] + tokens + [self.END_TOKEN]
        
        # Convert to indices
        indices = [self.word2idx.get(token, self.UNK_IDX) for token in tokens]
        
        # Truncate or pad
        if max_length:
            if len(indices) > max_length:
                indices = indices[:max_length]
            else:
                indices = indices + [self.PAD_IDX] * (max_length - len(indices))
        
        return indices
    
    def decode(self, indices, skip_special_tokens=True):
        """Convert list of indices back to text"""
        tokens = []
        for idx in indices:
            if idx in self.idx2word:
                token = self.idx2word[idx]
                
                if skip_special_tokens:
                    if token in [self.PAD_TOKEN, self.START_TOKEN, self.END_TOKEN]:
                        if token == self.END_TOKEN:
                            break
                        continue
                
                tokens.append(token)
        
        return ' '.join(tokens)
    
    def save(self, path):
        """Save tokenizer to file"""
        with open(path, 'wb') as f:
            pickle.dump({
                'word2idx': self.word2idx,
                'idx2word': self.idx2word,
                'word_counts': self.word_counts,
                'vocab_size': self.vocab_size
            }, f)
        print(f"Tokenizer saved to {path}")
    
    def load(self, path):
        """Load tokenizer from file"""
        if not os.path.exists(path):
            print(f"Tokenizer file not found: {path}")
            return False
        
        with open(path, 'rb') as f:
            data = pickle.load(f)
            self.word2idx = data['word2idx']
            self.idx2word = data['idx2word']
            self.word_counts = data['word_counts']
            self.vocab_size = data['vocab_size']
        
        print(f"Tokenizer loaded from {path} with {len(self.word2idx)} words")
        return True
    
    def __len__(self):
        return len(self.word2idx)


if __name__ == "__main__":
    # Test tokenizer
    tokenizer = SimpleTokenizer(vocab_size=100)
    
    # Build vocab from sample texts
    texts = [
        "What is artificial intelligence?",
        "How does machine learning work?",
        "Explain quantum computing in simple terms.",
        "Artificial intelligence is fascinating."
    ]
    
    tokenizer.build_vocab(texts)
    
    # Test encoding
    text = "What is artificial intelligence?"
    encoded = tokenizer.encode(text, max_length=20)
    print(f"Encoded: {encoded}")
    
    # Test decoding
    decoded = tokenizer.decode(encoded)
    print(f"Decoded: {decoded}")
    
    print("Tokenizer test successful!")

