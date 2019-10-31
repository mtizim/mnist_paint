import pygame as p
import itertools
import tensorflow.keras
import numpy as np

clock = p.time.Clock()
p.font.init()
f = p.font.Font(p.font.get_default_font(),50)
model = tensorflow.keras.models.load_model("modelfile")
# 25x25 na piksel
p.init()

s = p.display.set_mode((900,700))
done = False
# x=Rect(10,10,100,100)
i = 0
rectab = np.array([[0 for _ in range(28)] for _ in range(28)])
while not done:
    p.draw.rect(s,(0,0,0),p.Rect(0,0,900,700))
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
    p.draw.rect(s,(150,150,150),p.Rect(760,350,100,50))
    if p.mouse.get_pressed()[0]:
        # reset
        x,y = p.mouse.get_pos()
        if 760<x<860 and 350<y<400:
            rectab = np.array([[0 for _ in range(28)] for _ in range(28)])
        if 0<x<700:
            x_n = x//25
            y_n = y//25
            deltas = [-2,-1,0,1,2]
            for dx,dy in itertools.product(deltas,deltas):
                try:
                    rectab[y_n+dy][x_n+dx] = max(rectab[y_n+dy][x_n+dx],230//2)
                except:
                    pass
            deltas = [-1,0,1]
            for dx,dy in itertools.product(deltas,deltas):
                try:
                    rectab[y_n+dy][x_n+dx] = max(rectab[y_n+dy][x_n+dx],230/1.2)
                except:
                    pass
            rectab[y_n][x_n] = 230

    if i ==0:
        pred = model.predict_classes(x=np.reshape(rectab,(1,28,28,1)))
    i = (i + 1)%200
    s.blit(f.render(str(pred[0]),False,(255,255,255)),(790,170))

    p.display.flip()

