# hand_range_matrix.py

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


# 25%レンジに含まれるスターティングハンド（42種類）
STARTING_HANDS_25 = [
    "AA", "KK", "QQ", "JJ", "TT",
    "AKs", "AQs", "AJs", "ATs",
    "KQs", "KJs", "QJs", "JTs",
    "T9s", "98s", "87s", "76s", "65s", "54s",
    "A9s", "A8s", "A7s", "A6s", "A5s", "A4s", "A3s", "A2s",
    "AKo", "AQo", "AJo", "KQo", "QJo", "JTo",
    "T9o", "98o", "87o",
    "KTs", "QTs", "J9s", "T8s", "97s", "86s"
]

# スート付きに展開した全コンボを生成
VILLAIN_HANDS_25 = []
for hand in STARTING_HANDS_25:
    VILLAIN_HANDS_25.extend(expand_hand_to_combos(hand))

# 外部から呼び出せる形式に辞書化
PREDEFINED_HAND_RANGES = {
    "25%": VILLAIN_HANDS_25
}
