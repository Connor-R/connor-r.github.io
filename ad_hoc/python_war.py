import random
import os

suits = ['Spades', 'Clubs', 'Hearts', 'Diamonds']
val_dict = {
    '2':2,
    '3':3,
    '4':4,
    '5':5,
    '6':6,
    '7':7,
    '8':8,
    '9':9,
    '10':10,
    'J':11,
    'Q':12,
    'K':13,
    'A':14
    }

def initiate():
    deal_cards(suits, val_dict)

def deal_cards(suits, val_dict):
    total_hands = 0
    p1_hands = 0
    p2_hands = 0
    total_wars = 0
    p1_wars = 0
    p2_wars = 0

    all_cards = []
    for suit in suits:
        for k, v in val_dict.items():
            card_val = k + '_' + suit
            all_cards.append(card_val)

    player_1_hand = []
    player_2_hand = []
    for i in range(0,52):
        ind = random.sample(range(0, 52-i), 1)[0]
        card_val = all_cards[ind]
        all_cards.remove(card_val)

        if i % 2 == 0:
            player_1_hand.append(card_val)
        else:
            player_2_hand.append(card_val)

    play_hand(player_1_hand, player_2_hand, total_hands, p1_hands, p2_hands, total_wars, p1_wars, p2_wars)

def play_hand(player_1_hand, player_2_hand, total_hands, p1_hands, p2_hands, total_wars, p1_wars, p2_wars):
    if (total_hands+5*total_wars) > 899:
        print '\n\n\nDRAW! (too many hands played)'
        print 'total hands:\t', total_hands
        print 'total wars:\t', total_wars
        print 'p1 hand record:\t', p1_hands, '-', p2_hands
        print 'p1 war record:\t', p1_wars, '-', p2_wars
        print '\n\n'
        return None

    if (player_1_hand==[] or player_2_hand==[]):
        print '\n\n\nGAME OVER!!!'
        if player_2_hand==[]:
            print 'player 1 wins!'
            print 'total hands:\t', total_hands
            print 'total wars:\t', total_wars
            print 'p1 hand record:', p1_hands, '-', p2_hands
            print 'p1 war record:', p1_wars, '-', p2_wars
            print '\n\n'
        elif player_1_hand==[]:
            print 'player 2 wins!'
            print 'total hands:\t', total_hands
            print 'total wars:\t', total_wars
            print 'p2 hand record:\t', p2_hands, '-', p1_hands
            print 'p2 war record:\t', p2_wars, '-', p1_wars
            print '\n\n'
        return None
        
    else:
        p1_card = player_1_hand[0]
        p2_card = player_2_hand[0]

        player_1_hand.remove(p1_card)
        player_2_hand.remove(p2_card)

        p1_val = val_dict.get(p1_card.split('_')[0])
        p2_val = val_dict.get(p2_card.split('_')[0])

        # raw_input("")
        if p1_val > p2_val:
            total_hands += 1
            print 'Hand %s: %s(%s) vs %s(%s) -- P1 WINS' % (total_hands, p1_card, len(player_1_hand)+1, p2_card, len(player_2_hand)+1)
            p1_hands += 1
            player_1_hand.append(p1_card)
            player_1_hand.append(p2_card)
            play_hand(player_1_hand, player_2_hand, total_hands, p1_hands, p2_hands, total_wars, p1_wars, p2_wars)
        elif p1_val < p2_val:
            total_hands += 1
            print 'Hand %s: %s(%s) vs %s(%s) -- P2 WINS' % (total_hands, p1_card, len(player_1_hand)+1, p2_card, len(player_2_hand)+1)
            p2_hands += 1
            player_2_hand.append(p1_card)
            player_2_hand.append(p2_card)
            play_hand(player_1_hand, player_2_hand, total_hands, p1_hands, p2_hands, total_wars, p1_wars, p2_wars)
        elif (len(player_1_hand)<2):
            play_hand([], player_2_hand, total_hands, p1_hands, p2_hands, total_wars, p1_wars, p2_wars)
        elif (len(player_2_hand)<2):
            play_hand(player_1_hand, [], total_hands, p1_hands, p2_hands, total_wars, p1_wars, p2_wars)
        else:
            war(player_1_hand, player_2_hand, p1_card, p2_card, total_hands, p1_hands, p2_hands, total_wars, p1_wars, p2_wars, [], [])

def war(player_1_hand, player_2_hand, p1_card, p2_card, total_hands, p1_hands, p2_hands, total_wars, p1_wars, p2_wars, p1_pre_war, p2_pre_war):

    if (p1_pre_war == [] and p2_pre_war == []):
        print 'Pre-War: %s(%s) vs %s(%s)' % (p1_card, len(player_1_hand)+1, p2_card, len(player_2_hand)+1)

    # raw_input("")

    if len(player_1_hand) < 5:
        p1_cards = player_1_hand[0:(len(player_1_hand)-1)]
    else:
        p1_cards = player_1_hand[0:3]

    if len(player_2_hand) < 5:
        p2_cards = player_2_hand[0:(len(player_2_hand)-1)]
    else:
        p2_cards = player_2_hand[0:3]

    for c in p1_cards:
        player_1_hand.remove(c)
    for c in p2_cards:
        player_2_hand.remove(c)

    p1_war_card = player_1_hand[0]
    p2_war_card = player_2_hand[0]

    print '\tPlayer 1 Cards:'
    for c in p1_cards:
        print '\t\t', c

    print '\tPlayer 2 Cards:'
    for c in p2_cards:
        print '\t\t', c

    p1_val = val_dict.get(p1_war_card.split('_')[0])
    p2_val = val_dict.get(p2_war_card.split('_')[0])

    player_1_hand.remove(p1_war_card)
    player_2_hand.remove(p2_war_card)

    if p1_val > p2_val:
        # os.system('say "CULT OF THE V 8"')
        print '\t\t\tWar %s: %s(%s) vs %s(%s) -- P1 WINS\n' % (total_wars+1, p1_war_card, len(player_1_hand)+len(p1_cards)+len(p1_pre_war)+2, p2_war_card, len(player_2_hand)+len(p2_cards)+len(p2_pre_war)+2)
        total_wars += 1
        p1_wars += 1

        for c in p1_cards:
            player_1_hand.append(c)
        for c in p2_cards:
            player_1_hand.append(c)
        for c in p1_pre_war:
            player_1_hand.append(c)
        for c in p2_pre_war:
            player_1_hand.append(c)

        player_1_hand.append(p1_card)
        player_1_hand.append(p2_card)
        player_1_hand.append(p1_war_card)
        player_1_hand.append(p2_war_card)
        play_hand(player_1_hand, player_2_hand, total_hands, p1_hands, p2_hands, total_wars, p1_wars, p2_wars)
    elif p1_val < p2_val:
        # os.system('say "CULT OF THE V 8"')
        print '\t\t\tWar %s: %s(%s) vs %s(%s) -- P2 WINS\n' % (total_wars+1, p1_war_card, len(player_1_hand)+len(p1_cards)+len(p1_pre_war)+2, p2_war_card, len(player_2_hand)+len(p2_cards)+len(p2_pre_war)+2)
        total_wars += 1
        p2_wars += 1

        for c in p1_cards:
            player_2_hand.append(c)
        for c in p2_cards:
            player_2_hand.append(c)
        for c in p1_pre_war:
            player_2_hand.append(c)
        for c in p2_pre_war:
            player_2_hand.append(c)

        player_2_hand.append(p1_card)
        player_2_hand.append(p2_card)
        player_2_hand.append(p1_war_card)
        player_2_hand.append(p2_war_card)
        play_hand(player_1_hand, player_2_hand, total_hands, p1_hands, p2_hands, total_wars, p1_wars, p2_wars)
    elif (len(player_1_hand)<2):
        play_hand([], player_2_hand, total_hands, p1_hands, p2_hands, total_wars, p1_wars, p2_wars)
    elif (len(player_2_hand)<2):
        play_hand(player_1_hand, [], total_hands, p1_hands, p2_hands, total_wars, p1_wars, p2_wars)
    else:
        print 'Pre-Mega War: %s(%s) vs %s(%s)' % (p1_war_card, len(player_1_hand)+len(p1_cards)+len(p1_pre_war)+2, p2_war_card, len(player_2_hand)+len(p2_cards)+len(p2_pre_war)+2)
        p1_war_cards = []
        p2_war_cards = []

        for c in p1_pre_war:
            p1_war_cards.append(c)
        for c in p1_cards:
            p1_war_cards.append(c)
        p1_war_cards.append(p1_war_card)

        for c in p2_pre_war:
            p2_war_cards.append(c)
        for c in p2_cards:
            p2_war_cards.append(c)
        p2_war_cards.append(p2_war_card)

        war(player_1_hand, player_2_hand, p1_war_card, p2_war_card, total_hands, p1_hands, p2_hands, total_wars, p1_wars, p2_wars, p1_war_cards, p2_war_cards)


if __name__ == "__main__":     
    initiate()


