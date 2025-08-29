"""
Card module for representing playing cards.

This module defines a `Card` class and supporting constants for suits,
symbols, and card codes. It provides functionality to create, describe,
and manipulate cards from a standard 52-card deck plus Joker.

Classes
-------
Card
    Represents a playing card with attributes such as suit, value, symbol,
    label, and description.

Constants
---------
SUIT_SYMBOL : dict
    Mapping of suit names to their Unicode symbols.
CARD_SUIT : dict
    Mapping of suit names to integer identifiers.
"""

import random

SUIT_SYMBOL = {
    'Spade': '\u2660',
    'Club': '\u2663',
    'Heart': '\u2665',
    'Diamond': '\u2666'
}

CARD_SUIT = {
    'Spades': 0,
    'Clubs': 1,
    'Hearts': 2,
    'Diamonds': 3,
    'Joker': 4
}


class Card:
    """
    Represents a playing card with attributes such as suit, value, symbol,
    label, and description.

    Attributes
    ----------
    suit : int
        The suit of the card represented as an integer (see CARD_SUIT).
    value : int
        The numeric value of the card (1 = Ace, 11 = Jack, etc.).
    id : str
        The identifier of the card (e.g., 'AS' for Ace of Spades).
    card_id : str
        A formatted string combining suit and value (e.g., 'spades-01').
    card_code : int
        A numeric code representing the card.
    label : str
        A single-character label (e.g., 'A', 'K', 'Q', 'J', '2'–'10').
    symbol : str
        A Unicode symbol representing the card's suit.
    description : str
        A human-readable description of the card.
    altvalue : int
        An alternate numeric value (Ace = 14, others unchanged).
    random_value : float
        A randomly assigned value between 0 and 1.
    """

    def __init__(self, card_suit, card_value):
        """
        Initialize a Card instance.

        Parameters
        ----------
        card_suit : int
            The numeric suit value from CARD_SUIT.
        card_value : int
            The value of the card (1–13, or 0 for Joker).
        """
        self.suit = card_suit
        self.value = card_value
        self.id = self.suit_id()
        self.card_id = f"{self.suit_name()}-{card_value:02d}"
        self.card_code = self.get_card_code()
        self.label = self.get_card_label()
        self.symbol = self.get_suit_symbol()
        self.description = f"{card_value:02d} of {self.suit_name()}"
        self.altvalue = 14 if card_value == 1 else card_value
        self.random_value = 0

    def suit_id(self):
        """
        Return a unique identifier string for the card based on suit and value.

        Returns
        -------
        str or int
            Identifier string (e.g., 'AS', '10H'), or 0 for invalid.
        """
        if self.value == 1:
            prefix = 'A'
        elif self.value == 11:
            prefix = 'J'
        elif self.value == 12:
            prefix = 'Q'
        elif self.value == 13:
            prefix = 'K'
        else:
            prefix = f"{self.value}"

        if self.suit == CARD_SUIT['Spades']:
            return prefix + 'S'
        if self.suit == CARD_SUIT['Clubs']:
            return prefix + 'C'
        if self.suit == CARD_SUIT['Hearts']:
            return prefix + 'H'
        if self.suit == CARD_SUIT['Diamonds']:
            return prefix + 'D'
        return 0

    def suit_name(self):
        """
        Return the name of the suit in lowercase.

        Returns
        -------
        str
            Suit name ('spades', 'clubs', 'hearts', 'diamonds'),
            or 'joker' if invalid.
        """
        for key, value in CARD_SUIT.items():
            if value == self.suit:
                return key.lower()
        return "joker"

    @staticmethod
    def joker():
        """
        Create and return a Joker card.

        Returns
        -------
        Card
            A Card instance representing the Joker.
        """
        return Card(CARD_SUIT['Joker'], 0)

    def get_suit_symbol(self):
        """
        Return the Unicode symbol for the card's suit.

        Returns
        -------
        str
            The suit symbol (e.g., '♠', '♥', '♦', '♣') or '🃏' for Joker.
        """
        for key, value in CARD_SUIT.items():
            if value == self.suit:
                if key == 'Joker':
                    return '🃏'  # Joker symbol
                return SUIT_SYMBOL[key[:-1]]
        return '?'

    def get_card_code(self):
        """
        Return a numeric code for the card based on suit and value.

        Returns
        -------
        int
            Numeric representation of the card.
        """
        if self.suit == CARD_SUIT['Spades']:
            return ord('A') + self.value - 1
        if self.suit == CARD_SUIT['Clubs']:
            return ord('N') + self.value - 1
        if self.suit == CARD_SUIT['Hearts']:
            return ord('a') + self.value - 1
        if self.suit == CARD_SUIT['Diamonds']:
            return ord('n') + self.value - 1

    def get_card_label(self):
        """
        Return a short label for the card value.

        Returns
        -------
        str
            'A' for Ace, '2'–'10' for number cards,
            'J' for Jack, 'Q' for Queen, 'K' for King, 'U' otherwise.
        """
        if self.value == 1:
            return 'A'
        elif self.value <= 10:
            return str(self.value)
        elif self.value == 11:
            return 'J'
        elif self.value == 12:
            return 'Q'
        elif self.value == 13:
            return 'K'
        else:
            return 'U'

    def randomize_value(self):
        """
        Assign a random float between 0 and 1 to the card's random_value.
        """
        self.random_value = random.random()

    def short_name(self):
        """
        Return a short representation of the card.

        Returns
        -------
        str
            Combination of card label and suit symbol (e.g., 'A♠').
        """
        return self.label + self.symbol

    def __str__(self):
        """
        Return the string representation of the card.

        Returns
        -------
        str
            Combination of card label and suit symbol.
        """
        return self.label + self.symbol
