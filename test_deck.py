"""
Test file for the Deck class.
Contains one assert statement test for every method of the Deck class,
excluding dump_* methods.
"""

import sys
import os

from deck import Deck, CARDS_PER_DECK, CARDS_PER_SUIT
from card import Card, CARD_SUIT


def test_deck_class():
    """Test all methods of the Deck class with assert statements."""

    # Test __init__
    deck = Deck()
    assert len(deck.deck_of_cards) == CARDS_PER_DECK, "Deck should initialize with 52 cards"
    assert all(isinstance(c, Card) for c in deck.deck_of_cards), "All elements should be Card instances"
    assert all(c.suit != CARD_SUIT["Joker"] for c in deck.deck_of_cards), "Deck should not include Jokers"

    # Test cards_per_deck
    assert deck.cards_per_deck() == CARDS_PER_DECK, "cards_per_deck should return 52"

    # Test sort_by_random_value
    sorted_random = deck.sort_by_random_value()
    assert isinstance(sorted_random, list), "sort_by_random_value should return a list"
    assert all(isinstance(c, Card) for c in sorted_random), "All items should be Card instances"

    # Test sort_by_card_id
    sorted_by_id = deck.sort_by_card_id()
    ids = [c.card_id for c in sorted_by_id]
    assert ids == sorted(ids), "Cards should be sorted in ascending order by card_id"

    # Test sort_by_value
    sorted_by_value = deck.sort_by_value()
    values = [c.value for c in sorted_by_value]
    assert values == sorted(values), "Cards should be sorted in ascending order by value"

    # Test shuffle_deck
    deck.shuffle_deck(seed=42)
    assert len(deck.cards_by_random_value) == CARDS_PER_DECK, "Shuffled deck should still have 52 cards"
    shuffled_ids = [c.card_id for c in deck.cards_by_random_value]
    assert shuffled_ids != ids, "Shuffled deck order should differ from sorted-by-ID order"

    # Test __str__
    deck_str = str(deck)
    assert isinstance(deck_str, str), "__str__ should return a string"
    assert len(deck_str.strip()) > 0, "String representation should not be empty"
    assert all(len(token) >= 2 for token in deck_str.split()), "__str__ should return space-separated card names"

    print("All Deck tests passed!")


if __name__ == "__main__":
    test_deck_class()
