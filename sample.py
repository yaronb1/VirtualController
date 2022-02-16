#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 19 22:55:03 2022

@author: yaron

this is a sample project which illistrates how to use the SmartController module
to create an on screen UI which is designed to be controlled via hand gestures and movement

We will create several screens:
Youtube screen:
    control youtube with our finggers
    Please make sure you check the useYoutube box in the startup screen and sign in with a valid
    username and password

Draw ccanvas
    will ollow us to draw with our fingers and create an imprint of our lips


"""

import tkinter as tk

import cv2
import time

import handLandmarks as hl  #imports the module we have written
import youTube
import HA
import netflix
import SmartController as sc

#step 1
# create our default objects:
controller = sc.Controller() # handles all events and UI images
detector= hl.handDetector() # detects hands as well as info about them
brush = sc.Drawer()         # draws on the canvas which will be combined with the screen


global canvas                   # create a global variable for the canvas so we can access it througgh our functions
global yt                       # create a global variable for the youtube object and initialise it
yt=youTube.youTubeController()  # note: if we our using home assistant( for light control) or netflix(added in future updates)
                                # we will create and initailise here as well


width,height = 1280,720   # screen width and height in pixels. Please adjust according to your screen
size= (width,height)


# Step 2:
# initialise the different screens we will be using
# UI mode should be set according to you images
# if you are using my default images leave as is
# draw must be set to true if you plan on drawing on that screen
startScreen=sc.Screen(ui_mode='transparent')
homeScreen= sc.Screen(ui_mode='transparent')
drawScreenMain = sc.Screen(ui_mode='crop')
drawScreenBrush = sc.Screen(ui_mode='crop', draw=True)
drawScreenLips = sc.Screen(ui_mode='crop', draw = True)
youtubeScreen = sc.Screen(ui_mode='inside_screen')

# The following are our various functions which will be called when gesture or button pressed
# each function must be called with *args to avoid errors
# if arguments must be passed we will set a global variable arggs to the required arguments in the while loop
def fistG(*args):
    controller.cs=1
    print("fist")

def fin1G(*args):
    print("lights")
    
def fin2G(*args):
    print("you")
    controller.cs = 5
    youtubeScreen.start=True
    
def fin3G(*args):
    print("net")
    
def fin4G(*args):
    controller.cs=2
    
def colour_pallatte(*args):
    controller.cs = 3
    
def lip(*args):
    controller.cs= 4
    
def red_brush(*args):
    drawScreenBrush.cui=3
    brush.colour=(0,0,255)
    brush.thickness=15
    
def green_brush(*args):
    drawScreenBrush.cui=2
    brush.colour=(0,255,0)
    brush.thickness=15
    
def blue_brush(*args):
    drawScreenBrush.cui=1
    brush.colour=(255,0,0)
    brush.thickness=15
    
def eraser(*args):
    drawScreenBrush.cui=4
    brush.colour=(0,0,0)
    brush.thickness=100
    
def draw_brush(*args):
    canvas= brush.draw(args[0][0], args[0][1], args[0][2])
    
    
    
def stop_drawing(*args):
    brush.start=True
    
    
def blue_lips(*args):
    drawScreenLips.cui=0
    brush.colour=(255,0,0)
    brush.thickness=15
    
def green_lips(*args):
    drawScreenLips.cui=1
    brush.colour=(0,255,0)
    brush.thickness=15
    
def red_lips(*args):
    drawScreenLips.cui=2
    brush.colour=(0,0,255)
    brush.thickness=15
    
def default_lips(*args):
    drawScreenLips.cui=3
    brush.colour=(255,255,255)
    brush.thickness=15
    
def draw_lips(*args):
    canvas = brush.drawLips(args[0])
    print('lips')
    
    
    
def back_func(*args):
    controller.cs =1
    
def youtube_func(*args):
    x=args[0][0]
    y=args[0][1]
    
    yt.posClick(x, y)
    yt.waitForPageToLoad(width, height)
    youtubeScreen.start=True
    
def swipe(*args):
    yt.scroll()
    print('swipe')
    yt.waitForPageToLoad(width, height)
    youtubeScreen.start=True


    
# main will be called once the program starts
def main():
    print("started")
    
    
    args = []  # variable to be passed to the functions. must be updated accordingly in while loop
    pTime,cTime=0,0 # variables for fps
    hand = None # declared here and updated accordingly to right or left in  while loop
    start_ges, end_ges = False, False # will be used to determine movement

    #steap 3 :
    # declare gestures, movements and buttons and add them to their respective screens
    # as well as add the relevant UI to the screen
    # gestures check which finggers are raised (currently. more ggestures will be added in future updates)
    # the gesture will be passed in the following format:
        # [thumb, index, middle, ring, pinky]
        # where 1 indicates the finger is raised and 0 indicates the finger is lowered
    # func must equal the relevant function to be called and must be declared with the above functions

    back = sc.Gesture(gesture=[1,1,1,1,1], func=back_func) # 5 fingers will take us back to the home screen
    
    #cs  =  0
    startScreen.add_images('start', size)  # add images to the screen. each screen will have its own folder in the
    # projects images folder. This folder should be passed as the first argument and screen size (declared above) is the secod arggument
    fist=sc.Gesture(gesture=[0,0,0,0,0],func=fistG) # a fist will move from the first screen to the next one
    startScreen.add_gesture(fist) # make sure to add the gesture to the screen
    
    #cs = 1
    
    homeScreen.add_images('main', size)
    fin_1= sc.Gesture(gesture=[0,1,0,0,0],func=fin1G)
    fin_2= sc.Gesture(gesture=[0,1,1,0,0],func=fin2G)
    fin_3= sc.Gesture(gesture=[0,1,1,1,0], func=fin3G)
    fin_4= sc.Gesture(gesture=[0,1,1,1,1], func=fin4G)
    homeScreen.add_gesture(fin_1)
    homeScreen.add_gesture(fin_2)
    homeScreen.add_gesture(fin_3)
    homeScreen.add_gesture(fin_4)
    
    #cs = 2
    drawScreenMain.add_images('draw_screen_main', size)
    #buttons are created with a rectangle, that if our finger move through that rectangle it will be pressed
    # the coordinates of the rectangle will be passed as the following variables.
    # TIP: create a virtual button using UI ( just a regular image that when we hover with our fingers will be preesed )
    # then move around with your finger and print its x and y to determine where those coordinates are
    colour_pallatte_button = sc.Button(func=colour_pallatte,startX=100, startY=100, endX=150, endY=150)
    lipAdd = sc.Button(func=lip, startX=570, startY=70, endX=690, endY=120)
    drawScreenMain.add_button(colour_pallatte_button)
    drawScreenMain.add_button(lipAdd)
    drawScreenMain.add_gesture(back)
    
    #cs= 3
    
    drawScreenBrush.add_images('draw_screen_brush',(width,height))
    painterRed=sc.Button(func=red_brush,startX=450, startY=50, endX=580,endY=90)
    painterBlue = sc.Button(func=blue_brush,startX=90,startY=50, endX=220,endY=90)
    painterGreen = sc.Button(func=green_brush,startX=270, startY=50, endX=400, endY=90)
    eraserB = sc.Button(func=eraser,startX=1100,startY=50,endX=1200, endY=90)
    drawBG = sc.Gesture(gesture=[0,1,0,0,0],gestureTime = 0.1 ,func=draw_brush)
    stopDrawing = sc.Gesture(gesture=[0,1,1,0,0],gestureTime = 0.1 ,func=stop_drawing)
    drawScreenBrush.add_button(painterRed)
    drawScreenBrush.add_button(painterBlue)
    drawScreenBrush.add_button(painterGreen)
    drawScreenBrush.add_button(eraserB)
    drawScreenBrush.add_gesture(drawBG)
    drawScreenBrush.add_gesture(stopDrawing)    
    drawScreenBrush.add_gesture(back)
    
    #cs= 4
    drawScreenLips.add_images("draw_screen_lips", size)
    blueLips = sc.Button(func=blue_lips, startX=100,startY=60,endX=170,endY=120)
    greenLips = sc.Button(func=green_lips, startX=430,startY=60,endX=550,endY=120)
    redLips = sc.Button(func=red_lips, startX=780,startY=60,endX=900,endY=120)
    defaultLips = sc.Button(func=default_lips, startX=1160,startY=60,endX=1270,endY=120)
    drawG = sc.Gesture(gesture=[0,1,0,0,0], func = draw_lips)
    drawScreenLips.add_button(blueLips)
    drawScreenLips.add_button(redLips)
    drawScreenLips.add_button(greenLips)
    drawScreenLips.add_button(defaultLips)
    drawScreenLips.add_gesture(drawG)
    drawScreenLips.add_gesture(back)
    
    #cs= 5
    #youtubeScreen.add_images('optionsY', size)
    
    try:youtubeScreen.web_object= yt
    except: pass
    you_select = sc.Gesture(gesture=[0,1,1,0,0],func=youtube_func)
    you_swipe=sc.Gesture(single_gesture=False,func=swipe)  # swiping to scroll
                                                           # this is a movement and not a stationary gesture
                                                           # therefore single_gesture will be false and
                                                           # and we will update the start_ges( what triggers the gesture)
                                                           # and end_ges (what completes it) in the while loop accordingly
    youtubeScreen.add_gesture(you_select)
    youtubeScreen.add_gesture(you_swipe)


    # step 4:
    # add all the screens to the controller and note the order in which we are adding them
    # controller.cs will let us follow along which screen we are on
    controller.add_screen(startScreen) # cs = 0
    controller.add_screen(homeScreen)  # cs =1
    controller.add_screen(drawScreenMain) # cs = 2
    controller.add_screen(drawScreenBrush) # cs = 3
    controller.add_screen(drawScreenLips) # cs = 4
    controller.add_screen(youtubeScreen) # cs = 5
    

    # grab and set our camera
    # if you have multiple cameras connected adjust the videocapture value accordingly
    cap = cv2.VideoCapture(-1)
    cap.set(3,width)
    cap.set(4,height)
    

    # step 5:
    # create a while loop that will ggenerate a videostream
    # here we will see our camera stream, process the image and update variuos variables
    # such as controller.cs ( the current screen), args ( arguments to be passed to functions) and start_ges, end_ges
    # ( movements)
    while True:

        # grab the frame from the camera and mirror it
        success, img = cap.read()
        img = cv2.flip(img,1)
        
        imgUI = img.copy()

        # process the image to find and analyse the hands
        img = detector.findHands(img)
        handedness = detector.handedness() # determine whether right or left
        right, left= detector.findPosition(img) # returns a list with the positions of all the landmarks
        fingers = detector.fingerCounter()      # return a list with which fingers are raised
        angle = detector.fingerAngle(1, handedness) # angle of a specif finger ( index = 1)

        # check which hand is raised and update the approprete list
        # Note: since the hands are mirrors of each other right and left will be analysed differently
        # so this step is important to avoid errors
        if handedness == 'Right':
            lmList = right
        elif handedness == 'Left':
            lmList = left
        else: lmList = []
        
        screen = controller.screens[controller.cs] # this is the current screen we are on

        # if a hand is recognised
        if len(lmList)!=0:
            
            
            # 2 fingers raised will indicate we are in select mode and can press buttons
            # if we are not in select mode we cannot press buttons
            # if you wish to peress buttons with a different gesture change accordingly
            if fingers == [0,1,1,0,0]:#selectmode
                x,y= lmList[8][1],lmList[8][2]
            else: x,y=0,0
            
            
            # step 6:
            # update the relevant variables according to which screen we are on


            # in the draw screen we want to pass the x and y coordinates of the finger we will use to draw
            # so args is updated accordingly (index finger is used)
            if controller.cs==3:
                args=imgUI,lmList[8][1],lmList[8][2]

            
            if controller.cs==4:
                args=imgUI


            # in the youtube screen we want to update start and end ges for the swipe movemnet
            # update hand which will be put on the UI ( which is inside_screen)
            # and the args  x and y where we want to press
            if controller.cs==5:
                
                if angle < 5 and lmList[4][1]>lmList[6][1] :
                    start_ges= True
                else:start_ges=False
                
                if angle > 45:
                    end_ges=True
                else:end_ges=False
                
                hand = detector.isolateHand(img, handedness)
                x,y =lmList[8][1],lmList[8][2]
                args= x,y

            # controller.run must be called every frame to check if the gestures or buttons are being pressed
            # args - argguments to be passed to the functions which will be called if a gesture or button is pressed
            # fingers - list in the correct format (obtained from detector.fingercounter) which is the ggesture that is seen
            # x,y - coordinates of our finger (or something else) that if is in the button rectangle the button is considered pressed
            #start_ges, end_ges - used to determine if movement is seen
            controller.run(args,fingers=fingers,x=x,y=y,start_ges=start_ges,end_ges=end_ges)


        #step 7:
        # showing the imagge to the user along with UI and anything else we wish to display

        # displays the frames per second
        cTime = time.time()
        fps = 1/(cTime - pTime)
        pTime = cTime
        cv2.putText(img, str(int(fps)), (10,70), cv2.FONT_HERSHEY_COMPLEX,3,
                        (255,0,255),3)

        #put on the UI ( based on mode in the screen)
        try:finalI = screen.ui_handler(img, brush.imgCanvas,hand)
        except:
            print("display error")
            cv2.imshow("imagee", img)
            cv2.imshow('ui', screen.ui[screen.cui])
        else:
            cv2.imshow("image", finalI)


        # pressing q will break the loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            break

    
    
    
    
# the following is a simple UI which will help us sign in to our relevant accounts
# youtube, homeassistant ( used for lights and other smart devices), and netflix( currently unavailabe)
# check the box of the accounts you wish to sign in to and put in your username and password

def checkButtons():
    if HAvar.get()== 1:
        pass
        #print("checked")
        
    if HAvar.get() == 0:
        pass
        #print ("unchecked")
    
def signIn():
    global home
    global yt
    global nf
    if HAvar.get()==1:
        if HAuser.get() == 'Username' and HApassword.get()=='Password':
            home = HA.HAController()
            
        else:
            home = HA.HAController(username= HAuser.get(), password = HApassword.get())
        home.openHA()
    
    
    if YTvar.get()==1:
        if YTuser.get() == 'Username' and YTpassword.get()=='Password':
            yt = youTube.youTubeController()
        else:
            yt = youTube.youTubeController(username= YTuser.get(), password= YTpassword.get())
        
        yt.openYoutube()
        #print(yt.ping())
        
    
    if NFvar.get()==1:
        if NFuser.get() == 'Username' and NFpassword.get()=='Password':
            nf = netflix.netflixController()
        else:
            nf = netflix.netflixController(username=NFuser.get(),password= NFpassword.get())
        nf.openNetflix()
    #print ("s")



def signed():
    
    s = 'youtube'
    YTsigned =  tk.Label(root,bg = "green", text = "Signed in", width =10)
    YT_not_signed =  tk.Label(root,bg = "red", text = "NOT signed in", width =10)
    
    
    try:
        if s in yt.ping():
            YTsigned.grid (row= 5, column = 1)
            YT_not_signed.grid_remove()
            #print("yes")
        else:
            YT_not_signed.grid (row= 5, column = 1)
            YTsigned.grid_remove()
            #print("no")
            
    except Exception as e: 
        #print(e)
        YT_not_signed.grid (row= 5, column = 1)
        YTsigned.grid_remove()
        #print("hell no")
        
    h = 'homeassistant'
    HAsigned =  tk.Label(root,bg = "green", text = "Signed in", width =10)
    HA_not_signed =  tk.Label(root,bg = "red", text = "NOT signed in", width =10)
    
    
    try:
        if h in home.ping():
            HAsigned.grid (row= 2, column = 1)
            HA_not_signed.grid_remove()
        else:
            HA_not_signed.grid (row= 2, column = 1)
            HAsigned.grid_remove()
            
            
    except: 
        HA_not_signed.grid (row= 2, column = 1)
        HAsigned.grid_remove()


    n = 'netflix'
    NFsigned =  tk.Label(root,bg = "green", text = "Signed in", width =10)
    NF_not_signed =  tk.Label(root,bg = "red", text = "NOT signed in", width =10)
    
    
    try:
        if n in nf.ping():
            NFsigned.grid (row= 8, column = 1)
            NF_not_signed.grid_remove()
        else:
            NF_not_signed.grid (row= 8, column = 1)
            NFsigned.grid_remove()
            
    except: 
        NF_not_signed.grid (row= 8, column = 1)
        NFsigned.grid_remove()
    root.after(500,signed)      
            
root = tk.Tk() # create the base window / widget


HAvar = tk.IntVar()
NFvar = tk.IntVar()
YTvar = tk.IntVar()
ytsigned = tk.IntVar()
ytsigned =0
welcome = tk.Label(root, text = "Welcome")


#HAL = tk.Label(root, text = "Use Home Assistant")

HAL = tk.Checkbutton(root, text='Use Home Assistant',variable=HAvar, onvalue=1, offvalue=0, command=checkButtons)
HAuser = tk.Entry(root, width = 20)
HAuser.insert(0, "Username") # insert default text
HApassword = tk.Entry(root, width = 20)
HApassword.insert(0, "Password") # insert default text
#HAsign =  tk.Label(root,bg = "red", text = "NOT signed in")


#YTL = tk.Label(root, text = "Use Youtube")
YTL = tk.Checkbutton(root, text='Use Youtube',variable=YTvar, onvalue=1, offvalue=0, command=checkButtons)
YTuser = tk.Entry(root, width = 20)
YTuser.insert(0, "Username") # insert default text
YTpassword = tk.Entry(root, width = 20)
YTpassword.insert(0, "Password") # insert default text

#YTsign =  tk.Label(root,bg = "red", text = "NOT signed in")




NFL = tk.Checkbutton(root, text='Use Netflix',variable=NFvar, onvalue=1, offvalue=0, command=checkButtons)
NFuser = tk.Entry(root, width = 20)
NFuser.insert(0, "Username") # insert default text
NFpassword = tk.Entry(root, width = 20)
NFpassword.insert(0, "Password") # insert default text
#NFsign =  tk.Label(root,bg = "red", text = "NOT signed in")

signIn = tk.Button(root, text = "Sign In", padx=10, pady=10, #change size
                 command = signIn)

startButton = tk.Button(root, text = "Start", padx=10, pady=10, #change size
                 command = main)


welcome.grid(row = 0, column = 0)

HAL.grid(row = 1, column = 0)
HAuser.grid(row = 2, column = 0)
HApassword.grid(row = 3, column = 0)
#HAsign.grid (row= 2, column = 1)

YTL.grid(row = 4, column = 0)
YTuser.grid(row = 5, column = 0)
YTpassword.grid(row = 6, column = 0)
#YTsign.grid (row= 5, column = 1)

NFL.grid(row = 7, column = 0)
NFuser.grid(row = 8, column = 0)
NFpassword.grid(row = 9, column = 0)
#NFsign.grid (row= 8, column = 1)


signIn.grid(row= 10, column =0)
startButton.grid(row= 11, column =0)


signed()
#cb = Checkbutton(window, text='Python',variable=var1, onvalue=1, offvalue=0, command=print_selection)


root.mainloop() # loops the code til window exited
