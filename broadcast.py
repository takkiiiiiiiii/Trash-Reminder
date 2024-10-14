from flask import Flask, request, abort
import requests
from bs4 import BeautifulSoup
import os
import logging
import uuid
import scrapingPage
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
    BroadcastRequest,
    TextMessage
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent
)

from app import app


logger = logging.getLogger()
logger.setLevel(logging.ERROR)

channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN_SCRAPING')
channel_secret = os.getenv('LINE_CHANNEL_SECRET_SCRAPING')

configuration = Configuration(access_token=channel_access_token)
handler = WebhookHandler(channel_secret)
 

@app.route("/broadcast", methods=['POST'])
def broadcast():
    message = scrapingPage('800')
    messages = [TextMessage(text=message)]
    with ApiClient(configuration) as api_client:
        api_instance = MessagingApi(api_client)

        broadcast_request = BroadcastRequest(messages=messages)
        x_line_retry_key = str(uuid.uuid4())

        try:
            # api_response = api_instance.broadcast(broadcast_request, x_line_retry_key=x_line_retry_key)
            api_response = api_instance.broadcast_with_http_info(broadcast_request, x_line_retry_key=x_line_retry_key)
            print(api_response)
            return {'status Code': 200, 'body': 'Push message sent successfully'}
        
        except Exception as e:
            print("Exception when calling MessagingApi->broadcast: %s\n" % e)
            return {'status Code': 500, 'body': f'Error: {e}'}
