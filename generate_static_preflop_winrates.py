import eval7
import random
from hand_range_matrix import PREDEFINED_HAND_RANGES

def estimate_winrate(hero_hand, villain_range, iters=100000):
    hero = [eval7.Card(card) for card in hero_hand]
    hero_score = 0

    for _ in range(iters):
        deck = eval7.Deck()
        for card in hero:
            deck.cards.remove(card)

        while True:
            villain = random.sample(deck.cards, 2)
            v1, v2 = str(villain[0]), str(villain[1])
            if v1 + v2 in villain_range or v2 + v1 in villain_range:
                break

        for card in villain:
            deck.cards.remove(card)

        board = deck.sample(5)
        hero_combined = hero + board
        villain_combined = villain + board

        hero_value = eval7.evaluate(hero_combined)
        villain_value = eval7.evaluate(villain_combined)

        if hero_value > villain_value:
            hero_score += 1
        elif hero_value == villain_value:
            hero_score += 0.5

    return hero_score / iters

def get_all_starting_hands():
    ranks = "AKQJT98765432"
    hands = []
    for i, r1 in enumerate(ranks):
        for j, r2 in enumerate(ranks):
            if i < j:
                hands.append(r1 + r2 + "s")
            elif i > j:
                hands.append(r2 + r1 + "o")
            else:
                hands.append(r1 + r2)
    return hands

def estimate_winrate_for_hand_vs_range(hand_str, villain_range, iters=100000):
    rank1, rank2 = hand_str[0], hand_str[1]
    suited = hand_str.endswith("s")
    offsuit = hand_str.endswith("o")
    suits = ['c', 'd', 'h', 's']
    combos = []

    if suited:
        for s in suits:
            combos.append([rank1 + s, rank2 + s])
    elif offsuit:
        for s1 in suits:
            for s2 in suits:
                if s1 != s2:
                    combos.append([rank1 + s1, rank2 + s2])
    else:
        for i in range(len(suits)):
            for j in range(i + 1, len(suits)):
                combos.append([rank1 + suits[i], rank2 + suits[j]])

    results = []
    for combo in combos:
        try:
            wr = estimate_winrate(combo, villain_range, iters // len(combos))
            results.append(wr)
        except:
            continue

    return sum(results) / len(results) if results else 0

def generate_winrates(percent="25%", iters=100000):
    results = {}
    villain_range = PREDEFINED_HAND_RANGES[percent]
    all_hands = get_all_starting_hands()

    for i, hand in enumerate(all_hands, 1):
        print(f"[{i}/{len(all_hands)}] {hand}")
        wr = estimate_winrate_for_hand_vs_range(hand, villain_range, iters)
        results[hand] = round(wr * 100, 1)

    return results
