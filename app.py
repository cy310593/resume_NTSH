
from flask import Flask, request, render_template
import requests

app = Flask(__name__)

# =========================
# 一、中韓翻譯題庫
# =========================

zh_ko_dict = {
    "你好": "안녕하세요",
    "안녕하세요": "你好",
    "謝謝": "감사합니다",
    "對不起": "죄송합니다",
    "早安": "좋은 아침",
    "晚安": "안녕히 주무세요",
    "老師": "선생님",
    "學生": "학생",
    "朋友": "친구",
    "家人": "가족",
    "愛": "사랑"
}


# =========================
# 二、中日翻譯題庫
# =========================

zh_jp_dict = {
    "你好": "こんにちは",
    "謝謝": "ありがとう",
    "對不起": "ごめんなさい",
    "早安": "おはようございます",
    "晚安": "おやすみなさい",
    "老師": "先生（せんせい）",
    "學生": "学生（がくせい）",
    "朋友": "友達（ともだち）",
    "家人": "家族（かぞく）",
    "愛": "愛（あい）"
}


# =========================
# 三、首頁
# =========================

@app.route('/')
def index():
    return render_template('index.html')


# =========================
# 四、競賽頁面
# =========================

@app.route('/competition')
def competition():
    return render_template('competition.html')


# =========================
# 五、中韓、中日翻譯系統
# =========================

@app.route('/ask', methods=['GET', 'POST'])
def ask():

    question = ""
    answer = ""
    language = "ko"

    if request.method == 'POST':

        question = request.form.get('question', '').strip()
        language = request.form.get('language', 'ko')

        if language == 'ko':
            dictionary = zh_ko_dict
            language_name = "韓文"

        elif language == 'jp':
            dictionary = zh_jp_dict
            language_name = "日文"

        else:
            dictionary = {}
            language_name = "指定語言"

        if question:
            answer = dictionary.get(
                question,
                f"抱歉，我目前沒有這個詞的{language_name}對應。"
            )

    return render_template(
        'ask.html',
        question=question,
        answer=answer,
        language=language
    )


# =========================
# 六、互動活動
# =========================

@app.route('/activities', methods=['GET', 'POST'])
def activities():

    question = ""
    answer = ""

    if request.method == 'POST':

        question = request.form.get('question', '').strip()

        answer = "抱歉，我目前沒有這個詞的韓文對應。"

    return render_template(
        'activities.html',
        question=question,
        answer=answer
    )


# =========================
# 七、股票查詢系統
# =========================

@app.route('/stock', methods=['GET', 'POST'])
def stock():

    question = ""
    answer = ""

    if request.method == 'POST':

        # 讀取股票代號
        question = request.form.get('question', '').strip()

        if question:

            # 證交所 API
            url = (
                "https://www.twse.com.tw/exchangeReport/"
                f"STOCK_DAY?response=json&stockNo={question}"
            )

            try:

                # 發送 API 請求
                res = requests.get(url, timeout=10)
                res.raise_for_status()

                data = res.json()

                # 判斷查詢是否成功
                if data.get("stat") == "OK" and data.get("data"):

                    # 取得最近一筆交易資料
                    latest_data = data["data"][-1]

                    # 收盤價
                    answer = latest_data[6]

                else:

                    answer = "查無資料，請確認股票代號。"

            except requests.RequestException:

                answer = "股票資料查詢失敗，請稍後再試。"

            except (ValueError, KeyError, IndexError):

                answer = "股票資料格式異常，請稍後再試。"

        else:

            answer = "請輸入股票代號。"

    return render_template(
        'stock.html',
        question=question,
        answer=answer
    )


# =========================
# 八、領導力
# =========================

@app.route('/leadership')
def leadership():
    return render_template('leadership.html')


# =========================
# 九、社團
# =========================

@app.route('/club')
def club():
    return render_template('club.html')


# =========================
# 十、選修課程
# =========================

@app.route('/electives')
def electives():
    return render_template('electives.html')


# =========================
# 十一、AI 頁面
# =========================

@app.route('/ai')
def ai():
    return render_template('ai.html')


# =========================
# 十二、寶可夢
# =========================

@app.route('/pokemon')
def pokemon():
    return render_template('pokemon.html')


# =========================
# 十三、啟動 Flask
# =========================

if __name__ == '__main__':
    app.run(debug=True)


if __name__ == '__main__':
    app.run(debug=True)
