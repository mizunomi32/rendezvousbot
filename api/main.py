#!/usr/bin/python3.5
#-*- coding:utf_8 -*-

###############################################
###############################################
#
#  ##      ##   ##    ##   #####
#  ##      ##   ###   ##   ##
#  ##      ##   ## ## ##   #####
#  ##      ##   ##   ###   #
#  #####   ##   ##    ##   #####
#
#          #####     ####   ######
#          ##  ##   ##  ##    ##
#          #####    ##  ##    ##
#          ##  ##   ##  ##    ##
#          ##   ##   ####     ##
#          #####     ####     ##
#
###############################################

from flask import Flask, request, abort
import os, re, json
import sqlite3
from linebot import *
from linebot.exceptions import *
from linebot.models import *

app = Flask(__name__)

line_bot_api = LineBotApi('xxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
handler = WebhookParser('xxxxxxxxxxxxxx')
dbname = 'database.db'


def solve(event):
    connection = sqlite3.connect(dbname)
    cursor = connection.cursor()
    if event.type == "join":
        # ルームに参加したとき
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="目的地を教えてください"))
    elif event.type == "message":
        # メッセージを受信したとき
        if  re.compile("目的地").search(event.message.text):
            gole=event.message.text.replace("目的地は","")
            post_stationcarousel(event,gole)

        elif re.compile("の近くで決定!!").search(event.message.text):
            station=event.message.text.replace("の近くで決定!!","")
            post_spotcarousel(event,station)
        elif re.compile("を集合場所に決定!!").search(event.message.text):
            line_bot_api.leave_group(event.source.group_id)
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="I read it!!"))
    cursor.close()

# 駅名カルーセルを送る
def post_stationcarousel(event,gole):
    # DBに候補の駅を追加(setp=1)
    #connection = sqlite3.connect(dbname)
    #cursor = connection.cursor()
    #cursor.close()
    station_list=["a駅","b駅","c駅"]
    #############
    # 駅名取得
    ###########

    st_columns=[]
    for i in station_list:
        col = CarouselColumn(
            thumbnail_image_url='https://vps.miccchi.com/api/bk.png',
            title=i,
            text=i+"でいいですか？\n代表者と話し合って決めてね",
            actions=[
                    MessageTemplateAction(label='OK',text=i+'の近くで決定!!')
                    ]
                    )
        st_columns.append( col )
    stationcarousel = TemplateSendMessage(
        alt_text='どの駅の近くがいいですか？',
        template=CarouselTemplate(
            columns=st_columns
                    )
                )
    message = [TextSendMessage(text=gole+" の近くの駅を探します"),TextSendMessage(text="集合場所はどの駅の近くがいいですか？"),stationcarousel]
    line_bot_api.reply_message(event.reply_token,message)

# 集合場所候補地のカルーセルを送る
def post_spotcarousel(event,station):
    # DBに確定駅と候補地を追加(setp=2)
    #connection = sqlite3.connect(dbname)
    #cursor = connection.cursor()
    #cursor.close()
    spot_list=["1番広場","2番広場","3番広場"]
    #############
    # 場所取得
    ###########

    spot_columns=[]
    for i in spot_list:
        col = CarouselColumn(
            thumbnail_image_url='https://vps.miccchi.com/api/bk.png',
            title=i,
            text=i+"でいいですか？\n代表者と話し合って決めてね",
            actions=[
                    MessageTemplateAction(
                    label='OK',
                    text=i+'を集合場所に決定!!'
                    )
                    ]
                    )
        spot_columns.append( col )
    spotcarousel = TemplateSendMessage(
        alt_text='どこがいいですか？',
        template=CarouselTemplate(
            columns=spot_columns
                    )
                )
    message = [TextSendMessage(text=station+"ですね"),TextSendMessage(text="集合場所はどこがいいですか？"),spotcarousel]
    line_bot_api.reply_message(event.reply_token,message)

# joinメッセージを送る
def post_joinmessage(event):
    # DBにグループ追加(setp=0)
    #connection = sqlite3.connect(dbname)
    #cursor = connection.cursor()
    #cursor.close()
    message = [
        TextSendMessage(text="目的地を教えてください")
        ]
    line_bot_api.reply_message(event.reply_token,message)

@app.route("/callback", methods=['POST'])
def callback():
    #  X-Line-Signature header の値を取得
    signature = request.headers['X-Line-Signature']

    # リクエストのbody部分を取得
    body = request.get_data(as_text=True)
    events = handler.parse(body, signature)

    try:
        for event in events:
            solve(event)
        # eventを記録(デバック用)
        f = open('text.txt', 'a')
        for event in events:
            f.write(str(event)+'\n')
        f.close()
    except InvalidSignatureError:
        abort(400)

    return 'OK'

if __name__ == "__main__":
    app.run()
