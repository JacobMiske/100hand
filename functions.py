# Helper functions for 100 hand simulation code
from collections import defaultdict


# Standard scoring for 100 hand and similar electronic poker games
scoring_dict = {'royal_flush': 250, 'straight_flush': 50, '4kind': 25, 'full_house': 9,
                'flush': 5, 'straight': 4, '3kind': 3, 'two_pair': 2, 'pair': 1, 'high_card': 0}


card_order_dict = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "T": 10, "J": 11, "Q": 12,
                       "K": 13, "A": 14}


def check_flush(hand):
    suits = [h[1] for h in hand]
    if len(set(suits)) == 1:
        return "Flush"
    else:
        return False


def check_straight_flush(hand):
    if check_flush(hand) and check_straight(hand):
        return True
    else:
        return False


def check_four_of_a_kind(hand):
    values = [i[0] for i in hand]
    value_counts = defaultdict(lambda: 0)
    for v in values:
        value_counts[v] += 1
    if sorted(value_counts.values()) == [1, 4]:
        return True
    return False


def check_full_house(hand):
    values = [i[0] for i in hand]
    value_counts = defaultdict(lambda: 0)
    for v in values:
        value_counts[v] += 1
    if sorted(value_counts.values()) == [2, 3]:
        return True
    return False


def check_flush(hand):
    suits = [i[1] for i in hand]
    if len(set(suits)) == 1:
        return True
    else:
        return False


def check_straight(hand):
    values = [i[0] for i in hand]
    value_counts = defaultdict(lambda: 0)
    for v in values:
        value_counts[v] += 1
    rank_values = [card_order_dict[i] for i in values]
    value_range = max(rank_values) - min(rank_values)
    if len(set(value_counts.values())) == 1 and (value_range == 4):
        return True
    else:
        # check straight with low Ace
        if set(values) == set(["A", "2", "3", "4", "5"]):
            return True
        return False


def check_three_of_a_kind(hand):
    values = [i[0] for i in hand]
    value_counts = defaultdict(lambda: 0)
    for v in values:
        value_counts[v] += 1
    if set(value_counts.values()) == set([3, 1, 1]):
        return True
    else:
        return False


def check_two_pairs(hand):
    values = [i[0] for i in hand]
    value_counts = defaultdict(lambda: 0)
    for v in values:
        value_counts[v] += 1
    if sorted(value_counts.values()) == [1, 2, 2]:
        return True
    else:
        return False


def check_one_pairs(hand):
    # Uniquely, in 100 hand, only pairs of Jacks or Better will score, otherwise doesn't count as a pair
    # returns boolean as well as list of card index for the pair
    one_pair_indices = []
    values = [i[0] for i in hand]
    value_counts = defaultdict(lambda: 0)
    rank_values = [card_order_dict[i] for i in values]
    for v in values:
        value_counts[v] += 1
    if 2 in value_counts.values():
        # If the mode of the one_pair combo is greater than 10 'T', then it's Jacks or Better
        mode = max(set(rank_values), key=rank_values.count)
        one_pair_value = int(mode)

        if one_pair_value > 10:
            for i, count in enumerate(rank_values, 0):
                if i == one_pair_value:
                    one_pair_indices.append(int(count))
            return True, one_pair_indices
    else:
        return False, one_pair_indices


def score_hand(player_hand):
    # For a hand, determine best value
    # In order to do this, we need to determine if the hand has the highest possible
    # combinations, then work down to no combination at all
    # This avoids addition computation
    # Additionally, if a hand does not have a flush, then you do not need to check for royal flush
    # similarly, if there is no straight, there is no reason to check for a straight flush

    # First, find the highest card
    # TODO: Implement highest card, not needed initially for '100 hand' poker, doesn't score any points

    # Next, check if there are pairs
    one_pair = check_one_pairs(hand=player_hand)
    two_pair = check_two_pairs(hand=player_hand)
    # Next, three or four of a kind
    three_kind = check_three_of_a_kind(hand=player_hand)
    four_kind = check_four_of_a_kind(hand=player_hand)
    # Can only be a full house if there's a pair, verify with if statement
    f_house = check_full_house(hand=player_hand)
    # Check flush
    flush = check_flush(hand=player_hand)
    # Cannot be a straight if there is a pair, two pair, three kind, or four kind
    straight = False
    if not one_pair:
        straight = check_straight(hand=player_hand)
        s_flush = False
        if flush and straight:
            s_flush = check_straight_flush(hand=player_hand)
        # Lastly, verify royal flush
        if s_flush:
            values = [i[0] for i in player_hand]
            if 'A' in values:
                royal_flush = True
                return 'royal_flush'
            return 'straight_flush'
    if four_kind:
        return '4kind'
    if f_house:
        return 'full_house'
    if flush:
        return 'flush'
    if straight:
        return 'straight'
    if three_kind:
        return '3kind'
    if two_pair:
        return 'two_pair'
    if one_pair:
        return 'pair'
    # if reached this point, only high card, nothing won in 100 hand
    return 'high_card'
