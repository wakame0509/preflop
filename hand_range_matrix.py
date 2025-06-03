# hand_range_matrix.py

# ハンドレンジ：25%、30%（PokerStoveなどの標準を参考に手動定義）
PREDEFINED_HAND_RANGES = {
    "25%": [
        "AA", "KK", "QQ", "JJ", "TT", "99", "88", "77",
        "AKs", "AQs", "AJs", "ATs", "KQs", "KJs", "QJs", "JTs", "T9s",
        "AKo", "AQo", "AJo", "KQo", "QJo",
        "66", "55", "44", "33", "22", "98s", "87s", "76s", "65s"
    ],
    "30%": [
        "AA", "KK", "QQ", "JJ", "TT", "99", "88", "77", "66",
        "AKs", "AQs", "AJs", "ATs", "A9s", "KQs", "KJs", "KTs",
        "QJs", "QTs", "JTs", "T9s", "98s",
        "AKo", "AQo", "AJo", "ATo", "KQo", "KJo", "QJo",
        "55", "44", "33", "22", "87s", "76s", "65s", "54s"
    ]
}
