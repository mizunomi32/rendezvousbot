# -*- coding: utf-8 -*-
import numpy as np

def picked_up():
   messages = [
       "待ち合わせのときは手を振って教えてあげて",
       "待ち合わせ場所での合図はピースだ！",
       "みんな！迷子になるなよ",

   ]
   # NumPy の random.choice で配列からランダムに取り出し
   return np.random.choice(messages)
