from random import randint
import functions as fs

class Dealer():
    '''Initialise and manage the progress of the game'''

    def __init__(self, name='dealer'):
        self.name = name

    def initialise_cards(self, shape, figure):
        cards = []                      #Define the cards
        i = 0
        for card_shape in range (4):
            for card_number in range(2,15):
                cards.append('card')
                cards[i] = Card(i, card_shape, card_number, shape, figure)
                i += 1
        return cards

    def set_up_players(self, players_number):
        players = []
        for player_no in range(players_number):
                players.append('player')
                player_name = 'player ' + str(player_no + 1)
                players[player_no] = Player(player_name)
        return players

    def deal_cards(self, players_number, players, deck, cards):
        for player_no in range(players_number):     
            players[player_no].take_ids(deck)           #Deal cards to all players
            players[player_no].show_cards(cards)        #Players will show their hand for this application

    def open_flop(self, deck, open_ids, cards):
        for i in range(3):
            self.open_card(deck, open_ids, cards)
        print ('The flop ' + str([cards[i].name for i in open_ids]))

    def open_turn(self, deck, open_ids, cards):
        self.open_card(deck, open_ids, cards)
        print ('The turn ' + str([cards[i].name for i in open_ids]))

    def open_river(self, deck, open_ids, cards):
        self.open_card(deck, open_ids, cards)
        print ('The river ' + str([cards[i].name for i in open_ids]))

    def open_card(self, deck, open_ids, cards):
        open_ids.append(deck.pop(randint(0,len(deck)-1))) # Open Flop

class Card():
    '''Define a card of the deck'''

    def __init__(self, id, card_shape, card_number, shape, figure):
        self.id = id
        self.number = card_number
        self.shape = card_shape
        self.name = str(shape [self.shape]) + str(figure[self.number - 2])


class Player():
    def __init__(self, name):
        self.name = name

    def take_ids(self, deck):
        self.ids = []
        card_id1 = randint(0,len(deck)-1)
        self.ids.append(deck.pop(card_id1))
        card_id2 = randint(0,len(deck)-1)
        self.ids.append(deck.pop(card_id2))

    def show_cards(self, cards):
        print (self.name + ' holds ' + str([cards[i].name for i in self.ids]))

    def find_final_combination(self, open_ids, cards, combination):
        self.all_ids = self.ids + open_ids
        self.all_cards = [cards[i] for i in self.all_ids]
        self.useful_cards = [] #list of the position of the cards at the list all_cards, participating at the combination
        self.comp_type = fs.check_combination_type(self.all_cards, self.useful_cards)
        self.strength = [combination[self.comp_type]]
        self.strength.extend([self.all_cards[i].number for i in self.useful_cards])

    def show_final_combination (self):
        print (self.name + ' has ' + self.comp_type + ' ' + str([self.all_cards[i].name for i in self.useful_cards]))