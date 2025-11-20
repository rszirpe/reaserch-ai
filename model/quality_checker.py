"""
Quality Checker - Evaluates model performance
Decides when to switch from Gemini to local model
"""
import json
import os

class QualityChecker:
    """Evaluates model output quality"""
    
    def __init__(self, status_file):
        self.status_file = status_file
        self.load_status()
    
    def load_status(self):
        """Load current model status"""
        if os.path.exists(self.status_file):
            with open(self.status_file, 'r') as f:
                self.status = json.load(f)
        else:
            self.status = {
                'state': 'training',
                'total_examples': 0,
                'quality_score': 0.0,
                'grammar_score': 0.0,
                'last_evaluation': None,
                'use_local_model': False,
                'use_grammar_correction': True
            }
            self.save_status()
    
    def save_status(self):
        """Save model status to file"""
        os.makedirs(os.path.dirname(self.status_file), exist_ok=True)
        with open(self.status_file, 'w') as f:
            json.dump(self.status, f, indent=2)
    
    def update_metrics(self, total_examples, quality_score, grammar_score):
        """Update model metrics"""
        self.status['total_examples'] = total_examples
        self.status['quality_score'] = quality_score
        self.status['grammar_score'] = grammar_score
        self.status['last_evaluation'] = str(datetime.now())
        
        # Update state based on scores
        if quality_score >= 0.85 and grammar_score >= 0.90:
            self.status['state'] = 'expert'
            self.status['use_local_model'] = True
            self.status['use_grammar_correction'] = False
        elif quality_score >= 0.85:
            self.status['state'] = 'ready'
            self.status['use_local_model'] = True
            self.status['use_grammar_correction'] = True
        else:
            self.status['state'] = 'training'
            self.status['use_local_model'] = False
            self.status['use_grammar_correction'] = True
        
        self.save_status()
    
    def should_use_local_model(self):
        """Check if local model should be used"""
        return self.status.get('use_local_model', False)
    
    def should_use_grammar_correction(self):
        """Check if grammar correction should be used"""
        return self.status.get('use_grammar_correction', True)
    
    def get_status_display(self, current_total=None):
        """Get status string for UI display"""
        state = self.status['state']
        # Use current_total if provided (for real-time updates)
        total = current_total if current_total is not None else self.status['total_examples']
        quality = self.status['quality_score'] * 100
        grammar = self.status['grammar_score'] * 100
        
        if state == 'training':
            return f"TRAINING: {total} examples | Quality: {quality:.0f}%"
        elif state == 'ready':
            return f"LOCAL AI: Quality {quality:.0f}% ✓"
        elif state == 'expert':
            return f"EXPERT MODE: 100% Independent 🧠"
        
        return "INITIALIZING..."


from datetime import datetime

if __name__ == "__main__":
    checker = QualityChecker("model_status.json")
    print(checker.get_status_display())

