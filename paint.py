import pygame as p
import itertools
import tensorflow.keras
import numpy as np


mode = ["mnist","emnist"][0]

id_to_asci={0: 48,
 1: 49,
 2: 50,
 3: 51,
 4: 52,
 5: 53,
 6: 54,
 7: 55,
 8: 56,
 9: 57,
 10: 65,
 11: 66,
 12: 67,
 13: 68,
 14: 69,
 15: 70,
 16: 71,
 17: 72,
 18: 73,
 19: 74,
 20: 75,
 21: 76,
 22: 77,
 23: 78,
 24: 79,
 25: 80,
 26: 81,
 27: 82,
 28: 83,
 29: 84,
 30: 85,
 31: 86,
 32: 87,
 33: 88,
 34: 89,
 35: 90,
 36: 97,
 37: 98,
 38: 100,
 39: 101,
 40: 102,
 41: 103,
 42: 104,
 43: 110,
 44: 113,
 45: 114,
 46: 116}


import matplotlib as mpl
mpl.use("Agg")

import matplotlib.backends.backend_agg as agg
import pylab


clock = p.time.Clock()
p.font.init()
f = p.font.Font(p.font.get_default_font(),30)
f1 = p.font.Font(p.font.get_default_font(),7)
model = tensorflow.keras.models.load_model("modelfile_"+mode)
# 25x25 na piksel
p.init()

s = p.display.set_mode((1400,700),p.DOUBLEBUF,32)
done = False
# x=Rect(10,10,100,100)
i = 0
empty = True
rectab = np.array([[0 for _ in range(28)] for _ in range(28)])
while not done:
    # p.draw.rect(s,(0,0,0),p.Rect(0,0,700,700))
    for event in p.event.get():
        if event.type == p.QUIT:
            done = True

    for x_n in range(28):
        for y_n in range(28):
            col = rectab[y_n][x_n]
            color = (col,col,col)
            dx = x_n*25
            dy = y_n*25
            p.draw.rect(s,color,p.Rect(dx+1,dy+1,25,25))
    if p.mouse.get_pressed()[0]:
        # reset
        x,y = p.mouse.get_pos()
        if 1300<x<1400 and 0<y<50:
            empty = True
            rectab = np.array([[0 for _ in range(28)] for _ in range(28)])
        if 0<x<700:
            empty = False
            x_n = x//25
            y_n = y//25
            deltas = [0,1,2]
            for dx,dy in itertools.product(deltas,deltas):
                try:
                    rectab[y_n+dy][x_n+dx] = max(rectab[y_n+dy][x_n+dx],230//13)
                except:
                    pass
            deltas = [0,1]
            for dx,dy in itertools.product(deltas,deltas):
                try:
                    rectab[y_n+dy][x_n+dx] = max(rectab[y_n+dy][x_n+dx],230/1.1)
                except:
                    pass
            rectab[y_n][x_n] = 230

    if i ==0:
        if not empty:
            pred = model.predict(x=np.reshape(rectab,(1,28,28,1)))[0]
            v = np.argmax(pred)
        else:
            if mode=="mnist":
                pred = [0] * 10 # dla mnista
            if mode=="emnist":
                pred = [0] * 47
            v = -1

        barx = 700
        barw = 60
        bars = 10
        barc = (255,255,255)
        barvc = (20,200,20)
        valscale = 100
        barts = 20
        rowd = 100
        if mode =="mnist":
            rows = 1
            bary = 500
        if mode == "emnist":
            rows = 5
            bary = 150
        a = p.Surface((700,700))
        a.set_alpha(50)
        a.fill((0,0,0))
        s.blit(a,(700,0))
        i = 0
        for rownum in range(rows):
            for col in range(len(pred)//rows+1):
                if i>len(pred)-1:
                    break
                val = pred[i]
                valscaled = val * valscale
                p.draw.rect(s,barc,p.Rect(barx+col*(barw+bars),bary-valscaled+rownum*rowd,barw,valscaled))
                pos = ((barx+col*(barw+bars) + barw/2),bary+barts+rownum*rowd)
                if mode =="mnist":
                    s.blit(f.render(str(i),False,barvc if i == v else barc),pos) #dla mnista
                if mode =="emnist":
                    s.blit(f.render(chr(id_to_asci[i]),False,barvc if i == v else barc),pos) #dla emnista
                i = i + 1

    p.draw.rect(s,(150,150,150),p.Rect(1300,0,100,50))
    i = (i + 1)%20


    p.display.flip()

