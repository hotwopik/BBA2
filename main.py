from pygame import *
import sys
#init
init()
size = width,height = 1000,800
screen=display.set_mode(size)
display.set_caption("Blue Ball Adventure 2")
display.set_icon(image.load("assets/image/icon.png"))
#game conf
mm_bg=image.load("assets/image/mm_bg.png")
gm_bg=image.load("assets/image/gm_bg.png")
end = False
timen = time.Clock()
fps=60
pl_size=50
#game objects
drawed=sprite.Group()
colided=[]
def passes():
    pass
class Menu_item(sprite.Sprite):
    def __init__(self,x,y,dx,dy,pict,onclick=passes):
        sprite.Sprite.__init__(self)
        self.x=x
        self.y=y
        self.dx=dx
        self.dy=dy
        self.pict=image.load(pict)
        self.onclick=onclick
    def update(self,mouse,click):
        if mouse[0] > self.x and mouse[0] < (self.dx+self.x) and mouse[1] > self.y and mouse[1] < (self.dy+self.y) and click:
            self.onclick()
        screen.blit(self.pict,(self.x,self.y))
class Grass_platform(sprite.Sprite):
    def __init__(self,x,y):
        sprite.Sprite.__init__(self)
        self.image = image.load("assets/image/platforms/grass.png")
        self.rect = Rect(x,y,pl_size,pl_size)
        colided.append(self)
        drawed.add(self)
#game proces
def gamepr():
    xgn=0
    ygn=0
    for a in range(1,17):
        for b in range(0,20):
            if a == 16:
                Grass_platform(xgn,ygn)
            xgn+=pl_size
        ygn+=pl_size
        xgn=0
    while not end:
        timen.tick(fps)
        for e in event.get():
            if e.type == QUIT:
                quit()
                sys.exit()
        screen.blit(gm_bg,(0,0))
        for e in drawed:
            screen.blit(e.image,(e.rect.left,e.rect.top))
        display.update()
#menu init
#48, Corbel
def quitn():
    quit()
    sys.exit()
def ngame():
    gamepr()
def cgame():
    pass
ngame_i = Menu_item(50,300,287,67,"assets/image/menui/ngame.png",ngame)
cgame_i = Menu_item(50,400,220,60,"assets/image/menui/cgame.png",cgame)
quit_i = Menu_item(50,500,126,56,"assets/image/menui/quit.png",quitn)
title_i = Menu_item(50,50,563,55,"assets/image/menui/title.png")
menui=[ngame_i,cgame_i,quit_i,title_i]
#game cicle
while True:
    timen.tick(fps)
    for e in event.get():
        if e.type == QUIT:
            quit()
            sys.exit()
    screen.blit(mm_bg,(0,0))
    msdata = [mouse.get_pos(),mouse.get_pressed()[0]]
    for i in menui:
        i.update(msdata[0],msdata[1])
    display.update()