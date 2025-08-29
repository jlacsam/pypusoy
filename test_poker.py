#!/usr/bin/env python3
"""
Test file for the Poker class.
Contains one assert statement test for every method of the Poker class.
"""

import sys
import os

from poker import (Poker, PokerHandInfo, HIGH_CARD, ONE_PAIR, TWO_PAIR,
                   THREE_OF_A_KIND, STRAIGHT, FLUSH, FULL_HOUSE,
                   FOUR_OF_A_KIND, STRAIGHT_FLUSH, ROYAL_FLUSH)
from poker import (HIGH_TRIPLE, PAIR_TRIPLE, THREE_TRIPLE, FLUSH_TRIPLE,
                   STRAIGHT_TRIPLE, STRAIGHT_FLUSH_TRIPLE, ROYAL_FLUSH_TRIPLE)
from poker import LEFT_HAND_WINS, RIGHT_HAND_WINS, HANDS_ARE_EQUAL
from card import Card, CARD_SUIT
from player import PLAYER_TYPE


def test_poker_class():
    """Test all methods of the Poker class with assert statements."""

    # Test __init__
    poker = Poker()
    assert len(poker.players) == 4, "Poker should initialize with 4 players"

    # Test shuffle_deck
    poker.shuffle_deck(seed=42)
    assert poker.deck is not None, "Deck should exist after shuffling"

    # Test distribute_cards
    poker.distribute_cards()
    assert len(poker.packs) == 4, "Should have 4 packs after distribution"
    assert len(poker.packs[0]) == 13, "Each pack should have 13 cards"

    # Test distribute_hands
    poker.distribute_hands()
    assert len(poker.players[0].cards) == 13, "Each player should have 13 cards after distribution"

    # Test give_suit_value_to_player (just verify it doesn't crash)
    poker2 = Poker()
    try:
        poker2.give_suit_value_to_player(0, CARD_SUIT['Spades'], 14)  # Ace of Spades
        give_suit_value_works = True
    except Exception:
        give_suit_value_works = False
    assert give_suit_value_works, "give_suit_value_to_player should execute without error"

    # Test dump_pack (just verify it doesn't crash)
    try:
        poker.dump_pack(0)
        dump_pack_works = True
    except Exception:
        dump_pack_works = False
    assert dump_pack_works, "dump_pack should execute without error"

    # Test dump_player (just verify it doesn't crash)
    try:
        poker.dump_player(0)
        dump_player_works = True
    except Exception:
        dump_player_works = False
    assert dump_player_works, "dump_player should execute without error"

    # Test dump_players (just verify it doesn't crash)
    try:
        poker.dump_players()
        dump_players_works = True
    except Exception:
        dump_players_works = False
    assert dump_players_works, "dump_players should execute without error"

    # Test this_player
    this_player = poker.this_player()
    assert this_player == poker.players[PLAYER_TYPE['You']], "this_player should return the correct player"

    # Test players_ranked_by_score
    ranked_players = poker.players_ranked_by_score()
    assert len(ranked_players) == 4, "Should return all 4 players ranked by score"

    # Test update_player_scores (requires arranged cards)
    try:
        # First arrange cards for all players
        for i in range(4):
            poker.auto_arrange_for_player(i, 'greedy')
        poker.update_player_scores()
        update_scores_works = True
    except Exception:
        update_scores_works = False
    assert update_scores_works, "update_player_scores should execute without error after arranging cards"

    # Test combination (static method)
    result = Poker.combination(5, 2)
    assert result == 10, "C(5,2) should equal 10"

    # Test sort_hand_by_card_id (static method)
    cards = [Card(CARD_SUIT['Hearts'], 10), Card(CARD_SUIT['Spades'], 5)]
    sorted_cards = Poker.sort_hand_by_card_id(cards)
    assert len(sorted_cards) == 2, "Should return sorted hand with same number of cards"

    # Test sort_hand_by_suit (static method)
    sorted_by_suit = Poker.sort_hand_by_suit(cards)
    assert len(sorted_by_suit) == 2, "Should return sorted hand by suit"

    # Test sort_hand_by_value (static method)
    sorted_by_value = Poker.sort_hand_by_value(cards)
    assert len(sorted_by_value) == 2, "Should return sorted hand by value"

    # Test sort_hand_by_alt_value (static method)
    sorted_by_alt_value = Poker.sort_hand_by_alt_value(cards)
    assert len(sorted_by_alt_value) == 2, "Should return sorted hand by alt value"

    # Test extract_poker_hand (static method)
    test_hand = [Card(CARD_SUIT['Hearts'], 10), Card(CARD_SUIT['Hearts'], 11)]
    arranged = []
    result = Poker.extract_poker_hand(HIGH_CARD, test_hand, arranged)
    assert isinstance(result, bool), "extract_poker_hand should return a boolean"

    # Test extract_royal_flush (static method)
    royal_flush_hand = [
        Card(CARD_SUIT['Hearts'], 10),
        Card(CARD_SUIT['Hearts'], 11),
        Card(CARD_SUIT['Hearts'], 12),
        Card(CARD_SUIT['Hearts'], 13),
        Card(CARD_SUIT['Hearts'], 14)
    ]
    arranged = []
    result = Poker.extract_royal_flush(royal_flush_hand.copy(), arranged)
    assert isinstance(result, bool), "extract_royal_flush should return a boolean"

    # Test extract_straight_flush (static method)
    straight_flush_hand = [
        Card(CARD_SUIT['Hearts'], 5),
        Card(CARD_SUIT['Hearts'], 6),
        Card(CARD_SUIT['Hearts'], 7),
        Card(CARD_SUIT['Hearts'], 8),
        Card(CARD_SUIT['Hearts'], 9)
    ]
    arranged = []
    result = Poker.extract_straight_flush(straight_flush_hand.copy(), arranged)
    assert isinstance(result, bool), "extract_straight_flush should return a boolean"

    # Test extract_four_of_a_kind (static method)
    four_kind_hand = [
        Card(CARD_SUIT['Hearts'], 10),
        Card(CARD_SUIT['Spades'], 10),
        Card(CARD_SUIT['Diamonds'], 10),
        Card(CARD_SUIT['Clubs'], 10),
        Card(CARD_SUIT['Hearts'], 5)
    ]
    arranged = []
    result = Poker.extract_four_of_a_kind(four_kind_hand.copy(), arranged)
    assert isinstance(result, bool), "extract_four_of_a_kind should return a boolean"

    # Test extract_full_house (static method)
    full_house_hand = [
        Card(CARD_SUIT['Hearts'], 10),
        Card(CARD_SUIT['Spades'], 10),
        Card(CARD_SUIT['Diamonds'], 10),
        Card(CARD_SUIT['Clubs'], 5),
        Card(CARD_SUIT['Hearts'], 5)
    ]
    arranged = []
    result = Poker.extract_full_house(full_house_hand.copy(), arranged)
    assert isinstance(result, bool), "extract_full_house should return a boolean"

    # Test extract_flush (static method)
    flush_hand = [
        Card(CARD_SUIT['Hearts'], 2),
        Card(CARD_SUIT['Hearts'], 5),
        Card(CARD_SUIT['Hearts'], 8),
        Card(CARD_SUIT['Hearts'], 10),
        Card(CARD_SUIT['Hearts'], 13)
    ]
    arranged = []
    result = Poker.extract_flush(flush_hand.copy(), arranged)
    assert isinstance(result, bool), "extract_flush should return a boolean"

    # Test extract_straight (static method)
    straight_hand = [
        Card(CARD_SUIT['Hearts'], 5),
        Card(CARD_SUIT['Spades'], 6),
        Card(CARD_SUIT['Diamonds'], 7),
        Card(CARD_SUIT['Clubs'], 8),
        Card(CARD_SUIT['Hearts'], 9)
    ]
    arranged = []
    result = Poker.extract_straight(straight_hand.copy(), arranged)
    assert isinstance(result, bool), "extract_straight should return a boolean"

    # Test extract_three_of_a_kind (static method)
    three_kind_hand = [
        Card(CARD_SUIT['Hearts'], 10),
        Card(CARD_SUIT['Spades'], 10),
        Card(CARD_SUIT['Diamonds'], 10),
        Card(CARD_SUIT['Clubs'], 5),
        Card(CARD_SUIT['Hearts'], 7)
    ]
    arranged = []
    result = Poker.extract_three_of_a_kind(three_kind_hand.copy(), arranged)
    assert isinstance(result, bool), "extract_three_of_a_kind should return a boolean"

    # Test extract_two_pair (static method)
    two_pair_hand = [
        Card(CARD_SUIT['Hearts'], 10),
        Card(CARD_SUIT['Spades'], 10),
        Card(CARD_SUIT['Diamonds'], 5),
        Card(CARD_SUIT['Clubs'], 5),
        Card(CARD_SUIT['Hearts'], 7)
    ]
    arranged = []
    result = Poker.extract_two_pair(two_pair_hand.copy(), arranged)
    assert isinstance(result, bool), "extract_two_pair should return a boolean"

    # Test extract_one_pair (static method)
    one_pair_hand = [
        Card(CARD_SUIT['Hearts'], 10),
        Card(CARD_SUIT['Spades'], 10),
        Card(CARD_SUIT['Diamonds'], 5),
        Card(CARD_SUIT['Clubs'], 7),
        Card(CARD_SUIT['Hearts'], 9)
    ]
    arranged = []
    result = Poker.extract_one_pair(one_pair_hand.copy(), arranged)
    assert isinstance(result, bool), "extract_one_pair should return a boolean"

    # Test auto_arrange_for_player
    poker3 = Poker()
    poker3.shuffle_deck(seed=42)
    poker3.distribute_cards()
    poker3.distribute_hands()
    result = poker3.auto_arrange_for_player(0, 'greedy')
    assert isinstance(result, int), "auto_arrange_for_player should return an integer hand type"

    # Test find_best_poker_play (static method)
    test_cards = [Card(CARD_SUIT['Hearts'], i) for i in range(2, 15)]
    arranged = []
    result = Poker.find_best_poker_play(test_cards.copy(), arranged)
    assert isinstance(result, int), "find_best_poker_play should return an integer hand type"

    # Test find_balanced_poker_play (static method)
    test_cards = [Card(CARD_SUIT['Hearts'], i) for i in range(2, 15)]
    arranged = []
    result = Poker.find_balanced_poker_play(test_cards.copy(), arranged)
    assert isinstance(result, int), "find_balanced_poker_play should return an integer hand type"

    # Test is_valid_hand (static method)
    valid_hand = [Card(CARD_SUIT['Hearts'], i) for i in range(2, 15)]
    result = Poker.is_valid_hand(valid_hand)
    assert isinstance(result, bool), "is_valid_hand should return a boolean"

    # Test has_royal_flush (static method)
    royal_flush_test = [
        Card(CARD_SUIT['Hearts'], 10),
        Card(CARD_SUIT['Hearts'], 11),
        Card(CARD_SUIT['Hearts'], 12),
        Card(CARD_SUIT['Hearts'], 13),
        Card(CARD_SUIT['Hearts'], 14)
    ]
    result = Poker.has_royal_flush(royal_flush_test)
    assert isinstance(result, PokerHandInfo), "has_royal_flush should return PokerHandInfo"

    # Test has_straight_flush (static method)
    result = Poker.has_straight_flush(straight_flush_hand)
    assert isinstance(result, PokerHandInfo), "has_straight_flush should return PokerHandInfo"

    # Test has_four_of_a_kind (static method)
    result = Poker.has_four_of_a_kind(four_kind_hand)
    assert isinstance(result, PokerHandInfo), "has_four_of_a_kind should return PokerHandInfo"

    # Test has_full_house (static method)
    result = Poker.has_full_house(full_house_hand)
    assert isinstance(result, PokerHandInfo), "has_full_house should return PokerHandInfo"

    # Test has_flush (static method)
    result = Poker.has_flush(flush_hand)
    assert isinstance(result, PokerHandInfo), "has_flush should return PokerHandInfo"

    # Test has_royal_straight (static method)
    royal_straight_hand = [
        Card(CARD_SUIT['Hearts'], 10),
        Card(CARD_SUIT['Spades'], 11),
        Card(CARD_SUIT['Diamonds'], 12),
        Card(CARD_SUIT['Clubs'], 13),
        Card(CARD_SUIT['Hearts'], 14)
    ]
    result = Poker.has_royal_straight(royal_straight_hand)
    assert isinstance(result, PokerHandInfo), "has_royal_straight should return PokerHandInfo"

    # Test has_straight (static method)
    result = Poker.has_straight(straight_hand)
    assert isinstance(result, PokerHandInfo), "has_straight should return PokerHandInfo"

    # Test has_three_of_a_kind (static method)
    result = Poker.has_three_of_a_kind(three_kind_hand)
    assert isinstance(result, PokerHandInfo), "has_three_of_a_kind should return PokerHandInfo"

    # Test has_two_pair (static method)
    result = Poker.has_two_pair(two_pair_hand)
    assert isinstance(result, PokerHandInfo), "has_two_pair should return PokerHandInfo"

    # Test has_one_pair (static method)
    result = Poker.has_one_pair(one_pair_hand)
    assert isinstance(result, PokerHandInfo), "has_one_pair should return PokerHandInfo"

    # Test has_high_card (static method)
    high_card_hand = [
        Card(CARD_SUIT['Hearts'], 2),
        Card(CARD_SUIT['Spades'], 5),
        Card(CARD_SUIT['Diamonds'], 8),
        Card(CARD_SUIT['Clubs'], 10),
        Card(CARD_SUIT['Hearts'], 13)
    ]
    result = Poker.has_high_card(high_card_hand)
    assert isinstance(result, PokerHandInfo), "has_high_card should return PokerHandInfo"

    # Test get_hand_type_string (static method)
    result = Poker.get_hand_type_string(ROYAL_FLUSH)
    assert isinstance(result, str), "get_hand_type_string should return a string"
    assert result == "Royal flush", "Should return correct hand type string"

    # Test get_hand_type_rating (static method)
    result = Poker.get_hand_type_rating(ROYAL_FLUSH)
    assert isinstance(result, str), "get_hand_type_rating should return a string"

    # Test get_card_value_string (static method)
    result = Poker.get_card_value_string(14, True)
    assert result == "Ace", "Should return 'Ace' for value 14 with long_name=True"

    # Test match_hands (static method)
    hand1_info = PokerHandInfo()
    hand1_info.hand_type = ROYAL_FLUSH
    hand1_info.values = [14, 13, 12, 11, 10]

    hand2_info = PokerHandInfo()
    hand2_info.hand_type = STRAIGHT_FLUSH
    hand2_info.values = [9, 8, 7, 6, 5]

    result = Poker.match_hands(hand1_info, hand2_info)
    assert result == LEFT_HAND_WINS, "Royal flush should beat straight flush"

    # Test match_front_middle (static method)
    front_info = PokerHandInfo()
    front_info.hand_type = HIGH_TRIPLE
    front_info.values = [10, 8, 5, 0, 0]

    middle_info = PokerHandInfo()
    middle_info.hand_type = HIGH_CARD
    middle_info.values = [12, 10, 8, 5, 2]

    result = Poker.match_front_middle(front_info, middle_info)
    assert isinstance(result, int), "match_front_middle should return an integer result"

    # Test analyze_hand (static method)
    result = Poker.analyze_hand(royal_flush_test)
    assert isinstance(result, PokerHandInfo), "analyze_hand should return PokerHandInfo"
    assert result.hand_type == ROYAL_FLUSH, "Should correctly identify royal flush"

    print("All Poker tests passed!")


if __name__ == "__main__":
    test_poker_class()
