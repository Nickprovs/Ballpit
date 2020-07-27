#Nick Provost
#Montclair State University

import pygame 
from random import *
import random
import math #Used for distance formula

#To Define Colors, we give RGB values (in pygame)
#We use RGB as oppose to RYB because of the way compute monitors display
#pygame handles 256 bit colors
white = (255,255,255) 
black = (0,0,0) 
gray=(100,100,100)
red = (255,0,0)
green=(0,255,0)
blue=(0,0,255)
yellow=(255,255,0)

#Variables that are referenced/edited in our gameLoop but also needed before we enter the loop
#Start variable block
displayWidth=700
displayHeight=700
FPS=60
charColor = black
enColor = red
score = 0
pUpStartTime=0
reverseTime=3000
slowTime=4000
bonusTime=10000
roleReversal=False

list1 = [None] * 12 #Defines a list to contain objects that's 51 long.
listCounter= 0

direction= "none"
leadXChange = 0
leadYChange = 0
leadX=int(displayWidth/2)
leadY=int(displayHeight/2)
charRadius = 20
charThickness = 0
charSize=10
gameExit = False
gameOver = False
roleReversal = False
pUpActive= False
pUpType="none"
enCircleDisplacement=3
#End Variable Block

#Class that generates random enemy circles with spawn locations based on character position.
class Circle:
    def __init__(self):

        #If the character hasn't moved yet (character in center), spawning doesn't need to be calculated carefully.
        if (direction=="none"): 
            self.leftSpawn = choice([True,False])
            self.topSpawn = choice([True,False])
            
        #Determines which side of the X and Y plane enemy circles should spawn based on character position
        else:
            if(leadX - 0 > displayWidth-leadX):
                self.leftSpawn = True
            else:
                self.leftSpawn = False
            if(leadY - 0 > displayHeight - leadY):
                self.topSpawn = True
            else:
                self.topSpawn = False
                
        #Spawns based on previous if/else logic. Randomly calculated within those limits with a buffer
        if (self.leftSpawn == True):
            self.circleX = randint(20,displayWidth/2-150)#Left Most X-Coordinate of Circle
        else:
            self.circleX=randint(displayWidth/2+150,displayWidth-20)
        if (self.topSpawn==True):
            self.circleY = randint(20, displayHeight/2-150)
        else:
            self.circleY=randint(displayHeight/2+150,displayHeight-20)
                
        self.circleColor = red 
        self.circleRadius = randint(10,50) #Random Size
        self.edgeThickness=0 #Not used but still necessary for pygame
        self.headingRight = choice([True, False]) #Starts traversing in random x direction
        self.headingDown = choice([True, False]) #Starts traversing in random y direction

#initializes pygame modules. returns a tuple indicative of
#successful/unsuccessful initializations if you want it
pygame.init()

#Teturns a pygame clock object. Used to handle FPS.
clock=pygame.time.Clock() 

#Returns a pygame surface object (display) for us to draw on. We store in gameDisplay.  
gameDisplay = pygame.display.set_mode((displayWidth,displayHeight))#Must take resolution as tuple     

#Title of our pygame window
pygame.display.set_caption("BallPit")

#Images are loaded for later use. All pygame images are located in the same folder as the python file.
menuIMG = pygame.image.load('assets\Menu700.png')
pausedIMG = pygame.image.load('assets\Paused700.png')
gameOverIMG= pygame.image.load('assets\GameOver700.png')

#Icon image loaded and displayed
icon = pygame.image.load('assets\logo32.png')
pygame.display.set_icon(icon)

#Predefining font sizes and styles here to minimize code when displaying images
xsmallfont = pygame.font.SysFont("comicsansms",15) #A font of size 15
smallfont = pygame.font.SysFont("comicsansms",25) #A font of size 25
medfont = pygame.font.SysFont("comicsansms",50) #A font of size 50
largefont = pygame.font.SysFont("comicsansms",80) #A font of size 80

#Short and Simple Methods to handle enemy circle movement. These four methods taken from lab 9 example.
def moveLeft(circle):
    circle.circleX -= enCircleDisplacement
    
def moveRight(circle):
    circle.circleX += enCircleDisplacement

def moveUp(circle):
    circle.circleY -= enCircleDisplacement

def moveDown(circle):
    circle.circleY += enCircleDisplacement

#Called in game loop. Recalculates directions of enemy circles based on whether or not they hit the edges.
#They are always moving in a diagonal of either y=x+b or y=-x +b
def recalculateCirclePositions():
    for i in range(listCounter): #Do for each circle in the list
         if (list1[i].headingRight == True):
             if (list1[i].circleX + list1[i].circleRadius > displayWidth):
                 list1[i].headingRight = False
             else:
                 moveRight(list1[i])

         else:
             if (list1[i].circleX-list1[i].circleRadius < 0):
                 list1[i].headingRight = True
             else:
                 moveLeft(list1[i])

         if (list1[i].headingDown == True):
             if (list1[i].circleY + list1[i].circleRadius > displayHeight):
                 list1[i].headingDown = False
             else:
                 moveDown(list1[i])

         else:
             if (list1[i].circleY-list1[i].circleRadius < 0):
                 list1[i].headingDown = True
             else:
                 moveUp(list1[i])
                 
#Redraws circles based on their X and Y values as well as their other attributes (ie: color, radius)
def redrawCircles():
    
    #Loop to draw each circle in the list
    for i in range(listCounter):

        #The outline of each circle is drawn before the circles themselves as we want the outline circle to be BEHIND the actual enemy circle.    
        pygame.draw.circle(gameDisplay,white,(list1[i].circleX, list1[i].circleY), list1[i].circleRadius+1, list1[i].edgeThickness)#Outline

        #If the role-reversal power up is active, the enemy circles are drawn with the color black.       
        if (pUpActive==True and roleReversal==True):
                pygame.draw.circle(gameDisplay,
                                   black,
                                   (list1[i].circleX, list1[i].circleY),
                                   list1[i].circleRadius-1,
                                   list1[i].edgeThickness)
                
        #Otherwise, they are drawn with the color white
        else:
                pygame.draw.circle(gameDisplay,
                                   list1[i].circleColor,
                                   (list1[i].circleX, list1[i].circleY),
                                   list1[i].circleRadius-1,
                                   list1[i].edgeThickness)
                
        #These statements draw the eyes of the enemy circles. They are drawn last so they sit on top.          
        pygame.draw.circle(gameDisplay,white,(int(list1[i].circleX-list1[i].circleRadius/3), int(list1[i].circleY-list1[i].circleRadius/5)), int(list1[i].circleRadius/5), 0) #Left Eye
        pygame.draw.circle(gameDisplay,white,(int(list1[i].circleX+list1[i].circleRadius/3), int(list1[i].circleY-list1[i].circleRadius/5)), int(list1[i].circleRadius/5), 0)

#Handles collisions between player and enemy circles        
def collisionDetection():
    #We are editing these variables if conditions are met; so they must be made global
    global gameOver 
    global listCounter
    global score

    i = 0

    while (i < listCounter): #Collision logic explained in photo in root folder
       if(math.hypot(leadX-list1[i].circleX, leadY-list1[i].circleY)<= charRadius+list1[i].circleRadius):
           if roleReversal == False: 
               gameOver=True
           else:
               #If Role-Reversal Power up is active, the enemy circle collided with is deleted
               score=score+1
               list1.remove(list1[i])
               listCounter=listCounter-1
               i=i-1

       i+=1


#Creates pygame readable text-objects based on font size given in string form.
#This is just a method to reduce code related to displaying text
def text_objects(text, color,size):
    if size == "xsmall":
        textSurface= xsmallfont.render(text, True, color) 
    elif size =="small":
        textSurface= smallfont.render(text, True, color)
    elif size =="medium":
        textSurface= medfont.render(text, True, color)
    elif size =="large":
        textSurface= largefont.render(text, True, color)
        
    #returns pygame readable text object (a tuple of the text and it's rectangular surface area)
    return textSurface, textSurface.get_rect() 

def message_to_screen(msg, color,y_displace=0, size = "small"):
    #y_displace=0 is displacement from center of screen. if user doesn't enter a value, 0 is inferred.
    textSurf, textRect=text_objects(msg, color, size)
    textRect.center=((displayWidth/2), (displayHeight/2+y_displace)) #We define the center of our text object to be the center of the screen
    gameDisplay.blit(textSurf, textRect) #Now that we established where the center of our text object is, it will be centered when we blit it.

#Generates random circle coordinates for our power-ups and coins that aren't too close to the edges
def randCircleGen():
    randX = round(random.randrange(50, displayWidth-50))
    randY = round(random.randrange(50, displayHeight-50))
    return randX, randY

#This collision method is a simpler one just used for coins and pick-ups. Same logic though.
def circleCollision(scoreX, scoreY, scoreRadius):
     if(math.hypot(leadX-scoreX, leadY-scoreY)<= charRadius+scoreRadius):
         return True
     else:
         return False
        
#Displays score in the top right corner with a little bit of a space cushion.
def displayScore(score):
    text = smallfont.render("Score: " + str(score), True, white)
    gameDisplay.blit(text, [4,2])
    
#Displays the type of power-up picked up and how much longer it will last.
def displayPowerUp(pUp, pUpTime):
    text1 = smallfont.render(str(pUp), True, white)
    text2 = smallfont.render(("Remaining: " + str(float("{0:.2f}".format((((pUpTime-(pygame.time.get_ticks()-pUpStartTime))/1000)))))), True, white)
    gameDisplay.blit(text1, [displayWidth-200,20])
    gameDisplay.blit(text2, [displayWidth-200,50])
    
#Here we define our pause screen. Which is almost like a mini game itself. It has its own while loop and event handlers.
#This is done so that no logic is calculated in the main game. While we are paused, we are looping within this method.
def pause ():
    paused = True

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                    
        gameDisplay.fill(white)
        gameDisplay.blit(pausedIMG, (0,0))
        message_to_screen("Paused",
                          white,
                          -100,
                          "medium")
        message_to_screen("Press C to continue or Q to quit",
                          white,
                          -25)
        pygame.display.update()
        clock.tick(5)#Doesn't really matter the fps because we're just displaying static images/text. Saves resources. 

#A menu-esque screen that works exactly as the pause screen does.
def gameIntro():
    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    intro = False
                if event.key ==pygame.K_q:
                    pygame.quit()
                    quit()

                    
        gameDisplay.fill(white)
        gameDisplay.blit(menuIMG, (0,0))
        
        message_to_screen("Welcome to the Ball Pit",
                          white,
                          -170,
                          "small")
        message_to_screen("The objective of the game is to obtain the yellow balls.",
                          white,
                          -110,
                          "xsmall")
        message_to_screen("If you run into the moving balls, or the edges, you die.",
                          white,
                          -70,
                          "xsmall")
        message_to_screen("Pick up a blue ball to get a random power-up.",
                          white,
                          -30,
                          "xsmall")
        message_to_screen("Control your character with the ARROW keys.",
                          white,
                          10,
                          "xsmall")
        message_to_screen("Press C to play or Q to quit. Press P to Pause mid-game",
                          white,
                          50,
                          "xsmall")
        pygame.display.update()
        clock.tick(15)
        
#Adds an aditional enemy circle to the list by default. Can be overwridden with a parameter to add multiple.
def addEnCircle(numAdd=1):
    global listCounter #Turned global in this method since we edit it
    
    for i in range(numAdd): #Creates 10 circles and stores them in a list
        mycircle=Circle()
        list1[listCounter]=mycircle
        listCounter=listCounter+1

#returns a string used in calculating a random power up's attributes
def randPowerUp():
    return choice(["reverse", "time", "bonus"])
    
    
    
#Game Loop
def gameLoop():
    #Variables that are necessary at the start of the game and edited within the game loop are defined as global here.
    global gameExit
    global gameOver
    global leadXChange
    global leadYChange
    global direction
    global leadX
    global leadY
    global listCounter
    global list1
    global enCircleDisplacement
    global charColor
    global roleReversal
    global pUpType
    global pUpActive
    global pUpStartTime
    global roleReversal
    global score
    
    list1 = [None] * 12 #Defines a list to contain objects that's 12 long.
    listCounter= 0
    direction= "none" #Start off not moving
    leadXChange = 0
    leadYChange = 0
    leadX=int(displayWidth/2) #Start off center-x
    leadY=int(displayHeight/2)#Start off center-y
    score= 0 
    pUpThisModulus=False #Boolean used in determining if the user received a power up this %5 score points
    pickedUp=True #Used in determining if the power up was picked up. 
    pUpActive = False #Used in enabling/disabling power-ups based on time limit.
    pUpX, pUpY = randCircleGen() #Our first power-up location is calculated
    pUpStartTime = 0
    pUpType = "none"

    randScoreCircleX, randScoreCircleY = randCircleGen()

    gameExit = False
    gameOver = False

    addEnCircle(3) #Before we enter the game loop, three enemy circles are spawned
    
    while not gameExit: #not indicates false. Loops while gameExit is false.
        
        for event in pygame.event.get(): #While the game is running
            if event.type == pygame.QUIT: #pygame.quit is an object. Don't need ()
                gameExit = True #Invalidates loop, then the program can continue to quit
                
            #Character Movement Handling
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    direction = "left"
                    leadXChange = -4
                    leadYChange = 0
                elif event.key == pygame.K_RIGHT:
                    direction="right"
                    leadXChange = 4
                    leadYChange = 0    
                elif event.key == pygame.K_UP:
                    direction="up"
                    leadYChange = -4
                    leadXChange = 0
                elif event.key == pygame.K_DOWN:
                    direction="down"
                    leadYChange = 4
                    leadXChange= 0
                elif event.key == pygame.K_p:
                    pause()
                    
        #Game over if character travels out of bounds
        if (leadX+charRadius >= displayWidth or leadX-charRadius <= 0 or leadY +charRadius >=displayHeight or leadY-charRadius <= 0) == True:
            gameOver=True
            
        #Character coordinates are equal to their current coordinates plus and changes made to them
        leadX+= leadXChange
        leadY+= leadYChange
        
        #Coorinates Note: Coordinates start at (0,0) in top-left corner. Adding goes down and to the right.
        gameDisplay.fill(black)#Draws the background color
        pygame.draw.circle(gameDisplay,white,(leadX, leadY), charRadius+1, charThickness) #Outline for our char
        pygame.draw.circle(gameDisplay,charColor,(leadX, leadY), charRadius-1, charThickness) #Char Circle
        pygame.draw.ellipse(gameDisplay,white,(leadX-11, leadY-7,8,13), charThickness) #Char Left Eye
        pygame.draw.ellipse(gameDisplay,white,(leadX+4, leadY-7,8,13), charThickness) #Char Right Eye

        pygame.draw.circle(gameDisplay,white,(randScoreCircleX, randScoreCircleY),charRadius+1,charThickness)#Outline for our coin
        pygame.draw.circle(gameDisplay,yellow,(randScoreCircleX, randScoreCircleY),charRadius-1,charThickness)#Coin circle

#Power Up Logic Start

        #Draw the power up if it is ready to spawn and it hasn't been picked up yet (ie:pickedUp==False)
        if(pickedUp==False):
            pygame.draw.circle(gameDisplay,white,(pUpX, pUpY), charRadius+1, charThickness)#Outline
            pygame.draw.circle(gameDisplay,blue,(pUpX, pUpY), charRadius-1, charThickness)
            
        #If the character collided with a power-up's coordinates for the first time (ie: hasn't been used yet)
        if(circleCollision(pUpX, pUpY, charRadius)==True and pickedUp==False):
            pickedUp=True
            pUpX, pUpY = randCircleGen()#Generates coordinates of next power-up
            
            #Make sure running over coordinates before drawn doesn't give power-up
            pUpActive=True

            #Random power-up selected and the clock starts on its duration
            pUpType=randPowerUp()
            pUpStartTime=pygame.time.get_ticks()

        #Slow Time Logic
        if pUpActive==True and pUpType=="time" and pygame.time.get_ticks()-pUpStartTime<=slowTime:
            enCircleDisplacement=1
            displayPowerUp("Time Warp", slowTime)
        else:
            enCircleDisplacement=3

        #Role Reversal Logic
        if pUpActive==True and pUpType=="reverse" and pygame.time.get_ticks()-pUpStartTime<=reverseTime:
            roleReversal = True #Will swap roles in enemy Circle Collision method
            displayPowerUp("Invincible", reverseTime)
            charColor = red
        else:
            roleReversal = False
            charColor = black

        #Double Points Logic
        if pUpActive==True and pUpType=="bonus" and pygame.time.get_ticks()-pUpStartTime<=bonusTime: #longer time
            displayPowerUp("Double Points", bonusTime)
            pUpActive =True
        else:
            if pUpType== "bonus":
                pUpType="none"
                
#Power Up Logic End

        #Recalculating/redrawing of enemy circles and potential collisions with them    
        recalculateCirclePositions()
        redrawCircles() #Non-Char Circles
        collisionDetection() #For Enemy Circles

        #Score circle collision handling
        if (circleCollision(randScoreCircleX, randScoreCircleY,charRadius)==True):
            if (pUpType=="bonus" and pUpActive==True): #If double points active -- 2 points per circle
                score = score + 2 
            else:
                score = score + 1
                
            if(score%10==0): #Every %10 circles=0, 2 enemy circles spawn
                pickedUp=False
                if(listCounter<10):
                    addEnCircle(2)#By Default (no params given) adds 1 enemy circle
                    
            elif(score%5==0): #Every %5 circles=0, 1 enemy circle spawns
                pickedUp=False
                if(listCounter<10):
                    addEnCircle()
                    
            randScoreCircleX, randScoreCircleY = randCircleGen() #The position of the next score coin is calculated

#Game Over Screen Logic Start
            
        while gameOver == True: #loop is necessary so they can press multiple buttons
                gameDisplay.fill(white)
                gameDisplay.blit(gameOverIMG, (0,0))
                message_to_screen("Game Over", white, -150, size="medium")
                message_to_screen(("Your Score Was: " + str(score)), white, -100,"small")
                message_to_screen("Press C to play again or Q to quit",white,-60,size="small")
                pygame.display.update()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        gameExit = True #Needs to come first so we don't get stuck in gameOver loop
                        gameOver = False
                    if event.type==pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            gameExit = True 
                            gameOver = False
                        if event.key ==pygame.K_c:
                            gameLoop() #starts things over

#Game Over Screen Logic End

        
        displayScore(score)#Displays Score
        pygame.display.update()#Updates Screen
        clock.tick(FPS) #A mostly empty method which takes control for the amount of time required so this loop runs at FPS desired  
            
        
gameIntro()#Main Menu Screen Called To Start
gameLoop()#If Allowed To Proceed (User pressed C), we being the game

pygame.quit()#Uninitializes pygame modules and exit modulesf
quit()#exits out of python
