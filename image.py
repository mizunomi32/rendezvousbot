


def getStaticMapAddress(name,station):#name待ち合わせ場所、station駅名の配列かな
    i=0
    url = "http://maps.google.com/maps/api/staticmap?center="+str(name)"&zoom=16&size=400x464&sensor=false&markers="

    url += "str(name)&visible="

    while i < len(station):
        url += "station[i]"
        i+=1
        if i!=len(station) url +="|"

    url+="key="#key


    return url
