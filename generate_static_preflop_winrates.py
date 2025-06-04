import eval7
import random

# 高速な25%レンジスート付きコンボリスト
def get_fast_25_percent_combos():
    suits = ['c', 'd', 'h', 's']
    top_25_percent_hands = [
        "AA", "KK", "QQ", "JJ", "TT", "99", "88", "77",
        "AKs", "AQs", "AJs", "ATs", "KQs", "KJs", "QJs", "JTs",
        "AKo", "AQo", "AJo", "KQo", "QJo", "T9s", "98s", "87s",
        "A9s", "A8s", "A7s", "A6s", "A5s", "A4s", "A3s", "A2s"
    ]

    def generate_combo_list(hand_str):
        r1, r2 = hand_str[0], hand_str[1]
        combo_list = []
        if len(hand_str) == 2:
            for i in range(len(suits)):
                for j in range(i + 1, len(suits)):
                    combo_list.append(r1 + suits[i] + r2 + suits[j])
        elif hand_str.endswith('s'):
            for s in suits:
                combo_list.append(r1 + s + r2 + s)
        elif hand_str.endswith('o'):
            for s1 in suits:
                for s2 in suits:
                    if s1 != s2:
                        combo_list.append(r1 + s1 + r2 + s2)
        return combo_list

    all_combos = []
    for hand in top_25_percent_hands:
        all_combos.extend(generate_combo_list(hand))
    return sorted(set(all_combos))

# 勝率推定
def estimate_winrate(hero_hand, villain_combos, iters=100000):
    hero = [eval7.Card(card) for card in hero_hand]
    hero_score = 0
    for _ in range(iters):
        deck = eval7.Deck()
        for card in hero:
            deck.cards.remove(card)

        while True:
            combo = random.choice(villain_combos)
            v1, v2 = combo[:2], combo[2:]
            if v1 in str(deck) and v2 in str(deck):
                break

        villain = [eval7.Card(v1), eval7.Card(v2)]
        for card in villain:
            deck.cards.remove(card)

        board = deck.sample(5)
        hero_value = eval7.evaluate(hero + board)
        villain_value = eval7.evaluate(villain + board)

        if hero_value > villain_value:
            hero_score += 1
        elif hero_value == villain_value:
            hero_score += 0.5

    return hero_score / iters

# 全スターティングハンド
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

# 各ハンドで勝率を計算
def estimate_winrate_for_hand_vs_range(hand_str, villain_combos, iters=100000):
    r1, r2 = hand_str[0], hand_str[1]
    suited = hand_str.endswith("s")
    offsuit = hand_str.endswith("o")
    suits = ['c', 'd', 'h', 's']
    combos = []

    if suited:
        for s in suits:
            combos.append([r1 + s, r2 + s])
    elif offsuit:
        for s1 in suits:
            for s2 in suits:
                if s1 != s2:
                    combos.append([r1 + s1, r2 + s2])
    else:
        for i in range(len(suits)):
            for j in range(i + 1, len(suits)):
                combos.append([r1 + suits[i], r2 + suits[j]])

    results = []
    for combo in combos:
        try:
            wr = estimate_winrate(combo, villain_combos, iters // len(combos))
            results.append(wr)
        except:
            continue

    return sum(results) / len(results) if results else 0

# メイン関数
def generate_winrates(iters=100000):
    results = {}
    villain_combos = get_fast_25_percent_combos()
    all_hands = get_all_starting_hands()

    for i, hand in enumerate(all_hands, 1):
        print(f"[{i}/{len(all_hands)}] {hand}")
        wr = estimate_winrate_for_hand_vs_range(hand, villain_combos, iters)
        results[hand] = round(wr * 100, 1)

    return results
