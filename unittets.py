import unittest
from cards_classes import Card, Dealer, Player

class TestCards(unittest.TestCase):
    """Test for the class Cards"""

    def test_ace_card(self):
        """Test that the ace of clabs card is being correctly set up when defined with id=22"""
        shape = ['s', 'c', 'd', 'h']
        figure = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', '1']
        card_shape = 1
        card_number = 14
        id = 22
        ace_club = Card(id, card_shape, card_number, shape, figure)

        self.assertEqual(ace_club.number, 14)
        self.assertEqual(ace_club.shape, 1)
        self.assertEqual(ace_club.name, 'c1')

class TestPlayer(unittest.TestCase):
    """Test for the class player"""

    def setUp(self):
        """Define the cards, a case of 5 opened cards and a player"""
        shape = ['s', 'c', 'd', 'h']
        figure = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', '1']
        self.combination = { 'flush royale!' : 10, 'straight flush' : 9, 'four of a kind' : 8, 'full house' : 7, 'flush' : 6,
        'straight' : 5, 'three of a kind' : 4, 'two pairs' : 3, 'a pair' : 2, 'high card' : 1}
        self.cards = []                    #Define the cards
        i = 0
        for card_shape in range (4):
            for card_number in range(2,15):
                self.cards.append('card')
                self.cards[i] = Card(i, card_shape, card_number, shape, figure)
                i += 1
        self.open_ids = [12, 0, 1, 13, 18] #ace, two and three of spade plus two and seven of clubs
        name = "Player1"
        self.player = Player(name)

    def test_flush_royale(self):
        """Test flush royale case for a player"""
        open_ids = [12,11,10,8,7]
        self.player.ids = [9, 23]
        self.player.find_final_combination(open_ids, self.cards, self.combination)
        self.assertEqual(self.player.strength, [10, 14, 13, 12, 11, 10])
    
    def test_straight_flush(self):
        """Test the straight flush case for a player"""
        self.player.ids = [2, 3]
        self.player.find_final_combination(self.open_ids, self.cards, self.combination)
        self.assertEqual(self.player.strength, [9, 5, 4, 3, 2, 14])

    def test_four_of_a_kind(self):
        """Test the four of kind case for a player"""
        self.player.ids = [26, 39]
        self.player.find_final_combination(self.open_ids, self.cards, self.combination)
        self.assertEqual(self.player.strength, [8, 2, 2, 2, 2, 14])

    def test_full_house(self):
        """Test full house case for a player"""
        self.player.ids = [26, 40]
        self.player.find_final_combination(self.open_ids, self.cards, self.combination)
        self.assertEqual(self.player.strength, [7, 2, 2, 2, 3, 3])

    def test_flush(self):
        """Test the flush case for 7 cards of same figure for a player"""
        open_ids = [12,10,3,5,7]
        self.player.ids = [9, 11]
        self.player.find_final_combination(open_ids, self.cards, self.combination)
        self.assertEqual(self.player.strength, [6, 14, 13, 12, 11, 9])

    def test_straight_special(self):
        """Test the straight case of 1,2,3,4,5 for a player"""
        self.player.ids = [2, 16]
        self.player.find_final_combination(self.open_ids, self.cards, self.combination)
        self.assertEqual(self.player.strength, [5, 5, 4, 3, 2, 14])

    def test_straight(self):
        """Test the straight case for a player"""
        open_ids = [0,1,2,19,20]
        self.player.ids = [16, 17]
        self.player.find_final_combination(open_ids, self.cards, self.combination)
        self.assertEqual(self.player.strength, [5, 6, 5, 4, 3, 2])

    def test_three_of_kind(self):
        """Test the three of a kind case for a player"""
        self.player.ids = [26, 41]
        self.player.find_final_combination(self.open_ids, self.cards, self.combination)
        self.assertEqual(self.player.strength, [4, 2, 2, 2, 14, 7])

    def test_two_pairs(self):
        """Test the two pairs case for a player that has 3 pairs and higher single for kicker"""
        self.player.ids = [14, 31]
        self.player.find_final_combination(self.open_ids, self.cards, self.combination)
        self.assertEqual(self.player.strength, [3, 7, 7, 3, 3, 14])

    def test_one_pair(self):
        """Test the one pair case for a player"""
        self.player.ids = [15, 17]
        self.player.find_final_combination(self.open_ids, self.cards, self.combination)
        self.assertEqual(self.player.strength, [2, 2, 2, 14, 7, 6])

    def test_high_card(self):
        """Test the high card case for a player"""
        open_ids = [0,1,2,19,20]
        self.player.ids = [17, 18]
        self.player.find_final_combination(open_ids, self.cards, self.combination)
        self.assertEqual(self.player.strength, [1, 9, 8, 7, 6, 4])


unittest.main()

