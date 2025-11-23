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

# Training Settings - MAXIMUM SPEED MODE!
BATCH_SIZE = 2  # Train every 2 examples - ULTRA FAST!
LEARNING_RATE = 0.003  # 3x faster learning rate!
GRADIENT_CLIP = 5.0
CHECKPOINT_INTERVAL = 50  # Save less often to focus on training

# Quality Thresholds
QUALITY_THRESHOLD = 0.85  # Switch to local model
GRAMMAR_THRESHOLD = 0.90  # Stop using Gemini for grammar

# Background Learning - LUDICROUS SPEED MODE!
SCRAPE_INTERVAL = 5  # SCRAPE EVERY 5 SECONDS - MAXIMUM POSSIBLE!
MIN_TRAINING_EXAMPLES = 2  # Train every 2 examples!
EVAL_INTERVAL_CYCLES = 5  # Evaluate every 5 cycles (less overhead, more training)

# Model Status States
STATUS_TRAINING = "training"
STATUS_READY = "ready"
STATUS_EXPERT = "expert"

# Gemini API
GEMINI_API_KEY = "AIzaSyD1A1JWBvL2AZ4e4y3vYGffUbqyJBauBWs"

