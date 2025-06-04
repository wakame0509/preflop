import streamlit as st
from hand_range_matrix import PREDEFINED_HAND_RANGES
from generate_static_preflop_winrates import estimate_winrate_for_hand_vs_range

st.title("🂡 プリフロップ勝率シミュレーター")

st.markdown("""
任意のスターティングハンドに対して、  
**相手が上位25%のレンジでプレイする前提**での勝率を、モンテカルロ法で推定します。
""")

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

# レンジは25%固定
st.markdown("🎯 相手のハンドレンジは **上位25%** に固定されています。")
villain_range = PREDEFINED_HAND_RANGES["25%"]

# 試行回数
iters = st.selectbox("🎲 シミュレーション回数", [10000, 50000, 100000, 200000], index=2)

# 計算実行
if st.button("✅ 勝率を計算"):
    with st.spinner("計算中..."):
        winrate = estimate_winrate_for_hand_vs_range(selected_hand, villain_range, iters)
        st.success(f"{selected_hand} の勝率（vs 上位25%）：{winrate:.2f} %")
