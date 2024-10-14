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
    BroadcastRequest,
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent
)

import scrapingPage
from app import app


logger = logging.getLogger()
logger.setLevel(logging.ERROR)

channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN_SCRAPING')
channel_secret = os.getenv('LINE_CHANNEL_SECRET_SCRAPING')
USER_ID = os.getenv('LINE_USER_ID')

configuration = Configuration(access_token=channel_access_token)
handler = WebhookHandler(channel_secret)


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook request
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
        line_bot_api = MessagingApi(api_client)
        message = scrapingPage('800')
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=message)]
            )
        )
    