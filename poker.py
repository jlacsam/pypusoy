"""
Poker game implementation for Chinese Poker (Pusoy).

This module contains the core poker game logic including hand analysis,
card distribution, player management, and scoring systems for Chinese Poker.

Classes:
    PokerHandInfo: Contains information about a poker hand including type,
                   strength, and statistics
    Poker: Main game class that manages players, cards, and game logic

Constants:
    Various hand types, game constants, and scoring values
"""

from card import Card, CARD_SUIT
from deck import Deck
from player import Player, PLAYER_TYPE
from poker_stat import *
import random

# Constants
CARDS_ON_HAND = 13
LEFT_HAND_WINS = 1
RIGHT_HAND_WINS = -1
HANDS_ARE_EQUAL = 0
FRONT_HAND = 0
MIDDLE_HAND = 1
BACK_HAND = 2

MIN_CARDS_IN_HAND = 5
MAX_PLAYERS = 4
CARDS_PER_POKER_HAND = 13
CARDS_PER_PACK = 13

# Hand type constants
HIGH_TRIPLE = 1
PAIR_TRIPLE = 2
FLUSH_TRIPLE = 3  # Not used in a game
STRAIGHT_TRIPLE = 4  # Not used in a game
THREE_TRIPLE = 5
STRAIGHT_FLUSH_TRIPLE = 6  # Not used in a game
ROYAL_FLUSH_TRIPLE = 7  # Not used in a game
HIGH_CARD = 8
ONE_PAIR = 9
TWO_PAIR = 10
THREE_OF_A_KIND = 11
STRAIGHT = 12
FLUSH = 13
FULL_HOUSE = 14
FOUR_OF_A_KIND = 15
STRAIGHT_FLUSH = 16
ROYAL_FLUSH = 17
NO_ROYALTY = 32
THREE_FLUSHES = 33
SIX_PAIRS = 34
THREE_STRAIGHTS = 35
THIRTEEN_UNIQUE_CARDS = 36

# Symbol constants (assuming these exist)
STAR_SYMBOL = "★"
HOLLOW_STAR_SYMBOL = "☆"

# Hand type strings
HAND_TYPE_STRING = {
    HIGH_TRIPLE: "High Triple",
    PAIR_TRIPLE: "Pair Triple",
    THREE_TRIPLE: "Three Triple",
    HIGH_CARD: "High Card",
    ONE_PAIR: "One Pair",
    TWO_PAIR: "Two Pair",
    THREE_OF_A_KIND: "Three-Of-A-Kind",
    STRAIGHT: "Straight",
    FLUSH: "Flush",
    FULL_HOUSE: "Full House",
    FOUR_OF_A_KIND: "Four-Of-A-Kind",
    STRAIGHT_FLUSH: "Straight Flush",
    ROYAL_FLUSH: "Royal Flush",
    NO_ROYALTY: "No Royalty",
    THREE_FLUSHES: "Three Flushes",
    SIX_PAIRS: "Six Pairs",
    THREE_STRAIGHTS: "Three Straights",
    THIRTEEN_UNIQUE_CARDS: "Thirteen Unique Cards"
}


class PokerHandInfo:
    """
    Contains detailed information about a poker hand.

    This class stores the analysis results of a poker hand including its type,
    strength relative to other hands, probability statistics, and the values
    of the cards that determine the hand's strength.

    Attributes:
        hand_type (int): The type of poker hand (e.g., ROYAL_FLUSH, PAIR, etc.)
        hands_beaten (int): Number of hands this hand can beat
        probability (float): Probability of getting this hand
        percentile (float): Percentile ranking of this hand
        values (list): List of 5 integers representing the key card values for comparison
    """

    def __init__(self):
        """Initialize a PokerHandInfo object with default values."""
        self.hand_type = None
        self.hands_beaten = 0
        self.probability = 0
        self.percentile = 0
        self.values = [0, 0, 0, 0, 0]


class Poker:
    """
    Main poker game class for Chinese Poker (Pusoy).

    This class manages a complete poker game including deck management,
    card distribution to players, hand analysis, scoring, and game state.
    It supports up to 4 players and handles the complex rules of Chinese Poker
    where each player arranges 13 cards into three hands (front, middle, back).

    Attributes:
        game_no (int): Current game number
        deck (Deck): The deck of cards for the game
        players (list): List of Player objects in the game
        packs (list): List of card packs for distribution to players
    """

    def __init__(self):
        """
        Initialize a new poker game.

        Creates a new deck, initializes 4 players with default names,
        and sets up empty card packs for distribution.
        """
        self.game_no = 0
        self.deck = Deck()
        self.players = []
        self.packs = [[], [], [], []]

        default_names = ["Player1", "Player2", "Player3", "Player4"]
        for i in range(MAX_PLAYERS):
            player = Player()
            player.name = default_names[i]
            player.player_id = i
            self.players.append(player)

    def shuffle_deck(self, seed=None):
        """
        Shuffle the deck of cards.

        Args:
            seed (int, optional): Random seed for reproducible shuffling.
                                If None, uses system time for randomization.
        """
        self.deck.shuffle_deck(seed)

    def distribute_cards(self):
        """
        Distribute cards from the shuffled deck into 4 packs.

        Cards are distributed in round-robin fashion, with each pack
        receiving 13 cards. This prepares the cards for distribution
        to the 4 players.
        """
        self.packs = [[], [], [], []]
        for i, card in enumerate(self.deck.cards_by_random_value):
            self.packs[i % 4].append(card)

    def distribute_hands(self):
        """
        Give each player their pack of 13 cards.

        Distributes the previously created packs to each of the 4 players.
        Each player receives exactly 13 cards to arrange into their hands.
        """
        for i in range(MAX_PLAYERS):
            self.players[i].receive_pack(self.packs[i])

    def give_suit_value_to_player(self, player_no, suit, value):
        """
        Give a specific card to a specific player.

        Searches through the deck for a card with the specified suit and value,
        then gives it to the specified player. Used for testing or special
        game scenarios.

        Args:
            player_no (int): Index of the player (0-3)
            suit (int): Suit of the card (from CARD_SUIT constants)
            value (int): Value of the card (1-14, where 1 and 14 are Aces)
        """
        for card in self.deck.deck_of_cards:
            if card.suit == suit and card.value == value:
                self.players[player_no].receive_card(card)

    def dump_pack(self, pack_no):
        """
        Print all cards in a specific pack to console.

        Debugging utility that displays all cards in the specified pack
        with their descriptions.

        Args:
            pack_no (int): Index of the pack to display (0-3)
        """
        print(f"Pack {pack_no} dump:")
        for card in self.packs[pack_no]:
            print(card.description)

    def dump_player(self, player_no):
        """
        Print all cards held by a specific player to console.

        Debugging utility that displays all cards currently held by
        the specified player.

        Args:
            player_no (int): Index of the player (0-3)
        """
        print(f"Player {player_no} dump:")
        for card in self.players[player_no].cards:
            print(card.description)

    def dump_players(self):
        """
        Print all cards for all players to console.

        Debugging utility that calls each player's dump_cards method
        to display their current hands.
        """
        for player in self.players:
            player.dump_cards()

    def this_player(self):
        """
        Get the human player object.

        Returns:
            Player: The player object representing the human player
        """
        return self.players[PLAYER_TYPE['You']]

    def players_ranked_by_score(self):
        """
        Get players sorted by their game performance.

        Sorts players by whether they folded, their total score,
        and their best hand strength.

        Returns:
            list: List of Player objects sorted by performance
        """
        sorted_players = self.players.copy()
        sorted_players.sort(key=lambda player: (
            player.did_fold,
            player.score,
            player.best_hand
        ))
        return sorted_players

    def update_player_scores(self):
        """
        Calculate and update scores for all players.

        Compares each player's three hands (front, middle, back) against
        every other player's corresponding hands. Awards points for wins
        and deducts points for losses. Also tracks the best hand percentile
        for ranking purposes.
        """
        for i, player in enumerate(self.players):
            hand_scores = [0, 0, 0]
            player.score = 0
            player.reset_hand_scores()

            for j, opponent in enumerate(self.players):
                if player.player_id != opponent.player_id:
                    for k in range(3):
                        from_index = 0 if k == 0 else (3 if k == 1 else 8)
                        to_index = 3 if k == 0 else (8 if k == 1 else 13)

                        player_hand = player.arranged_cards[from_index:to_index]
                        player_hand_info = Poker.analyze_hand(player_hand)

                        opponent_hand = opponent.arranged_cards[from_index:to_index]
                        opponent_hand_info = Poker.analyze_hand(opponent_hand)

                        result = Poker.match_hands(player_hand_info, opponent_hand_info)

                        if result == 1:
                            hand_scores[k] += 1
                            player.score += 1
                        elif result == -1:
                            hand_scores[k] -= 1
                            player.score -= 1

                        if k == 2:
                            player.best_hand = player_hand_info.percentile

                        player.raw_scores[j][k] = result

            player.set_hand_score_at_index(hand_scores[0], 0)
            player.set_hand_score_at_index(hand_scores[1], 1)
            player.set_hand_score_at_index(hand_scores[2], 2)

    @staticmethod
    def combination(n, k):
        """
        Calculate binomial coefficient (n choose k).

        Computes the number of ways to choose k items from n items
        without regard to order.

        Args:
            n (int): Total number of items
            k (int): Number of items to choose

        Returns:
            int: The binomial coefficient, or 0 if k > n
        """
        if k > n:
            return 0
        else:
            r = 1
            for d in range(1, k + 1):
                r *= n
                n -= 1
                r //= d
            return r

    @staticmethod
    def sort_hand_by_card_id(hand):
        """
        Sort a hand of cards by their card ID.

        Args:
            hand (list): List of Card objects

        Returns:
            list: New list of cards sorted by card_id
        """
        return sorted(hand, key=lambda card: card.card_id)

    @staticmethod
    def sort_hand_by_suit(hand):
        """
        Sort a hand of cards by suit, then by value.

        Args:
            hand (list): List of Card objects

        Returns:
            list: New list of cards sorted by suit and value
        """
        return sorted(hand, key=lambda card: (card.suit, card.altvalue))

    @staticmethod
    def sort_hand_by_value(hand):
        """
        Sort a hand of cards by their face value.

        Args:
            hand (list): List of Card objects

        Returns:
            list: New list of cards sorted by value
        """
        return sorted(hand, key=lambda card: card.value)

    @staticmethod
    def sort_hand_by_alt_value(hand):
        """
        Sort a hand of cards by their alternative value.

        Alternative value treats Aces as high (14) instead of low (1).

        Args:
            hand (list): List of Card objects

        Returns:
            list: New list of cards sorted by alternative value
        """
        return sorted(hand, key=lambda card: card.altvalue)

    @staticmethod
    def extract_poker_hand(hand_type, hand, arranged):
        """
        Extract a specific type of poker hand from available cards.

        Attempts to find and extract cards that form the specified poker hand type.
        If found, removes those cards from the hand and adds them to arranged.

        Args:
            hand_type (int): Type of poker hand to extract (e.g., ROYAL_FLUSH)
            hand (list): List of available Card objects (modified in place)
            arranged (list): List to add extracted cards to (modified in place)

        Returns:
            bool: True if the hand type was found and extracted, False otherwise
        """
        if hand_type == ROYAL_FLUSH:
            return Poker.extract_royal_flush(hand, arranged)
        elif hand_type == STRAIGHT_FLUSH:
            return Poker.extract_straight_flush(hand, arranged)
        elif hand_type == FOUR_OF_A_KIND:
            return Poker.extract_four_of_a_kind(hand, arranged)
        elif hand_type == FULL_HOUSE:
            return Poker.extract_full_house(hand, arranged)
        elif hand_type == FLUSH:
            return Poker.extract_flush(hand, arranged)
        elif hand_type == STRAIGHT:
            return Poker.extract_straight(hand, arranged)
        elif hand_type == THREE_OF_A_KIND:
            return Poker.extract_three_of_a_kind(hand, arranged)
        elif hand_type == TWO_PAIR:
            return Poker.extract_two_pair(hand, arranged)
        elif hand_type == ONE_PAIR:
            return Poker.extract_one_pair(hand, arranged)
        else:  # HIGH_CARD
            return True

    @staticmethod
    def extract_royal_flush(hand, arranged):
        """
        Extract a royal flush from the hand if present.

        A royal flush is A-K-Q-J-10 all of the same suit.

        Args:
            hand (list): List of Card objects (modified in place)
            arranged (list): List to add extracted cards to (modified in place)

        Returns:
            bool: True if royal flush found and extracted, False otherwise
        """
        if len(hand) < 5:
            return False

        sorted_hand = Poker.sort_hand_by_suit(hand)

        for i in range(0, len(sorted_hand) - 4):
            card1 = sorted_hand[i]
            card2 = sorted_hand[i + 1]
            card3 = sorted_hand[i + 2]
            card4 = sorted_hand[i + 3]
            card5 = sorted_hand[i + 4]

            if ((card1.altvalue + 1) == card2.altvalue and
                    (card2.altvalue + 1) == card3.altvalue and
                    (card3.altvalue + 1) == card4.altvalue and
                    (card4.altvalue + 1) == card5.altvalue and
                    card1.suit == card2.suit == card3.suit == card4.suit == card5.suit):

                arranged.extend([card5, card4, card3, card2, card1])

                hand.remove(card5)
                hand.remove(card4)
                hand.remove(card3)
                hand.remove(card2)
                hand.remove(card1)

                return True

        return False

    @staticmethod
    def extract_straight_flush(hand, arranged):
        """
        Extract a straight flush from the hand if present.

        A straight flush is five consecutive cards all of the same suit.

        Args:
            hand (list): List of Card objects (modified in place)
            arranged (list): List to add extracted cards to (modified in place)

        Returns:
            bool: True if straight flush found and extracted, False otherwise
        """
        if len(hand) < 5:
            return False

        sorted_hand = Poker.sort_hand_by_card_id(hand)

        for i in range(0, len(sorted_hand) - 4):
            card1 = sorted_hand[i]
            card2 = sorted_hand[i + 1]
            card3 = sorted_hand[i + 2]
            card4 = sorted_hand[i + 3]
            card5 = sorted_hand[i + 4]

            if ((card1.value + 1) == card2.value and
                    (card2.value + 1) == card3.value and
                    (card3.value + 1) == card4.value and
                    (card4.value + 1) == card5.value and
                    card1.suit == card2.suit == card3.suit == card4.suit == card5.suit):

                arranged.extend([card5, card4, card3, card2, card1])

                hand.remove(card5)
                hand.remove(card4)
                hand.remove(card3)
                hand.remove(card2)
                hand.remove(card1)

                return True

        return False

    @staticmethod
    def extract_four_of_a_kind(hand, arranged):
        """
        Extract four of a kind from the hand if present.

        Four of a kind is four cards of the same rank.

        Args:
            hand (list): List of Card objects (modified in place)
            arranged (list): List to add extracted cards to (modified in place)

        Returns:
            bool: True if four of a kind found and extracted, False otherwise
        """
        if len(hand) < 5:
            return False

        joker = Card.joker()
        sorted_hand = Poker.sort_hand_by_alt_value(hand)

        for i in range(len(sorted_hand) - 4, -1, -1):
            card1 = sorted_hand[i]
            card2 = sorted_hand[i + 1]
            card3 = sorted_hand[i + 2]
            card4 = sorted_hand[i + 3]

            if (card1.value == card2.value == card3.value == card4.value):
                arranged.extend([joker, card4, card3, card2, card1])

                hand.remove(card4)
                hand.remove(card3)
                hand.remove(card2)
                hand.remove(card1)

                return True

        return False

    @staticmethod
    def extract_full_house(hand, arranged):
        """
        Extract a full house from the hand if present.

        A full house is three cards of one rank and two cards of another rank.

        Args:
            hand (list): List of Card objects (modified in place)
            arranged (list): List to add extracted cards to (modified in place)

        Returns:
            bool: True if full house found and extracted, False otherwise
        """
        if len(hand) < 5:
            return False

        sorted_hand = Poker.sort_hand_by_alt_value(hand)

        # Start from the highest possible triple
        for i in range(len(sorted_hand) - 3, -1, -1):
            card1 = sorted_hand[i]
            card2 = sorted_hand[i + 1]
            card3 = sorted_hand[i + 2]

            if card1.altvalue == card2.altvalue == card3.altvalue:
                # Start from the lowest possible pair
                for j in range(0, len(sorted_hand) - 1):
                    if j > (i + 2) or (j + 1) < i:
                        if j < len(sorted_hand) - 1:
                            card4 = sorted_hand[j]
                            card5 = sorted_hand[j + 1]

                            if card4.altvalue == card5.altvalue:
                                arranged.extend([card5, card4, card3, card2, card1])

                                hand.remove(card5)
                                hand.remove(card4)
                                hand.remove(card3)
                                hand.remove(card2)
                                hand.remove(card1)

                                return True
        return False

    @staticmethod
    def extract_flush(hand, arranged):
        """
        Extract a flush from the hand if present.

        A flush is five cards all of the same suit, not in sequence.

        Args:
            hand (list): List of Card objects (modified in place)
            arranged (list): List to add extracted cards to (modified in place)

        Returns:
            bool: True if flush found and extracted, False otherwise
        """
        if len(hand) < 5:
            return False

        sorted_hand = Poker.sort_hand_by_suit(hand)

        for i in range(len(sorted_hand) - 5, -1, -1):
            card1 = sorted_hand[i]
            card2 = sorted_hand[i + 1]
            card3 = sorted_hand[i + 2]
            card4 = sorted_hand[i + 3]
            card5 = sorted_hand[i + 4]

            if (card1.suit == card2.suit == card3.suit == card4.suit == card5.suit):

                # Check if the remaining cards can still form a flush
                if i > 4:
                    for j in range(i - 5, -1, -1):
                        card1_1 = sorted_hand[j]
                        card2_1 = sorted_hand[j + 1]
                        card3_1 = sorted_hand[j + 2]
                        card4_1 = sorted_hand[j + 3]
                        card5_1 = sorted_hand[j + 4]

                        if (card1_1.suit == card2_1.suit == card3_1.suit == card4_1.suit == card5_1.suit):

                            if card5.altvalue >= card5_1.altvalue:
                                arranged.extend([card5, card4, card3, card2, card1])
                                hand.remove(card5)
                                hand.remove(card4)
                                hand.remove(card3)
                                hand.remove(card2)
                                hand.remove(card1)
                                return True

                            else:
                                arranged.extend([card5_1, card4_1, card3_1, card2_1, card1_1])
                                hand.remove(card5_1)
                                hand.remove(card4_1)
                                hand.remove(card3_1)
                                hand.remove(card2_1)
                                hand.remove(card1_1)
                                return True

                    arranged.extend([card5, card4, card3, card2, card1])
                    hand.remove(card5)
                    hand.remove(card4)
                    hand.remove(card3)
                    hand.remove(card2)
                    hand.remove(card1)
                    return True

                else:
                    arranged.extend([card5, card4, card3, card2, card1])
                    hand.remove(card5)
                    hand.remove(card4)
                    hand.remove(card3)
                    hand.remove(card2)
                    hand.remove(card1)
                    return True

        return False

    @staticmethod
    def extract_straight(hand, arranged):
        """
        Extract a straight from the hand if present.

        A straight is five consecutive cards of mixed suits.

        Args:
            hand (list): List of Card objects (modified in place)
            arranged (list): List to add extracted cards to (modified in place)

        Returns:
            bool: True if straight found and extracted, False otherwise
        """
        if len(hand) < 5:
            return False

        sorted_hand = Poker.sort_hand_by_value(hand)

        for i in range(len(sorted_hand) - 5, -1, -1):
            for j in range(len(sorted_hand) - 4, i, -1):
                for k in range(len(sorted_hand) - 3, j, -1):
                    for m in range(len(sorted_hand) - 2, k, -1):
                        for n in range(len(sorted_hand) - 1, m, -1):
                            if n < len(sorted_hand):
                                card1 = sorted_hand[i]
                                card2 = sorted_hand[j]
                                card3 = sorted_hand[k]
                                card4 = sorted_hand[m]
                                card5 = sorted_hand[n]

                                if ((card1.value + 1) == card2.value and
                                        (card2.value + 1) == card3.value and
                                        (card3.value + 1) == card4.value and
                                        (card4.value + 1) == card5.value):

                                    arranged.extend([card5, card4, card3, card2, card1])

                                    hand.remove(card5)
                                    hand.remove(card4)
                                    hand.remove(card3)
                                    hand.remove(card2)
                                    hand.remove(card1)

                                    return True
        return False

    @staticmethod
    def extract_three_of_a_kind(hand, arranged):
        """
        Extract three of a kind from the hand if present.

        Three of a kind is three cards of the same rank.

        Args:
            hand (list): List of Card objects (modified in place)
            arranged (list): List to add extracted cards to (modified in place)

        Returns:
            bool: True if three of a kind found and extracted, False otherwise
        """
        if len(hand) < 5:
            return False

        joker = Card.joker()
        sorted_hand = Poker.sort_hand_by_alt_value(hand)

        for i in range(len(sorted_hand) - 3, -1, -1):
            card1 = sorted_hand[i]
            card2 = sorted_hand[i + 1]
            card3 = sorted_hand[i + 2]

            if card1.value == card2.value == card3.value:
                arranged.extend([joker, joker, card3, card2, card1])

                hand.remove(card3)
                hand.remove(card2)
                hand.remove(card1)

                return True

        return False

    @staticmethod
    def extract_two_pair(hand, arranged):
        """
        Extract two pair from the hand if present.

        Two pair is two cards of one rank and two cards of another rank.

        Args:
            hand (list): List of Card objects (modified in place)
            arranged (list): List to add extracted cards to (modified in place)

        Returns:
            bool: True if two pair found and extracted, False otherwise
        """
        if len(hand) < 5:
            return False

        joker = Card.joker()
        sorted_hand = Poker.sort_hand_by_alt_value(hand)

        # Start from the highest possible pair
        for i in range(len(sorted_hand) - 2, -1, -1):
            card1 = sorted_hand[i]
            card2 = sorted_hand[i + 1]

            if card1.value == card2.value:
                # Start from the lowest possible pair
                for j in range(0, len(sorted_hand) - 2):
                    if j > i + 1 or j + 1 < i:
                        if j < len(sorted_hand) - 1:
                            card3 = sorted_hand[j]
                            card4 = sorted_hand[j + 1]

                            if card3.value == card4.value:
                                arranged.extend([joker, card1, card2, card3, card4])

                                hand.remove(card1)
                                hand.remove(card2)
                                hand.remove(card3)
                                hand.remove(card4)

                                return True
        return False

    @staticmethod
    def extract_one_pair(hand, arranged):
        """
        Extract one pair from the hand if present.

        One pair is two cards of the same rank.

        Args:
            hand (list): List of Card objects (modified in place)
            arranged (list): List to add extracted cards to (modified in place)

        Returns:
            bool: True if one pair found and extracted, False otherwise
        """
        if len(hand) < 5:
            return False

        joker = Card.joker()
        sorted_hand = Poker.sort_hand_by_alt_value(hand)

        for i in range(len(sorted_hand) - 2, -1, -1):
            card1 = sorted_hand[i]
            card2 = sorted_hand[i + 1]

            if card1.value == card2.value:
                arranged.extend([joker, joker, joker, card2, card1])

                hand.remove(card2)
                hand.remove(card1)

                return True

        return False

    def auto_arrange_for_player(self, player_no, algo='greedy'):
        """
        Automatically arrange a player's 13 cards into optimal hands.

        Uses the specified algorithm to arrange the player's cards into
        front (3 cards), middle (5 cards), and back (5 cards) hands
        according to Chinese Poker rules.

        Args:
            player_no (int): Index of the player (0-3)
            algo (str): Algorithm to use ('greedy' or 'balanced')

        Returns:
            int: The strength of the best hand found
        """
        player = self.players[player_no]
        if algo == 'balanced':
            return Poker.find_balanced_poker_play(player.cards, player.arranged_cards)
        elif algo == 'greedy':
            return Poker.find_best_poker_play(player.cards, player.arranged_cards)
        else:
            return Poker.find_best_poker_play(player.cards, player.arranged_cards)

    @staticmethod
    def find_best_poker_play(hand, arranged, start_from=ROYAL_FLUSH):
        """
        Find the best poker play using a greedy algorithm.

        This algorithm works as follows:
        1. Find the highest possible 5-card poker hand from the available set of cards.
        2. From the remaining cards, find the next highest possible 5-card poker hand.
        3. Whatever is left becomes the front hand.

        Args:
            hand (list): List of 13 Card objects (modified in place)
            arranged (list): List to store the arranged cards (modified in place)
            start_from (int): Highest hand type to start searching from

        Returns:
            int: The type of the best hand found
        """
        hand_type = [HIGH_CARD, HIGH_CARD]
        temp_hand_type = [HIGH_CARD, HIGH_CARD]
        best_hand = HIGH_CARD

        for i in range(start_from, HIGH_CARD, -1):
            mutable_hand = Poker.sort_hand_by_value(hand.copy())
            arranged_hand = []
            hand_type_index = i
            index = 0

            while index < 2 and hand_type_index > HIGH_CARD:
                if Poker.extract_poker_hand(hand_type_index, mutable_hand, arranged_hand):
                    temp_hand_type[index] = hand_type_index
                    index += 1
                hand_type_index -= 1

            if temp_hand_type[0] > HIGH_CARD or temp_hand_type[1] > HIGH_CARD:
                # Both are better than a high card
                if temp_hand_type[0] > hand_type[0]:
                    best_hand = temp_hand_type[0]
                    hand_type[0] = temp_hand_type[0]
                    hand_type[1] = temp_hand_type[1]
                    arranged[:] = arranged_hand[:]
                    hand[:] = mutable_hand[:]

            elif temp_hand_type[0] > HIGH_CARD:
                # Only one is better than a high card
                if temp_hand_type[0] > hand_type[0] and hand_type[1] == HIGH_CARD:
                    best_hand = temp_hand_type[0]
                    hand_type[0] = temp_hand_type[0]
                    hand_type[1] = temp_hand_type[1]
                    arranged[:] = arranged_hand[:]
                    hand[:] = mutable_hand[:]

        # Replace the jokers with the remaining cards, start from the lowest
        for i in range(len(arranged)):
            each_card = arranged[i]
            if each_card.suit == CARD_SUIT['Joker']:
                arranged[i] = hand[0]
                hand.pop(0)

        # Swap the first and last cards so that the middle gets the highest
        # value card in case both middle and front are HIGH CARDS.
        if len(hand) > 0:
            if hand[0].altvalue != 14:  # Only if the first card is not an Ace!
                hand[0], hand[-1] = hand[-1], hand[0]

        # Transfer remaining cards to arranged, then reverse order
        arranged.extend(hand)
        arranged.reverse()
        hand.clear()

        return best_hand

    @staticmethod
    def find_balanced_poker_play(hand, arranged):
        """
        Find a balanced poker play using a defensive strategy.

        This method starts with the greedy method and then explores other poker plays
        that may have a weaker back hand, but potentially stronger middle and front hands
        without compromising the front <= middle <= back rule.
        This method is more defensive than the greedy algorithm.

        Args:
            hand (list): List of 13 Card objects
            arranged (list): List to store the arranged cards (modified in place)

        Returns:
            int: The type of the best hand found
        """
        poker_plays = []
        current_best = HIGH_CARD
        i = ROYAL_FLUSH
        while i > HIGH_CARD:
            cards = hand.copy()
            arranged_cards = []

            # Find the best possible hand that is equal or higher than i
            # using the greedy algorithm
            best_hand = Poker.find_best_poker_play(cards, arranged_cards, i)

            if not Poker.is_valid_hand(arranged_cards):
                i = best_hand - 1
                continue

            # If we found a good hand, store it.
            if best_hand > HIGH_CARD and best_hand != current_best:
                poker_plays.append({'best_hand': best_hand, 'hand': arranged_cards})
                current_best = best_hand
                i = best_hand - 1
            else:
                # No better hand was found
                break

        # Evaluate the poker plays that were found
        best_play = -1
        best_score = 0
        best_hand = HIGH_CARD
        current_score = 0

        for i, play in enumerate(poker_plays):

            # Analyze each hand
            front_info = Poker.analyze_hand(play['hand'][0:3])
            middle_info = Poker.analyze_hand(play['hand'][3:8])
            back_info = Poker.analyze_hand(play['hand'][8:13])

            # Calculate weighted score
            current_score = (
                3 * front_info.hand_type +
                5 * middle_info.hand_type +
                5 * back_info.hand_type
            ) / 13.0

            # Keep track of best poker play
            if current_score > best_score:
                best_play = i
                best_score = current_score
                best_hand = play['best_hand']

        arranged.extend(poker_plays[best_play]['hand'])

        return best_hand

    @staticmethod
    def is_valid_hand(hand):
        """
        Check if a 13-card arrangement is valid according to Chinese Poker rules.

        In Chinese Poker, the back hand must be stronger than or equal to the middle hand,
        and the middle hand must be stronger than or equal to the front hand.

        Args:
            hand (list): List of 13 arranged Card objects

        Returns:
            bool: True if the hand arrangement is valid, False otherwise
        """
        if hand is None or len(hand) < CARDS_ON_HAND:
            return False

        front_hand = hand[0:3]
        front_hand_info = Poker.analyze_hand(front_hand)

        middle_hand = hand[3:8]
        middle_hand_info = Poker.analyze_hand(middle_hand)

        back_hand = hand[8:13]
        back_hand_info = Poker.analyze_hand(back_hand)

        if Poker.match_hands(middle_hand_info, back_hand_info) == LEFT_HAND_WINS:
            return False

        if Poker.match_front_middle(front_hand_info, middle_hand_info) == LEFT_HAND_WINS:
            return False

        return True

    @staticmethod
    def has_royal_flush(hand):
        """
        Check if the hand contains a royal flush and return detailed information.

        A royal flush is A-K-Q-J-10 all of the same suit. For 3-card hands,
        it checks for Q-K-A of the same suit.

        Args:
            hand (list): List of Card objects to analyze

        Returns:
            PokerHandInfo: Information about the royal flush, or empty info if not found
        """
        poker_hand_info = PokerHandInfo()

        if len(hand) < MIN_CARDS_IN_HAND:
            return poker_hand_info

        sorted_hand = Poker.sort_hand_by_alt_value(hand)

        if len(hand) == 3:
            card1, card2, card3 = sorted_hand[0], sorted_hand[1], sorted_hand[2]

            if (card2.altvalue - card1.altvalue == 1 and card2.suit == card1.suit and
                    card3.altvalue - card2.altvalue == 1 and card3.suit == card2.suit and
                    card1.altvalue == 12):

                poker_hand_info.hands_beaten = ROYAL_FLUSH_TRIPLE_BEATS
                poker_hand_info.hand_type = ROYAL_FLUSH_TRIPLE
                poker_hand_info.percentile = poker_hand_info.hands_beaten / ALL_TRIPLES
                poker_hand_info.frequency = ROYAL_FLUSH_TRIPLES
                poker_hand_info.probability = ROYAL_FLUSH_TRIPLE_PROB
                poker_hand_info.values[0] = card3.altvalue

                return poker_hand_info
            else:
                return poker_hand_info

        card1, card2, card3, card4, card5 = sorted_hand[0:5]

        if (card2.altvalue - card1.altvalue == 1 and card2.suit == card1.suit and
                card3.altvalue - card2.altvalue == 1 and card3.suit == card2.suit and
                card4.altvalue - card3.altvalue == 1 and card4.suit == card3.suit and
                card5.altvalue - card4.altvalue == 1 and card5.suit == card4.suit and
                card1.altvalue == 10):

            poker_hand_info.hands_beaten = ROYAL_FLUSH_BEATS
        else:
            return poker_hand_info

        poker_hand_info.hand_type = ROYAL_FLUSH
        poker_hand_info.percentile = poker_hand_info.hands_beaten / ALL_POKER_HANDS
        poker_hand_info.frequency = ROYAL_FLUSH_HANDS
        poker_hand_info.probability = ROYAL_FLUSH_PROBABILITY
        poker_hand_info.values[0] = card5.altvalue

        return poker_hand_info

    @staticmethod
    def has_straight_flush(hand):
        """
        Check if the hand contains a straight flush and return detailed information.

        A straight flush is five consecutive cards all of the same suit.
        For 3-card hands, it checks for three consecutive cards of the same suit.

        Args:
            hand (list): List of Card objects to analyze

        Returns:
            PokerHandInfo: Information about the straight flush, or empty info if not found
        """
        poker_hand_info = PokerHandInfo()

        if len(hand) < MIN_CARDS_IN_HAND:
            return poker_hand_info

        sorted_hand = Poker.sort_hand_by_value(hand)

        if len(hand) == 3:
            card1, card2, card3 = sorted_hand[0], sorted_hand[1], sorted_hand[2]

            if (card2.value - card1.value == 1 and card2.suit == card1.suit and
                    card3.value - card2.value == 1 and card3.suit == card2.suit):

                poker_hand_info.hands_beaten = (
                    STRAIGHT_FLUSH_TRIPLE_BEATS + 4 * (card3.value - 3)
                )
                poker_hand_info.hand_type = STRAIGHT_FLUSH_TRIPLE
                poker_hand_info.percentile = poker_hand_info.hands_beaten / ALL_TRIPLES
                poker_hand_info.frequency = STRAIGHT_FLUSH_TRIPLES
                poker_hand_info.probability = STRAIGHT_FLUSH_TRIPLE_PROB
                poker_hand_info.values[0] = card3.value

                return poker_hand_info
            else:
                return poker_hand_info

        card1, card2, card3, card4, card5 = sorted_hand[0:5]

        if (card2.value - card1.value == 1 and card2.suit == card1.suit and
                card3.value - card2.value == 1 and card3.suit == card2.suit and
                card4.value - card3.value == 1 and card4.suit == card3.suit and
                card5.value - card4.value == 1 and card5.suit == card4.suit):

            poker_hand_info.hands_beaten = STRAIGHT_FLUSH_BEATS + 4 * (card5.value - 5)
        else:
            return poker_hand_info

        poker_hand_info.hand_type = STRAIGHT_FLUSH
        poker_hand_info.percentile = poker_hand_info.hands_beaten / ALL_POKER_HANDS
        poker_hand_info.frequency = STRAIGHT_FLUSH_HANDS
        poker_hand_info.probability = STRAIGHT_FLUSH_PROBABILITY
        poker_hand_info.values[0] = card5.value

        return poker_hand_info

    @staticmethod
    def has_four_of_a_kind(hand):
        """
        Check if the hand contains four of a kind and return detailed information.

        Four of a kind is four cards of the same rank.

        Args:
            hand (list): List of Card objects to analyze

        Returns:
            PokerHandInfo: Information about the four of a kind, or empty info if not found
        """
        poker_hand_info = PokerHandInfo()

        if len(hand) < 5:
            return poker_hand_info

        sorted_hand = Poker.sort_hand_by_alt_value(hand)
        card1, card2, card3, card4, card5 = sorted_hand[0:5]

        if card1.altvalue == card2.altvalue == card3.altvalue == card4.altvalue:
            poker_hand_info.hands_beaten = FOUR_OF_A_KIND_BEATS + 48 * (card1.altvalue - 2)
            poker_hand_info.values[0] = card1.altvalue
        elif card2.altvalue == card3.altvalue == card4.altvalue == card5.altvalue:
            poker_hand_info.hands_beaten = FOUR_OF_A_KIND_BEATS + 48 * (card2.altvalue - 2)
            poker_hand_info.values[0] = card2.altvalue
        else:
            return poker_hand_info

        poker_hand_info.hand_type = FOUR_OF_A_KIND
        poker_hand_info.percentile = poker_hand_info.hands_beaten / ALL_POKER_HANDS
        poker_hand_info.frequency = FOUR_OF_A_KIND_HANDS
        poker_hand_info.probability = FOUR_OF_A_KIND_PROBABILITY

        return poker_hand_info

    @staticmethod
    def has_full_house(hand):
        """
        Check if the hand contains a full house and return detailed information.

        A full house is three cards of one rank and two cards of another rank.

        Args:
            hand (list): List of Card objects to analyze

        Returns:
            PokerHandInfo: Information about the full house, or empty info if not found
        """
        poker_hand_info = PokerHandInfo()

        if len(hand) < 5:
            return poker_hand_info

        sorted_hand = Poker.sort_hand_by_alt_value(hand)
        card1, card2, card3, card4, card5 = sorted_hand[0:5]

        if (card1.altvalue == card2.altvalue == card3.altvalue and
                card4.altvalue == card5.altvalue and
                card1.suit != CARD_SUIT['Joker'] and card4.suit != CARD_SUIT['Joker']):

            poker_hand_info.hands_beaten = FULL_HOUSE_BEATS + 72 * (card1.altvalue - 2)
            poker_hand_info.values[0] = card1.altvalue
            poker_hand_info.values[1] = card4.altvalue

        elif (card1.altvalue == card2.altvalue and
              card3.altvalue == card4.altvalue == card5.altvalue and
              card1.suit != CARD_SUIT['Joker'] and card3.suit != CARD_SUIT['Joker']):

            poker_hand_info.hands_beaten = FULL_HOUSE_BEATS + 72 * (card3.altvalue - 2)
            poker_hand_info.values[0] = card3.altvalue
            poker_hand_info.values[1] = card1.altvalue
        else:
            return poker_hand_info

        poker_hand_info.hand_type = FULL_HOUSE
        poker_hand_info.percentile = poker_hand_info.hands_beaten / ALL_POKER_HANDS
        poker_hand_info.frequency = FULL_HOUSE_HANDS
        poker_hand_info.probability = FULL_HOUSE_PROBABILITY

        return poker_hand_info

    @staticmethod
    def has_flush(hand):
        """
        Check if the hand contains a flush and return detailed information.

        A flush is five cards all of the same suit, not in sequence.
        For 3-card hands, it checks for three cards of the same suit.

        Args:
            hand (list): List of Card objects to analyze

        Returns:
            PokerHandInfo: Information about the flush, or empty info if not found
        """
        poker_hand_info = PokerHandInfo()

        if len(hand) < MIN_CARDS_IN_HAND:
            return poker_hand_info

        sorted_hand = Poker.sort_hand_by_alt_value(hand)

        if len(hand) == 3:
            card1, card2, card3 = sorted_hand[0], sorted_hand[1], sorted_hand[2]

            if card2.suit == card1.suit == card3.suit:
                poker_hand_info.hands_beaten = (
                    FLUSH_TRIPLE_BEATS +
                    4 * (card1.altvalue - 2) *
                    (card2.altvalue - 2) *
                    (card3.altvalue - 2) // 6
                )
                poker_hand_info.hand_type = FLUSH_TRIPLE
                poker_hand_info.percentile = poker_hand_info.hands_beaten / ALL_TRIPLES
                poker_hand_info.frequency = FLUSH_TRIPLES
                poker_hand_info.probability = FLUSH_TRIPLE_PROBABILITY
                poker_hand_info.values[0] = card3.altvalue
                poker_hand_info.values[1] = card2.altvalue
                poker_hand_info.values[2] = card1.altvalue

                return poker_hand_info
            else:
                return poker_hand_info

        card1, card2, card3, card4, card5 = sorted_hand[0:5]

        if not (card1.suit == card2.suit == card3.suit == card4.suit == card5.suit):
            return poker_hand_info

        poker_hand_info.hands_beaten = (
            (card1.altvalue - 2) *
            (card2.altvalue - 2) *
            (card3.altvalue - 2) *
            (card4.altvalue - 2) *
            (card5.altvalue - 2)
        )
        poker_hand_info.hands_beaten *= 4
        poker_hand_info.hands_beaten //= 120
        poker_hand_info.hands_beaten += FLUSH_BEATS

        poker_hand_info.hand_type = FLUSH
        poker_hand_info.percentile = poker_hand_info.hands_beaten / ALL_POKER_HANDS
        poker_hand_info.frequency = FLUSH_HANDS
        poker_hand_info.probability = FLUSH_PROBABILITY

        poker_hand_info.values[0] = card5.altvalue
        poker_hand_info.values[1] = card4.altvalue
        poker_hand_info.values[2] = card3.altvalue
        poker_hand_info.values[3] = card2.altvalue
        poker_hand_info.values[4] = card1.altvalue

        return poker_hand_info

    @staticmethod
    def has_royal_straight(hand):
        """
        Check if the hand contains a royal straight and return detailed information.

        A royal straight is 10-J-Q-K-A of mixed suits.
        For 3-card hands, it checks for Q-K-A of mixed suits.

        Args:
            hand (list): List of Card objects to analyze

        Returns:
            PokerHandInfo: Information about the royal straight, or empty info if not found
        """
        poker_hand_info = PokerHandInfo()

        if len(hand) < MIN_CARDS_IN_HAND:
            return poker_hand_info

        sorted_hand = Poker.sort_hand_by_alt_value(hand)

        if len(hand) == 3:
            card1, card2, card3 = sorted_hand[0], sorted_hand[1], sorted_hand[2]

            if (card2.altvalue - card1.altvalue == 1 and
                    card3.altvalue - card2.altvalue == 1 and
                    card1.altvalue == 12):

                poker_hand_info.hands_beaten = (
                    STRAIGHT_TRIPLE_BEATS + 60 * (card3.altvalue - 3)
                )
                poker_hand_info.hand_type = STRAIGHT_TRIPLE
                poker_hand_info.percentile = poker_hand_info.hands_beaten / ALL_TRIPLES
                poker_hand_info.frequency = STRAIGHT_TRIPLES
                poker_hand_info.probability = STRAIGHT_TRIPLE_PROBABILITY
                poker_hand_info.values[0] = card3.altvalue

                return poker_hand_info
            else:
                return poker_hand_info

        card1, card2, card3, card4, card5 = sorted_hand[0:5]

        if (card2.altvalue - card1.altvalue == 1 and
                card3.altvalue - card2.altvalue == 1 and
                card4.altvalue - card3.altvalue == 1 and
                card5.altvalue - card4.altvalue == 1 and
                card1.altvalue == 10):

            poker_hand_info.hands_beaten = STRAIGHT_BEATS + 1020 * (card5.altvalue - 5)
        else:
            return poker_hand_info

        poker_hand_info.hand_type = STRAIGHT
        poker_hand_info.percentile = poker_hand_info.hands_beaten / ALL_POKER_HANDS
        poker_hand_info.frequency = STRAIGHT_HANDS
        poker_hand_info.probability = STRAIGHT_PROBABILITY
        poker_hand_info.values[0] = card5.altvalue

        return poker_hand_info

    @staticmethod
    def has_straight(hand):
        """
        Check if the hand contains a straight and return detailed information.

        A straight is five consecutive cards of mixed suits.
        For 3-card hands, it checks for three consecutive cards of mixed suits.

        Args:
            hand (list): List of Card objects to analyze

        Returns:
            PokerHandInfo: Information about the straight, or empty info if not found
        """
        poker_hand_info = PokerHandInfo()

        if len(hand) < MIN_CARDS_IN_HAND:
            return poker_hand_info

        sorted_hand = Poker.sort_hand_by_value(hand)

        if len(hand) == 3:
            card1, card2, card3 = sorted_hand[0], sorted_hand[1], sorted_hand[2]

            if card2.value - card1.value == 1 and card3.value - card2.value == 1:
                poker_hand_info.hands_beaten = STRAIGHT_TRIPLE_BEATS + 60 * (card3.value - 3)
                poker_hand_info.hand_type = STRAIGHT_TRIPLE
                poker_hand_info.percentile = poker_hand_info.hands_beaten / ALL_TRIPLES
                poker_hand_info.frequency = STRAIGHT_TRIPLES
                poker_hand_info.probability = STRAIGHT_TRIPLE_PROBABILITY
                poker_hand_info.values[0] = card3.value

                return poker_hand_info
            else:
                return poker_hand_info

        card1, card2, card3, card4, card5 = sorted_hand[0:5]

        if (card2.value - card1.value == 1 and
                card3.value - card2.value == 1 and
                card4.value - card3.value == 1 and
                card5.value - card4.value == 1):

            poker_hand_info.hands_beaten = STRAIGHT_BEATS + 1020 * (card5.value - 5)
        else:
            return poker_hand_info

        poker_hand_info.hand_type = STRAIGHT
        poker_hand_info.percentile = poker_hand_info.hands_beaten / ALL_POKER_HANDS
        poker_hand_info.frequency = STRAIGHT_HANDS
        poker_hand_info.probability = STRAIGHT_PROBABILITY
        poker_hand_info.values[0] = card5.value

        return poker_hand_info

    @staticmethod
    def has_three_of_a_kind(hand):
        """
        Check if the hand contains three of a kind and return detailed information.

        Three of a kind is three cards of the same rank.

        Args:
            hand (list): List of Card objects to analyze

        Returns:
            PokerHandInfo: Information about the three of a kind, or empty info if not found
        """
        poker_hand_info = PokerHandInfo()

        if len(hand) < 3:
            return poker_hand_info

        sorted_hand = Poker.sort_hand_by_alt_value(hand)
        card1, card2, card3 = sorted_hand[0], sorted_hand[1], sorted_hand[2]

        hands_beaten = 0
        if card1.altvalue == card2.altvalue == card3.altvalue:
            hands_beaten = card1.altvalue

        if len(hand) < 5:
            if hands_beaten > 0:
                poker_hand_info.hands_beaten = (
                    THREE_OF_A_KIND_TRIPLE_BEATS +
                    4 * (hands_beaten - 2)
                )
                poker_hand_info.hand_type = THREE_TRIPLE
                poker_hand_info.percentile = poker_hand_info.hands_beaten / ALL_TRIPLES
                poker_hand_info.frequency = THREE_OF_A_KIND_TRIPLES
                poker_hand_info.probability = THREE_OF_A_KIND_TRIPLE_PROB
                poker_hand_info.values[0] = card1.altvalue

                return poker_hand_info
            else:
                return poker_hand_info

        card4, card5 = sorted_hand[3], sorted_hand[4]

        if (card1.altvalue == card2.altvalue == card3.altvalue and
                card1.suit != CARD_SUIT['Joker']):

            hands_beaten = card1.altvalue
            poker_hand_info.values[0] = card1.altvalue
            poker_hand_info.values[1] = card5.altvalue
            poker_hand_info.values[2] = card4.altvalue

        elif (card2.altvalue == card3.altvalue == card4.altvalue and
              card2.suit != CARD_SUIT['Joker']):

            hands_beaten = card2.altvalue
            poker_hand_info.values[0] = card2.altvalue
            poker_hand_info.values[1] = card5.altvalue
            poker_hand_info.values[2] = card1.altvalue

        elif (card3.altvalue == card4.altvalue == card5.altvalue and
              card3.suit != CARD_SUIT['Joker']):

            hands_beaten = card3.altvalue
            poker_hand_info.values[0] = card3.altvalue
            poker_hand_info.values[1] = card2.altvalue
            poker_hand_info.values[2] = card1.altvalue
        else:
            return poker_hand_info

        poker_hand_info.hands_beaten = THREE_OF_A_KIND_BEATS + 4224 * (hands_beaten - 2)
        poker_hand_info.hand_type = THREE_OF_A_KIND
        poker_hand_info.percentile = poker_hand_info.hands_beaten / ALL_POKER_HANDS
        poker_hand_info.frequency = THREE_OF_A_KIND_HANDS
        poker_hand_info.probability = THREE_OF_A_KIND_PROBABILITY

        return poker_hand_info

    @staticmethod
    def has_two_pair(hand):
        """
        Check if the hand contains two pair and return detailed information.

        Two pair is two cards of one rank and two cards of another rank.

        Args:
            hand (list): List of Card objects to analyze

        Returns:
            PokerHandInfo: Information about the two pair, or empty info if not found
        """
        poker_hand_info = PokerHandInfo()

        if len(hand) < 5:
            return poker_hand_info

        sorted_hand = Poker.sort_hand_by_alt_value(hand)
        card1, card2, card3, card4, card5 = sorted_hand[0:5]

        if (card1.altvalue == card2.altvalue and card3.altvalue == card4.altvalue and
                card1.suit != CARD_SUIT['Joker'] and card3.suit != CARD_SUIT['Joker']):

            poker_hand_info.values[0] = card3.altvalue  # Highest pair
            poker_hand_info.values[1] = card1.altvalue  # Other pair
            poker_hand_info.values[2] = card5.altvalue  # Kicker

        elif (card1.altvalue == card2.altvalue and card4.altvalue == card5.altvalue and
              card1.suit != CARD_SUIT['Joker'] and card4.suit != CARD_SUIT['Joker']):

            poker_hand_info.values[0] = card4.altvalue
            poker_hand_info.values[1] = card1.altvalue
            poker_hand_info.values[2] = card3.altvalue

        elif (card2.altvalue == card3.altvalue and card4.altvalue == card5.altvalue and
              card2.suit != CARD_SUIT['Joker'] and card4.suit != CARD_SUIT['Joker']):

            poker_hand_info.values[0] = card4.altvalue
            poker_hand_info.values[1] = card2.altvalue
            poker_hand_info.values[2] = card1.altvalue
        else:
            return poker_hand_info

        if poker_hand_info.values[0] > 3:
            poker_hand_info.hands_beaten = (
                TWO_PAIR_BEATS +
                1584 * (
                    Poker.combination(poker_hand_info.values[0] - 2, 2) +
                    poker_hand_info.values[1] - 2
                ) +
                (poker_hand_info.values[2] - 2)
            )
        else:
            poker_hand_info.hands_beaten = TWO_PAIR_BEATS + poker_hand_info.values[2] - 2

        poker_hand_info.hand_type = TWO_PAIR
        poker_hand_info.percentile = poker_hand_info.hands_beaten / ALL_POKER_HANDS
        poker_hand_info.frequency = TWO_PAIR_HANDS
        poker_hand_info.probability = TWO_PAIR_PROBABILITY

        return poker_hand_info

    @staticmethod
    def has_one_pair(hand):
        """
        Check if the hand contains one pair and return detailed information.

        One pair is two cards of the same rank.

        Args:
            hand (list): List of Card objects to analyze

        Returns:
            PokerHandInfo: Information about the one pair, or empty info if not found
        """
        poker_hand_info = PokerHandInfo()

        if len(hand) < 3:
            return poker_hand_info

        sorted_hand = Poker.sort_hand_by_alt_value(hand)
        card1, card2, card3 = sorted_hand[0], sorted_hand[1], sorted_hand[2]

        if len(hand) == 3:
            if card1.altvalue == card2.altvalue:
                poker_hand_info.values[0] = card1.altvalue
                poker_hand_info.values[1] = card3.altvalue
            elif card2.altvalue == card3.altvalue:
                poker_hand_info.values[0] = card2.altvalue
                poker_hand_info.values[1] = card1.altvalue
            else:
                return poker_hand_info

            poker_hand_info.hands_beaten = (PAIR_BEATS +
                                            284 * (poker_hand_info.values[0] - 2) +
                                            4 * poker_hand_info.values[1])
            poker_hand_info.hand_type = PAIR_TRIPLE
            poker_hand_info.percentile = poker_hand_info.hands_beaten / ALL_TRIPLES
            poker_hand_info.frequency = PAIR_TRIPLES
            poker_hand_info.probability = PAIR_PROBABILITY

            return poker_hand_info

        card4, card5 = sorted_hand[3], sorted_hand[4]

        if card1.altvalue == card2.altvalue:
            poker_hand_info.values[0] = card1.altvalue
            poker_hand_info.values[1] = card5.altvalue
            poker_hand_info.values[2] = card4.altvalue
            poker_hand_info.values[3] = card3.altvalue
        elif card2.altvalue == card3.altvalue:
            poker_hand_info.values[0] = card2.altvalue
            poker_hand_info.values[1] = card5.altvalue
            poker_hand_info.values[2] = card4.altvalue
            poker_hand_info.values[3] = card1.altvalue
        elif card3.altvalue == card4.altvalue:
            poker_hand_info.values[0] = card3.altvalue
            poker_hand_info.values[1] = card5.altvalue
            poker_hand_info.values[2] = card2.altvalue
            poker_hand_info.values[3] = card1.altvalue
        elif card4.altvalue == card5.altvalue:
            poker_hand_info.values[0] = card4.altvalue
            poker_hand_info.values[1] = card3.altvalue
            poker_hand_info.values[2] = card2.altvalue
            poker_hand_info.values[3] = card1.altvalue
        else:
            return poker_hand_info

        # BUG: The kickers should be accounted for.
        poker_hand_info.hands_beaten = (
            ONE_PAIR_BEATS +
            84480 * (poker_hand_info.values[0] - 2) +
            320 * (poker_hand_info.values[1] - 2) *
            (poker_hand_info.values[2] - 2) *
            (poker_hand_info.values[3] - 2)
        )
        poker_hand_info.hand_type = ONE_PAIR
        poker_hand_info.percentile = poker_hand_info.hands_beaten / ALL_POKER_HANDS
        poker_hand_info.frequency = ONE_PAIR_HANDS
        poker_hand_info.probability = ONE_PAIR_PROBABILITY

        return poker_hand_info

    @staticmethod
    def has_high_card(hand):
        """
        Check if the hand is a high card hand and return detailed information.

        High card is when no other poker hand patterns are present.
        The hand is ranked by the highest cards in descending order.

        Args:
            hand (list): List of Card objects to analyze

        Returns:
            PokerHandInfo: Information about the high card hand
        """
        poker_hand_info = PokerHandInfo()
        sorted_hand = Poker.sort_hand_by_alt_value(hand)

        card1, card2, card3 = sorted_hand[0], sorted_hand[1], sorted_hand[2]

        if len(hand) == 3:
            poker_hand_info.values[0] = card3.altvalue
            poker_hand_info.values[1] = card2.altvalue
            poker_hand_info.values[2] = card1.altvalue

            poker_hand_info.hands_beaten = (
                64 * Poker.combination(poker_hand_info.values[0] - 2, 3)
            )
            poker_hand_info.hand_type = HIGH_TRIPLE
            poker_hand_info.percentile = poker_hand_info.hands_beaten / ALL_TRIPLES
            poker_hand_info.frequency = HIGH_TRIPLES
            poker_hand_info.probability = HIGH_TRIPLE_PROBABILITY

            return poker_hand_info
        else:
            card4, card5 = sorted_hand[3], sorted_hand[4]

            poker_hand_info.values[0] = card5.altvalue
            poker_hand_info.values[1] = card4.altvalue
            poker_hand_info.values[2] = card3.altvalue
            poker_hand_info.values[3] = card2.altvalue
            poker_hand_info.values[4] = card1.altvalue

            # BUG: Kickers should be accounted for
            poker_hand_info.hands_beaten = (
                1020 * (
                    Poker.combination(poker_hand_info.values[0] - 2, 5) -
                    (poker_hand_info.values[0] - 5)
                )
            )
            poker_hand_info.hand_type = HIGH_CARD
            poker_hand_info.percentile = poker_hand_info.hands_beaten / ALL_POKER_HANDS
            poker_hand_info.frequency = HIGH_CARD_HANDS
            poker_hand_info.probability = HIGH_CARD_PROBABILITY

            return poker_hand_info

    @staticmethod
    def get_hand_type_string(hand_type):
        """
        Get the human-readable string representation of a hand type.

        Args:
            hand_type (int): The hand type constant

        Returns:
            str: Human-readable name of the hand type, or None if not found
        """
        hand_type_map = {
            HIGH_TRIPLE: "High card",
            HIGH_CARD: "High card",
            PAIR_TRIPLE: "One pair",
            ONE_PAIR: "One pair",
            TWO_PAIR: "Two pairs",
            THREE_TRIPLE: "Three-of-a-kind",
            THREE_OF_A_KIND: "Three-of-a-kind",
            FLUSH_TRIPLE: "Flush",
            FLUSH: "Flush",
            STRAIGHT_TRIPLE: "Straight",
            STRAIGHT: "Straight",
            FULL_HOUSE: "Full house",
            FOUR_OF_A_KIND: "Four-of-a-kind",
            STRAIGHT_FLUSH_TRIPLE: "Straight flush",
            STRAIGHT_FLUSH: "Straight flush",
            ROYAL_FLUSH_TRIPLE: "Royal flush",
            ROYAL_FLUSH: "Royal flush"
        }
        return hand_type_map.get(hand_type)

    @staticmethod
    def get_hand_type_rating(hand_type):
        """
        Get the star rating representation of a hand type.

        Returns a string of star symbols representing the strength of the hand type.
        Higher-ranked hands get more stars.

        Args:
            hand_type (int): The hand type constant

        Returns:
            str: String of star symbols representing the hand strength
        """
        rating_map = {
            HIGH_TRIPLE: 1,
            HIGH_CARD: 1,
            PAIR_TRIPLE: 2,
            ONE_PAIR: 2,
            TWO_PAIR: 3,
            THREE_TRIPLE: 4,
            THREE_OF_A_KIND: 4,
            FLUSH_TRIPLE: 5,
            STRAIGHT: 5,
            STRAIGHT_TRIPLE: 6,
            FLUSH: 6,
            FULL_HOUSE: 7,
            FOUR_OF_A_KIND: 8,
            STRAIGHT_FLUSH_TRIPLE: 9,
            STRAIGHT_FLUSH: 9,
            ROYAL_FLUSH: 10
        }
        stars = rating_map.get(hand_type, 0)
        return STAR_SYMBOL * stars

    @staticmethod
    def get_card_value_string(value, long_name=True):
        """
        Get the string representation of a card value.

        Args:
            value (int): The card value (1-14)
            long_name (bool): If True, return full names (e.g., "Ace"),
                            if False, return abbreviations (e.g., "A")

        Returns:
            str: String representation of the card value
        """
        if 1 < value < 11:
            return str(value)
        elif value == 1 or value == 14:
            return "Ace" if long_name else "A"
        elif value == 11:
            return "Jack" if long_name else "J"
        elif value == 12:
            return "Queen" if long_name else "Q"
        elif value == 13:
            return "King" if long_name else "K"
        else:
            return "?"

    @staticmethod
    def match_hands(hand1, hand2):
        """
        Compare two poker hands to determine which is stronger.

        Compares hand types first, then individual card values if hand types are equal.

        Args:
            hand1 (PokerHandInfo): Information about the first hand
            hand2 (PokerHandInfo): Information about the second hand

        Returns:
            int: LEFT_HAND_WINS (1) if hand1 wins, RIGHT_HAND_WINS (-1) if hand2 wins,
                 HANDS_ARE_EQUAL (0) if hands are equal
        """
        if hand1.hand_type > hand2.hand_type:
            return LEFT_HAND_WINS
        elif hand1.hand_type < hand2.hand_type:
            return RIGHT_HAND_WINS
        else:
            for i in range(5):
                if hand1.values[i] > hand2.values[i]:
                    return LEFT_HAND_WINS
                elif hand1.values[i] < hand2.values[i]:
                    return RIGHT_HAND_WINS
            return HANDS_ARE_EQUAL

    @staticmethod
    def match_front_middle(hand1, hand2):
        """
        Compare front hand (3 cards) against middle hand (5 cards).

        Special comparison rules for Chinese Poker where front hands have
        different valid types than middle/back hands.

        Args:
            hand1 (PokerHandInfo): Information about the front hand (3 cards)
            hand2 (PokerHandInfo): Information about the middle hand (5 cards)

        Returns:
            int: LEFT_HAND_WINS (1) if front hand wins, RIGHT_HAND_WINS (-1) if middle hand wins,
                 HANDS_ARE_EQUAL (0) if hands are equal
        """
        if hand1.hand_type == HIGH_TRIPLE:
            if hand2.hand_type == HIGH_CARD:
                for i in range(5):
                    if hand1.values[i] > hand2.values[i]:
                        return LEFT_HAND_WINS
                    elif hand1.values[i] < hand2.values[i]:
                        return RIGHT_HAND_WINS
                print("Impossible case detected!")
                return HANDS_ARE_EQUAL  # Impossible to have two equal high cards!
            else:
                return RIGHT_HAND_WINS

        elif hand1.hand_type == PAIR_TRIPLE:
            if hand2.hand_type == ONE_PAIR:
                if hand1.values[0] > hand2.values[0]:
                    return LEFT_HAND_WINS
                elif hand1.values[0] < hand2.values[0]:
                    return RIGHT_HAND_WINS
                elif hand1.values[1] > hand2.values[1]:
                    return LEFT_HAND_WINS
                elif hand1.values[1] < hand2.values[1]:
                    return RIGHT_HAND_WINS
                else:
                    return RIGHT_HAND_WINS  # The two hands can't really be equal.
            elif hand2.hand_type < ONE_PAIR:
                return LEFT_HAND_WINS
            else:
                return RIGHT_HAND_WINS

        elif hand1.hand_type == THREE_TRIPLE:
            if hand2.hand_type == THREE_OF_A_KIND:
                if hand1.values[0] > hand2.values[0]:
                    return LEFT_HAND_WINS
                elif hand1.values[0] < hand2.values[0]:
                    return RIGHT_HAND_WINS
                else:
                    print("Impossible case detected!")
                    return HANDS_ARE_EQUAL  # Impossible to have two equal triples!
            elif hand2.hand_type < THREE_OF_A_KIND:
                return LEFT_HAND_WINS
            else:
                return RIGHT_HAND_WINS
        else:
            print("Impossible case detected!")
            return HANDS_ARE_EQUAL  # Impossible. No other possible hand type.

    @staticmethod
    def analyze_hand(hand):
        """
        Analyze a poker hand and return detailed information about its type and strength.

        Tries each hand type from highest to lowest (royal flush down to high card)
        and returns information about the first match found.

        Args:
            hand (list): List of Card objects to analyze

        Returns:
            PokerHandInfo: Detailed information about the hand including type,
                          strength, probability, and key card values
        """
        # Try each hand type from highest to lowest
        hand_info = Poker.has_royal_flush(hand)
        if hand_info.hand_type in [ROYAL_FLUSH, ROYAL_FLUSH_TRIPLE]:
            return hand_info

        hand_info = Poker.has_straight_flush(hand)
        if hand_info.hand_type in [STRAIGHT_FLUSH, STRAIGHT_FLUSH_TRIPLE]:
            return hand_info

        hand_info = Poker.has_four_of_a_kind(hand)
        if hand_info.hand_type == FOUR_OF_A_KIND:
            return hand_info

        hand_info = Poker.has_full_house(hand)
        if hand_info.hand_type == FULL_HOUSE:
            return hand_info

        hand_info = Poker.has_flush(hand)
        if hand_info.hand_type in [FLUSH, FLUSH_TRIPLE]:
            return hand_info

        hand_info = Poker.has_royal_straight(hand)
        if hand_info.hand_type in [STRAIGHT, STRAIGHT_TRIPLE]:
            return hand_info

        hand_info = Poker.has_straight(hand)
        if hand_info.hand_type in [STRAIGHT, STRAIGHT_TRIPLE]:
            return hand_info

        hand_info = Poker.has_three_of_a_kind(hand)
        if hand_info.hand_type in [THREE_OF_A_KIND, THREE_TRIPLE]:
            return hand_info

        hand_info = Poker.has_two_pair(hand)
        if hand_info.hand_type == TWO_PAIR:
            return hand_info

        hand_info = Poker.has_one_pair(hand)
        if hand_info.hand_type in [ONE_PAIR, PAIR_TRIPLE]:
            return hand_info

        hand_info = Poker.has_high_card(hand)
        if hand_info.hand_type in [HIGH_CARD, HIGH_TRIPLE]:
            return hand_info

        return hand_info
