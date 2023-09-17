# 100 hand poker model
import os
import random
# import numpy as np
import terminal_playing_cards
from functions import score_hand

# main variables
suits = ['H', 'S', 'C', 'D']
values = ['9', '10', 'J', 'Q', 'K', 'A']
values_dict = {'9': 1, '10': 2, 'J': 3, 'Q': 4, 'K': 5, 'A': 6}
card_dict = {'AC': 0, 'AD': 1, 'AS': 2, 'AH': 3, '2C': 4, '2D': 5, '2S': 6, '2H': 7, '3C': 8, '3D': 9, '3S': 10,
             '3H': 11,
             '4C': 12, '4D': 13, '4S': 14, '4H': 15, '5C': 16, '5D': 17, '5S': 18, '5H': 19, '6C': 20, '6D': 21,
             '6S': 22, '6H': 23,
             '7C': 24, '7D': 25, '7S': 26, '7H': 27, '8C': 28, '8D': 29, '8S': 30, '8H': 31, '9C': 32, '9D': 33,
             '9S': 34, '9H': 35,
             '10C': 36, '10D': 37, '10S': 38, '10H': 39, 'JC': 40, 'JD': 41, 'JS': 42, 'JH': 43, 'QC': 44, 'QD': 45,
             'QS': 46, 'QH': 47,
             'KC': 48, 'KD': 49, 'KS': 50, 'KH': 51}

# Standard scoring for 100 hand and similar electronic poker games
scoring_dict = {'royal_flush': 250, 'straight_flush': 50, '4kind': 25, 'full_house': 9,
                'flush': 5, 'straight': 4, '3kind': 3, 'two_pair': 2, 'pair': 1, 'high_card': 0}

card_order_dict = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "T": 10, "J": 11, "Q": 12,
                   "K": 13, "A": 14}


def deal_hand(deck):
    # select five cards from deck at random and return hand and remaining deck
    hand = []
    rem_deck = deck
    while len(hand) < 5:
        A = rem_deck[random.randint(0, len(rem_deck) - 1)]
        hand.append(A)
        rem_deck.remove(A)
    return hand, rem_deck


def player_play_card(hand):
    # given player's hand and lead's suit, asks for which card to play, returns card chosen
    print("Your hand: {}".format(hand))
    choice = input("pick cards to hold (integers with spaces in between)")
    return choice


def get_simple_hand_data_structure(terminal_cards_hand):
    shorthand_cards = []
    suit_dict = {'spades': 'S', 'diamonds': 'D', 'hearts': 'H', 'clubs': 'C'}
    for card in terminal_cards_hand.cards:
        # print(vars(card))
        # print(suit_dict[card._suit])
        if card._face == "10":
            face = "T"
        else:
            face = card._face
        shorthand_card = str(face) + str(suit_dict[card._suit])
        shorthand_cards.append(shorthand_card)
    return shorthand_cards


def get_points_from_score(res: str, b: int):
    # Given a string for a potential value combination, return points 'pennies' for that combo
    return b * scoring_dict[res]


def test_function_score_hand():
    # For a bunch of hands, can score_hand give the right, best value combo output?
    # Return True if all test hands are good, otherwise return False
    list_of_true_results = ['pair', 'two_pair', 'high_card', 'straight', 'flush',
                            '4kind', 'royal_flush', 'full_house', '3kind']
    hand_1 = ['KD', 'JS', '2S', 'KC', 'AC']
    hand_2 = ['KD', 'JS', 'JH', 'KC', 'AC']
    hand_3 = ['3D', '4H', 'JS', 'KC', 'AC']
    hand_4 = ['4D', '5S', '6S', '7C', '8C']
    hand_5 = ['KS', 'JS', '5S', '8S', '9S']
    hand_6 = ['KD', 'KH', 'KS', 'KC', 'AC']
    hand_7 = ['TC', 'JC', 'QC', 'KC', 'AC']
    hand_8 = ['4S', '4H', '4D', 'JH', 'JD']
    hand_9 = ['4S', '4H', '4D', '7H', 'JD']
    hands = [hand_1, hand_2, hand_3, hand_4, hand_5, hand_6, hand_7, hand_8, hand_9]
    # for count, hand in enumerate(hands, 1):
    #     print(count)
    #     print(score_hand(player_hand=hand))
    return True


def user_gameplay():
    # Play 100 hand manually with some starter credit
    # First, show player's hand

    credit = 1000

    while credit > 0:
        # Each hand uses a new deck
        deck = terminal_playing_cards.Deck()
        deck.shuffle()
        player_hand = terminal_playing_cards.View([deck.pop() for _ in range(5)])
        player_cards = player_hand.cards

        credit_from_round = 0
        # Player operated game, one set of hands at a time
        bet = input("What is your per hand bet? (1 to 5 cents inclusive)")
        # print one hand for user
        number_of_hands = input("How many hands are played at once? (1 to 100 inclusive)")
        input_cost = int(bet) * int(number_of_hands)
        print(player_hand)
        held_cards = input(
            "Cards 1 thru 5 are shown, list which cards should be held with commas between each (e.g. 1, 3, 4)")
        held_cards_index = [int(i) for i in held_cards.split(",")]
        return_cards_index = [int(i) for i in [1,2,3,4,5] if i not in held_cards_index]
        print(return_cards_index)
        # how many cards to add after cut?
        cards_to_add = 5 - len(held_cards_index)
        # create new hand with remaining cards and new ones
        cards_to_hold = []
        cards_to_return = []
        for i in held_cards_index:
            cards_to_hold.append(player_cards[i - 1])
        for i in return_cards_index:
            cards_to_return.append(player_cards[i - 1])
        print(cards_to_return)
        for card in cards_to_return:
            # insert cards to return (not held) back into the deck at zero index, one at a time
            #TODO: test case should verify that deck.cards length is equal to 52-len(cards_to_hold)
            deck.cards.insert(0, card)
        # Generate object to save held cards for later use in many hands
        print('CARD(S) TO hold')
        print(cards_to_hold)
        # Adjusts held cards to shorthand style
        test_cards = []
        for i in cards_to_hold:
            suit_dict = {'spades': 'S', 'diamonds': 'D', 'hearts': 'H', 'clubs': 'C'}
            print(vars(i))
            if i._face == "10":
                face = "T"
            else:
                face = i._face
            shorthand_card = str(face) + str(suit_dict[i._suit])
            print(shorthand_card)
            test_cards.append(shorthand_card)
        #TODO: need to readd the cards burned back into the deck

        # Add new cards to saved cards to make new hand
        player_hand.cards = cards_to_hold
        print(player_hand)
        held_cards_hand = player_hand
        # deal in new cards after another shuffle
        deck.shuffle()
        new_cards = terminal_playing_cards.View([deck[i] for i in range(cards_to_add)])
        print(new_cards)
        for card in new_cards.cards:
            player_hand.cards.append(card)
        player_hand._max = 5
        # This is the hand to score!
        print(player_hand)
        # Convert complex form of cards to simple form for quick processing
        shorthand_player_hand = get_simple_hand_data_structure(terminal_cards_hand=player_hand)
        # print(shorthand_player_hand)
        result = score_hand(player_hand=shorthand_player_hand)
        print(result)
        # Score points for the first hand pulled before scoring the other 99 or so
        points = get_points_from_score(res=result, b=int(bet))
        print('Points from first hand: ')
        print(points)
        credit += points
        credit_from_round += points

        print('Cards originally held')
        print(test_cards)

        # test_function_score_hand()

        # Generate X other hands with held cards in 'player_hand' and score those
        multitude_of_hands = []
        deck_of_cards_remaining = deck
        print(len(deck.cards))
        for count, i in enumerate(range(int(number_of_hands) - 1), 0):
            print(len(deck.cards))
            new_cards_for_ith_hand = terminal_playing_cards.View([random.choice(deck) for _ in range(cards_to_add)])
            # pull new cards from deck_of_cards_remaining for each new hand
            shorthand_cards_for_ith_hand = get_simple_hand_data_structure(terminal_cards_hand=new_cards_for_ith_hand)
            # print(shorthand_cards_for_ith_hand)
            ith_hand = test_cards + shorthand_cards_for_ith_hand
            multitude_of_hands.append(ith_hand)
        print(multitude_of_hands)

        for hand in multitude_of_hands:
            combo = score_hand(player_hand=hand)
            points_from_hand = get_points_from_score(res=combo, b=int(bet))
            #print('Combo made: {}'.format(combo))
            #print('Points from combo: {}'.format(points_from_hand))
            # Adjust total credit and determine total credit from this round
            credit += points_from_hand
            credit_from_round += points_from_hand
        # Print out situation after round to player
        print('Credit from round: {}'.format(credit_from_round))
        print('Input cost: {}'.format(input_cost))
        print('Credit (cents):')
        print(credit - input_cost)
    return 0


def play_hand_hold_highest_card(player_hand):
    # Given a hand, will return list of one integer 'held_cards_index' for highest card
    # First, need to find highest value card and get index

    return 0

def play_hand_hold_pairs(player_hand):
    # Given a hand, will return list of card indexes for pairs, 1 pair or 2 pairs
    # If only highest card, will return result of play_hand_hold_highest_card()
    # Convert complex form of cards to simple form for quick processing
    shorthand_player_hand = get_simple_hand_data_structure(terminal_cards_hand=player_hand)
    result = score_hand(player_hand=shorthand_player_hand)
    if result == 'pair':
        print('1 Pair detected')
    if result == 'two_pair':
        print('2 pair detected')
    return 0

def play_hand_hold_highest_value_combination(players_hand):
    # Given a hand, will determine existing highest value combination and hold the cards associated with combo
    # If only highest card, will return result of play_hand_hold_highest_card()
    return 0


def main():
    # 100 hand poker game
    print("This is a 100 hand poker game simulator")
    total_score = 0

    play_options = input("Would you like to play 100 hand or simulate gameplay? [0 for play, 1 for simulate]")
    if play_options == '0':
        user_gameplay()
    if play_options == '1':
        print('simulator not ready yet')


if __name__ == '__main__':
    main()
