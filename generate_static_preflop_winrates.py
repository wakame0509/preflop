import eval7
import random

# 25%レンジに含まれるスターティングハンド（42種類）
HAND_25 = [
    "AA", "KK", "QQ", "JJ", "TT",
    "AKs", "AQs", "AJs", "ATs", "KQs", "KJs", "QJs", "JTs", "T9s",
    "98s", "87s", "76s", "65s", "54s", "A9s", "A8s", "A7s", "A6s", "A5s", "A4s", "A3s", "A2s",
    "AKo", "AQo", "AJo", "KQo", "QJo", "JTo", "T9o", "98o", "87o", "KTs", "QTs", "J9s", "T8s", "97s", "86s"
]

# スート付きハンドに展開する関数
def expand_hand_to_combos(hand_str):
    suits = ['c', 'd', 'h', 's']
    combos = []

    if len(hand_str) == 2:  # ペア
        rank = hand_str[0]
        for i in range(len(suits)):
            for j in range(i + 1, len(suits)):
                combos.append([rank + suits[i], rank + suits[j]])
    else:
        r1, r2, suitedness = hand_str[0], hand_str[1], hand_str[2]
        if suitedness == 's':
            for s in suits:
                combos.append([r1 + s, r2 + s])
        elif suitedness == 'o':
            for s1 in suits:
                for s2 in suits:
                    if s1 != s2:
                        combos.append([r1 + s1, r2 + s2])
    return combos

# 全ハンドを展開
VILLAIN_HANDS_25 = []
for hand in HAND_25:
    VILLAIN_HANDS_25.extend(expand_hand_to_combos(hand))


def estimate_winrate(hero_hand, villain_hands, iters=100000):
    hero = [eval7.Card(card) for card in hero_hand]
    hero_score = 0
    completed = 0

    for _ in range(iters):
        deck = eval7.Deck()
        for card in hero:
            deck.cards.remove(card)

        attempts = 0
        while True:
            villain = random.choice(villain_hands)
            try:
                v_cards = [eval7.Card(villain[0]), eval7.Card(villain[1])]
                if v_cards[0] in deck.cards and v_cards[1] in deck.cards:
                    deck.cards.remove(v_cards[0])
                    deck.cards.remove(v_cards[1])
                    break
            except:
                continue
            attempts += 1
            if attempts > 10:
                break

        board = deck.sample(5)
        hero_combined = hero + board
        villain_combined = v_cards + board

        hero_value = eval7.evaluate(hero_combined)
        villain_value = eval7.evaluate(villain_combined)

        if hero_value > villain_value:
            hero_score += 1
        elif hero_value == villain_value:
            hero_score += 0.5

        completed += 1

    return hero_score / completed if completed else 0.0


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


def estimate_winrate_for_hand_vs_range(hand_str, villain_hands, iters=100000):
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
    else:  # ペア
        for i in range(len(suits)):
            for j in range(i + 1, len(suits)):
                combos.append([rank1 + suits[i], rank2 + suits[j]])

    results = []
    for combo in combos:
        try:
            wr = estimate_winrate(combo, villain_hands, iters // len(combos))
            results.append(wr)
        except:
            continue

    return sum(results) / len(results) if results else 0.0
