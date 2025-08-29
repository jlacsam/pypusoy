"""
Deck module for managing a standard 52-card deck.

This module defines the `Deck` class, which represents a standard deck of
cards (excluding Jokers). It provides functionality for creating, shuffling,
sorting, and displaying cards. The deck uses the `Card` class defined in
`card.py`.

Constants
---------
CARDS_PER_DECK : int
    The number of cards in a standard deck (52).
CARDS_PER_SUIT : int
    The number of cards in each suit (13).
"""

from card import CARD_SUIT, Card
import random

CARDS_PER_DECK = 52
CARDS_PER_SUIT = 13


class Deck:
    """
    A standard 52-card deck (excluding Jokers).

    The `Deck` class supports creation, sorting, shuffling, and display
    of cards. Each card is represented by the `Card` class imported
    from `card`.

    Attributes
    ----------
    deck_of_cards : list[Card]
        Full set of cards in the deck.
    cards_by_random_value : list[Card]
        Cards sorted by random value (after shuffling).
    cards_by_card_id : list[Card]
        Cards sorted by unique card ID.
    cards_by_value : list[Card]
        Cards sorted by face value.
    """

    def __init__(self):
        """Initialize a 52-card deck without Jokers."""
        self.deck_of_cards = []
        for key, value in CARD_SUIT.items():
            for i in range(CARDS_PER_SUIT):
                if key != 'Joker':
                    self.deck_of_cards.append(Card(value, i + 1))
        self.cards_by_random_value = []
        self.cards_by_card_id = self.sort_by_card_id()
        self.cards_by_value = self.sort_by_value()

    def cards_per_deck(self):
        """
        Return the number of cards in the deck.

        Returns
        -------
        int
            The total number of cards.
        """
        return len(self.deck_of_cards)

    def sort_by_random_value(self):
        """
        Sort the deck by random value.

        Returns
        -------
        list[Card]
            Cards sorted by their random_value attribute.
        """
        return sorted(self.deck_of_cards, key=lambda x: x.random_value)

    def sort_by_card_id(self):
        """
        Sort the deck by unique card ID.

        Returns
        -------
        list[Card]
            Cards sorted by card_id.
        """
        return sorted(self.deck_of_cards, key=lambda x: x.card_id)

    def sort_by_value(self):
        """
        Sort the deck by card face value.

        Returns
        -------
        list[Card]
            Cards sorted by value.
        """
        return sorted(self.deck_of_cards, key=lambda x: x.value)

    def shuffle_deck(self, seed=None):
        """
        Shuffle the deck randomly.

        Parameters
        ----------
        seed : int, optional
            Random seed number for reproducible shuffling. Defaults to None.

        Side Effects
        ------------
        Updates `self.cards_by_random_value` with a shuffled deck.
        """
        if seed is not None:
            random.seed(seed)
        for card in self.deck_of_cards:
            card.randomize_value()
        self.cards_by_random_value = self.sort_by_random_value()

    def dump_deck(self):
        """Print all cards in the deck."""
        print("Cards in deck:")
        for c in self.deck_of_cards:
            print(f"{c.card_code:3d}:{c.random_value:.6f}:{c.description}")

    def dump_randomized_deck(self):
        """Print cards sorted by random value."""
        print("Cards in randomized deck:")
        for c in self.cards_by_random_value:
            print(f"{c.card_code}:{c.random_value:.6f}:{c.description}")

    def dump_deck_by_card_id(self):
        """Print cards sorted by unique card ID."""
        print("Cards in deck by ID:")
        for c in self.cards_by_card_id:
            print(f"{c.card_code}:{c.random_value:.6f}:{c.description}")

    def dump_deck_by_value(self):
        """Print cards sorted by face value."""
        print("Cards in deck by value:")
        for c in self.cards_by_value:
            print(f"{c.card_code}:{c.random_value:.6f}:{c.description}")

    def __str__(self):
        """
        Return a string representation of the deck.

        Returns
        -------
        str
            Space-separated short names of all cards in the deck.
        """
        return " ".join([c.short_name() for c in self.deck_of_cards])
