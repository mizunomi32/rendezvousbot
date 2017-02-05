#-*- coding:utf_8 -*-
key = "xxxxxxxxxxxxxxxxxxxxxxxxxxxx"

def getStaticMapAddress(name):#name待ち合わせ場所、station駅名の配列かな

    url = "https://maps.google.com/maps/api/staticmap?center="+str(name)+"&zoom=18&size=604x400&sensor=false&markers="
    url += str(name)
    url+="&key="+key

    return url
