"""Configuration for AI model and training"""
import os

# Model Settings
MODEL_DIR = "model"
CHECKPOINT_DIR = os.path.join(MODEL_DIR, "checkpoints")
MODEL_PATH = os.path.join(CHECKPOINT_DIR, "model_latest.pth")
VOCAB_PATH = os.path.join(MODEL_DIR, "vocab.pkl")
STATUS_FILE = os.path.join(MODEL_DIR, "model_status.json")
TRAINING_DB = os.path.join(MODEL_DIR, "training_data.db")

# Model Architecture
EMBEDDING_DIM = 256
HIDDEN_DIM = 512
NUM_LAYERS = 2
VOCAB_SIZE = 30000
MAX_LENGTH = 512

# Training Settings
BATCH_SIZE = 1  # MAXIMUM SPEED: Train after EVERY example! 🚀
LEARNING_RATE = 0.001
GRADIENT_CLIP = 5.0
CHECKPOINT_INTERVAL = 25  # Save every 25 steps (frequent saves)

# Quality Thresholds
QUALITY_THRESHOLD = 0.85  # Switch to local model
GRAMMAR_THRESHOLD = 0.90  # Stop using Gemini for grammar

# Background Learning
SCRAPE_INTERVAL = 10  # MAXIMUM SPEED: Scrape every 10 seconds! 🔥
MIN_TRAINING_EXAMPLES = 100  # Minimum examples before first evaluation
EVAL_INTERVAL_CYCLES = 3  # Evaluate quality every 3 cycles (fastest feedback!)

# Model Status States
STATUS_TRAINING = "training"
STATUS_READY = "ready"
STATUS_EXPERT = "expert"

# Gemini API
GEMINI_API_KEY = "AIzaSyD1A1JWBvL2AZ4e4y3vYGffUbqyJBauBWs"

