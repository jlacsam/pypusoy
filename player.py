"""
Player module for managing players in a card game.

This module defines the `Player` class and constants for different player
types. A `Player` instance maintains attributes such as player identity,
cards, scores, and hand arrangements. It also provides methods to manage
cards, display them, and track scores.

Constants
---------
PLAYER_TYPE : dict
    Mapping of player names to numeric identifiers.
"""

PLAYER_TYPE = {
    'You': 0,
    'Dumbot': 1,
    'Elizabot': 2,
    'Gilbot': 3
}


class Player:
    """
    Represents a player in a card game, with attributes for player type,
    identity, cards, scores, and hand arrangements.

    Attributes
    ----------
    player_type : int
        The type of the player (see PLAYER_TYPE).
    player_id : int
        Unique identifier for the player.
    name : str or None
        The name of the player.
    cards : list
        List of cards currently held by the player.
    arranged_cards : list
        List of cards arranged into front, middle, and back hands.
    hand_no : str
        Identifier for the hand (-1 if no hand is selected).
    score : int
        The total score accumulated by the player.
    best_hand : int
        The highest-ranking hand achieved by the player.
    hand_score : list
        Scores of the player's front, middle, and back hands.
    raw_scores : list of list
        Raw scoring data across multiple hands.
    did_fold : bool
        Whether the player has folded in the current game.
    """

    def __init__(self):
        """Initialize a Player with default attributes."""
        self.player_type = 0
        self.player_id = 0
        self.name = None
        self.cards = []
        self.arranged_cards = []
        self.hand_no = "-1"
        self.score = 0
        self.best_hand = 0
        self.hand_score = [0, 0, 0]
        self.raw_scores = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.did_fold = False

    def dump_cards(self):
        """Print all cards currently held by the player."""
        print(f"{self.name}>>")
        print(" ".join([c.short_name() for c in self.cards]))

    def dump_arranged_cards(self):
        """Print the player's arranged cards in order."""
        print(f"{self.name}>>")
        print(" ".join([c.short_name() for c in self.arranged_cards]))

    def receive_card(self, card):
        """
        Add a single card to the player's hand.

        Parameters
        ----------
        card : Card
            The card to be added.
        """
        self.cards.append(card)

    def receive_pack(self, pack):
        """
        Replace the player's cards with a new pack.

        Parameters
        ----------
        pack : list
            A list of Card objects.
        """
        self.cards = pack.copy()

    def receive_card_from_list(self, deck, list_str):
        """
        Assign cards to the player based on a list of card codes.

        Parameters
        ----------
        deck : list
            The full deck of Card objects.
        list_str : str
            Comma-separated string of card codes.
        """
        pack = list_str.split(",")
        self.cards = []
        for cd in deck:
            for ca in pack:
                if ca == cd.card_code:
                    self.cards.append(cd)

    def surrender_cards(self):
        """Clear the player's hand and reset the hand number."""
        self.hand_no = "-1"
        self.cards = []

    def has_selected_hand(self):
        """
        Check if the player has selected a hand.

        Returns
        -------
        bool
            True if the player has selected a hand, False otherwise.
        """
        return self.hand_no != "-1"

    def card_list(self):
        """
        Return a string of the player's current cards.

        Returns
        -------
        str
            Space-separated list of card short names.
        """
        return " ".join([c.short_name() for c in self.cards])

    def arranged_card_list(self):
        """
        Return a string of the player's arranged cards.

        Returns
        -------
        str
            Space-separated list of arranged card short names.
        """
        return " ".join([c.short_name() for c in self.arranged_cards])

    def reset_hand_scores(self):
        """Reset the player's hand scores and raw scores."""
        self.hand_score = [0, 0, 0]
        self.raw_scores = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]

    def set_hand_score_at_index(self, value, index):
        """
        Set the score for a hand at the given index.

        Parameters
        ----------
        value : int
            Score to assign.
        index : int
            Index of the hand (0 = front, 1 = middle, 2 = back).
        """
        self.hand_score[index] = value

    def hand_score_at_index(self, index):
        """
        Retrieve the score for a hand at the given index.

        Parameters
        ----------
        index : int
            Index of the hand (0 = front, 1 = middle, 2 = back).

        Returns
        -------
        int
            The score of the hand at the given index.
        """
        return self.hand_score[index]

    def get_first_name(self):
        """
        Return the player's first name.

        Returns
        -------
        str
            The first name of the player.
        """
        return self.name.split()[0]

    def front_hand(self):
        """
        Return a string of the player's front hand cards.

        Returns
        -------
        str
            Space-separated short names of the first 3 arranged cards.
        """
        return " ".join([c.short_name() for c in self.arranged_cards[:3]])

    def middle_hand(self):
        """
        Return a string of the player's middle hand cards.

        Returns
        -------
        str
            Space-separated short names of the 4 middle arranged cards.
        """
        return " ".join([c.short_name() for c in self.arranged_cards[3:8]])

    def back_hand(self):
        """
        Return a string of the player's back hand cards.

        Returns
        -------
        str
            Space-separated short names of the last 5 arranged cards.
        """
        return " ".join([c.short_name() for c in self.arranged_cards[8:]])

    def hand_string(self, row):
        """
        Return a string representation of the player's hand
        based on the specified row index.

        Parameters
        ----------
        row : int
            The row index (0 = front, 1 = middle, 2 = back).

        Returns
        -------
        str
            Space-separated short names of the cards in the specified hand.
        """
        match row:
            case 0:
                return self.front_hand()
            case 1:
                return self.middle_hand()
            case 2:
                return self.back_hand()
            case _:
                return self.back_hand()
