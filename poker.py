import functions as fs
from random import randint
from cards_classes import Dealer, Card, Player

shape = ['s', 'c', 'd', 'h']
figure = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', '1']
combination = { 'flush royale!' : 10, 'straight flush' : 9, 'four of a kind' : 8, 'full house' : 7, 'flush' : 6,
        'straight' : 5, 'three of a kind' : 4, 'two pairs' : 3, 'a pair' : 2, 'high card' : 1}

dealer = Dealer()               #Set up a dealer
deck = list(range(52))          #Define the deck
cards = dealer.initialise_cards(shape, figure)

players_number = 10             
players = dealer.set_up_players(players_number)
dealer.deal_cards(players_number, players, deck, cards)

open_ids = []
#fs.win_prob(deck, cards, players, open_ids[:], players_number, combination) #calculate win probability
dealer.open_flop(deck, open_ids, cards)
# fs.win_prob(deck, cards, players, open_ids[:], players_number, combination)   #calculate win probability
dealer.open_turn(deck, open_ids, cards)
fs.win_prob(deck, cards, players, open_ids[:], players_number, combination)   #calculate win probability
dealer.open_river(deck, open_ids, cards)

for player_no in range(players_number):
    players[player_no].find_final_combination(open_ids, cards, combination)
winner = []
players_rank = fs.players_ranking(players, winner)

for player_no in players_rank:
    players[player_no].show_final_combination()

if len(winner) == 1:
        print ("The winner is " + players[winner[0]].name)
else:
        print ("The first " + str(len(winner)) + " players tie in first position")