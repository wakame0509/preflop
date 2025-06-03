import streamlit as st
from generate_static_preflop_winrates import generate_winrates

st.title("プリフロップ勝率生成ツール（vs 指定レンジ）")

selected_range = st.selectbox("対象レンジを選択してください", ["25%", "30%"])
iterations = st.slider("試行回数（1ハンドあたり）", 10000, 100000, 50000, step=10000)

if st.button("勝率を生成する"):
    st.write("⏳ 勝率計算中...（数分かかることがあります）")
    results = generate_winrates(percent=selected_range, iters=iterations)
    st.success("✅ 勝率生成が完了しました！以下の結果をコピーして utils.py に貼り付けてください。")
    st.json(results)
