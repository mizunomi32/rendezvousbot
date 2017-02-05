# -*- coding: utf-8 -*-
import requests
import math
import json
from xml.etree import ElementTree
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# ランドマークの名前から、緯度、経度を取得、それぞれ数値を返す。
def nameToLatLng(word):
    url = 'http://www.geocoding.jp/api/?v=1.1&q='+word
    r = requests.get(url)
    tree = ElementTree.fromstring(r.content)

    x = tree.find(".//lng").text
    y = tree.find(".//lat").text

    return (x,y)

# 緯度経度から駅のデータを検索、List型で返す。
def nearStation(x,y):
    geourl = 'http://map.simpleapi.net/stationapi?' + 'x=' + x + '&y='+y
    ekiresults = requests.get(geourl)
    ekitree = ElementTree.fromstring(ekiresults.content)
    list = []
    count = 0
    for e in ekitree.findall(".//station"):
        print(e.find('name').text, e.find('line').text)
        data = {"name":e.find('name').text, 'line':e.find('line').text}
        list.append(data)
        count += 1
    if count > 5:
        list = list[0:5]
    return list

#距離計測関数、それぞれ、座標を打ち込む
def distance(x1,y1,x2,y2):
    rx1 = float(x1)/180.0 * math.pi
    rx2 = float(x2)/180.0 * math.pi
    ry1 = float(y1)/180.0 * math.pi
    ry2 = float(y2)/180.0 * math.pi
    dx = rx2 - rx1
    dy = ry2 - ry1
    my = (ry1 + ry2)/2.0
    e2 = 0.00669438002301188
    W = math.sqrt(1- e2 * math.sin(my)**2)
    M = 6335439.32708317 / (W*W*W)
    N = 6378137.000	/ W
    return math.sqrt((dy * M)**2 + (dx * N * math.cos(my))**2)

# 目的地から駅の候補を検索する関数
def NameToStation(word):
    x,y = nameToLatLng(word)
    list = nearStation(x,y)
    return list

# 待ち合わせ場所リコメンド関数
def recommend(Xx):
    # まず、駅名から、座標を取得
    locationData = []
    counter = 0
    datafiler = 0
    latlngdata = []
    for i in range(len(Xx)):
        x1, y1 = nameToLatLng(Xx[i]['name'])
        latlngdata.append({"x":x1,"y":y1})

    for i in range(len(Xx)):
        yolpurl = "https://map.yahooapis.jp/placeinfo/V1/get?lat="+latlngdata[i]["y"]+"&lon="+latlngdata[i]["x"]+"&appid=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx&output=json"
        data = requests.get(yolpurl).json()

        for j in range(0,2):
            counter += 1
            x2,y2=nameToLatLng(str(str(data['ResultSet']['Result'][j]['Label'])))
            score = 0.0
            for k in range(len(latlngdata)):
                score += 1.0/distance(latlngdata[k]["x"],latlngdata[k]["y"],x2,y2) * float(Xx[k]["num"])
            tmp = {'name':str(str(data['ResultSet']['Result'][j]['Label'])),"score":score}
            locationData.append(tmp)
    output = []

    for i in locationData:
        if not i in output:
            output.append(i)
    result = []

    for i in output:
        if not i in result:
            result.append(i)
    ans = sorted(output, key=lambda x:-x['score'])
    if len(ans) > 5:
        ans = ans[0:5]

    return ans
