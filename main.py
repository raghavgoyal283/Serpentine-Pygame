import pygame, random, sys, pygame.mixer, pygame.display
from pygame.locals import *
maxi=0 # maximum score for that level stored in records
score = 0 #score of the player
wh=10 #width of bar
ww=150 #length of bar
img1 = [] #list holding the static bars
ycoofdb=-500 
dropbaout=1
img_mb=[]
b_pos_t = [] #holds coordinates of the static bars
ri = 0 #
shutdown = 0 #to check if the user has quit the game window 
dead = 0 #to check for game over
sw = 1300 #screen width
sh = 700 #screen height
hob=10 #height of the ball
wob=10 #width of the ball
xymarginforb=40 #margin where static bars can't appear
mlrintbar=50 
height_of_score_show=90 #height of the score showing window
a_pos = (random.randint(0,sw-wob), random.randint(height_of_score_show,sh-hob)) #random inyteger for the position of ball
score_added_by_ex_sc_ball=10 #extra score added on eating extra score ball
speed_of_drop=30
def calc_high_score(r,uip,uip_gl): #calculate_highest_score_of_given_level 
    global rr
    rr = open("highscores.txt","r")
    global maxi
    maxi=0
    high_sc_names=[]
    for aline in rr.readlines():
        aline=aline.strip()
        if int(aline.split('#')[1])>maxi and int(aline.split('#')[2])==uip_gl:
            maxi=int(aline.split('#')[1])             
        if int(aline.split('#')[1])==maxi and int(aline.split('#')[2])==uip_gl: #selecting max score for same level as user chose
             high_sc_names.append(aline.split('#')[0]) 
    if len(high_sc_names)>5:
        high_sc_names=high_sc_names[-6:-1]                                      
    return(high_sc_names)
    rr.close()

def collision(x1,x2,y1,y2,w1,w2,h1,h2): #check collision of two objects
    if x1+w1>x2 and x1<x2+w2 and y1+h1>y2 and y1<y2+h2:
        return True
    else:
        return False
def over(screen,score,uip,uip_gl): #game over screen display
    global maxi
    global go
    global shutdown
    f = pygame.font.SysFont("Showcard Gothic",30)
    r = open("highscores.txt","a")
    r.write(uip+"#"+str(score)+"#"+str(uip_gl)+"\n")
    r.close()        
    hsn=calc_high_score(r,uip,uip_gl)
    pygame.display.update()
    screen.fill((0,0,0))
    t = f.render("Your score was: " + str(score), True, (255,255,255))
    t2 = f.render("Game Over", True, (255,255,255))
    t3 = f.render("Press spacebar to continue", True, (255,255,255))
    screen.blit(t,(50,100+height_of_score_show))
    screen.blit(t2,(50,50+height_of_score_show))
    dftop=200
    tt= f.render("Highest Score: "+str(maxi)+" (Level "+str(uip_gl)+")  by:", True, (255,255,255))
    screen.blit(tt,(50,dftop-30+height_of_score_show))
    
    for hsns in hsn:
        tt = f.render(hsns, True, (255,255,255))
        screen.blit(tt,(50,dftop+height_of_score_show))
        dftop+=30
    screen.blit(t3,(50,550+height_of_score_show))
    pygame.display.update()
    out = 0
    while out!=1:
        for e in pygame.event.get():
            if e.type == QUIT:
                pygame.quit()
                shutdown = 1
            elif e.type == KEYDOWN:
                if e.key == K_SPACE:
                    out = 1
                    break


    
def gamemainloop(uip,uip_gl): #main game loop
    global dead, shutdown
    global dropbaout
    no_of_lives=(uip_gl//8)+(uip_gl//5)+3 #no. of lives the user gets in beginning
    no_of_lives_left=no_of_lives #no. of lives left with the user
    pygame.init()
    #--------Music credit: http://soundimage.org/wp-content/uploads/2014/04/Game-Menu.mp3----------
    pygame.mixer.music.load('Game.mp3')
    pygame.mixer.music.play(-1)
    #--------Music credit: http://soundimage.org/wp-content/uploads/2014/04/Game-Menu.mp3----------
    f = pygame.font.SysFont("Arial",20)
    f2 = pygame.font.SysFont("Chiller",250)
    rg3 = pygame.font.SysFont("Arial",40)
    rg1 = pygame.font.SysFont("Brush Script MT",100)
    rg2 = pygame.font.SysFont("Showcard Gothic",150)
    s = pygame.display.set_mode((sw,sh))
    pygame.display.set_caption("Serpentine")
    
    presenter = pygame.image.load("presenter.jpg") #presenting window
    presenter = pygame.transform.scale(presenter,(sw,sh))
    
    q1 = rg1.render("Raghav",True,(255,255,255))
    q2 = rg1.render("and",True,(255,255,255))
    q3 = rg1.render("Nishikant",True,(255,255,255))
    q4 = rg2.render("PRESENTS",True,(255,255,255))
    #-----------presenter window------------
    for i in range(75999):
        print("")
        
        for e in pygame.event.get():
            if e.type == QUIT:
                pygame.quit()
                shutdown = 1
            else:
                s.blit(presenter,(0,0))
                s.blit(q1,((800/1500)*sw,(200/800)*sh))
                s.blit(q2,((850/1500)*sw,(300/800)*sh))
                s.blit(q3,((780/1500)*sw,(400/800)*sh))
                s.blit(q4,((6/15)*sw,(600/800)*sh))
                pygame.display.update()
                
    game_back = pygame.Surface((sw,sh))
    
    game_back.fill((0,255,128))
    front = pygame.image.load("front.jpg") #main game picture
    front = pygame.transform.scale(front,(sw,sh))

    
    appleimage = pygame.Surface((wob,hob)) #score ball
    appleimage2 = pygame.Surface((wob+10,hob+10)) #extra life ball
    appleimage3 = pygame.Surface((wob+10,hob+10)) #extra score ball
   
    def givepos():  #gives position of score ball, extra score ball and life ball
        global a_pos
        okay2 = 0
        while okay2 == 0:
            a_pos = (random.randint(0,sw-wob), random.randint(height_of_score_show,sh-hob))
            okay2 = 1
            for i in range(len(b_pos_t)):
                if collision(a_pos[0],b_pos_t[i][0],a_pos[1],b_pos_t[i][1],10,10,10,ww):
                    okay2 = 0    
        #----- gives life ball position -------
        global lb_pos
        okay3 = 0
        while okay3 == 0:
            lb_pos = (random.randint(0,sw-wob-10), random.randint(height_of_score_show,sh-hob-10))
            okay3 = 1
            for i in range(len(b_pos_t)):
                if collision(lb_pos[0],b_pos_t[i][0],lb_pos[1],b_pos_t[i][1],wob+10,wh,hob+10,ww):
                    okay3 = 0   
        global riforlifeball
        riforlifeball=random.randint(1,11) #less chances of getting life ball
        #----- gives life ball position-------    
        #----- gives extra score ball position -------
        global esb_pos
        okay4 = 0
        while okay4 == 0:
            esb_pos = (random.randint(0,sw-wob-10), random.randint(height_of_score_show,sh-hob-10))
            okay4 = 1
            for i in range(len(b_pos_t)):
                if collision(esb_pos[0],b_pos_t[i][0],esb_pos[1],b_pos_t[i][1],wob+10,wh,hob+10,ww):
                    okay4 = 0   
            if collision(lb_pos[0],esb_pos[0],lb_pos[1],esb_pos[1],10,10,10,ww): #checking if more score ball do not collide with life ball
                okay4 = 0
        global riformscball
        riformscball=random.randint(1,11) #less chances of getting more score ball
        #----- gives extra score ball position-------
        
    def add_new_bar(): # adds a new bar 
        rii=random.randint(0,3)
        if rii==1 or rii==2: #sometimes add bars and sometimes not #bars addition probability = 2/3
            imgl.append(pygame.Surface((wh,ww))) 
            imgl[-1].fill((0,0,0)) #filling above added surface
            okay1 = 0
            while okay1 == 0: #checks if bar does not collide with existing bars
                b_pos_t.append((random.randint(xymarginforb,sw-xymarginforb-wh),random.randint(xymarginforb+height_of_score_show,sh-xymarginforb-ww)))
                okay1 = 1
                for counter_next1 in range((len(b_pos_t)-2),-1,-1):
                    if collision(b_pos_t[len(b_pos_t)-1][0],b_pos_t[counter_next1][0],b_pos_t[len(b_pos_t)-1][1],b_pos_t[counter_next1][1],10,10,ww,ww):
                        okay1 = 0
                        del b_pos_t[len(b_pos_t)-1]
                        break
    def dropbar(): #dropping bar function
        global xcoofdb, img_mb
        img_mb=[]
        img_mb.append(pygame.Surface((wh,ww+100))) 
        img_mb[-1].fill((255,0,0)) #filling above added surface
        okay6 = 0
        xcoofdb = random.randint(0,sw-wh)
        while okay6==0: #checks it's x-coordinate does not coincide with other bars and also with balls
            okay6=1
            for bpos in b_pos_t:
                if bpos[0]==xcoofdb:
                    xcoofdb += wh
                    okay6=0
            if xcoofdb == a_pos[0]:
                xcoofdb += wh
                okay6=0
        if (xcoofdb+wh)>=sw:
            dropbar()
    
    def setbars(): #sets the bars when the game starts
        global imgl, wh, ww, ri, b_pos_t
        #-----------------obstacles-----------
        wh=10
        ww=70
        ri=uip_gl #decides game level #can add variable no. of obstacles at start of game
        imgl=[]
        for rin in range(ri):
            imgl.append(pygame.Surface((wh,ww)))
        for img2 in imgl:
            img2.fill((0,0,0))
        b_pos_t=[]
        b_pos_t.append((random.randint(xymarginforb,sw-xymarginforb-wh),random.randint(xymarginforb+height_of_score_show,sh-xymarginforb-ww)))
        for counter in range(1,len(imgl)): #checking for collision
            okay = 0
            while okay == 0:
                b_pos_t.append((random.randint(xymarginforb,sw-xymarginforb-wh),random.randint(xymarginforb+height_of_score_show,sh-xymarginforb-ww)))
                okay = 1
                for counter_next in range((counter-1),-1,-1):
                    if collision(b_pos_t[counter][0],b_pos_t[counter_next][0],b_pos_t[counter][1],b_pos_t[counter_next][1],wob,hob,wh,ww):
                        okay = 0
                        del b_pos_t[counter]
                        break


            
         #-----------------obstacles----------- 
    setbars()     
    snake_blocks = pygame.Surface((20,20))
    appleimage.fill((0,0,255))
    
    clock = pygame.time.Clock()
    
    
    while(True):
        #------------------displays game title--------------
        
        s.blit(front,(0,0))
        title = f2.render("SERPENTINE", True, (0,51,0))
        press = rg3.render("Press Spacebar to continue", True, (255,255,255))
        
        s.blit(title,((200/1500)*sw,(20/800)*sh))
        s.blit(press,((550/1500)*sw,(700/800)*sh))
        pygame.display.update()
        x = [0,0,0,0,0] #set location 
        y = [height_of_score_show+80,height_of_score_show+60,height_of_score_show+40,height_of_score_show+20,height_of_score_show] #y coord snake    
                                
        move = 0 #directions: 0 down 1 right 2 up 3 down
        score = 0
        givepos()
        #------------------actual game starts------------
        for e in pygame.event.get():
            if e.type == QUIT: #-------------quits the game if cross button on game window pressed
                pygame.quit()
                shutdown = 1
                
            elif e.type == KEYDOWN:
                if e.key == K_SPACE:
                    dead = 0
                    #pygame.mixer.music.play()
                    while True and dead != 1:
                        clock.tick(10)
                        for e in pygame.event.get():
                            if e.type == QUIT:
                                pygame.quit()
                                shutdown = 1
                            #-----------------checking which direction key pressed---------
                            #----------Ref. for below code  https://www.pygame.org/project-Snake+in+35+lines-818-.html--------------
                            elif e.type == KEYDOWN:
                                if e.key == K_UP and move!=0:
                                    move = 2
                                if e.key == K_DOWN and move!=2:
                                    move = 0
                                if e.key == K_LEFT and move!=1:
                                    move = 3
                                if e.key == K_RIGHT and move!=3:
                                    move = 1
                            #----------Ref. for above code  https://www.pygame.org/project-Snake+in+35+lines-818-.html--------------
                        
                        i = len(x) - 1
                        #-------------checking if snake colliding with itself------------
                        while(i>=2):
                            if collision(x[0], x[i], y[0], y[i], 20, 20, 20, 20):
                                #dead = 1
                                #over(s,score,uip,uip_gl)
                                
                                move = 0 
                                x = [0,0,0,0,0] #reset location 
                                y = [height_of_score_show+80,height_of_score_show+60,height_of_score_show+40,height_of_score_show+20,height_of_score_show] #y coord snake    
                                no_of_lives_left-=1
                                if no_of_lives_left<=0:
                                    dead=1
                                    setbars()
                                    over(s,score,uip,uip_gl)
                                    no_of_lives_left=no_of_lives
                                break
                            i -= 1
                        numb=0    
                        #-------------checking if snake colliding with bar------------
                        for al in imgl:    
                            if collision(x[0], b_pos_t[numb][0], y[0], b_pos_t[numb][1], 20, wh, 20 ,ww) and dead != 1:
                                move = 0 #------------------------------------------------------------------------------
                                x = [0,0,0,0,0] #reset location 
                                y = [height_of_score_show+80,height_of_score_show+60,height_of_score_show+40,height_of_score_show+20,height_of_score_show] #y coord snake    
                                no_of_lives_left-=1
                                if no_of_lives_left<=0:
                                    dead=1
                                    setbars()
                                    over(s,score,uip,uip_gl)
                                    no_of_lives_left=no_of_lives
                                break
                            numb+=1    
                        #--------------------for score ball -----------------------
                        if collision(x[0], a_pos[0], y[0], a_pos[1], 20, 10, 20 ,10) and dead != 1:
                            musicsound = pygame.mixer.Sound('crash.wav')
                            pygame.mixer.music.pause()
                            musicsound.play()
                            pygame.mixer.music.unpause()
                            score += 1
                            add_new_bar()
                            x.append(700)
                            y.append(700)
                            givepos()
                        #--------------------for life ball -----------------------    
                        if collision(x[0], lb_pos[0], y[0], lb_pos[1], 20, 20, 20 ,20) and dead != 1:
                            musicsound = pygame.mixer.Sound('crash.wav')
                            pygame.mixer.music.pause()
                            musicsound.play()
                            pygame.mixer.music.unpause()
                            score += 0 #no score added
                            no_of_lives_left+=1 #life added
                            add_new_bar()
                                
                            x.append(700)
                            y.append(700)
                            givepos()    
                                                        
                        #--------------------for more score ball -----------------------    
                        if collision(x[0], esb_pos[0], y[0], esb_pos[1], 20, 20, 20 ,20) and dead != 1:
                            musicsound = pygame.mixer.Sound('crash.wav')
                            pygame.mixer.music.pause()
                            musicsound.play()
                            pygame.mixer.music.unpause()
                            score += score_added_by_ex_sc_ball #no score added
                            add_new_bar()                         
                                
                            x.append(700)
                            y.append(700)
                            givepos()    
                        #-------------checking if snake colliding with screen borders------------                            
                        if x[0]<0 or x[0]>(sw-20) or y[0]<height_of_score_show or y[0]>(sh-20) and dead != 1:
                            move = 0 #------------------------------------------------------------------------------
                            x = [0,0,0,0,0] #reset location 
                            y = [height_of_score_show+80,height_of_score_show+60,height_of_score_show+40,height_of_score_show+20,height_of_score_show] #y coord snake    
                            no_of_lives_left-=1
                            if no_of_lives_left<=0:
                                dead=1
                                setbars()
                                over(s,score,uip,uip_gl)
                                no_of_lives_left=no_of_lives
                        #calling dropbar function
                        rifordb = random.randint(0,10) #probability of dropping bar
                        global dropbaout, ycoofdb
                        if rifordb==1 and dropbaout==1:
                            dropbar()
                            dropbaout=0
                            
                        try:
                            #print("dd")
                            #checking if none of snake block collide with dropping bar
                            for evrypos in range(len(x)):
                                if collision(x[evrypos], xcoofdb, y[evrypos], ycoofdb, 20, wh, 20 ,ww+100) and dead != 1:
                                        move = 0 #------------------------------------------------------------------------------
                                        x = [0,0,0,0,0] #reset location 
                                        y = [height_of_score_show+80,height_of_score_show+60,height_of_score_show+40,height_of_score_show+20,height_of_score_show] #y coord snake    
                                        no_of_lives_left-=1
                                        if no_of_lives_left==0:
                                            dead=1
                                            setbars()
                                            over(s,score,uip,uip_gl)
                                            no_of_lives_left=no_of_lives
                        except:
                            nothing= " " #does nothing
                                
                        if dead != 1:
                            i = len(x) - 1
                            
                            while(i>=1):
                                x[i]=x[i-1]
                                y[i]=y[i-1]
                                i-=1
                            #-------------------changing snake's image--------------
                            #----------Ref. for below code  https://www.pygame.org/project-Snake+in+35+lines-818-.html--------------
                            if move == 0:
                                y[0] += 20
                            elif move == 1:
                                x[0] += 20
                            elif move == 2:
                                y[0] -= 20
                            elif move == 3:
                                x[0] -= 20
                            #----------Ref. for above code https://www.pygame.org/project-Snake+in+35+lines-818-.html--------------
                            
                            s.blit(game_back,(0,0))
                            cont=0
                            try:
                                
                                if ycoofdb<=sh-height_of_score_show:
                                    
                                    ycoofdb+=speed_of_drop
                                    
                                    s.blit(img_mb[-1], (xcoofdb,ycoofdb+height_of_score_show))
                                else:
                                    ycoofdb=-500
                                    for element in img_mb:
                                         img_mb.remove(element)
                                    #img_mb.pop(-1)
                                    dropbaout=1
                                    
                            except:
                                #print("ww")
                                nothing=" " #do nothing    
                            for img2 in imgl:
                                s.blit(img2, b_pos_t[cont])
                                cont+=1
                            for i in range(0,len(x)):
                                #s.blit(img, (x[i], y[i]))
                                snake_blocks.fill((255,random.randint(0,130),random.randint(0,130)))
                                s.blit(snake_blocks, (x[i], y[i]))    
                            
                            s.blit(appleimage, a_pos)
                            #getting life ball
                            if riforlifeball==1 and (no_of_lives_left!=no_of_lives or (no_of_lives_left+1)>no_of_lives): #doesn't show life balls when lives are full
                                appleimage2.fill((255,0,0))
                                s.blit(appleimage2,lb_pos)
                            #getting more score ball
                            if riformscball==1:
                                appleimage3.fill((0,0,255))
                                s.blit(appleimage3,esb_pos)
                            topBar = pygame.Surface((sw,height_of_score_show))
                            bl1= pygame.Surface((20,20))
                            re1= pygame.Surface((20,20))
                            bs1= pygame.Surface((10,10))
                            topBar.fill((0,0,0))
                            bl1.fill((0,0,255))
                            re1.fill((255,0,0))
                            bs1.fill((0,0,255))
                            s.blit(topBar, (0,0))
                            text1 = f.render("Score : "+str(score), True, (255,255,255))
                            text2 = f.render("Level : "+str(uip_gl), True, (255,255,255))
                            text32 = f.render("Extra score ball", True, (255,255,255))
                            text4 = f.render("Life ball", True, (255,255,255))
                            text5 = f.render("Score ball", True, (255,255,255))
                            if no_of_lives_left==1: #checking plural/singular
                                aaa="fe"
                            else:
                                aaa="ves"
                            text3 = f.render("Li"+aaa+" : "+str(no_of_lives_left), True, (255,255,255))
                            #s.blit(t,(10,10))
                            s.blit(bl1,(mlrintbar,10))
                            s.blit(re1,(mlrintbar,32))
                            s.blit(bs1,(mlrintbar,58))
                            s.blit(text32,(mlrintbar+25,7))
                            s.blit(text4,(mlrintbar+25,29))
                            s.blit(text5,(mlrintbar+25,51))
                            s.blit(text1,(sw-mlrintbar-80,9))
                            s.blit(text2,(sw-mlrintbar-80,34))
                            s.blit(text3,(sw//2-5,5))
                            lc=0
                            lsur=[]
                            for lc in range(no_of_lives_left):
                                lsur.append(pygame.Surface((15,15)))
                                lsur[-1].fill((255,0,0))    
                                s.blit(lsur[-1], (sw//2-no_of_lives*17//2+17*(lc+1),30)) #whatever no. of lives is, it will come in center 
                            for lc2 in range(no_of_lives-no_of_lives_left):
                                lsur.append(pygame.Surface((15,15)))
                                lsur[-1].fill((70,0,0))    
                                s.blit(lsur[-1], (sw//2-no_of_lives*17//2+17*(lc2+lc+2),30)) #whatever no. of lives is, it will come in center 
                            
                            pygame.display.update()
                                
lf = 0 #checks if valid level found
nf = 0 #checks if valid name found
while(nf == 0):                                
    
    uip = input("Please enter your name:")

    if uip.count("#")!=0: #prevents user from typing "#"
        print("Enter a good name please.")         
    else:
        try:
            xdd = int(uip)
            print("Enter valid name.")  
        except:
            nf = 1
            gls=1 #start game level
            gle=10 #maximum game level
            
            while lf == 0:
                uip_gl = input("Please type any game level from "+str(gls)+" to "+str(gle)+":")
            
                try:
                    uip_gl = int(uip_gl)
                    if uip_gl>=gls and uip_gl<=gle:
                        lf = 1
                        gamemainloop(uip,uip_gl)
                    if shutdown == 1:
                        #-------------Picture credits---------
                        print("PICTURE CREDITS:")
                        print("1. ","https://www.google.co.in/search?q=snake+game+wallpaper&rlz=1C1CHBF_enIN813IN813&source=lnms&tbm=isch&sa=X&ved=0ahUKEwj73fDnye_eAhUaSI8KHZvZD8IQ_AUIDigB&biw=1396&bih=641#imgrc=RMxlnfjAT_iXaM:")
                        print("2.", "https://www.google.co.in/search?rlz=1C1CHBF_enIN813IN813&biw=1396&bih=641&tbm=isch&sa=1&ei=y5n6W-S8KonyvgTt-pmoBA&q=plain+black+wallpaper&oq=plain+black+wallpaper&gs_l=img.3..0l10.3826776.3828496..3828693...0.0..0.179.1408.1j10......1....1..gws-wiz-img.......0i7i30.7mMkmizEtAc#imgrc=y7Rf_kEOP8nrjM:")
                        sys.exit(0)
                    else:
                        print("Enter valid game level.")
                except:
                    if shutdown == 1:
                        print("PICTURE CREDITS:")
                        print("1. ","https://www.google.co.in/search?q=snake+game+wallpaper&rlz=1C1CHBF_enIN813IN813&source=lnms&tbm=isch&sa=X&ved=0ahUKEwj73fDnye_eAhUaSI8KHZvZD8IQ_AUIDigB&biw=1396&bih=641#imgrc=RMxlnfjAT_iXaM:")
                        print("2.", "https://www.google.co.in/search?rlz=1C1CHBF_enIN813IN813&biw=1396&bih=641&tbm=isch&sa=1&ei=y5n6W-S8KonyvgTt-pmoBA&q=plain+black+wallpaper&oq=plain+black+wallpaper&gs_l=img.3..0l10.3826776.3828496..3828693...0.0..0.179.1408.1j10......1....1..gws-wiz-img.......0i7i30.7mMkmizEtAc#imgrc=y7Rf_kEOP8nrjM:")
                        sys.exit(0)
                    print("Enter valid level.")