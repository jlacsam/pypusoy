"""
Test file for the Player class.
Contains one assert statement test for every method of the Player class.
"""

# test_player.py
from player import Player


# --- Mock Card class for testing ---
class MockCard:
    def __init__(self, code, short=None):
        self.card_code = code
        self._short = short if short else code

    def short_name(self):
        return self._short


def test_player_class():
    p = Player()

    p.receive_card("KH")
    assert len(p.cards) == 1
    assert p.cards[0] == "KH"

    pack1 = ["AH", "KH", "1H", "4S"]
    p.receive_pack(pack1)
    assert len(p.cards) == 4
    assert p.cards == pack1.copy()

    deck = [MockCard("AS"), MockCard("KH"), MockCard("QC"), MockCard("AC")]
    list_str = "AS,QC,4H,AH,JH"
    p.cards = []
    p.receive_card_from_list(deck, list_str)
    assert len(p.cards) == 2
    assert [c.card_code for c in p.cards] == ["AS", "QC"]

    p.surrender_cards()
    assert p.hand_no == "-1"
    assert len(p.cards) == 0

    p.hand_no = "1"
    assert p.has_selected_hand() is True

    p.cards = [MockCard("AS"), MockCard("KH"), MockCard("QC"), MockCard("AC")]
    assert p.card_list() == "AS KH QC AC"

    p.arranged_cards = [MockCard("AS"), MockCard("KH"), MockCard("QC"), MockCard("AC")]
    assert p.arranged_card_list() == "AS KH QC AC"

    p.hand_score = [1, 1, 1]
    p.raw_scores = [[1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1]]

    p.reset_hand_scores()
    assert p.hand_score[1] == 0
    assert p.raw_scores[3] == [0, 0, 0]

    p.set_hand_score_at_index(5, 1)
    assert p.hand_score == [0, 5, 0]
    assert p.hand_score_at_index(1) == 5

    p.name = "John Doe"
    assert p.get_first_name() == "John"

    p.arranged_cards = [MockCard(str(i)) for i in range(1, 14)]
    assert p.front_hand() == "1 2 3"
    assert p.middle_hand() == "4 5 6 7 8"
    assert p.back_hand() == "9 10 11 12 13"
    assert p.hand_string(0) == "1 2 3"
    assert p.hand_string(1) == "4 5 6 7 8"
    assert p.hand_string(2) == "9 10 11 12 13"

    print("All Player tests passed ✅")


if __name__ == "__main__":
    test_player_class()
