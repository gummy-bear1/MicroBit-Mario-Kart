#-----------------------------------------------------------------------------
# Name:        Mario Kart
# Purpose:     To create a program that includes everything I have learned in this class
# Author:      Lana Nguyen
# Created:     2-Dec-2022
# Updated:     10-Jan-2023
#-----------------------------------------------------------------------------

# I think this project deserves a level 4+ because I completed the entire rubric and went beyond
# by using a mircobit for sensor data, adding sound effects, having power ups,
# scrolling background/images and the program is visually appealing

#Features Added:
# Collision detection between players and obstacles/powerups/road/finishline
# External file reading and writing
# Able to control the car/player and use power ups using a mircobit
# Replay button
# random obstacles pop up in random places and scroll down at different speeds
# Able to save and use power ups
# scrolling background, obstacles, power ups and finish line
# a mini map to see how far the player is from the finish line
#------------- ----------------------------------------------------------------

# Notes when using the mircobit
# 1) please plug in the left mircobit first then the right so the intructions and comments in the code matchup with the controllers
# 2) if for any reason the mircobits stop working, exit thonny, unplug mircobits, replug them in and reopen thonny

''' Code to be run on the microbit 1:
from microbit import *
import music
DELAY_VALUE =100
while True:
    x = accelerometer.get_x() # gets accelerometers value of x 
    print(x)           
    sleep(DELAY_VALUE)
    
    if button_a.was_pressed() or button_b.was_pressed(): # if one of buttons pressed
        print(3000)
'''

''' Code to be run on the microbit 2:
from microbit import *
import music
DELAY_VALUE =100
while True:
    x = accelerometer.get_x() # gets accelerometers value of x 
    print('n',x)           
    sleep(DELAY_VALUE)
    
    if button_a.was_pressed() or button_b.was_pressed(): # if one of buttons pressed
        print('n',3000)
'''
# importing
import pygame
from Microbit import *
from pygame import mixer
import random
import math

def distFromPoints(point1, point2):
    '''
    This function calculates the distance between two points
    
    This function calculates the distance between two points given by a set
    of tuples (x1,y1) and (x2,y2) for the use of colllision detection of a button
    
    Parameters
    ----------
    point1 : float
        The first point to compare
    point2 : float
        The second point to compare
        
    Returns
    ----------
    float
        The distance between the two points
    '''
    distance = math.sqrt( ((point2[0]-point1[0])**2)+((point2[1]-point1[1])**2) )
    return distance                 

def dimensions(PosX,PosY,width,height):
    '''
    This functions turns images into rectangles
    
    This function turns images into rectangles using dimensions (width and height)
    and positions (posX,posY) of the image for the use of collision detection
    
    Parameters
    -----------
    posX : float
       The x position of the image
    posY : float
       The y position of the image
    width : integer
       The width of the image
    height : integer
       The height of the image
    
    Returns
    ----------
    Rect
        The rectangle of an image including position and dimensions of rectangle
    '''
    rect = (PosX,PosY,width,height)
    collision = pygame.Rect(rect)
    return collision

def fileReadingAndWriting(file,amount):
     '''
     This function reads and writes files to change the total wins
    
     This function reads and writes to an external file to change the total wins of the players.
     The function reads a number in a file, saves it to a variable and then writes into the file
     by adding a new number depending on if the player has won. The total wins will be since the game won
     not when the program was opened.
    
     Parameters
     -----------
     
     file : string
         The name of the external file
     
     amount : integer
         The number added to the external value, meaning 1 if the player has won or 0 if the player has lost
     
     Returns
     ----------
     integer
         The total number of wins for a player 
     '''
     f = open(file,"r")              
     fileList = f.readlines()        
     totalWins = int(fileList[0])       
     f.close()
                
     f = open(file,"w")                
     newTotalWins = totalWins + amount  
     fileList2 = str(newTotalWins)
     f.write(fileList2)
     f.close()
     return fileList2                   
     
def scrolling(pos,pos2,height,scroll,num):
    '''
     This function calucates the y position of an image in order for it to scoll
     
     This function calucates the y position of an image to make it scroll/move downwards.
     The position is made negative and then adds a scrolling value making
     the y axis increase, which makes the image scroll downwards. 
     
     Parameters
     ----------
     pos : float
         Position of the first image
         
     pos2 : float
         Position of the second image
     
     height : integer
         Height of the image
     
     scroll : integer
         Number of how fast the image will scroll at
     
     num : integer
         Additionally numbers to scroll at (needed for powerups)
     
     Returns
     --------
     pos: float
        Position of the first image
        
     pos2: float
        Position of the second image
     '''
    
    pos[1] = -1*height + scroll + num
    pos2[1] = -1*height + scroll + num
    return pos,pos2
       
     
def main():
    """
    This function sets up the game and runs the main game loop
    
    Parameters
    ----------
    None
    
    Returns
    -------
    None
    
    """
    pygame.init()                      # Prepare the pygame module for use
    surfaceSize = [800,600]            # Desired physical surface size, in pixels.
    
    
    clock = pygame.time.Clock()        #Force frame rate to be slower

    mainSurface = pygame.display.set_mode((surfaceSize[0], surfaceSize[1]))
    
    #setup
    
    gamestate = "set microbit"
    
    # variables for screen
    screenColour = (0,200,255)
    screenPos = [0,0]
    
    # images
    yoshiImage = pygame.image.load("yoshi.png")
    toadImage = pygame.image.load("toad.png")
    backgroundImage = pygame.image.load("background.jpg")
    ghostImage = pygame.image.load("ghost.png")
    mushroomImage = pygame.image.load("mushroom.png")
    shyguyImage = pygame.image.load("shyguy.png")
    starImage = pygame.image.load("star.png")
    starPowerImage = pygame.image.load("star.png")
    bowserImage = pygame.image.load("bowser.png")
    finishLineMapImage = pygame.image.load("finishlinemap.png")
    finishLineBigImage = pygame.image.load("finishlinebig.png")
    
    # images screen
    startImage = pygame.image.load("startscreen.png")
    instructionImage = pygame.image.load("instruction.png")
    loseImage = pygame.image.load("loseblackscreen.png")
    bothLoseImage = pygame.image.load("bothlose.png")
    toadWinsImage = pygame.image.load("toadwins.png")
    yoshiWinsImage = pygame.image.load("yoshiwins.png")

    backgroundImage_rect = backgroundImage.get_rect()
    backgroundImage_height = backgroundImage.get_height()
    
    # fonts and texts
    font = pygame.font.SysFont("Arial", 26)   
    startText = font.render("START", 10, pygame.Color("black"))
    playText = font.render("PLAY", 10, pygame.Color("black"))
    againText = font.render("AGAIN", 10, pygame.Color("black"))
    yoshiiText = font.render("YOSHI", 20, pygame.Color("green"))
    toaddText = font.render("TOAD", 20, pygame.Color("red"))
    
    # variables for buttons
    button1Pos = [150,100]  
    button2Pos = [400,520]  
    button3Pos = [400,530]
    buttonSize = 60  
    buttonColour = (255, 255, 255)
    
    # variables for yoshi (player 1)
    yoshiPos = [50,300]
    yoshiRect  =yoshiImage.get_rect(center = (yoshiPos[0],yoshiPos[1]))
    yoshi_height =yoshiImage.get_height()
    yoshiSpeed = [0,0]
    
    # variables for toad (player 2)
    toadPos = [575,300]
    toad_height =toadImage.get_height()
    toadSpeed = [0,0]
    
    # variables for bad guys
    scroll = 0
    badGuysScroll = 0
    badGuysStart = 0
    badGuysPos = [0,0]
    badGuysPos2 = [0,0]
    badGuysList = [ghostImage, mushroomImage, shyguyImage]
    
    # variables for bowser
    bowserScroll = 0
    bowserStart = 0
    bowserPos = [0,0]
    bowserPos2 = [0,0]
    bowserImage_height = bowserImage.get_height()
    
    # variables for star
    starScroll = 0
    starStart = 0
    starPos = [0,0]
    starPos2 = [0,0]
    starImage_height = starImage.get_height()
    
    # variables for star power up
    starPowerUp = 0         # counts how many times star and car have collide, powerup loadup
    starPowerUp2 = 0   
    actualStartPowerUp = 0  # variable to start the actual powerup
    actualStartPowerUp2 = 0
    starPowerPos = [370,10]
    starPowerPos2 = [770,10]
 
    # variables for maps circle
    circleMapPos = [370,200]
    circleMap2Pos = [770,200]
    circleMapSpeed = 0.08
    CircleMapSize = 10
    circleMapColour1 = (245, 29, 22)
    circleMapColour2 = (23, 94, 29)
    circleMap = 0
    
    # variables for maps finish line
    finishLineMapPos = (345,50)
    finishLineMap2Pos = (745,50)
    
    # variables for games finish line
    finishLineBigPos = [78,-50]
    finishLineBig2Pos = [478,-50]
    finishLineScroll = 0
    finishLineBigImage_height = finishLineBigImage.get_height()
    
    # variables for if yoshi or toad wins
    yoshiWins = 0
    toadWins = 0
    
    # variables for if yoshi or toad loses
    yoshiDead = False
    toadDead = False
    
    # variables for sound and music
    pygame.mixer.init()
    powerUpSound = pygame.mixer.Sound("powerup.wav")
    
    # start of program
    while True:
        ev = pygame.event.poll()                       # Look for any event
        if ev.type == pygame.QUIT:                     # Window close button clicked?
            break
                                                       #   ... leave game loop
                                                       
        mouseCirclePos = pygame.mouse.get_pos()        # makes position of the mouse into a variable
        
        if gamestate == "set microbit":
            mb = Microbit()                            # sets up microbits
            mb2 = Microbit(excludePorts=mb.getPort())
                
            if not mb.isReady() and not mb2.isReady(): # checks to see if microbit is set up 
                print("Error opening Microbit - Trying again in 5 seconds")    
                time.sleep(5)
            else:
                pygame.mixer.music.load("intro.mp3")   # if mircobit ready, music plays and gamestate changes
                pygame.mixer.music.play(-1)
                gamestate = "start"
                
                
        # start startscreen
        elif gamestate == "start":                     
            
            # displays start screen
            mainSurface.blit(startImage,(0,0))
            pygame.draw.circle(mainSurface, buttonColour, button1Pos, buttonSize)
            mainSurface.blit(startText, (110,85))
            
            # reseting variables for if game is replayed
            # variables for yoshi
            yoshiPos = [50,300]
            
            # variables for toad
            toadPos = [575,300]
            
            # variables for bad guys
            scroll = 0
            badGuysScroll = 0
            badGuysStart = 0
            badGuysPos = [0,0]
            badGuysPos2 = [0,0]
            
            # variables for bowser
            bowserScroll = 0
            bowserStart = 0
            bowserPos = [0,0]
            bowserPos2 = [0,0]
            
            # variables for star
            starScroll = 0
            starStart = 0
            starPos = [0,0]
            starPos2 = [0,0]
            
            # variables for star power up
            starPowerUp = 0         # counts how many times star and car have collide, loadup
            starPowerUp2 = 0   
            actualStartPowerUp = 0  # variable to start the actual powerup
            actualStartPowerUp2 = 0
            starPowerPos = [370,10]
            starPowerPos2 = [770,10]
            
            # variables for maps circle
            circleMapPos = [370,200]
            circleMap2Pos = [770,200]
            
            # variables for games finish line
            finishLineBigPos = [78,-50]
            finishLineBig2Pos = [478,-50]
            finishLineScroll = 0
            
            # variables for if yoshi or toad wins
            yoshiWins = 0
            toadWins = 0
            
            # variables for if yoshi or toad loses
            yoshiDead = False
            toadDead = False
                
            # if button is pressed, instruction screen displays
            if ev.type == pygame.MOUSEBUTTONUP: 
                    if distFromPoints(button1Pos,mouseCirclePos) < (buttonSize):
                        gamestate = "instructions"
        
        
        # instruction screen
        elif gamestate == "instructions": 
            
            # displays intruction screen
            mainSurface.blit(instructionImage,(0,0))
            pygame.draw.circle(mainSurface, buttonColour, button2Pos, buttonSize)
            mainSurface.blit(playText, (370,500))
            
            # if button pressed, game starts
            if ev.type == pygame.MOUSEBUTTONUP: 
                    if distFromPoints(button2Pos,mouseCirclePos) < (buttonSize):
                        gamestate = "game"
        
        
        # game screen
        elif gamestate == "game":
            
            # using dimensions function to make images into rectangles for collision detection
            # yoshi (player 1)
            yoshiCollision = dimensions(yoshiPos[0],yoshiPos[1],40,1)
            badGuysCollision = dimensions(badGuysPos[0],badGuysPos[1],50,50)
            bowserCollision = dimensions(bowserPos[0],bowserPos[1],60,60)
            starCollision = dimensions(starPos[0],starPos[1],30,30)
            finishLineCollision = dimensions(finishLineBigPos[0],finishLineBigPos[1],242,37)
            
            # toad (player 2)
            toadCollision = dimensions(toadPos[0],toadPos[1],40,1)
            badGuysCollision2 = dimensions(badGuysPos2[0],badGuysPos2[1],50,50)
            bowserCollision2 = dimensions(bowserPos2[0],bowserPos2[1],60,60)
            starCollision2 = dimensions(starPos2[0],starPos2[1],30,30)
            finishLineCollision2 = dimensions(finishLineBig2Pos[0],finishLineBig2Pos[1],242,37)
                             
            # moving background           
            for car in range(0,2):                                                         # if in range of the spaces of image and screen
                mainSurface.blit(backgroundImage,(0,-car*backgroundImage_height + scroll)) # print out the background image constantly so it looks like its moving as the y increases
                mainSurface.blit(backgroundImage,(400,-car*backgroundImage_height + scroll))
                
            scroll += 5                                                                    # scroll y increases 5, which is scroll of background
            
            # draws lines and circles, bilts text and images
            pygame.draw.line(mainSurface,0,(370,50),(370,200), width = 3)                   # line for map
            pygame.draw.line(mainSurface,0,(400,0),(400,600), width = 5)                    # line to seperate player 1 and 2
            pygame.draw.line(mainSurface,0,(770,50),(770,200), width = 3)                   # line for map player 2
            mainSurface.blit(yoshiiText, (160,10))
            mainSurface.blit(toaddText, (570,10))
            mainSurface.blit(finishLineMapImage, finishLineMapPos)                           # finish line for player 1
            mainSurface.blit(finishLineMapImage, finishLineMap2Pos)                          # finish line for player 2
            pygame.draw.circle(mainSurface,circleMapColour2,circleMapPos,10)                 # map circle for player 1
            pygame.draw.circle(mainSurface,circleMapColour1,circleMap2Pos,10)                # map circle for player 2
            
            if scroll > backgroundImage_height:                                              # if scroll or the y of the background goes outside the images height
                scroll = 0                                                                   # resets scroll
                
                # counts how many times the background scrolls
                badGuysStart += 1
                bowserStart += 1
                starStart += 1
                
                # random bad guy image
                badGuysImage = random.choice(badGuysList)
                badGuysImage_height = badGuysImage.get_height()
                
                # random position to scroll from
                badGuysPos[0] = random.randint(70,250)
                bowserPos[0] = random.randint(70,250)
                starPos[0] = random.randint(70,250)
                badGuysPos2[0] = random.randint(470,650)
                bowserPos2[0] = random.randint(470,650)
                starPos2[0] = random.randint(470,650)
    
            if badGuysStart %2 == 1:                                              # every two times the scroll background happens, a badguy appears at a random x and scroll
                for distance in range (0,2):                                      # the range is the distance of how far the image will be before bliting another one, making it seem like its scrolling
                    scrolling(badGuysPos,badGuysPos2,badGuysImage_height,badGuysScroll,0) # calls function that makes the y pos move downwards, scrolling affect
                    mainSurface.blit(badGuysImage,(badGuysPos[0],badGuysPos[1]))  # blits image
                    mainSurface.blit(badGuysImage,(badGuysPos2[0],badGuysPos2[1]))
                    badGuysScroll += 3    # how fast the image will move
            
            if bowserStart % 5 == 1:                                              # every five times the scroll background happens, a bowser appears at a random x and scroll
                for distance in range (0,2):                                      # the range is the distance of how far the image will be before bliting another one, making it seem like its scrolling
                    scrolling(bowserPos,bowserPos2,bowserImage_height,bowserScroll,0) # calls function that makes the y pos move downwards, scrolling affect
                    mainSurface.blit(bowserImage,(bowserPos[0],bowserPos[1]))     # blits image
                    mainSurface.blit(bowserImage,(bowserPos2[0],bowserPos2[1]))
                    bowserScroll += 7                                             # how fast the image will move
            
            if starStart % 4 == 1:                                                # every four times the scroll background happens, a bowser appears at a random x and scroll
                for distance in range (0,2):# the range is the distance of how far the image will be before bliting another one, making it seem like its scrolling
                    scrolling(starPos,starPos2,starImage_height,starScroll,25)    # calls function that makes the y pos move downwards, scrolling affect
                    mainSurface.blit(starImage,(starPos[0],starPos[1]))           # blits image
                    mainSurface.blit(starImage,(starPos2[0],starPos2[1]))
                    starScroll += 5                                               # how fast the image will move
            
            if circleMapPos[1] < 70:                                              # once the circle on mini map reaches the end, a scroll finish line will display
                for distance in range (0,2):                                      # the range is the distance of how far the image will be before bliting another one, making it seem like its scrolling
                    scrolling(finishLineBigPos,finishLineBig2Pos,finishLineBigImage_height,finishLineScroll,0) # calls function that makes the y pos move downwards, scrolling affect
                    mainSurface.blit(finishLineBigImage,(finishLineBigPos[0],finishLineBigPos[1])) # blits image
                    mainSurface.blit(finishLineBigImage,(finishLineBig2Pos[0],finishLineBig2Pos[1]))
                    finishLineScroll += 2                                         # how fast the image will move
                      
            # if the obstacles/objects go out of the road, resets value to start at the beginning
            if badGuysScroll > 650: 
                badGuysScroll = 0 
                badGuysStart = 0
            
            if bowserScroll > 650: 
                bowserScroll = 0 
                bowserStart = 0
            
            if starPos[1] > 650: 
                starScroll = 0 
                starStart = 0
            
            # collision detection for yoshi (player 1)
            if yoshiCollision.colliderect(badGuysCollision):                   # between yoshi and badguys
                yoshiPos[1] = badGuysPos[1] + 50                               # makes yoshi move downwards
                        
            elif yoshiCollision.colliderect(bowserCollision):                  # between yoshi and bower
                yoshiPos[1] = bowserPos[1] + 60                                # makes yoshi move downwards
            
            elif yoshiCollision.colliderect(starCollision) and starPowerUp < 4:# between yoshi and star 
                starPos[0] = 900             
                starPowerUp += 1                                               # loads up a star powerup, ready for use
            
            elif yoshiCollision.colliderect(finishLineCollision):              # between yoshi and finish line 
                fileList1 = fileReadingAndWriting("yoshistotalwins.txt",1)     # function for file reading and writing to find total wins, add a win to yoshi wins
                fileList2 = fileReadingAndWriting("toadstotalwins.txt",0)
                pygame.mixer.music.load("win.mp3")                             # music
                pygame.mixer.music.play()
                gamestate = "yoshiwins"                                        # yoshi wins, gamestate changes
            
            # if entire car goes outside the screen from the bottom, yoshi loses
            if yoshiPos[1] > 600:                
                yoshiDead = True
                mainSurface.blit(loseImage,(0,0))
               
            # collision detection for toad (player 2)
            if toadCollision.colliderect(badGuysCollision2):                   # collision detection between car and badguys player 2
                toadPos[1] = badGuysPos2[1] + 50
            
            elif toadCollision.colliderect(bowserCollision2):                  # collision detection between car and bowser player 2
                toadPos[1] = bowserPos2[1] + 60
            
            elif toadCollision.colliderect(starCollision2) and starPowerUp2 < 4: # collision detection between car and star player 2
                starPos2[0] = 900
                starPowerUp2 += 1
            
            elif toadCollision.colliderect(finishLineCollision2):         # collision detection between car and finish line player 2
               fileList1 = fileReadingAndWriting("yoshistotalwins.txt",0) # function for file reading and writing to find total wins
               fileList2 = fileReadingAndWriting("toadstotalwins.txt",1)  # add a win to toad win
               pygame.mixer.music.load("win.mp3")                         # music
               pygame.mixer.music.play()
               gamestate = "toadwins"                                     # toad wins, gamestate changes
               
            if toadPos[1] > 600:                                          # if entire goes outside the screen from the bottom, toad loses
                toadDead = True
                mainSurface.blit(loseImage,(400,0))
              
            # yoshi (player 1) power up star display on the side
            if yoshiPos[1] < 600:                                         # if yoshi is still on the road/screen
                if starPowerUp > 3:                                       # player can't have over 3 power ups
                    starPowerUp = 3
                             
                if starPowerUp == 1:                                      # if player has 1 star loadup, display 1 star
                    mainSurface.blit(starPowerImage,starPowerPos)
                    
                elif starPowerUp == 2:                                    # if player has 2 star loadup, display 2 star
                    mainSurface.blit(starPowerImage,starPowerPos)
                    mainSurface.blit(starPowerImage,(starPowerPos[0] - 22,starPowerPos[1]))
                                
                elif starPowerUp == 3:                                    # if player has 3 star loadup, display 3 star
                    mainSurface.blit(starPowerImage,starPowerPos)
                    mainSurface.blit(starPowerImage,(starPowerPos[0] - 22,starPowerPos[1]) )
                    mainSurface.blit(starPowerImage,(starPowerPos[0] - 44,starPowerPos[1]) )
                    
            # toad (player 2) power up star display on the side
            if toadPos[1] < 600:                                         # if toad is still on the road/screen
    
                if starPowerUp2 > 3:                                     # player can't have over 3 power ups
                    starPowerUp2 = 3
                             
                if starPowerUp2 == 1:                                    # if player has 1 star load up, 1 star displays
                    mainSurface.blit(starPowerImage,starPowerPos2)
                    
                elif starPowerUp2 == 2:                                  # if player has 2 star load up, 2 stars display
                    mainSurface.blit(starPowerImage,starPowerPos2)
                    mainSurface.blit(starPowerImage,(starPowerPos2[0] - 22,starPowerPos2[1]))
                                
                elif starPowerUp2 == 3:                                  # if player has 3 star load up, 3 stars display
                    mainSurface.blit(starPowerImage,starPowerPos2)
                    mainSurface.blit(starPowerImage,(starPowerPos2[0] - 22,starPowerPos2[1]) )
                    mainSurface.blit(starPowerImage,(starPowerPos2[0] - 44,starPowerPos2[1]) )
                
            # restrictions for yoshi (player 1)
            if yoshiPos[1] < 10:                                        # yoshi can't go outside the screen at the top
                yoshiPos[1] = 10
                
            if yoshiPos[0] < 75:                                        # yoshi can't go outside track from the left
                yoshiPos[0] = 75
   
            elif yoshiPos[0] > 275:                                     # yoshi can't go outside track from the right
                yoshiPos[0] = 275
        
            # restrictions for toad (player 2)
            
            if toadPos[1] < 10:                                         # toad can't outside the screen at the top
                toadPos[1] = 10
            if toadPos[0] < 475:                                        # toad can't go outside track from the left
                toadPos[0] = 475
                       
            elif toadPos[0] > 675:                                      # toad can't go outside track from the right
                toadPos[0] = 675
            
            # position of the map circle equals speed, making it move constantly upwards
            circleMapPos[1] -= circleMapSpeed  
            circleMap2Pos[1] -= circleMapSpeed
            
        
            line = mb.nonBlockingReadLine()                              # takes data from the microbit for yoshi (player 1)
            line2 = mb2.nonBlockingReadLine()                            # takes data from the microbit for toad (player 2)
             
            # yoshi (player 1) movement from mircobit
            if line != None:                                             # if there is a value in line
                line = int(line) 
                
                if line > 0 and line < 3000:                             # makes yoshi go right
                    yoshiPos[0] = line/12 + 200
                
                elif line < 0:                                           # makes car go left
                    yoshiPos[0] = 200 - (line/8*-1)
                
                elif line == 0:                                          # midline 
                    yoshiPos[0] = 200
                
                if (starPowerUp > 0 and starPowerUp < 4) and line == 3000 and yoshiDead == False: # if star loadup is between 1-3, button on microbit is pressed and yoshi is not dead
                    pygame.mixer.Sound.play(powerUpSound)                # sound
                    actualStartPowerUp = 1                               # adds 1 to variable to start the power up
                    starPowerUp -= 1                                     # remove 1 star loadup 
                
            # player 2
            if line2 != None:                                            # if there is a value in line
                line2 = int(line2)
                 
                if line2 > 0 and line2 < 3000:                           # makes car go right
                    toadPos[0] = line2/12 + 600
     
                elif line2 < 0:                                          # makes car go left
                    toadPos[0] = 600 - (line2/7*-1)
                         
                if (starPowerUp2 > 0 and starPowerUp2 < 4) and line2 == 3000 and toadDead == False: # if star loadup is between 1-3, button on microbit is pressed and toad is not dead
                    pygame.mixer.Sound.play(powerUpSound)                # music
                    actualStartPowerUp2 = 1                              # adds 1 to variable to start the power up
                    starPowerUp2 -= 1                                    # remove 1 star loadup

            # powerup movement for yoshi (player 1)
            if actualStartPowerUp == 1:                                  # variable for when player presses button
                yoshiSpeed[1] -= 1                                       # car moves
                if yoshiSpeed[1] < -15:
                    actualStartPowerUp = 0                               # variable to start power up off
            else:
                yoshiSpeed[1] = 0                                        # car stops moving
            
            # makes car move from power up for player 2
            if actualStartPowerUp2 == 1: 
                toadSpeed[1] -= 1                                        # car moves
                if toadSpeed[1] < -15:
                    actualStartPowerUp2 = 0                              # variable to start power up off
            else:
                toadSpeed[1] = 0                                         # car stops moving
            
            if yoshiPos[1] > 600 and toadPos[1] > 600:                   # if yoshi and toad are outside the road/screen, meaing both players lost
                pygame.mixer.music.load("died.mp3")                      # music
                pygame.mixer.music.play() 
                fileList1 = fileReadingAndWriting("yoshistotalwins.txt",0) # function for file reading and writing to find total wins
                fileList2 = fileReadingAndWriting("toadstotalwins.txt",0)  # don't add any wins as both players lose
                gamestate = "bothlose"

            # position y increases when speed greater than 0 for players
            yoshiPos[1] += yoshiSpeed[1] 
            toadPos[1] += toadSpeed[1]
            
            #  the images on the screen
            mainSurface.blit(yoshiImage, yoshiPos) 
            mainSurface.blit(toadImage, toadPos)
        
        
        # if yoshi wins, display yoshi win screen
        elif gamestate == "yoshiwins":
            mainSurface.blit(yoshiWinsImage, (0,0))
        
        
        # if toad wins, display toad win screen
        elif gamestate == "toadwins":
            mainSurface.blit(toadWinsImage, (0,0))
        
        
        # if both players lose, display both lose screen
        elif gamestate == "bothlose":
            mainSurface.blit(bothLoseImage, (0,0))
        
        
        # if game finishes, display replay button 
        if gamestate =="toadwins" or gamestate == "yoshiwins" or gamestate == "bothlose":
            pygame.draw.circle(mainSurface, buttonColour, button3Pos, buttonSize)
            mainSurface.blit(playText, (370,530))
            mainSurface.blit(againText, (360,500))
            
            # displays text of how many times yoshi has won since the program started
            yoshiText = font.render(f"TOTAL YOSHI WINS:{fileList1}", 7, pygame.Color("white"))
            mainSurface.blit(yoshiText, (40,550))
            
            # displays text of how many times toad has won since the program started
            toadText = font.render(f"TOTAL TOAD WINS:{fileList2}", 7, pygame.Color("white"))
            mainSurface.blit(toadText, (500,550))
            
            # if button is pressed, replay game
            if ev.type == pygame.MOUSEBUTTONUP: 
                    if distFromPoints(button3Pos,mouseCirclePos) < (buttonSize):
                        gamestate = "set microbit"

            #mb.closeConnection()
        pygame.display.flip()
        
        clock.tick(60) #Force frame rate to be slower
    
    pygame.quit()     # Once we leave the loop, close the window.

main()                