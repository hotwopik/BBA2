from pygame import *
import sys
import pyganim
import random
#init
init()
size = width,height = 1000,800
screen=display.set_mode(size)
display.set_caption("Blue Ball Adventure 2")
display.set_icon(image.load("assets/icon.png"))
#levels
levels=[
    [["                    ",
      "                    ",
      "                    ",
      "                    ",
      "_                   ",
      "_                   ",
      "_                   ",
      "_                   ",
      "_                   ",
      "_                   ",
      "_                   ",
      "_                   ",
      "_                   ",
      "_                   ",
      "= P                 ",
      "--------------------"],
      ["                    ",
      "                    ",
      "                    ",
      "                    ",
      "_                   ",
      "_                   ",
      "_                   ",
      "_                   ",
      "_                   ",
      "_                   ",
      "_                   ",
      "_                   ",
      "_                   ",
      "_            --     ",
      "= P         ----    ",
      "--------------------"]]
]
#game conf
mm_bg=image.load("assets/mm_bg.png")
gm_bg=image.load("assets/gm_bg.png")
end = False
timen = time.Clock()
fps=60
pl_size=50
speed = 4
player_width = 35
player_height = 50
jump_power = 8
gravity = 0.2
player_color =  "#00FFE9"
level=0
#game objects
drawed=sprite.Group()
colided=[]
menui=[]
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
        menui.append(self)
    def update(self,mouse,click):
        if mouse[0] > self.x and mouse[0] < (self.dx+self.x) and mouse[1] > self.y and mouse[1] < (self.dy+self.y) and click:
            self.onclick()
        screen.blit(self.pict,(self.x,self.y))
class Platform(sprite.Sprite):
    def __init__(self,x,y,state=0):
        sprite.Sprite.__init__(self)
        if state == 0:
            self.image = image.load("assets/platforms/grass.png")
        elif state == 1:
            self.image = image.load("assets/platforms/old_platform.png")
        elif state == 2:
            self.image = image.load("assets/platforms/old_enter.png")
        else:
            self.image = image.load("assets/platforms/grass.png")
        self.rect = Rect(x,y,pl_size,pl_size)
        colided.append(self)
        drawed.add(self)
class Player(sprite.Sprite):
    def __init__(self,x,y):
        sprite.Sprite.__init__(self)
        self.sp_x = x
        self.sp_y = y
        self.xspeed = 0
        self.yspeed = 0
        self.rect = Rect(x,y,player_width,player_height)
        self.ongraund=False
        self.turn=False
        drawed.add(self)
        #animation
        self.image = Surface((player_width,player_height))
        self.image.set_colorkey(Color(player_color))

        self.animRight = pyganim.PygAnimation([(("assets/player/right/r1.png"),100),(("assets/player/right/r2.png"),100),(("assets/player/right/r3.png"),100)])
        self.animRight.play()
        self.animLeft = pyganim.PygAnimation([(("assets/player/left/l1.png"),100),(("assets/player/left/l2.png"),100),(("assets/player/left/l3.png"),100)])
        self.animLeft.play()
        self.animStayRight = pyganim.PygAnimation([(("assets/player/stay_right.png"),100)])
        self.animStayRight.play()
        self.animStayLeft = pyganim.PygAnimation([(("assets/player/stay_left.png"),100)])
        self.animStayLeft.play()
    def update(self,left,right,up,colided):
        if left:
            self.xspeed = -speed
            self.image.fill(Color(player_color))
            self.animLeft.blit(self.image, (0, 0))
            self.turn=True
        if right:
            self.xspeed = speed
            self.image.fill(Color(player_color))
            self.animRight.blit(self.image, (0, 0))
            self.turn=False
        if not(left or right):
            self.xspeed = 0
            self.image.fill(Color(player_color))
            if self.turn:
                self.animStayLeft.blit(self.image, (0, 0))
            else:
                self.animStayRight.blit(self.image, (0, 0))
        if up:
            if self.ongraund:
                self.yspeed = -jump_power
        if not self.ongraund:
            self.yspeed += gravity
        self.ongraund = False
        self.rect.y += self.yspeed
        self.collide(0, self.yspeed, colided)
        self.rect.x += self.xspeed
        self.collide(self.xspeed, 0, colided)
    def collide(self, xspeed, yspeed, colided):
        for p in colided:
            if sprite.collide_rect(self, p):
                if xspeed > 0:
                    self.rect.right = p.rect.left
                    self.xspeed = 0
                if xspeed < 0:
                    self.rect.left = p.rect.right
                    self.xspeed = 0
                if yspeed > 0:
                    self.rect.bottom = p.rect.top
                    self.ongraund = True
                    self.yspeed = 0
                if yspeed < 0:
                    self.rect.top = p.rect.bottom
                    self.yspeed = 0
        if self.rect.x <= -1:
            self.rect.x = 0
            self.xspeed = 0
class Camera(object):
    def __init__(self,width,height):
        self.rect = Rect(0,0,width,height)
    def move(self,moveble):
        return moveble.rect.move(self.rect.topleft)
    def update(self,player):
        l, t, _, _ = player.rect
        _, _, w, h = self.rect
        l, t = -l+width / 2, -t+height / 2
        l = min(0, l)
        l = max(-(self.rect.width-width), l)
        t = max(-(self.rect.height-height), t)
        t = min(0, t)
        self.rect = Rect(l, t, w, h)
#game proces
def gamepr():
    level_var=random.randint(0,len(levels[level])-1)
    level_width=len(levels[level][level_var][0])*pl_size
    level_height=len(levels[level][level_var])*pl_size
    xgn=ygn=0
    left_press=right_press=up_press=f_press=False
    #level gen
    for l in levels[level][level_var]:
        for n in l:
            if n == "P":
                player = Player(xgn,ygn)
            if n == "-":
                Platform(xgn,ygn)
            if n == "_":
                Platform(xgn,ygn,1)
            if n == "=":
                Platform(xgn,ygn,2)
            xgn+=pl_size
        ygn+=pl_size
        xgn=0
    #game cicle
    camera = Camera(level_width,level_height)
    while not end:
        timen.tick(fps)
        for e in event.get():
            if e.type == QUIT:
                quit()
                sys.exit()
            if e.type == KEYDOWN:
                if e.key == K_UP or e.key == K_w or e.key == K_SPACE:
                    up_press = True
                if e.key == K_f:
                    f_press = True
                if e.key == K_LEFT or e.key == K_a:
                    left_press = True
                if e.key == K_RIGHT or e.key == K_d:
                    right_press = True
                if e.key == K_ESCAPE:
                    drawed.empty()
                    colided.clear()
                    return
            if e.type == KEYUP:
                if e.key == K_UP or e.key == K_w or e.key == K_SPACE:
                    up_press = False
                if e.key == K_LEFT or e.key == K_a:
                    left_press = False
                if e.key == K_f:
                    f_press = False
                if e.key == K_RIGHT or e.key == K_d:
                    right_press = False
        screen.blit(gm_bg,(0,0))
        for e in drawed:
            screen.blit(e.image,camera.move(e))
        player.update(left_press,right_press,up_press,colided)
        camera.update(player)
        display.update()
#menu init
#48, Corbel
def out():
    quit()
    sys.exit()
def ngame():
    gamepr()
def cgame():
    pass
Menu_item(50,300,287,67,"assets/menui/ngame.png",ngame)
Menu_item(50,400,220,60,"assets/menui/cgame.png",cgame)
Menu_item(50,500,126,56,"assets/menui/quit.png",out)
Menu_item(50,50,563,55,"assets/menui/title.png")
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