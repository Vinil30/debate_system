import re
import ast

def extract_winner_from_log(filename: str) -> str:
    """
    Extracts the winner from a log file containing a judge's verdict dictionary.
    
    Args:
        filename: Path to the log file (e.g., 'debate.log')
    
    Returns:
        str: 'Scientist', 'Philosopher', or 'Draw' if no clear winner found
    """
    with open(filename, 'r') as file:
        log_content = file.read()
    
    # Find the dictionary pattern in the log file
    dict_pattern = re.compile(r"\{.*?\}", re.DOTALL)
    dict_match = dict_pattern.search(log_content)
    
    if not dict_match:
        return "Draw"  # No dictionary found
    
    try:
        # Safely evaluate the dictionary string
        verdict_dict = ast.literal_eval(dict_match.group(0))
        
        # First try to get the direct winner
        winner = verdict_dict.get('winner', '').capitalize()
        if winner in ['Scientist', 'Philosopher']:
            return winner
        
        # Fallback to text analysis if winner isn't directly specified
        text = verdict_dict.get('summary', '') or verdict_dict.get('reasoning', '')
        text_lower = text.lower()
        
        # Try direct match in text
        match = re.search(r"winner:\s*(scientist|philosopher)", text_lower)
        if match:
            return match.group(1).capitalize()
        
        # Count mentions as final fallback
        scientist_count = text_lower.count('scientist')
        philosopher_count = text_lower.count('philosopher')
        
        if scientist_count > philosopher_count:
            return 'Scientist'
        elif philosopher_count > scientist_count:
            return 'Philosopher'
        
    except (SyntaxError, ValueError):
        pass  # Handle malformed dictionary
    
    return "Draw"

# Usage
winner = extract_winner_from_log('debate.log')
print(f"The winner is: {winner}")