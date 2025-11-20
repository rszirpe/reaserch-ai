"""
Grammar Corrector - Uses Gemini to polish model outputs
"""
import google.generativeai as genai
import config

genai.configure(api_key=config.GEMINI_API_KEY)

class GrammarCorrector:
    """Uses Gemini API to correct grammar and improve sentence structure"""
    
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-2.0-flash')
    
    def correct(self, text):
        """
        Correct grammar and improve clarity of text
        Returns corrected text
        """
        try:
            prompt = f"""You are a grammar correction assistant. Fix any grammar errors, improve sentence structure, and make the text clearer while preserving the original meaning and information.

Original text:
{text}

Return ONLY the corrected text without any explanations or additional comments."""

            response = self.model.generate_content(prompt)
            corrected = response.text.strip()
            
            return corrected
            
        except Exception as e:
            print(f"Grammar correction error: {e}")
            return text  # Return original if correction fails
    
    def evaluate_grammar(self, original, corrected):
        """
        Compare original and corrected text to calculate grammar quality
        Returns score 0-1 (1 = perfect grammar, no corrections needed)
        """
        if original == corrected:
            return 1.0  # Perfect, no corrections needed
        
        # Simple metric: fewer changes = better grammar
        original_words = set(original.lower().split())
        corrected_words = set(corrected.lower().split())
        
        # Calculate similarity
        intersection = original_words & corrected_words
        union = original_words | corrected_words
        
        similarity = len(intersection) / len(union) if union else 0
        
        return similarity


if __name__ == "__main__":
    corrector = GrammarCorrector()
    
    test_text = "AI is very good at doing thing that human do but faster"
    corrected = corrector.correct(test_text)
    
    print(f"Original: {test_text}")
    print(f"Corrected: {corrected}")
    print(f"Quality: {corrector.evaluate_grammar(test_text, corrected)}")

