from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import openai
import os

app = Flask(__name__)

# 環境變數 or 直接貼上（安全起見建議放 env）
line_bot_api = LineBotApi('你的Channel Access Token')
handler = WebhookHandler('你的Channel Secret')
openai.api_key = '你的OpenAI API Key'

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_text = event.message.text

    # 發送訊息給 OpenAI
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": user_text}]
    )

    reply_text = response['choices'][0]['message']['content']
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_text)
    )

if __name__ == "__main__":
    app.run()
