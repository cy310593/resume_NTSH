
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
# 五、中韓、中日翻譯共用路由
# =========================

@app.route('/ask', methods=['GET', 'POST'])
def ask():

    if request.method == 'POST':

        # 讀取學生輸入的問題
        question = request.form.get('question', '').strip()

        # 讀取選擇的語言
        language = request.form.get('language', 'ko')

        # 根據語言選擇題庫
        if language == 'ko':

            dictionary = zh_ko_dict
            language_name = "韓文"

        elif language == 'jp':

            dictionary = zh_jp_dict
            language_name = "日文"

        else:

            dictionary = zh_ko_dict
            language = 'ko'
            language_name = "韓文"

        # 查詢答案
        answer = dictionary.get(
            question,
            f"抱歉，我目前沒有這個詞的{language_name}對應。"
        )

        # 回傳翻譯結果
        return render_template(
            'ask.html',
            question=question,
            answer=answer,
            language=language
        )

    # GET 時給空白欄位
    return render_template(
        'ask.html',
        question="",
        answer="",
        language="ko"
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

        question = request.form.get('question', '').strip()

        if question:

            url = (
                "https://www.twse.com.tw/exchangeReport/"
                f"STOCK_DAY?response=json&stockNo={question}"
            )

            try:

                res = requests.get(url, timeout=10)
                res.raise_for_status()

                data = res.json()

                if data.get("stat") == "OK" and data.get("data"):

                    latest_data = data["data"][-1]

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
