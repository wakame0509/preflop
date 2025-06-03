import threading
import time
from flask import Flask
from generate_static_preflop_winrates import main

app = Flask(__name__)

@app.route('/')
def index():
    return "Monte Carlo worker is running..."

def run_worker():
    print("▶️ Monte Carlo勝率計算開始")
    main()
    print("✅ 完了。結果はログに表示されました")
    time.sleep(600)  # Renderが切られないよう10分キープ

if __name__ == "__main__":
    threading.Thread(target=run_worker).start()
    app.run(host='0.0.0.0', port=10000)
