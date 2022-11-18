from fastapi import FastAPI, Request, BackgroundTasks,UploadFile
from linebot import WebhookParser
from linebot.models import TextMessage, ImageSendMessage, TextSendMessage
from imgurpython import ImgurClient
from aiolinebot import AioLineBotApi
from urllib import request
import json
import os
from os.path import join, dirname

from dotenv import load_dotenv

load_dotenv(verbose=True)

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# APIクライアントとパーサーをインスタンス化
line_api = AioLineBotApi(channel_access_token=os.environ.get("TOKEN"))
parser = WebhookParser(channel_secret=os.environ.get("CHANNEL_SECRET"))

imgur_client = ImgurClient(os.environ.get("IMGUR_CLIENT_ID"), os.environ.get("IMGUR_CLIENT_SECRET"))

# FastAPIの起動
app = FastAPI()


# 画像アップロード
def upload_image(file:UploadFile):
    # 一時的に保存
    with open("image.jpg", "wb") as f:
        f.write(file.file.read())
    # アップロード
    image = imgur_client.upload_from_path("image.jpg", anon=True)
    # 一時的に保存した画像を削除
    os.remove("image.jpg")
    return image["link"]


# 画像送信
async def handle_events_image(flag, original_image_url, preview_image_url):
    message_text = ""
    if flag == 0:
        message_text = "棚に荷物が届きました．"
    elif flag == 1:
        message_text = "棚の荷物が無くなりました．"
    else:
        message_text = "不明なフラグ"
    try:
        line_api.broadcast(
            TextSendMessage(text=message_text)
        )
        line_api.broadcast(
            ImageSendMessage(
                original_content_url=original_image_url,
                preview_image_url=preview_image_url
            )
        )
    except Exception:
        # エラーログ書いたりする
        pass

@app.post("/send")
async def send(upload_file:UploadFile): 
    # 🌟イベント処理をバックグラウンドタスクに渡す
    
    filelink = upload_image(upload_file)
    print(filelink)
    flag = int(upload_file.filename.split(".")[0])
    await handle_events_image(flag, filelink, filelink)