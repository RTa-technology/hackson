from fastapi import FastAPI, Request, BackgroundTasks,UploadFile
from linebot import WebhookParser
from linebot.models import TextMessage, ImageSendMessage, TextSendMessage
from imgurpython import ImgurClient
from aiolinebot import AioLineBotApi
from urllib import request
import json
import os
from os.path import join, dirname
import cv2
import numpy as np


from dotenv import load_dotenv
import uvicorn

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
def upload_image(file):
    # 一時的に保存
    with open("image.jpg", "wb") as f:
        f.write(file.read())
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

# octet-streamで送られてくる画像を受け取る
@app.post("/send/{flag}")
async def send(request: Request, flag: int):
    
    # application/octet-streamで送られてくるバイナリデータを受け取る
    body = await request.body()


    _bytes = np.frombuffer(body, np.uint8)
    img = cv2.imdecode(_bytes, flags=cv2.IMREAD_COLOR)
    
    # 画像を一時的に保存

    cv2.imwrite(str(flag)+".jpg", img)

    # 画像をアップロード
    filelink = upload_image(open(str(flag)+".jpg", "rb"))



    filelink = upload_image(img)
    print(filelink)
    await handle_events_image(flag, filelink, filelink)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)