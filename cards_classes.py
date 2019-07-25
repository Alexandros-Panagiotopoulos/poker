from random import randint
import functions as fs

class Card():
    '''Define a card of the deck'''

    def __init__(self, id, shape, figure):
        self.id = id
        self.number = id % 13 +1
        if self.number == 1:
            self.number = 14
        self.shape = id // 13
        self.name = str(shape [self.shape]) + str(figure[self.number - 2])


class Player():
    def __init__(self, name, deck):
        self.name = name

    def take_ids(self, deck):
        self.ids = []
        card_id1 = randint(0,len(deck)-1)
        self.ids.append(deck.pop(card_id1))
        card_id2 = randint(0,len(deck)-1)
        self.ids.append(deck.pop(card_id2))

    def show_cards(self, cards):
        print (self.name + ' holds ' + str([cards[i].name for i in self.ids]))

    def final_hand(self, open_ids, cards, combination):
        self.all_ids = self.ids + open_ids
        # print ([cards[i].name for i in self.all_ids])
        self.all_cards = [cards[i] for i in self.all_ids]
        self.usefull_cards = [] #list of the position of the cards at the list all_cards, participating at the combination
        self.comp_type = fs.combination_checker(self.all_cards, self.usefull_cards)
        self.strength = [combination[self.comp_type]]
        self.strength.extend([self.all_cards[i].number for i in self.usefull_cards])

    def printer (self):
        print (self.name + ' has ' + self.comp_type + ' ' + str([self.all_cards[i].name for i in self.usefull_cards]))
        # print ([self.all_cards[i].name for i in self.usefull_cards])
        # print (self.strength)