import eval7
import random
from hand_range_matrix import PREDEFINED_HAND_RANGES

def estimate_winrate(hero_hand, villain_combos, iters=10000):
    hero = [eval7.Card(card) for card in hero_hand]
    hero_score = 0

    for _ in range(iters):
        deck = eval7.Deck()
        for card in hero:
            deck.cards.remove(card)

        # 相手のハンドを1つランダムに選ぶ（衝突チェック不要）
        villain = random.choice(villain_combos)
        if villain[0] in [str(c) for c in hero] or villain[1] in [str(c) for c in hero]:
            continue  # 念のため再抽選（理論上起こらないが保険）

        for card_str in villain:
            deck.cards.remove(eval7.Card(card_str))

        board = deck.sample(5)
        hero_combined = hero + board
        villain_combined = [eval7.Card(c) for c in villain] + board

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

def estimate_winrate_for_hand_vs_range(hand_str, villain_combos, iters=10000):
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
            wr = estimate_winrate(combo, villain_combos, iters // len(combos))
            results.append(wr)
        except:
            continue

    return sum(results) / len(results) if results else 0

def generate_winrates(percent="25%", iters=10000):
    results = {}
    villain_combos = PREDEFINED_HAND_RANGES[percent]  # [['As', 'Ks'], ['Kd', 'Kh'], ...]
    all_hands = get_all_starting_hands()

    for i, hand in enumerate(all_hands, 1):
        print(f"[{i}/{len(all_hands)}] {hand}")
        wr = estimate_winrate_for_hand_vs_range(hand, villain_combos, iters)
        results[hand] = round(wr * 100, 1)

    return results
