from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *


#======這裡是呼叫的檔案內容=====
from Breakout import * 

#======python的函數庫==========

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('8LYmo6Utiic54BEIGHBdXfTPPmes/OTu10NLmmAs+3TW6WKuEr8XBBuBHAMku/pKb0xcq0W2zoRKonwRWCqYmBDer8D5SfahVYKgccddIa5BX+zkcNug9gBZN2acsuECcGdh7A9mMDOYI7OC89KlNAdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('3cd406d88f9b09e626125e2330efdeaa')

#監聽所有來自 /callback 的 Post Request
#######
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400, "Invalid signature. Please check your channel access token/channel secret.")
    return "OK"
#########

@app.route("/")
def hello():

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    return "Hello Dylan bot!"

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    if '~' in msg[0]:
        message = TextSendMessage(text="測試")
        line_bot_api.reply_message(event.reply_token, message)#

    if 'G' in msg[0]:
        message = TextSendMessage(Breakout())
        line_bot_api.reply_message(event.reply_token, message)#

