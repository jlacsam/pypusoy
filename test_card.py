"""
Test file for the Card class.
Contains one assert statement test for every method of the Card class.
"""

import sys
import os

from card import Card, CARD_SUIT, SUIT_SYMBOL


def test_card_class():
    """Test all methods of the Card class with assert statements."""

    # Test __init__
    card = Card(CARD_SUIT['Spades'], 1)  # Ace of Spades
    assert card.suit == CARD_SUIT['Spades'], "Card suit should be Spades"
    assert card.value == 1, "Card value should be 1 for Ace"
    assert card.label == "A", "Card label should be 'A' for Ace"
    assert card.symbol == SUIT_SYMBOL["Spade"], "Card symbol should match Spade"
    assert card.altvalue == 14, "Ace should map to altvalue 14"

    # Test suit_id
    king_hearts = Card(CARD_SUIT['Hearts'], 13)
    assert king_hearts.suit_id() == "KH", "King of Hearts should return 'KH'"

    # Test suit_name
    five_diamonds = Card(CARD_SUIT['Diamonds'], 5)
    assert five_diamonds.suit_name() == "diamonds", "Suit name should be diamonds"

    # Test joker (static method)
    joker = Card.joker()
    assert joker.suit == CARD_SUIT["Joker"], "Joker suit should match CARD_SUIT['Joker']"
    assert joker.value == 0, "Joker value should be 0"
    assert joker.get_suit_symbol() == "🃏", "Joker should use 🃏 symbol"

    # Test get_suit_symbol for all suits
    spade = Card(CARD_SUIT["Spades"], 2)
    club = Card(CARD_SUIT["Clubs"], 2)
    heart = Card(CARD_SUIT["Hearts"], 2)
    diamond = Card(CARD_SUIT["Diamonds"], 2)
    assert spade.get_suit_symbol() == SUIT_SYMBOL["Spade"], "Symbol should be ♠ for spades"
    assert club.get_suit_symbol() == SUIT_SYMBOL["Club"], "Symbol should be ♣ for clubs"
    assert heart.get_suit_symbol() == SUIT_SYMBOL["Heart"], "Symbol should be ♥ for hearts"
    assert diamond.get_suit_symbol() == SUIT_SYMBOL["Diamond"], "Symbol should be ♦ for diamonds"

    # Test get_card_code for all suits
    ace_spades = Card(CARD_SUIT["Spades"], 1)
    two_clubs = Card(CARD_SUIT["Clubs"], 2)
    three_hearts = Card(CARD_SUIT["Hearts"], 3)
    four_diamonds = Card(CARD_SUIT["Diamonds"], 4)
    assert ace_spades.get_card_code() == ord("A"), "Ace of Spades code should be ord('A')"
    assert two_clubs.get_card_code() == ord("N") + 1, "2 of Clubs code should be ord('N')+1"
    assert three_hearts.get_card_code() == ord("a") + 2, "3 of Hearts code should be ord('a')+2"
    assert four_diamonds.get_card_code() == ord("n") + 3, "4 of Diamonds code should be ord('n')+3"

    # Test get_card_label
    assert Card(CARD_SUIT["Hearts"], 11).get_card_label() == "J", "11 should label as J"
    assert Card(CARD_SUIT["Hearts"], 12).get_card_label() == "Q", "12 should label as Q"
    assert Card(CARD_SUIT["Hearts"], 13).get_card_label() == "K", "13 should label as K"
    assert Card(CARD_SUIT["Hearts"], 9).get_card_label() == "9", "9 should label as '9'"
    assert Card(CARD_SUIT["Hearts"], 20).get_card_label() == "U", "Invalid value should label as 'U'"

    # Test randomize_value (just ensure no crash and valid range)
    c = Card(CARD_SUIT["Clubs"], 3)
    try:
        c.randomize_value()
        random_ok = 0 <= c.random_value <= 1
    except Exception:
        random_ok = False
    assert random_ok, "randomize_value should assign a value between 0 and 1"

    # Test short_name
    ace_spades = Card(CARD_SUIT["Spades"], 1)
    assert ace_spades.short_name() == "A♠", "short_name should be 'A♠'"

    # Test __str__
    king_diamonds = Card(CARD_SUIT["Diamonds"], 13)
    assert str(king_diamonds) == "K♦", "__str__ should return 'K♦'"

    print("All Card tests passed!")


if __name__ == "__main__":
    test_card_class()
