# python3 syntax added
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
    print('\n\n')
    p1_prompt = "Player 1 Name: "
    p1_name = input(p1_prompt)

    p2_prompt = "Player 2 Name: "
    p2_name = input(p2_prompt)

    print('\nReady?')
    deal_cards(suits, val_dict, p1_name, p2_name)

def deal_cards(suits, val_dict, p1_name, p2_name):
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

    play_hand(player_1_hand, player_2_hand, total_hands, p1_hands, p2_hands, total_wars, p1_wars, p2_wars, p1_name, p2_name, False)

def play_hand(player_1_hand, player_2_hand, total_hands, p1_hands, p2_hands, total_wars, p1_wars, p2_wars, p1_name, p2_name, finish):
    if (total_hands+5*total_wars) > 899:
        print('\n\n\nDRAW! (too many hands played)')
        print('Total Hands:\t', total_hands)
        print('Total Wars:\t', total_wars)
        print('Hands:\t', p1_hands, '('+p1_name+')', '-', p2_hands, '('+p2_name+')')
        print('Wars:\t', p1_wars, '('+p1_name+')', '-', p2_wars, '('+p2_name+')')
        print('\n\n')
        return None

    if (player_1_hand==[] or player_2_hand==[]):
        print('\n\n\nGAME OVER!!!\n')
        if player_2_hand==[]:
            print('%s Wins!!' % (p1_name))
            print('Total Hands:\t', total_hands)
            print('Total Wars:\t', total_wars)
            print('Hands:\t', p1_hands, '('+p1_name+')', '-', p2_hands, '('+p2_name+')')
            print('Wars:\t', p1_wars, '('+p1_name+')', '-', p2_wars, '('+p2_name+')')
            print('\n\n')
        elif player_1_hand==[]:
            print('%s Wins!!' % (p2_name))
            print('Total Hands:\t', total_hands)
            print('Total Wars:\t', total_wars)
            print('Hands:\t', p1_hands, '('+p1_name+')', '-', p2_hands, '('+p2_name+')')
            print('Wars:\t', p1_wars, '('+p1_name+')', '-', p2_wars, '('+p2_name+')')
            print('\n\n')
        return None
        
    else:
        p1_card = player_1_hand[0]
        p2_card = player_2_hand[0]

        player_1_hand.remove(p1_card)
        player_2_hand.remove(p2_card)

        p1_val = val_dict.get(p1_card.split('_')[0])
        p2_val = val_dict.get(p2_card.split('_')[0])

        if finish is False:
            fin = input("")
            if fin != "":
                finish = True


        won_cards = [p1_card, p2_card]
        cards_won = len(won_cards)
        if p1_val > p2_val:
            total_hands += 1
            print('Hand %s: %s(%s) vs %s(%s) -- %s Wins' % (total_hands, p1_card, len(player_1_hand)+1, p2_card, len(player_2_hand)+1, p1_name))
            p1_hands += 1
            for i in range(0,cards_won):
                ind = random.sample(range(0, cards_won-i), 1)[0]
                card_val = won_cards[ind]
                won_cards.remove(card_val)
                player_1_hand.append(card_val)
            play_hand(player_1_hand, player_2_hand, total_hands, p1_hands, p2_hands, total_wars, p1_wars, p2_wars, p1_name, p2_name, finish)
        elif p1_val < p2_val:
            total_hands += 1
            print('Hand %s: %s(%s) vs %s(%s) -- %s Wins' % (total_hands, p1_card, len(player_1_hand)+1, p2_card, len(player_2_hand)+1, p2_name))
            p2_hands += 1
            for i in range(0,cards_won):
                ind = random.sample(range(0, cards_won-i), 1)[0]
                card_val = won_cards[ind]
                won_cards.remove(card_val)
                player_2_hand.append(card_val)
            play_hand(player_1_hand, player_2_hand, total_hands, p1_hands, p2_hands, total_wars, p1_wars, p2_wars, p1_name, p2_name, finish)
        elif (len(player_1_hand)<1):
            print('WAR!! %s(%s) vs %s(%s)' % (p1_card, len(player_1_hand)+1, p2_card, len(player_2_hand)+1))
            print('\n\n%s does not have enough cards to do war' % (p1_name))
            play_hand([], player_2_hand, total_hands, p1_hands, p2_hands, total_wars, p1_wars, p2_wars, p1_name, p2_name, finish)
        elif (len(player_2_hand)<1):
            print('WAR!! %s(%s) vs %s(%s)' % (p1_card, len(player_1_hand)+1, p2_card, len(player_2_hand)+1))
            print('\n\n%s does not have enough cards to do war' % (p2_name))
            play_hand(player_1_hand, [], total_hands, p1_hands, p2_hands, total_wars, p1_wars, p2_wars, p1_name, p2_name, finish)
        else:
            war(player_1_hand, player_2_hand, p1_card, p2_card, total_hands, p1_hands, p2_hands, total_wars, p1_wars, p2_wars, [], [], p1_name, p2_name, finish)

def war(player_1_hand, player_2_hand, p1_card, p2_card, total_hands, p1_hands, p2_hands, total_wars, p1_wars, p2_wars, p1_pre_war, p2_pre_war, p1_name, p2_name, finish):

    if (p1_pre_war == [] and p2_pre_war == []):
        print('WAR!! %s(%s) vs %s(%s)' % (p1_card, len(player_1_hand)+1, p2_card, len(player_2_hand)+1))

    if finish is False:
        fin = input("")
        if fin != "":
            finish = True

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

    print('\t%s Cards:' % (p1_name))
    for c in p1_cards:
        print('\t\t', c)

    print('\t%s Cards:' % (p2_name))
    for c in p2_cards:
        print('\t\t', c)

    p1_val = val_dict.get(p1_war_card.split('_')[0])
    p2_val = val_dict.get(p2_war_card.split('_')[0])

    player_1_hand.remove(p1_war_card)
    player_2_hand.remove(p2_war_card)

    won_cards = []
    for c in p1_cards:
        won_cards.append(c)
    for c in p2_cards:
        won_cards.append(c)
    for c in p1_pre_war:
        won_cards.append(c)
    for c in p2_pre_war:
        won_cards.append(c)
    won_cards.append(p1_card)
    won_cards.append(p2_card)
    won_cards.append(p1_war_card)
    won_cards.append(p2_war_card)
    cards_won = len(won_cards)
    if p1_val > p2_val:
        # os.system('say "CULT OF THE V 8"')
        print('\t\t\tWar %s: %s(%s) vs %s(%s) -- %s Wins\n' % (total_wars+1, p1_war_card, len(player_1_hand)+len(p1_cards)+len(p1_pre_war)+2, p2_war_card, len(player_2_hand)+len(p2_cards)+len(p2_pre_war)+2, p1_name))
        total_wars += 1
        p1_wars += 1

        for i in range(0,cards_won):
            ind = random.sample(range(0, cards_won-i), 1)[0]
            card_val = won_cards[ind]
            won_cards.remove(card_val)
            player_1_hand.append(card_val)


        play_hand(player_1_hand, player_2_hand, total_hands, p1_hands, p2_hands, total_wars, p1_wars, p2_wars, p1_name, p2_name, finish)
    elif p1_val < p2_val:
        # os.system('say "CULT OF THE V 8"')
        print('\t\t\tWar %s: %s(%s) vs %s(%s) -- %s Wins\n' % (total_wars+1, p1_war_card, len(player_1_hand)+len(p1_cards)+len(p1_pre_war)+2, p2_war_card, len(player_2_hand)+len(p2_cards)+len(p2_pre_war)+2, p2_name))
        total_wars += 1
        p2_wars += 1

        for i in range(0,cards_won):
            ind = random.sample(range(0, cards_won-i), 1)[0]
            card_val = won_cards[ind]
            won_cards.remove(card_val)
            player_2_hand.append(card_val)

        play_hand(player_1_hand, player_2_hand, total_hands, p1_hands, p2_hands, total_wars, p1_wars, p2_wars, p1_name, p2_name, finish)
    elif (len(player_1_hand)<2):
        print('MEGA WAR!!! %s(%s) vs %s(%s)' % (p1_war_card, len(player_1_hand)+len(p1_cards)+len(p1_pre_war)+2, p2_war_card, len(player_2_hand)+len(p2_cards)+len(p2_pre_war)+2))
        print('\n\n%s does not have enough cards to do war' % (p1_name))
        play_hand([], player_2_hand, total_hands, p1_hands, p2_hands, total_wars, p1_wars, p2_wars, p1_name, p2_name, finish)
    elif (len(player_2_hand)<2):
        print('MEGA WAR!!! %s(%s) vs %s(%s)' % (p1_war_card, len(player_1_hand)+len(p1_cards)+len(p1_pre_war)+2, p2_war_card, len(player_2_hand)+len(p2_cards)+len(p2_pre_war)+2))
        print('\n\n%s does not have enough cards to do war' % (p2_name))
        play_hand(player_1_hand, [], total_hands, p1_hands, p2_hands, total_wars, p1_wars, p2_wars, p1_name, p2_name, finish)
    else:
        print('MEGA WAR!!! %s(%s) vs %s(%s)' % (p1_war_card, len(player_1_hand)+len(p1_cards)+len(p1_pre_war)+2, p2_war_card, len(player_2_hand)+len(p2_cards)+len(p2_pre_war)+2))
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

        war(player_1_hand, player_2_hand, p1_war_card, p2_war_card, total_hands, p1_hands, p2_hands, total_wars, p1_wars, p2_wars, p1_war_cards, p2_war_cards, p1_name, p2_name, finish)


if __name__ == "__main__":     
    initiate()

