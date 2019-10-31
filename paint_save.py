import pygame as p

clock = p.time.Clock()
p.font.init()
f = p.font.Font(p.font.get_default_font(),13)

# 25x25 na piksel
p.init()

s = p.display.set_mode((900,700))
done = False
# x=Rect(10,10,100,100)
rectab = [[0 for _ in range(28)] for _ in range(28)]
while not done:
    for event in p.event.get():
        if event.type == p.QUIT:
            done = True

    for x_n in range(28):
        for y_n in range(28):
            color = (255,255,255) if rectab[x_n][y_n]==0 else (0,0,0)
            dx = x_n*25
            dy = y_n*25
            p.draw.rect(s,color,p.Rect(dx+1,dy+1,23,23))
    p.draw.rect(s,(150,150,150),p.Rect(760,350,100,50))
    if p.mouse.get_pressed()[0]:
        # reset
        x,y = p.mouse.get_pos()
        if 760<x<860 and 350<y<400:
            rectab = [[0 for _ in range(28)] for _ in range(28)]
        if 0<x<700:
            x_n = x//25
            y_n = y//25
            rectab[x_n][y_n] = 1
    p.draw(f.render(15))

    p.display.flip()

