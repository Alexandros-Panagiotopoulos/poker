from cards_classes import Card, Player
import functions as fs
from random import randint

shape = ['s', 'c', 'd', 'h']
figure = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', '1']
combination = { 'flush royale!' : 10, 'straight flush' : 9, 'four of a kind' : 8, 'full house' : 7, 'flush' : 6,
        'straight' : 5, 'three of a kind' : 4, 'two pairs' : 3, 'a pair' : 2, 'high card' : 1}

deck = list(range(52))          #Define the deck
cards = []                      #Define the cards
for card_number in range(52):
    cards.append('card')
    cards[card_number] = Card(card_number, shape, figure)

players_number = 10             #Define the players
players = []
for player_no in range(players_number):
    players.append('player')
    player_name = 'player ' + str(player_no + 1)
    players[player_no] = Player(player_name, deck)

for player_no in range(players_number):     
    players[player_no].take_ids(deck)           #Deal cards to all players
    players[player_no].show_cards(cards)        #Players will show their hand for this application

open_ids = []
#fs.win_prob(deck, cards, players, open_ids[:], players_number, combination) #calculate win probability

for i in range(3):
    open_ids.append(deck.pop(randint(0,len(deck)-1))) # Open Flop
print ('The flop ' + str([cards[i].name for i in open_ids]))
# fs.win_prob(deck, cards, players, open_ids[:], players_number, combination)   #calculate win probability

open_ids.append(deck.pop(randint(0,len(deck)-1)))   # Open_turn
print ('The turn ' + str([cards[i].name for i in open_ids]))
# fs.win_prob(deck, cards, players, open_ids[:], players_number, combination)   #calculate win probability

open_ids.append(deck.pop(randint(0,len(deck)-1)))   # Open_river
print ('The river ' + str([cards[i].name for i in open_ids]))

for player_no in range(players_number):
    players[player_no].final_hand(open_ids, cards, combination)

winner = []
players_rank = fs.players_ranking(players, winner)

for player_no in players_rank:
    players[player_no].printer()

if len(winner) == 1:
        print ("The winner is " + players[winner[0]].name)
else:
        print ("The first " + str(len(winner)) + " players tie in first position")