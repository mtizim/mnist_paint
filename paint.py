import pygame as p
import itertools
import tensorflow.keras
import numpy as np

import matplotlib as mpl
mpl.use("Agg")

import matplotlib.backends.backend_agg as agg
import pylab


clock = p.time.Clock()
p.font.init()
f = p.font.Font(p.font.get_default_font(),30)
f1 = p.font.Font(p.font.get_default_font(),7)
model = tensorflow.keras.models.load_model("modelfile")
# 25x25 na piksel
p.init()

s = p.display.set_mode((1400,700),p.DOUBLEBUF,32)
done = False
# x=Rect(10,10,100,100)
i = 0
empty = True
rectab = np.array([[0 for _ in range(28)] for _ in range(28)])
while not done:
    p.draw.rect(s,(0,0,0),p.Rect(0,0,700,700))
    for event in p.event.get():
        if event.type == p.QUIT:
            done = True

    for x_n in range(28):
        for y_n in range(28):
            col = rectab[y_n][x_n]
            color = (col,col,col)
            dx = x_n*25
            dy = y_n*25
            p.draw.rect(s,color,p.Rect(dx+1,dy+1,23,23))
    p.draw.rect(s,(150,150,150),p.Rect(760,50,100,50))
    if p.mouse.get_pressed()[0]:
        # reset
        x,y = p.mouse.get_pos()
        if 760<x<860 and 50<y<150:
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
            pred = [0] * 10
            v = -1
        # fig = pylab.figure(figsize=[4, 4], dpi=100)
        fig = mpl.pyplot.bar([i for i in range(10)],pred)

        barx = 700
        bary = 600
        barw = 60
        bars = 10
        barc = (255,255,255)
        barvc = (20,200,20)
        valscale = 100
        barts = 20
        a = p.Surface((700,350))
        a.set_alpha(50)
        a.fill((0,0,0))
        s.blit(a,(700,350))
        # p.draw.rect(s,(0,0,0,20),p.Rect(700,350,700,700))
        for i,val in zip(range(10),pred):
            valscaled = val * valscale
            p.draw.rect(s,barc,p.Rect(barx+i*(barw+bars),bary-valscaled,barw,valscaled))
            pos = ((barx+i*(barw+bars) + barw/2),bary+barts)
            s.blit(f.render(str(i),False,barvc if i == v else barc),pos)


    i = (i + 1)%20
    # s.blit(f.render(str(pred),False,(255,255,255)),(0,17))
    # s.blit(f.render(str([f"{el}.0" for el in range(10)]),False,(255,255,255)),(0,54))


    p.display.flip()

