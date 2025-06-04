# app.py for preflop winrate estimation

import streamlit as st
import pandas as pd
from generate_static_preflop_winrates import estimate_winrate_for_hand_vs_range, get_all_starting_hands
from hand_range_matrix import PREDEFINED_HAND_RANGES

st.title("♠️ プリフロップ勝率計算ツール")

st.markdown("""
任意のスターティングハンドに対し、  
**相手が25%レンジからプレイする前提での勝率**をモンテカルロ法で推定します。
""")

# --- ハンド選択 ---
all_hands = get_all_starting_hands()
selected_hand = st.selectbox("🃏 自分のハンドを選んでください", all_hands)

# --- 試行回数選択 ---
iters = st.selectbox("🎲 シミュレーション回数", [10000, 50000, 100000, 200000], index=2)

# --- 計算実行 ---
if st.button("✅ 勝率を計算する"):
    with st.spinner("計算中...しばらくお待ちください。"):
        villain_range = PREDEFINED_HAND_RANGES["25%"]
        winrate = estimate_winrate_for_hand_vs_range(selected_hand, villain_range, iters)
        st.success(f"✅ 推定勝率: {round(winrate * 100, 2)} %")
