import streamlit as st
from hand_range_matrix import PREDEFINED_HAND_RANGES
from generate_static_preflop_winrates import estimate_winrate_for_hand_vs_range

st.title("🂡 プリフロップ勝率シミュレーター")

# ハンド選択
ranks = "AKQJT98765432"
all_hands = []
for i, r1 in enumerate(ranks):
    for j, r2 in enumerate(ranks):
        if i < j:
            all_hands.append(r1 + r2 + "s")
        elif i > j:
            all_hands.append(r2 + r1 + "o")
        else:
            all_hands.append(r1 + r2)

selected_hand = st.selectbox("🎴 ハンドを選んでください", all_hands)

# レンジ選択
range_option = st.radio("🎯 相手のレンジ", ["25%", "30%"])
villain_range = PREDEFINED_HAND_RANGES[range_option]

# 試行回数
iters = st.selectbox("🎲 シミュレーション回数", [1000, 5000, 10000], index=2)

if st.button("✅ 勝率を計算"):
    st.write("計算中...")
    winrate = estimate_winrate_for_hand_vs_range(selected_hand, villain_range, iters)
    st.success(f"{selected_hand} の勝率（vs {range_option}）：{winrate:.2f}%")
