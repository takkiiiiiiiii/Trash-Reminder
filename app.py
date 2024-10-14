from flask import Flask, request, abort
import requests
from bs4 import BeautifulSoup
import os
import logging
from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage,
    ImageMessage,
    BroadcastRequest,
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent,
    ContentProvider
)

import uuid

logger = logging.getLogger()
logger.setLevel(logging.ERROR)

# channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN_SCRAPING')
# channel_secret = os.getenv('LINE_CHANNEL_SECRET_SCRAPING')

channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN_TRASH')
channel_secret = os.getenv('LINE_CHANNEL_ACCESS_SECRET_TRASH')

configuration = Configuration(access_token=channel_access_token)
handler = WebhookHandler(channel_secret)


app = Flask(__name__)


# Args: Area where you live in
def scrapingPageforReply(area:str) -> list:
    payload = {"m": area}
    req = requests.post("https://www.city.aizuwakamatsu.fukushima.jp/index_php/gomical/index_i.php?typ=p", data=payload)
    req.encoding = req.apparent_encoding
    bsObj = BeautifulSoup(req.text, "html.parser")
    items = bsObj.select("li.tri1")
    text_list = [items[i].text for i in range(4, 10)]
    trash_info = "\n".join(text_list)
    trash_info = "一週間のゴミ出しカレンダー\n" + trash_info

    return trash_info
    

def scrapingPageforPush(area:str) -> list:
    payload = {"m": area}
    req = requests.post("https://www.city.aizuwakamatsu.fukushima.jp/index_php/gomical/index_i.php?typ=p", data=payload)
    req.encoding = req.apparent_encoding
    bsObj = BeautifulSoup(req.text, "html.parser")
    items = bsObj.select("li.tri1")
    return items[5].text


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        message = "Invalid signature. Please check your channel access token/channel secret."  
        logger.error(message)
        return {'status Code': 400, 'body':message}

    return {'status Code': 200, 'body': 'OK'}


@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    with ApiClient(configuration) as api_client:
        try:
            line_bot_api = MessagingApi(api_client)
            message = scrapingPageforReply('800')
            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text=message),
                              ]
                    )
            )
            
        except Exception as e:
            print("Exception when calling MessagingApi->reply: %s\n" % e)
            return {'status Code': 500, 'body': f'Error: {e}'}


# 新しく/pushエンドポイントを作成して、サーバー側からプッシュメッセージを送信する
@app.route("/broadcast", methods=['POST'])
def push_message():
    with ApiClient(configuration) as api_client:
        try:
            line_bot_api = MessagingApi(api_client)
            message = scrapingPageforPush('800')
            message = "ゴミだししてください\n" + message
            x_line_retry_key = str(uuid.uuid4())
            print(message[19])

            if message[19] == 'び':
                line_bot_api.broadcast_with_http_info(
                    BroadcastRequest(
                        messages=[TextMessage(text=message), 
                                  ImageMessage (
                                      originalContentUrl="https://www2.m0m0nga.com/images/bottle.png",
                                      previewImageUrl="https://www2.m0m0nga.com/images/bottle.png"
                                  ),
                                  ImageMessage(
                                      originalContentUrl="https://www2.m0m0nga.com/images/plastic.png",
                                      previewImageUrl="https://www2.m0m0nga.com/images/plastic.png"
                                  ),
                                  ImageMessage(
                                      originalContentUrl="https://www2.m0m0nga.com/images/paper.png",
                                      previewImageUrl="https://www2.m0m0nga.com/images/paper.png"
                                  )
                                ]
                    ),
                    x_line_retry_key=x_line_retry_key
                )
            elif message[19] == 'か':
                line_bot_api.broadcast_with_http_info(
                    BroadcastRequest(
                        messages=[TextMessage(text=message), 
                                  ImageMessage(
                                      originalContentUrl="https://www2.m0m0nga.com/images/cans.png",
                                      previewImageUrl="https://www2.m0m0nga.com/images/cans.png"
                                  ),
                                  ImageMessage(
                                      originalContentUrl="https://www2.m0m0nga.com/images/petbottle.png",
                                      previewImageUrl="https://www2.m0m0nga.com/images/petbottle.png"
                                  ),
                                  ImageMessage(
                                      originalContentUrl="https://www2.m0m0nga.com/images/plastic.png",
                                      previewImageUrl="https://www2.m0m0nga.com/images/plastic.png"
                                  ),
                                  ImageMessage(
                                      originalContentUrl="https://www2.m0m0nga.com/images/paper.png",
                                      previewImageUrl="https://www2.m0m0nga.com/images/paper.png"
                                  ),
                                  ImageMessage(
                                      originalContentUrl="https://www2.m0m0nga.com/images/incombustible.png",
                                      previewImageUrl="https://www2.m0m0nga.com/images/incombustible.png"
                                  )
                                ]
                    ),
                    x_line_retry_key=x_line_retry_key
                )
            elif message[19] == '燃':
                line_bot_api.broadcast_with_http_info(
                    BroadcastRequest(
                        messages=[TextMessage(text=message), 
                                  ImageMessage(
                                      originalContentUrl="https://www2.m0m0nga.com/images/combustible.png",
                                      previewImageUrl="https://www2.m0m0nga.com/images/combustible.png"
                                  )
                                ]
                    ),
                    x_line_retry_key=x_line_retry_key
                )
            # else:
            #     line_bot_api.broadcast_with_http_info(
            #         BroadcastRequest(
            #             messages=[TextMessage(text=message)]
            #         ),
            #         x_line_retry_key=x_line_retry_key
            #     )
            
            return {'status Code': 200, 'body': 'Push message sent successfully'}
        
        except Exception as e:
            print("Exception when calling MessagingApi->broadcast: %s\n" % e)
            return {'status Code': 500, 'body': f'Error: {e}'}


if __name__ == "__main__":
    app.run(port=7777)
