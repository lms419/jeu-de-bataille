"""
Utility functions for card handling in the La Bataille (War) card game
"""

def get_card_display(card):
    """
    Returns a more visual representation of a card
    
    Args:
        card: Tuple with (value, suit)
        
    Returns:
        String with pretty card display
    """
    value, suit = card
    
    # Convert suit to symbol
    suit_symbols = {
        "pique": "♠",
        "coeur": "♥",
        "carreau": "♦",
        "trèfle": "♣"
    }
    
    # Use symbol if available, otherwise use the name
    suit_display = suit_symbols.get(suit, suit)
    
    # Format card with value and suit
    return f"{value} {suit_display}"

def get_card_color(suit):
    """
    Returns the color to use for a given suit
    
    Args:
        suit: String with the suit name
        
    Returns:
        String with the color to use ('red' or 'black')
    """
    if suit in ["coeur", "carreau"]:
        return "red"
    return "black"

def get_card_frame(card):
    """
    Returns a frame representation of a card
    
    Args:
        card: Tuple with (value, suit)
        
    Returns:
        tuple: (value, suit_symbol, color) for the card display
    """
    value, suit = card
    
    # Convert value to string if it's not already
    if not isinstance(value, str):
        value = str(value)
    
    # Special case for the Cavalier card in the complement mode
    if value == "C":
        value = "C"  # "Cavalier" represented by "C"
        
    # Get suit symbol
    suit_symbols = {
        "pique": "♠",
        "coeur": "♥",
        "carreau": "♦",
        "trèfle": "♣"
    }
    suit_symbol = suit_symbols.get(suit, suit)
    
    # Get color based on suit
    color = get_card_color(suit)
    
    # Create the card representation
    return value, suit_symbol, color
