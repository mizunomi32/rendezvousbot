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
#   待ち合わせモブ
###############################################
#
# TODO : Station voting
# TODO : recommend from voting
###############################################
###############################################
from flask import Flask, request, abort
import os, re, json
import sqlite3
from linebot import *
from linebot.exceptions import *
from linebot.models import *

from mapimage import getStaticMapAddress
from logic import *
from final_random_message import *

app = Flask(__name__)

line_bot_api = LineBotApi('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
handler = WebhookParser('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')

def solve(event):

    if event.type == "join":
        # join event
        PostJoinMessage(event)

    elif event.type == "message":
        #  message event

        if  re.compile("目的地").search(event.message.text):
            # Goal is determined

            PostStationCarousel(event)

        elif re.compile("の近くで決定!!").search(event.message.text):
            # Station is determined
            # TODO : Station voting

            PostSpotCarousel(event)

        elif re.compile("を集合場所に決定!!").search(event.message.text):
            # determined
            pos=event.message.text.replace("を集合場所に決定!!","")
            message=[
                TextSendMessage(text="待ち合わせ場所は"+pos+"だね。"),TextSendMessage(text=str(picked_up()))
                ]
            line_bot_api.reply_message(event.reply_token,message)
            line_bot_api.leave_group(event.source.group_id)


#  make station`s Carousel and post it.
def PostStationCarousel(event):

    gole=event.message.text.replace("目的地は","")
    station_list=NameToStation(gole)
    st_columns=[]

    for i in station_list:
        colaction=[
            MessageTemplateAction(label='OK',text=str(i.get("name"))+'の近くで決定!!')
            ]
        col = CarouselColumn(
            thumbnail_image_url=getStaticMapAddress(i.get("name")),
            title=str(i.get("name")),
            text=str(i.get("name"))+"でいいですか？\n代表者と話し合って決めてね",
            actions=colaction
            )
        st_columns.append( col )

    stationcarousel = TemplateSendMessage(
        alt_text='どの駅の近くがいいですか？',
        template=CarouselTemplate(columns=st_columns)
        )
    message = [
        TextSendMessage(text="目的地の最寄り駅の候補をあげたよ\n皆の最寄り駅をタップしてね\nなるべく皆にとって都合のいい候補をだしたいから。"),
        stationcarousel
        ]

    line_bot_api.reply_message(event.reply_token,message)

# make site`s proposed carousel and post it
def PostSpotCarousel(event):

    station=event.message.text.replace("の近くで決定!!","")
    # TODO : recommend from voting
    recdata = [{"name":station,"num":1}]
    spot_list=recommend(recdata)

    spot_columns=[]
    for i in spot_list:
        colaction=[
            MessageTemplateAction(label='OK',text=str(i.get("name"))+'を集合場所に決定!!')
            ]
        col = CarouselColumn(
            thumbnail_image_url=getStaticMapAddress(i.get("name")),
            title=str(i.get("name")),
            text=str(i.get("name"))+"でいいですか？\n代表者と話し合って決めてね",
            actions=colaction
            )
        spot_columns.append( col )

    spotcarousel = TemplateSendMessage(
        alt_text='どこがいいですか？',
        template=CarouselTemplate(columns=spot_columns)
        )
    message = [
        TextSendMessage(text="候補をあげたよ\n皆で待ち合わせ場所を決めて！"),
        spotcarousel
        ]

    line_bot_api.reply_message(event.reply_token,message)

# post join message
def PostJoinMessage(event):

    message = [
        TextSendMessage(text="こんにちは\n私は皆にとってベストな待ち合わせ場所の候補をあげるよ\n候補から待ち合わせ場所を決めたら僕は退出するね！"),
        TextSendMessage(text="まず目的地を教えてください！")
        ]

    line_bot_api.reply_message(event.reply_token,message)

@app.route("/callback", methods=['POST'])
def callback():
    #  Get X-Line-Signature header
    signature = request.headers['X-Line-Signature']

    # Get request`s body and events
    body = request.get_data(as_text=True)
    events = handler.parse(body, signature)


    for event in events:
        try:
            solve(event)
        except InvalidSignatureError:
            abort(400)

    # Event loging (Debag)
    f = open('text.json', 'a')
    for event in events:
        f.write(str(event)+'\n')
    f.close()

    return 'OK'

if __name__ == "__main__":
    app.run()
