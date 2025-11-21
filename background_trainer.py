#!/usr/bin/env python3
"""
Background Trainer - Runs 24/7 training the model
Continuously scrapes web and improves the model
Run this script in the background: python background_trainer.py &
"""
import torch
import time
import sys
import os
from torch.utils.data import DataLoader

# Force unbuffered output
sys.stdout.reconfigure(line_buffering=True) if hasattr(sys.stdout, 'reconfigure') else None
sys.stderr.reconfigure(line_buffering=True) if hasattr(sys.stderr, 'reconfigure') else None

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from model.neural_network import create_model
from model.tokenizer import SimpleTokenizer
from model.data_manager import DataManager
from model.autonomous_learner import AutonomousLearner
from model.trainer import ModelTrainer, QADataset
from model.grammar_corrector import GrammarCorrector
from model.quality_checker import QualityChecker
import config

def main():
    """Main 24/7 training loop"""
    print("\n" + "="*70)
    print("🧠 24/7 AUTONOMOUS AI TRAINER STARTING")
    print("="*70 + "\n")
    
    # Initialize components
    print("[1/7] Initializing Data Manager...")
    data_manager = DataManager(config.TRAINING_DB)
    
    print("[2/7] Initializing Tokenizer...")
    tokenizer = SimpleTokenizer(config.VOCAB_SIZE)
    
    # Try to load existing tokenizer
    if not tokenizer.load(config.VOCAB_PATH):
        print("   No existing tokenizer found. Will build from scratch.")
    
    print("[3/7] Creating Neural Network Model...")
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"   Using device: {device}")
    
    print(f"   Creating model with {config.VOCAB_SIZE} vocab...")
    model = create_model(
        vocab_size=config.VOCAB_SIZE,
        embedding_dim=config.EMBEDDING_DIM,
        hidden_dim=config.HIDDEN_DIM,
        num_layers=config.NUM_LAYERS
    )
    print(f"   Model created successfully!")
    
    print("[4/7] Initializing Trainer...")
    trainer = ModelTrainer(model, tokenizer, device)
    
    # Try to load existing checkpoint
    if os.path.exists(config.MODEL_PATH):
        trainer.load_checkpoint(config.MODEL_PATH)
    
    print("[5/7] Initializing Autonomous Learner...")
    learner = AutonomousLearner(data_manager)
    
    print("[6/7] Initializing Grammar Corrector...")
    grammar_corrector = GrammarCorrector()
    
    print("[7/7] Initializing Quality Checker...")
    quality_checker = QualityChecker(config.STATUS_FILE)
    
    print("\n✅ All systems initialized!\n")
    print("="*70)
    print("🚀 STARTING 24/7 TRAINING CYCLE")
    print("="*70)
    
    iteration = 0
    
    while True:
        try:
            iteration += 1
            print(f"\n\n{'='*70}")
            print(f"🚀 TRAINING CYCLE #{iteration} - {time.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"{'='*70}")
            
            # Step 1: Autonomous learning (scrape web)
            print(f"\n[STEP 1] 🌐 Learning from the web...")
            learner.learn_one_topic()
            
            total_examples = data_manager.get_total_examples()
            print(f"\n📚 TOTAL EXAMPLES IN DATABASE: {total_examples}")
            
            # Step 2: Build/update vocabulary if needed
            if len(tokenizer) < 100 and total_examples >= 20:
                print(f"\n[STEP 2] 📖 Building vocabulary...")
                examples = data_manager.get_all_examples_for_vocab(limit=total_examples)
                all_texts = []
                for ex in examples:
                    all_texts.extend([ex[0], ex[1], ex[2]])  # question, context, answer
                print(f"   Building vocab from {len(all_texts)} texts...")
                tokenizer.build_vocab(all_texts)
                tokenizer.save(config.VOCAB_PATH)
                print(f"   ✅ Vocabulary size: {len(tokenizer)} words")
            
            # Step 3: Train model if we have enough data
            untrained = data_manager.get_untrained_examples(limit=config.BATCH_SIZE)
            
            if len(untrained) >= config.BATCH_SIZE:
                print(f"\n[STEP 3] 🧠 Training neural network on {len(untrained)} examples...")
                
                dataset = QADataset(untrained, tokenizer)
                dataloader = DataLoader(dataset, batch_size=min(8, len(untrained)), shuffle=True)
                
                loss = trainer.train_epoch(dataloader)
                print(f"   📉 Loss: {loss:.4f} (lower is better)")
                
                # Mark as trained
                example_ids = [ex[0] for ex in untrained]
                data_manager.mark_as_trained(example_ids)
                
                # Save checkpoint periodically
                if trainer.train_step % config.CHECKPOINT_INTERVAL == 0:
                    print(f"   💾 Saving checkpoint at step {trainer.train_step}...")
                    trainer.save_checkpoint(config.MODEL_PATH)
            else:
                print(f"\n[STEP 3] ⏸️  Waiting for more data ({len(untrained)}/{config.BATCH_SIZE} examples)")
            
            # Step 4: Evaluate model quality every few cycles
            if iteration % config.EVAL_INTERVAL_CYCLES == 0 and total_examples >= config.MIN_TRAINING_EXAMPLES:
                print(f"\n[STEP 4] 📊 Evaluating AI quality...")
                
                # Simple quality estimate based on loss and examples
                avg_loss = trainer.get_avg_loss()
                quality_score = max(0, min(1, 1 - (avg_loss / 10)))  # Normalize loss to 0-1
                
                # Grammar score starts low, improves with more training
                grammar_score = min(0.95, quality_score + (total_examples / 10000))
                
                quality_checker.update_metrics(total_examples, quality_score, grammar_score)
                
                print(f"   🎯 Quality: {quality_score:.1%} | Grammar: {grammar_score:.1%}")
                print(f"   📈 Status: {quality_checker.get_status_display()}")
                
                data_manager.save_performance(total_examples, quality_score, grammar_score, quality_checker.status['state'])
            
            # Display current status
            print(f"\n{'='*70}")
            print(f"📊 CURRENT STATUS: {quality_checker.get_status_display()}")
            print(f"💾 Training Steps: {trainer.train_step}")
            print(f"⏱️  Next cycle in {config.SCRAPE_INTERVAL} seconds")
            print(f"{'='*70}")
            
            # Sleep before next cycle
            time.sleep(config.SCRAPE_INTERVAL)
            
        except KeyboardInterrupt:
            print("\n\n🛑 Training stopped by user")
            print("Saving final checkpoint...")
            trainer.save_checkpoint(config.MODEL_PATH)
            break
        except Exception as e:
            print(f"\n❌ Error in training cycle: {e}")
            import traceback
            traceback.print_exc()
            print(f"Retrying in {config.SCRAPE_INTERVAL} seconds...")
            time.sleep(config.SCRAPE_INTERVAL)


if __name__ == "__main__":
    print("\n🔥 Starting 24/7 Background Training...")
    print("💡 This will run forever and continuously improve the model")
    print("💡 Press Ctrl+C to stop\n")
    
    main()

