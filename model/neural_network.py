"""
Simple LSTM Encoder-Decoder Neural Network for Text Generation
Built from scratch for web research question answering
"""
import torch
import torch.nn as nn
import torch.nn.functional as F

class Attention(nn.Module):
    """Simple attention mechanism"""
    def __init__(self, hidden_dim):
        super(Attention, self).__init__()
        self.hidden_dim = hidden_dim
        self.attn = nn.Linear(hidden_dim * 2, hidden_dim)
        self.v = nn.Linear(hidden_dim, 1, bias=False)
        
    def forward(self, hidden, encoder_outputs):
        """
        hidden: [batch_size, hidden_dim]
        encoder_outputs: [batch_size, seq_len, hidden_dim]
        """
        batch_size = encoder_outputs.shape[0]
        seq_len = encoder_outputs.shape[1]
        
        # Repeat hidden state seq_len times
        hidden = hidden.unsqueeze(1).repeat(1, seq_len, 1)
        
        # Calculate attention scores
        energy = torch.tanh(self.attn(torch.cat((hidden, encoder_outputs), dim=2)))
        attention = self.v(energy).squeeze(2)
        
        # Apply softmax to get weights
        attn_weights = F.softmax(attention, dim=1)
        
        # Apply weights to encoder outputs
        context = torch.bmm(attn_weights.unsqueeze(1), encoder_outputs)
        
        return context.squeeze(1), attn_weights


class WebResearchModel(nn.Module):
    """
    LSTM-based Encoder-Decoder model for question answering
    Takes question + context, generates answer
    """
    def __init__(self, vocab_size, embedding_dim, hidden_dim, num_layers, dropout=0.3):
        super(WebResearchModel, self).__init__()
        
        self.vocab_size = vocab_size
        self.embedding_dim = embedding_dim
        self.hidden_dim = hidden_dim
        self.num_layers = num_layers
        
        # Embedding layer (shared between encoder and decoder)
        self.embedding = nn.Embedding(vocab_size, embedding_dim, padding_idx=0)
        
        # Encoder LSTM
        self.encoder = nn.LSTM(
            embedding_dim,
            hidden_dim,
            num_layers,
            batch_first=True,
            dropout=dropout if num_layers > 1 else 0,
            bidirectional=False
        )
        
        # Decoder LSTM
        self.decoder = nn.LSTM(
            embedding_dim + hidden_dim,  # embedding + context from attention
            hidden_dim,
            num_layers,
            batch_first=True,
            dropout=dropout if num_layers > 1 else 0
        )
        
        # Attention mechanism
        self.attention = Attention(hidden_dim)
        
        # Output layer
        self.fc_out = nn.Linear(hidden_dim, vocab_size)
        
        # Dropout
        self.dropout = nn.Dropout(dropout)
        
    def forward(self, src, trg, teacher_forcing_ratio=0.5):
        """
        src: [batch_size, src_len] - question + context
        trg: [batch_size, trg_len] - target answer
        """
        batch_size = src.shape[0]
        trg_len = trg.shape[1]
        
        # Encode source (question + context)
        embedded_src = self.dropout(self.embedding(src))
        encoder_outputs, (hidden, cell) = self.encoder(embedded_src)
        
        # Prepare for decoding
        outputs = torch.zeros(batch_size, trg_len, self.vocab_size).to(src.device)
        
        # First input to decoder is <START> token
        input = trg[:, 0].unsqueeze(1)
        
        for t in range(1, trg_len):
            # Embed input
            embedded = self.dropout(self.embedding(input))
            
            # Apply attention
            context, attn_weights = self.attention(hidden[-1], encoder_outputs)
            context = context.unsqueeze(1)
            
            # Concatenate embedding with context
            rnn_input = torch.cat((embedded, context), dim=2)
            
            # Pass through decoder
            output, (hidden, cell) = self.decoder(rnn_input, (hidden, cell))
            
            # Generate prediction
            prediction = self.fc_out(output.squeeze(1))
            outputs[:, t, :] = prediction
            
            # Teacher forcing: use real target as next input
            teacher_force = torch.rand(1).item() < teacher_forcing_ratio
            input = trg[:, t].unsqueeze(1) if teacher_force else prediction.argmax(1).unsqueeze(1)
        
        return outputs
    
    def generate(self, src, max_length=100, start_token=2, end_token=3):
        """
        Generate answer given question + context
        Used for inference (no teacher forcing)
        """
        self.eval()
        with torch.no_grad():
            batch_size = src.shape[0]
            
            # Encode
            embedded_src = self.embedding(src)
            encoder_outputs, (hidden, cell) = self.encoder(embedded_src)
            
            # Start with <START> token
            input = torch.LongTensor([[start_token]] * batch_size).to(src.device)
            
            outputs = []
            
            for _ in range(max_length):
                # Embed input
                embedded = self.embedding(input)
                
                # Apply attention
                context, _ = self.attention(hidden[-1], encoder_outputs)
                context = context.unsqueeze(1)
                
                # Concatenate and decode
                rnn_input = torch.cat((embedded, context), dim=2)
                output, (hidden, cell) = self.decoder(rnn_input, (hidden, cell))
                
                # Predict next token
                prediction = self.fc_out(output.squeeze(1))
                predicted_token = prediction.argmax(1)
                
                outputs.append(predicted_token.item())
                
                # Stop if <END> token generated
                if predicted_token.item() == end_token:
                    break
                
                # Use prediction as next input
                input = predicted_token.unsqueeze(1)
            
            return outputs


def create_model(vocab_size=30000, embedding_dim=256, hidden_dim=512, num_layers=2):
    """Factory function to create model"""
    return WebResearchModel(vocab_size, embedding_dim, hidden_dim, num_layers)


if __name__ == "__main__":
    # Test model creation
    model = create_model()
    print(f"Model created with {sum(p.numel() for p in model.parameters())} parameters")
    
    # Test forward pass
    batch_size = 4
    src_len = 50
    trg_len = 30
    
    src = torch.randint(0, 30000, (batch_size, src_len))
    trg = torch.randint(0, 30000, (batch_size, trg_len))
    
    output = model(src, trg)
    print(f"Output shape: {output.shape}")
    print("Model test successful!")

