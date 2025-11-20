"""
Model Trainer - Training loop for the neural network
"""
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import os
import json
from datetime import datetime

class QADataset(Dataset):
    """Dataset for question-answering pairs"""
    
    def __init__(self, examples, tokenizer, max_src_len=256, max_trg_len=128):
        self.examples = examples
        self.tokenizer = tokenizer
        self.max_src_len = max_src_len
        self.max_trg_len = max_trg_len
    
    def __len__(self):
        return len(self.examples)
    
    def __getitem__(self, idx):
        example = self.examples[idx]
        question = example[1]  # question
        context = example[2]    # context
        answer = example[4] if example[4] else example[3]  # corrected_answer or answer
        
        # Combine question and context
        src_text = f"{question} {context}"
        
        # Encode
        src = self.tokenizer.encode(src_text, max_length=self.max_src_len)
        trg = self.tokenizer.encode(answer, max_length=self.max_trg_len)
        
        return torch.LongTensor(src), torch.LongTensor(trg)


class ModelTrainer:
    """Handles model training"""
    
    def __init__(self, model, tokenizer, device='cpu'):
        self.model = model.to(device)
        self.tokenizer = tokenizer
        self.device = device
        
        self.optimizer = optim.Adam(model.parameters(), lr=0.001)
        self.criterion = nn.CrossEntropyLoss(ignore_index=0)  # Ignore padding
        
        self.train_step = 0
        self.total_loss = 0.0
    
    def train_batch(self, src, trg):
        """Train on one batch"""
        self.model.train()
        self.optimizer.zero_grad()
        
        src = src.to(self.device)
        trg = trg.to(self.device)
        
        # Forward pass
        output = self.model(src, trg)
        
        # Calculate loss (skip first token which is <START>)
        output_dim = output.shape[-1]
        output = output[:, 1:].contiguous().view(-1, output_dim)
        trg = trg[:, 1:].contiguous().view(-1)
        
        loss = self.criterion(output, trg)
        
        # Backward pass
        loss.backward()
        torch.nn.utils.clip_grad_norm_(self.model.parameters(), 5.0)
        self.optimizer.step()
        
        self.train_step += 1
        self.total_loss += loss.item()
        
        return loss.item()
    
    def train_epoch(self, dataloader):
        """Train for one epoch"""
        epoch_loss = 0
        
        for batch_idx, (src, trg) in enumerate(dataloader):
            loss = self.train_batch(src, trg)
            epoch_loss += loss
            
            if batch_idx % 10 == 0:
                avg_loss = epoch_loss / (batch_idx + 1)
                print(f"  Batch {batch_idx}/{len(dataloader)} | Loss: {avg_loss:.4f}")
        
        return epoch_loss / len(dataloader)
    
    def save_checkpoint(self, path, metadata=None):
        """Save model checkpoint"""
        os.makedirs(os.path.dirname(path), exist_ok=True)
        
        checkpoint = {
            'model_state_dict': self.model.state_dict(),
            'optimizer_state_dict': self.optimizer.state_dict(),
            'train_step': self.train_step,
            'total_loss': self.total_loss,
            'timestamp': datetime.now().isoformat()
        }
        
        if metadata:
            checkpoint['metadata'] = metadata
        
        torch.save(checkpoint, path)
        print(f"✅ Checkpoint saved: {path}")
    
    def load_checkpoint(self, path):
        """Load model checkpoint"""
        if not os.path.exists(path):
            print(f"No checkpoint found at {path}")
            return False
        
        checkpoint = torch.load(path, map_location=self.device)
        self.model.load_state_dict(checkpoint['model_state_dict'])
        self.optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
        self.train_step = checkpoint.get('train_step', 0)
        self.total_loss = checkpoint.get('total_loss', 0.0)
        
        print(f"✅ Checkpoint loaded from {path}")
        print(f"   Training step: {self.train_step}")
        return True
    
    def get_avg_loss(self):
        """Get average loss"""
        if self.train_step == 0:
            return 0.0
        return self.total_loss / self.train_step


if __name__ == "__main__":
    print("Trainer module loaded successfully!")

