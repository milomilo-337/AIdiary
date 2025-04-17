from flask import Flask, request, jsonify  # Flaskを使ってWeb APIを作成
import sqlite3  # SQLiteデータベースを使用

app = Flask(__name__)

# データベースを初期化する関数
def init_db():
    conn = sqlite3.connect("diary.db")  # SQLiteデータベースに接続（なければ作成）
    c = conn.cursor()
    # diaryテーブルを作成（id: 主キー、text: 日記内容）
    c.execute('''CREATE TABLE IF NOT EXISTS diary (id INTEGER PRIMARY KEY, text TEXT)''')
    conn.commit()
    conn.close()

# アプリ起動時にデータベースを初期化
init_db()

# 日記を保存するAPI（POSTリクエスト）
@app.route("/save", methods=["POST"])
def save_diary():
    data = request.json  # クライアントから送られてきたJSONデータを取得
    text = data.get("text", "")  # "text"キーの値を取得（なければ空文字）
    conn = sqlite3.connect("diary.db")  # データベース接続
    c = conn.cursor()
    c.execute("INSERT INTO diary (text) VALUES (?)", (text,))  # 日記を保存
    conn.commit()
    conn.close()
    return jsonify({"message": "Saved successfully"}), 200  # 保存成功のメッセージを返す

# 保存された日記を取得するAPI（GETリクエスト）
@app.route("/get", methods=["GET"])
def get_diary():
    conn = sqlite3.connect("diary.db")  # データベース接続
    c = conn.cursor()
    c.execute("SELECT * FROM diary")  # すべての日記を取得
    entries = [{"id": row[0], "text": row[1]} for row in c.fetchall()]  # データを辞書形式に変換
    conn.close()
    return jsonify(entries), 200  # JSON形式で日記データを返す

# Flaskアプリを実行
if __name__ == "__main__":
    app.run(debug=True)