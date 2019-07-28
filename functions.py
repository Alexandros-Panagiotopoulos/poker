import pandas as pd

def check_combination_type(all_cards, useful_cards):
    all_shapes = [all_cards[i].shape for i in range(len(all_cards))]
    all_numbers = [all_cards[i].number for i in range(len(all_cards))]
    df_all_cards = pd.DataFrame()
    df_all_cards['shape'] = all_shapes
    df_all_cards['number'] = all_numbers
    all_dif_num = list(set(all_numbers))
    comb_type = None
    if len(all_dif_num) >= 5:
        comb_type = flush(df_all_cards, useful_cards)
        if comb_type == None:
                comb_type = straight(df_all_cards, useful_cards)
    if comb_type == None:
        comb_type = many_of_a_kind(df_all_cards, useful_cards, len(all_dif_num))
    return comb_type

def flush(df_all_cards, useful_cards):
    grouped_ds = df_all_cards.groupby('shape')['number'].apply(list)
    for i, numbers_list in enumerate(grouped_ds):
        if len(numbers_list) >= 5: #There is a flush
                shape_of_flush = grouped_ds.index[i]
                positions = df_all_cards[df_all_cards['shape'] == shape_of_flush].index.tolist()
                df_useful_cards = df_all_cards.iloc[positions,:].sort_values(by =['number'], ascending = False)
                comb_type = straight(df_useful_cards, useful_cards)
                if comb_type =='straight':
                        if df_all_cards.loc[useful_cards[0]]['number'] == 14:
                                comb_type = 'flush royale!'
                        else:
                                comb_type = 'straight flush'
                else:
                        comb_type = 'flush'
                        useful_cards.extend(df_useful_cards.iloc[0:5].index.values.tolist())
                return (comb_type)

def straight(df_cards, useful_cards):
        comb_type = 'straight'
        df_useful_cards = df_cards.sort_values(by =['number'], ascending = False)
        df_useful_cards.drop_duplicates(subset= 'number', keep="last", inplace=True)
        if df_useful_cards.iloc[0]['number'] == 14:
                df_useful_cards = df_useful_cards.append(df_useful_cards[0:1])
                df_useful_cards.iloc[-1]['number'] = 1
        for i in range(len(df_useful_cards)-4):
                if df_useful_cards.iloc[i]['number'] - df_useful_cards.iloc[i+4]['number'] == 4: # there is a straight
                        df_useful_cards = df_useful_cards[i:] #drop higher from the straight cards
                        useful_cards.extend(df_useful_cards.iloc[0:5].index.values.tolist())
                        return (comb_type)

def many_of_a_kind(df_cards, useful_cards, dif_num_count):
        df_cards ['freq'] = df_cards.groupby('number')['number'].transform('count')
        df_useful_cards = df_cards.sort_values(by=['freq', 'number'], ascending = False)
        useful_cards.extend(df_useful_cards.iloc[0:5].index.values.tolist())
        if dif_num_count == 7:          #With 7 different cards it is high card
                comb_type = 'high card'  
        elif dif_num_count == 6:        #With 6 different cards it is a pair
                comb_type = 'a pair'    
        elif dif_num_count == 5:        #With 5 different cards it is three of a kind or two pairs
                if df_useful_cards.iloc[0]['freq'] == 3:
                        comb_type = 'three of a kind'
                else:
                        comb_type = 'two pairs'
        else:                           #With 4 or less different cards it is full house or four of a kind or three pairs (i.e. two pairs)
                if df_useful_cards.iloc[0]['freq'] == 3:
                        comb_type = 'full house'
                else:                   # For the 4 of a kind and the 3 pairs the kicker can be the single card so useful cards need recalculation
                        df_useful_cards.iloc[4:,df_useful_cards.columns.get_loc('freq')] = 1
                        df_useful_cards.sort_values(by=['freq','number'], ascending = False, inplace=True)
                        del useful_cards[:]
                        useful_cards.extend(df_useful_cards.iloc[0:5].index.values.tolist())
                        if df_useful_cards.iloc[0]['freq'] == 2:       #case of 3 pairs
                                comb_type = 'two pairs'
                        else:
                                comb_type = 'four of a kind'
        return (comb_type)

def players_ranking(players, winner):
        df = pd.DataFrame([players[i].strength for i in range(len(players))], columns=list('ABCDEF'))
        df.sort_values(by=['A','B','C','D','E','F'], ascending = False, inplace=True)
        for i, row in df.iterrows():
                if (row.tolist() == df.iloc[0].values.tolist()):
                        winner.append(i)
        return df.index.values.tolist()

def win_prob(deck, cards, players, open_ids, players_number, combination):
        players_prob = [0 for i in range(players_number)]
        if len(open_ids) == 0:
                open_ids = [deck[0] for i in range(5)]
                combs_no = preflop_all_combs(deck, cards, players, open_ids, players_number, combination, players_prob)
        elif len(open_ids) == 3:
                open_ids.extend([deck[0] for i in range(2)])
                combs_no = flop_all_combs(deck, cards, players, open_ids, players_number, combination, players_prob)
        else:
                open_ids.append([0])
                combs_no = turn_all_combs(deck, cards, players, open_ids, players_number, combination, players_prob)
        players_prob = [players_prob[i]/combs_no for i in range(players_number)]
        print (players_prob)
        
def preflop_all_combs(deck, cards, players, open_ids, players_number, combination, players_prob):
        combs_no = 0
        for a in range(0,len(deck)-4):
                open_ids[0] = deck[a]
                for b in range(a+1,len(deck)-3):
                        open_ids[1] = deck[b]
                        for c in range(b+1,len(deck)-2):
                                open_ids[2] = deck[c]
                                for d in range(c+1,len(deck)-1):
                                        open_ids[3] = deck[d]
                                        for e in range(d+1,len(deck)):
                                                open_ids[4] = deck[e]
                                                winner_reward(cards, players, open_ids, players_number, combination, players_prob)
                                                combs_no += 1
        return combs_no

def flop_all_combs(deck, cards, players, open_ids, players_number, combination, players_prob):
        combs_no = 0
        for d in range(0,len(deck)-1):
                open_ids[3] = deck[d]
                for e in range(d+1,len(deck)):
                        open_ids[4] = deck[e]
                        winner_reward(cards, players, open_ids, players_number, combination, players_prob)
                        combs_no += 1
        return combs_no

def turn_all_combs(deck, cards, players, open_ids, players_number, combination, players_prob):
        combs_no = 0
        for e in range(0,len(deck)):
                open_ids[4] = deck[e]
                winner_reward(cards, players, open_ids, players_number, combination, players_prob)
                combs_no += 1
        return combs_no

def winner_reward(cards, players, open_ids, players_number, combination, players_prob):
        for player_no in range(players_number):
                players[player_no].find_final_combination(open_ids, cards, combination)
        winner = winner_finder(players)
        for i in range(len(winner)):
                players_prob[winner[i]] += 1.0/len(winner)

def winner_finder(players):
        players_strength_list = [players[i].strength for i in range(len(players))]
        all_players_strength_list = players_strength_list[:]
        for i in range(5):
                strongest_hands = []
                max_val = max(players_strength_list, key=lambda x: x[i])[i]
                for players_strength in players_strength_list:
                        if players_strength[i] == max_val:
                                strongest_hands.append(players_strength)
                if len(strongest_hands) == 1:
                        break
                players_strength_list = strongest_hands
        return [i for i, e in enumerate (all_players_strength_list) if (e == strongest_hands[0])]