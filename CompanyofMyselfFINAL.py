"""
Diana Chang
Leo Feng
CS FSE
2013-2014"""

############################################################################
########## I N I T I A L I Z I N G  &  I M P O R T I N G ###################
from pygame import *
import time, sys
from random import *
screen = display.set_mode((1000,598))
display.set_caption("Company of Myself")
############################################################################
################################ C L A S S #################################
class character:
    def __init__(self,x,y,vy,state):
        self.x = x
        self.y = y
        self.onground = True
        self.vy = vy
        self.jump=False
        self.reset = False
        self.fall = False
        self.state = state #True = actual character, False = shadow
    def move(self):                 
        if keystates['right']:          #movement of the character
            self.x += 4
        if keystates['left']:
            self.x -= 4
        if keystates['up'] and self.onground:
            self.onground=False
            self.vy = -3
            keystates['up'] = False
        self.y+=self.vy
        self.vy+=0.1
        self.check_collide()    
        self.check_offscreen()
        if lever_bool[level-1]:
            self.check_lever(press_a)
        if level == 11:
            self.check_lever2(press_a)
        if pfog_bool[level-1] == True and self.state == False:
            self.check_pink_fog()
        if gfog_bool[level-1] and self.state:
            self.check_green_fog()
    def check_offscreen(self):          #checks of character gets off screen, if so, set it back to just before the perimeter
        if self.x + 40 > 1004:
            self.x = 955
        elif self.x - 4 < 0:
            self.x =0
        if self.y < 0:
            self.y = 0

    def check_pink_fog(self):
        myrect = Rect(self.x+2,self.y,40,46) 
        for blocks in pink_fog[level-1]:        
            if myrect.colliderect(blocks):              #if the character touches any part of the pink fog
                if self.vy>0 and myrect.move(0,-self.vy).colliderect(blocks)==False:
                    self.onground=True
                    self.vy=0
                    self.y=blocks.top-46
                if myrect.move(4,0).colliderect(blocks)==False:     #relocates the character
                    self.x+=4
                elif myrect.move(-4,0).colliderect(blocks)==False:
                    self.x-=4

        for blocks in map1temprects:                                #checks the shadows
            if myrect.colliderect(blocks):
                if self.vy>0 and myrect.move(0,-self.vy).colliderect(blocks)==False:
                    self.onground=True
                    self.vy=0
                    self.y=blocks.top+46
    def check_green_fog(self):              #same idea as check_pink_fog
        myrect = Rect(self.x+2,self.y,40,46)
        for blocks in green_fog[level-1]:
            if myrect.colliderect(blocks):
                if myrect.move(4,0).colliderect(blocks)==False:
                    self.x+=4
                elif myrect.move(-4,0).colliderect(blocks)==False:
                    self.x-=4
                if self.vy<0 and myrect.move(0,-self.vy).colliderect(blocks)==False:
                    self.vy=0
                    self.y=blocks.bottom-46
        
        for blocks in map1temprects:
            if myrect.colliderect(blocks):
                if self.vy>0 and myrect.move(0,-self.vy).colliderect(blocks)==False:
                    self.onground=True
                    self.vy=0
                    self.y=blocks.top+46
        
                
    def check_collide(self):                #checks if character/shadow runs into anything
        myrect = Rect(self.x+2,self.y,40,46)
        y = self.y
        for blocks in map1rects[level-1]:               #checks every block in the list of blocks that they cannot walk through
            if myrect.colliderect(blocks):
                if self.vy>0 and myrect.move(0,-self.vy).colliderect(blocks)==False:
                    self.onground=True                                          #checks if person lands on the block
                    self.vy=0
                    self.y=blocks.top-46
                if myrect.move(4,0).colliderect(blocks)==False:         #checks if person moves left or right and runs into the block
                    self.x+=4
                elif myrect.move(-4,0).colliderect(blocks)==False:
                    self.x-=4
                if self.vy <0 and myrect.colliderect(blocks):
                    if myrect.move(4,0).colliderect(blocks) and myrect.move(-4,0).colliderect(blocks):
                        self.vy = 0
                        self.y = blocks.bottom - 46

        for blocks in map1temprects:                    #checks the shadows
            if myrect.colliderect(blocks):
                if self.vy>0 and myrect.move(0,-self.vy).colliderect(blocks)==False:
                    self.onground=True
                    self.vy=0
                    self.y=blocks.top+46
        self.y = y -1
    def check_crates(self):                 #checks if the person/shadow goes on the crates controlled by the lever
        myrect = Rect(self.x+2,self.y,40,46)
        y = self.y
        if crates_bool[level-1]:
            for blocks in cratesRects[level-1]:
                if myrect.colliderect(blocks):
                    if self.vy>0 and myrect.move(0,-self.vy).colliderect(blocks)==False:
                        self.onground=True
                        self.vy=0
                        self.y=blocks.top-46
                    if myrect.move(4,0).colliderect(blocks)==False:
                        self.x+=4
                    elif myrect.move(-4,0).colliderect(blocks)==False:
                        self.x-=4
                    if self.vy <0 and myrect.move(0,-self.vy).colliderect(blocks) ==False:
                        self.vy = 0
                        self.y = blocks.bottom - 46
    def check_crates2(self):            #this checks the second set of crates
        myrect = Rect(self.x+2,self.y,40,46)
        y = self.y
        if crates2_bool:
            blocks = Rect(285,279,30,93)
            if myrect.colliderect(blocks):
                if self.vy>0 and myrect.move(0,-self.vy).colliderect(blocks)==False:
                    self.onground=True
                    self.vy=0
                    self.y=blocks.top-46
                if myrect.move(4,0).colliderect(blocks)==False:
                    self.x+=4
                elif myrect.move(-4,0).colliderect(blocks)==False:
                    self.x-=4
                if self.vy <0 and myrect.move(0,-self.vy).colliderect(blocks) ==False:
                    self.vy = 0
                    self.y = blocks.bottom - 46
    def check_lever(self,press_a):              #checks if the person changes the state of the lever or not
        global leverVal, crates_bool
        myRect = Rect(self.x+2,self.y,40,46)
        if leverRects[level-1][0].colliderect(myRect) and press_a: 
            leverVal = True                 #True means that the lever has been pulled
            trans = True                    #Trans = True means that it is in the transition state between on and off
            crates_bool[level-1] = False    #False means that the crates in that level no longer exists for that game (since the lever was pulled)
    def check_lever2(self,press_a):         #same idea as check_lever, except it is for the 2nd lever
        global lever2Val,crates2_bool
        myRect = Rect(self.x+2,self.y,40,46)
        if lever2Rects[level-1][0].colliderect(myRect) and press_a: 
            lever2Val = True
            trans2 = True
            crates2_bool[level-1] = False
            
    def falldown(self):         #controls the character falling down
        if self.reset!=True:
            self.vy=0
            self.reset=True
            self.onground=False
            self.fall=True
        self.vy+=0.10
        self.y+=self.vy
            
                
###################################### CHARACTER ###################################
################################## S P R I T E S ################################
charpicR=[] #GOING TO THE RIGHT SPRITES
charpicL = [] #going left sprites
char2picR =[]
char2picL = []
picnum=[0]
##################SHADOWS #############################
shadowR = []
shadowL= []
shadowscopy=[]
shadcount=0
shadpos=[40,400]
shadows=[]
movements = []
moves=[]
###################APPENDING IMAGES#######################
for k in range(1,28):
    charpicR.append(image.load("guy1/guy"+str(k)+".png"))
    charpicL.append(image.load("guy1/guyl"+str(k)+".png"))
    shadowR.append(image.load("shadow1/sh"+str(k)+".png"))
    shadowL.append(image.load("shadow1/shl"+str(k)+".png"))
for k in range(1,5):
    char2picR.append(image.load("girl/girl00"+str(k)+"R.png"))
    char2picL.append(image.load("girl/girl00"+str(k)+"L.png"))
########################VALUES OF THE BLOCKS IN WHICH THE CHARACTER(S) CANNOT WALK THROUGH##############
file=open("texts/Level1.txt","r")
map1rects=[]
map1temprects=[] #Rects for shadows
while True:
    x=file.readline().strip()
    if x != "0":
        temprects = []
        for i in range(int(x)):
            x = file.readline().strip()
            y=list(map(int,x.strip().split(',')))
            temprects.append(Rect(y[0],y[1],y[2]-y[0],y[3]-y[1]))
        map1rects.append(temprects)
    else:
        break
#######Shadow Limit#############
file=open("texts/ShadowLim.txt","r")      #limits the number of shadows a player can use in each level
shadlim=[]
x=file.readline().strip()
while x!="":
    shadlim.append(int(x))
    x=file.readline().strip()


############################# GENERAL ###############################
################### V A R I A B L E  S E T T I N G ####################
keystates={'up':False, 'down':False, 'left':False, 'right':False,'space':False}
count=0
count2 = 0
pic=0
lastdir="R"
lastdir2="R"

mx,my = 0,0
dead = False
press_a = False

#################BOOLEAN#######################################
running = True
up=False
down=False
right=False
left=False
newlevel = False

################TIME############
time1=time.time()
time2=time.time()

###############LOADING IMAGES###########################
menuPic = image.load("pictures/menuPic.jpg")
instruction1 = image.load("pictures/instructions1.png")
instruction2 = image.load("pictures/instructions2.png")

########################CREATING TEXT################
font.init()
era = font.SysFont("erasitc",46)
black = (0,0,0)
blue = (0,0,255)
era = font.SysFont("erasitc",46)

###############################################################################
################################# M U S I C ###################################
mixer.init()
mixer.music.load("Music/Company of Myself - Jack.mp3")
mixer.music.play(-1)

###############################################################################
############################# L E V E L  S T U F F ############################
#------start coordinates
startfile=open("texts/start.txt","r")
start=[]
x=startfile.readline()
while x!='':
    y=list(map(int,x.strip('\n').split(',')))
    start.append((y[0],y[1]-46))#dont forget to subtract 46 for all y's
    x=startfile.readline()
#-----start for girl
start2 = []
start2txt = open("texts/start2.txt")
while True:
    line = start2txt.readline().strip()
    if line == "0":
        start2.append([0,0])   #place olders
    elif line != "*":
        line = line.split(',')
        start2.append([int(line[0]),int(line[1])-46])
    else:
        break
#------door coordinates
doorfile=open("texts/doors.txt","r")
door=[]
x=doorfile.readline()
while x!='':
    y=list(map(int,x.strip('\n').split(',')))
    door.append(Rect(y[0],y[1],y[2]-y[0],y[3]-y[1]))
    x=doorfile.readline()
#################LEVEL SPRITES
levels = []
for i in range(1,13):
    levels.append(image.load("levels/level"+str(i)+".jpg"))
level=1

####################CREATING THE CHARACTERS#########################3
char = character(start[level-1][0],start[level-1][1],0,True)
char2 = character(start2[level-1][0],start2[level-1][1],0,True)
############################END OF GAME & GAME OVER SCREENS ####################
ending = image.load("pictures/ending.jpg")
gameover = image.load("pictures/gameover.jpg")
gameoverBool = False
endingBool = False
endingFlag = False


###################PLAY#######################
playTxt = era.render("play",True,black)
playselTxt = era.render("play",True,blue)
playRect = Rect(200,280,88,46)
play = False

##################INSTRUCTION###########################
instrState = 0 #which page the instruction is on
instrList = [instruction1,instruction2]
instructionTxt = era.render("instructions",True,black)
instructionselTxt = era.render("instructions",True,blue)
instructionRect=Rect(390,280,220,46)
back = era.render("back",True,black)
backRect = Rect(20,530,88,46)
nextTxt = era.render("next", True,black)
nextRect = Rect(890,530,88,46)
instructionVal = False
#################CREDITS#######################3
creditVal = False
credit = image.load("pictures/credits.jpg")
creditTxt = era.render("credits",True,black)
creditselTxt = era.render("credits",True,blue)
creditRect = Rect(700,280,130,46)
################LEVER#######################
leverVal = False
lever2Val = False
trans = False #transition of the lever, only blit this once to show transition from on to off and off to on
trans2 = False

##################################################################################
#################################### F O G ######################################
#########################PINK FOG#####################
pink_fog = []
pfogfile = open("texts/pfogfile.txt")
while True:
    line = pfogfile.readline().strip()
    if line == "0":
        pink_fog.append([])
    elif line != "*":
        tempfog = []
        for i in range(int(line)):
            x = pfogfile.readline().strip()
            y=list(map(int,x.strip().split(',')))
            tempfog.append(Rect(y[0],y[1],y[2]-y[0],y[3]-y[1]))
        pink_fog.append(tempfog)
    else:
        break
                #blank lists indicate no pink fog

pfog_bool = [False,False,False,False,True,False,False,True,False,False,False,False]
########## GREEN FOG###################3
green_fog = [[],[],[],[],[],[],[],[],[Rect(533,201,46,197)],[],[],[]]
gfog_bool = [False, False, False,False,False,False,False,False,True,False,False,False]

##############LEVER########################
lever = [[],[],[],[],[(91,413)],[],[(600,532)],[(831,71)],[],[],[(249,345)],[(523,370)]] #add
lever2 = [[],[],[],[],[],[],[],[],[],[],[(847,437)],[]] #add lever 2
leverRects = [[],[],[],[],[Rect(91,413,32,26)],[],[Rect(600,532,32,26)],[Rect(831,71,32,26)],[],[],[Rect(249,345,32,26)],[Rect(523,370,32,36)]] #add
lever2Rects = [[],[],[],[],[],[],[],[],[],[],[Rect(847,437,32,26)],[]] #add stuff
lever_bool = [False,False,False,False,True,False,True,True,False,False,True,True]
lever2_bool = [False,False,False,False,False,False,False,False,False,False,True,False]
lever_on= image.load("Levers/lever003.png")
lever_off = image.load("Levers/lever001.png")
lever_mid = image.load("Levers/lever002.png")
lever2_on = image.load("Levers/lever003P.png")  #pink levers
lever2_off = image.load("Levers/lever001P.png")
lever2_mid = image.load("Levers/lever002P.png")
press_a_bool = []
for i in range(len(levels)):
    press_a_bool.append(False)
########################CRATES###########################3
crates = [[],[],[],[],[(848,286),(878,286),(908,286),(938,286)],[],[(513,39),(513,71),(513,103),(513,135)],[(710,401),(710,433),(710,466)],[],[],[(790,462),(822,462),(854,462),(886,462),(918,462),(43,370),(73,370),(103,370),(133,370),(163,370),(193,370)],[(416,397),(446,397),(476,397),(507,397),(538,397),(570,397)]] #add crates here
cratesRects = [[],[],[],[],[Rect(848,286,120,31)],[],[Rect(513,39,30,126)],[Rect(710,401,28,95)],[],[],[Rect(790,462,148,31),Rect(43,370,169,31)],[Rect(416,397,184,31)]]
crates2Rects = [[],[],[],[],[],[],[],[],[],[],[Rect(285,279,30,93)],[]]
crate = image.load("pictures/crate.png")
crate2 = image.load("pictures/crateP.png")
crates_bool = [False,False,False,False,True,False,True,True,False,False,True,True]
crates2_bool = [ False,False,False,False,False,False,False,False,False,False,True,False]
########################## PUMPKINS ###################################
pumpkinVal = 0
pumpkin = [[],[],[],[],[],[(577,339),(710,339),(840,339)],[],[],[],[(750,339),(200,339),(430,339)],[],[(0,342),(60,342),(120,342),(180,342),(240,342),(300,342),(360,342),(602,342),(662,342),(722,342),(782,342),(842,342),(902,342),(962,342)]]
pumpkinRects = [[],[],[],[],[],[Rect(577,339,59,57),Rect(710,339,59,57),Rect(840,339,59,57)],[],[],[],[Rect(750,339,59,57),Rect(200,339,59,57),Rect(430,339,59,57)],[],[Rect(0,342,59,57),Rect(60,342,59,57),Rect(120,342,59,57),Rect(180,342,59,57),Rect(240,342,59,57),Rect(300,342,59,57),Rect(360,342,59,57),Rect(602,342,59,57),Rect(662,342,59,57),Rect(722,342,59,57),Rect(782,342,59,57),Rect(842,342,59,57),Rect(902,342,59,57),Rect(962,342,59,57)]]
pumpkin_bool = [False, False, False, False, False, True,False,False,False,True,False,True]
pumpkin_sprite = image.load("Obstacles/pumpkin2.png")
##########################LOADING SHADOWS #####################
loadshad = []
for i in range(1,28):
    loadshad.append(image.load("shadow2/sh"+str(i)+".png"))         #THE LITTLE SHADOW THAT RUNS ACROSS THE LOADING SCREEN
########################CONTROL##########
####DETERMINES THE NUMBER OF PLAYERS IN EACH LEVEL --> TRUE = 2 PLAYERS , FALSE = 1 PLAYER
control=[True,False]
controllvl=[False,False,False,False,False,False,False,False,False,True,True,False]

##################################################################################
############################# F U N C T I O N S  ###############################
def shadowsFunc():                  #this function controls all the shadows
    global newlevel
    for mimic in shadows:
        if count<len(movements[shadows.index(mimic)]):
            keystates['up']=movements[shadows.index(mimic)][count][0]           #this is a record of the movements for the shadows to follow
            keystates['down']=movements[shadows.index(mimic)][count][1]
            keystates['left']=movements[shadows.index(mimic)][count][2]
            keystates['right']=movements[shadows.index(mimic)][count][3]
            press_a = movements[shadows.index(mimic)][count][4]

            if lever_bool[level-1]:                                             #to check if the shadow pulled on a lever
                mimic.check_lever(press_a)
            mimic.move()                        	                    #to move the shadow
            if crates_bool[level-1]:                            #check if shadow is on the crates
                mimic.check_crates()
            if keystates['left']:
                mimicmove[shadows.index(mimic)]="L"                 #this decides which direction the shadow is facing
            if keystates['right']:
                mimicmove[shadows.index(mimic)]="R"
            if movements[shadows.index(mimic)][count][4] and door[level-1].colliderect(Rect(mimic.x,mimic.y,40,46)) and mimic.state == False:
                newlevel = True
            if mimicmove[shadows.index(mimic)]=="L":                        #blitting the sprites
                screen.blit(shadowL[int(pic/2-1)],(mimic.x,int(mimic.y)))
            elif mimicmove[shadows.index(mimic)]=="R":
                screen.blit(shadowR[int(pic/2-1)],(mimic.x,int(mimic.y)))
        else:
            if mimic.onground!=True:
                mimic.falldown()
                mimic.check_collide()
            if crates_bool[level-1]:
                mimic.check_crates()
            keystates['left']=movements[shadows.index(mimic)][-1][2]            #grabbing the value from the history of the character's movement
            keystates['right']=movements[shadows.index(mimic)][-1][3]           #they are used for the shadow's movements
            if keystates['left'] == True:                           	        #direction of the shadow
                mimicmove[shadows.index(mimic)]="L"
            if keystates['right'] == True:
                mimicmove[shadows.index(mimic)]="R"
            if mimicmove[shadows.index(mimic)]=="L":
                screen.blit(shadowL[int(pic/2-1)],(mimic.x,int(mimic.y)))       #blitting
            elif mimicmove[shadows.index(mimic)]=="R":
                screen.blit(shadowR[int(pic/2-1)],(mimic.x,int(mimic.y)))
def pumpkin_blit():             #a simple function blitting all the pumpkins
    global pumpkinVal
    pumpkinVal +=1
    pumpkinVal = pumpkinVal % 120
    if 0<pumpkinVal < 46:
        return True

#####################################MENU CODE#########################
while play != True and running:
    for e in event.get():
        if e.type == QUIT:
            running = False
    screen.blit(menuPic, (0,0))
    screen.blit(playTxt,(200,280))
    screen.blit(instructionTxt,(390,280))
    screen.blit(creditTxt,(700,280))
    #-----play code----------------
    mx,my = mouse.get_pos()
    screen.blit(playTxt,(200,280))
    if playRect.collidepoint(mx,my):
        collide=True
        screen.blit(playselTxt,(200,280))           #blit the highlighted text
        display.flip()
        while collide==True and play!=True:
            mx,my = mouse.get_pos()
            if playRect.collidepoint(mx,my)==False:
                collide=False
            else:
                for evt in event.get():                 #if user clicks on 'play'
                    if evt.type == MOUSEBUTTONDOWN:     #loop breaks, game starts loading
                        play=True
                        collide=False

    #-----instruction code----------
    screen.blit(instructionTxt,(390,280))           #this part is the user's selection to enter the instruction pages
    if instructionRect.collidepoint(mx,my):
        collide=True
        screen.blit(instructionselTxt,(390,280))    #blit the highlighted text
        display.flip()
        while collide==True and instructionVal!=True:
            mx,my = mouse.get_pos()
            if instructionRect.collidepoint(mx,my)==False:
                collide=False
            else:
                for evt in event.get():
                    if evt.type == MOUSEBUTTONDOWN:
                        instructionVal=True
                        collide=False
    #----credits code-----                      #similar ideas to the previous two
    screen.blit(creditTxt,(700,280))
    if creditRect.collidepoint(mx,my):
        collide = True
        screen.blit(creditselTxt,(700,280))
        display.flip()
        while collide==True and creditVal!=True:
            mx,my = mouse.get_pos()
            if creditRect.collidepoint(mx,my)==False:
                collide=False
            elif instructionVal != True:
                for evt in event.get():
                    if evt.type == MOUSEBUTTONDOWN:
                        creditVal=True
                        collide=False

    #------instruction page code----                #this is actually blitting the instruction page on
    while instructionVal or creditVal:
        mx,my = mouse.get_pos()
        if instructionVal:
            screen.blit(instrList[instrState],(0,0))
            screen.blit(back,(20,530))
            if backRect.collidepoint(mx,my):
                for evt in event.get():
                    if evt.type == MOUSEBUTTONDOWN:
                        if instrState == 0:                 #if on page 0 and clicks back, bring back to menu page
                            instructionVal = False
                        else:                               #if on page 1 and clicks back, bring to page 0
                            instrState = 0
            if instrState == 0:                     #if we are on page 0 and user clicks next, move on to page 1
                screen.blit(nextTxt,(890,530))
                if nextRect.collidepoint(mx,my):
                    for evt in event.get():
                        if evt.type == MOUSEBUTTONDOWN:
                            instrState = 1
        #------creds page code----
        if creditVal:
            screen.blit(credit,(0,0))
            screen.blit(back,(20,530))
            if backRect.collidepoint(mx,my):
                for evt in event.get():
                    if evt.type == MOUSEBUTTONDOWN:         #if user clicks 'back', bring back to menu page
                        creditVal = False
        for evt in event.get():
            if evt.type == QUIT:
                creditVal = False
                instructionVal = False
                running = False
        display.flip()
    display.flip()
    
##################################################################################
######################## L O A D I N G  S C R E E N ##############################
loading=image.load("pictures/Scroll.png")
screen.blit(loading,(0,0))
display.flip()

################################################################################
################## G A M E  C O D E ##############################
while time2-time1<2 and running:            #the loading screen where the shadow runs across the screen
    time2=time.time()
    shadcount+=1
    shadpos[0]+=9                       #movement of the shadow
    shadcount=shadcount%27
    screen.blit(loading,(0,0))
    screen.blit(loadshad[shadcount],(shadpos[0],shadpos[1]))
    if shadpos[0]>960:
        shadpos[0]=40               #if shadow runs off the page, restart from near the beginning
    display.flip()
    for evt in event.get():
        if evt.type == QUIT:
            running=False
while running:
    mx,my = mouse.get_pos()
    for evt in event.get():
        if evt.type == QUIT:
            running=False

        #check for key down events
        if evt.type == KEYDOWN: 
            if evt.key == K_UP:
                keystates['up']=True
                up=True
            if evt.key == K_DOWN:
                keystates['down']=True
                down=True
            if evt.key == K_LEFT:
                keystates['left']=True
                left=True
                if control[0]==True:
                    lastdir = "L"           #the direction that the character(s) are facing
                else:
                    lastdir2 = "L"
            if evt.key == K_RIGHT:
                keystates['right']=True
                right=True
                if control[0]==True:            
                    lastdir = "R"
                else:
                    lastdir2 = "R"

            if evt.key == K_SPACE:
                keystates['space'] = True
                for shadoww in shadows:                                     #if a shadow is at the door and user presses space, move on to a new level
                    if door[level-1].colliderect(Rect(shadoww.x,shadoww.y,40,46)):
                        newlevel = True

                if newlevel==False:
                    if door[level-1].colliderect(Rect(char.x,char.y,40,46)):        #if character is at the door and presses space, new level
                        if controllvl[level-1]==False or level==11:                 #level 11 is the execption because although there are 2 characters, one dies
                            newlevel = True
                        else:
                            if door[level-1].colliderect(Rect(char2.x,char2.y,40,46)):
                                newlevel = True
                            else:
                                control=[False,True]                            #change the user's control of the characters
                    else:
                        if controllvl[level-1]==True:
                            if control[0]==True:
                                control=[False,True]
                                map1temprects=[Rect(char.x,char.y,40,46)]
                            elif control[1]==True:
                                control=[True,False]

                        else:
                            if len(shadows)<shadlim[level-1]:                   #create a new shadow
                                moves.append((False,False,False,False,False))
                                movements.append(moves)
                                leverVal = False                                #the lever is off again
                                crates_bool = [False,False,False,False,True,False,True,True,False,False,True,True]  #reset the value of crates_bool for use next time
                                shadows=[character(start[level-1][0],start[level-1][1],0,False) for k in range(len(shadows)+1)]
                                map1temprects=[Rect(300,map1rects[level-1][0].top-46,40,46) for k in range(len(shadows)+1)]
                                char = character(start[level-1][0],start[level-1][1],0,True)            #reset the level and starting points for the characters
                                char2 = character(start2[level-1][0],start2[level-1][1],0,True)
                                moves=[]
                                mimicmove=["R" for i in shadows]    
                                count=0                 #clears the value of count, restart the counting of the character sprites
            if evt.key == K_r:  #Restarting the level
                    moves=[]            #clear/reset everything
                    crates_bool = [False,False,False,False,True,False,True,True,False,False,True,True]
                    char = character(start[level-1][0],start[level-1][1],0,True)
                    char2 = character(start2[level-1][0],start2[level-1][1],0,True)
                    map1temprects=[]
                    movements=[]
                    shadows=[]
                    count=0
                    count2 = 0
            elif evt.key == K_p:  #Pausing the game
                pause=True
                while pause:
                    for evt in event.get():
                        if evt.type == QUIT:
                            running=False
                        if evt.type == KEYDOWN:
                            if evt.key == K_p:
                                pause=False
            if evt.key == K_a:
                press_a = True

        #check for key up events
        if evt.type == KEYUP:
            if evt.key == K_DOWN:
                keystates['down']=False
                down=False
            if evt.key == K_LEFT:
                keystates['left']=False
                left=False
            if evt.key == K_RIGHT:
                keystates['right']=False
                right=False
            if evt.key == K_a:
                press_a = False
            if evt.key == K_SPACE:
                keystates['space']=False
    
    moves.append((keystates['up'],keystates['down'],keystates['left'],keystates['right'],press_a))      #appending the moves of the character for the use of a future shadow

    screen.blit(levels[level-1],(0,0))          #blit the level maps
    if control[0]==True:                    #determine which character to move base on which character is currently selected
        char2.falldown()
        char2.check_collide()
        char.move()
    elif control[1]==True:
        char.falldown()
        char.check_collide()
        char2.move()
    myrect = Rect(char.x+2,char.y,40,46)
    if level != 12:
        myrect2 = Rect(char2.x+2,char2.y,40,46)
    else:                                       #sets the char2 to 0,0,0,0 so she doesn't appear in level 12
        myrect2 = Rect(0,0,0,0)
    if len(pumpkin[level-1])>0:
        if pumpkin_blit():
            for i in range(len(pumpkin[level-1])):          #blits& checks every pumpkin 
                screen.blit(pumpkin_sprite, pumpkin[level-1][i])
                if pumpkinRects[level-1][i].colliderect(myrect) or pumpkinRects[level-1][i].colliderect(myrect2):       #if person touches pumpkin, dies
                    dead = True
        
    if dead:            #if character dies, clear/reset everything
        moves=[]
        char = character(start[level-1][0],start[level-1][1],0,True)
        char2 = character(start2[level-1][0],start2[level-1][1],0,True) 
        map1temprects=[]
        movements=[]
        shadows=[]
        count=0
        count2 = 0
        dead = False

    if controllvl[level-1]!=True:
        map1temprects=[Rect(mimic.x,mimic.y,40,46) for mimic in shadows]
    count+=1
    if lastdir == "R":                                                  #blit character based on the direction he's facing
        screen.blit(charpicR[int(pic/2-1)],(char.x, int(char.y)))
    else:
        screen.blit(charpicL[int(pic/2-1)],(char.x,int(char.y)))                #int(pic/2-1) to allow slower motion in terms of character running sprite
    if controllvl[level-1]==True:                               #if the char2 is supposed to be in the level
        if count2 < 10:
            pic2 = 0
        elif count2 < 20:
            pic2 = 1
        elif count2 < 30:
            pic2 = 2
        elif count2 <40:
            pic2 = 3
        if lastdir2 == "R":
            screen.blit(char2picR[pic2],(char2.x, int(char2.y)))            #blits the second character sprites
        else:
            screen.blit(char2picL[pic2],(char2.x,int(char2.y)))
    pic=count%54                        #there are only 27 sprites, this allows the sprites to be used over and over again in a loop
    pic2 = 0
    count2 += 1
    count2 = count2%40                  #the second character has only 4 sprites
    shadowsFunc()                   #calls the shadow function to update all the shadows
    if len(leverRects[level-1])>0:
        if trans:                   #if the lever is in transition mode
            screen.blit(lever_mid,(lever[level-1][0][0],lever[level-1][0][1]+6))
        elif leverVal == False:             #if lever is off
            screen.blit(lever_off,(lever[level-1][0]))
        elif leverVal:
            screen.blit(lever_on,(lever[level-1][0]))
    if len(crates[level-1])>0:              #looks at the crates and see if character run into them
        if crates_bool[level-1]:
            char.check_crates()
            char2.check_crates()
            for i in range(len(crates[level-1])):
                screen.blit(crate,crates[level-1][i])        #blitting the crates when the lever is not pulled
    if level == 11:             #level 11 has two sets of crates, which makes it the exception
        if crates2_bool[level-1]:
            char.check_crates2()
            char2.check_crates2()
            for i in range(3):
                screen.blit(crate2,[(285,279),(285,310),(285,341)][i])
        if trans2:
            screen.blit(lever2_mid(lever2[level-1][0][0],lever2[level-1][0][1]+6))
        elif lever2Val == False:
            screen.blit(lever2_off,(lever2[level-1][0]))
        elif lever2Val:
            screen.blit(lever_on,(lever2[level-1][0]))
            
    if newlevel:                #if progressing to a new level, reset/clear everything
        leverVal = False
        crates_bool = [False,False,False,False,True,False,True,True,False,False,True,True] #return to original list to reuse
        map1temprects=[]
        level += 1
        moves=[]
        char = character(start[level-1][0],start[level-1][1],0,True)
        char2 = character(start2[level-1][0],start2[level-1][1],0,True) 
        map1temprects=[]
        movements=[]
        shadows=[]
        count=0
        count2 = 0
        newlevel = False
    keystates['up']=False                       #reset all the values back to what the character had, since these values were set to the shadows after being set to the character's
    keystates['down']=down
    keystates['left']=left
    keystates['right']=right
    trans = False                       #sets transition mode to false automatically every loop because the transition sprite should only be blitted once

    if level == 12:                     #if in level 12 and falls off the screen, game over
        if 595<int(char.y) < 605:
            gameoverBool = True

    if gameoverBool:                    #if game over, blit pics, wait for user to click on screen and then move on to the ending screen
        screen.blit(gameover,(0,0))
        display.flip()
        blitend = False
        while blitend ==False:
            for evt in event.get():
                if evt.type == MOUSEBUTTONDOWN:
                    gameoverBool = False
                    blitend = True
                    endingBool = True
    if endingBool:                  #blits the ending screen
        screen.blit(ending,(0,0))
        display.flip()
        endingBool = True

    display.flip()
running = True
quit()
