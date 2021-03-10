#This python script is designed to display a live feed  of Gamestop's price
#Dominic Wojewodka
#03/09/2021 
from tkinter import *
import time
    #for animation
    #(arch) sudo pacman -S tkinter
from Stock_Alert import Stock 
    #List of functions in Stock
    #__init__(self,ticker)
    #getPrice()
    #getOpenPrice()
    #init_treshold()
    #stdTresh()
    #alertPercent()
#Setting up the animation
WIDTH = 1920
HEIGHT = 1080
xVelocity = 3
yVelocity = 2
window = Tk()
canvas = Canvas(window,width=WIDTH,height=HEIGHT)
canvas.pack()
#selecting pictures and placing them on the canvas
andromeda = PhotoImage(file='Images/andromeda1080.png')
wsb = PhotoImage(file='Images/wsb.png')
IMG_W = wsb.width()
IMG_H = wsb.height()
background = canvas.create_image(0,0,image=andromeda,anchor=NW)
myImage = canvas.create_image(0,0,image=wsb,anchor=NW)


GME = Stock("GME")
prev=GME.getPrice()
#timer prevents lag
timer = 0 
while True:
    coordinates = canvas.coords(myImage)
    if (coordinates[0] >= (WIDTH-IMG_W) or coordinates[0]<0):
        xVelocity *= -1
    if (coordinates[1] >= (HEIGHT-IMG_H) or coordinates[1]<0):
        yVelocity *= -1 
    canvas.move(myImage,xVelocity,yVelocity)
    #Code for discplaying price
    if (timer == 180):
        new = GME.getPrice()
        if((float(new) - float(prev))<= 0):
            color = "red"
        else:
            color = "green"
        price = Label(text=new,bg="black",fg=color,font=("Helvetica",36))
        price.place(height=150,width=150,x=((WIDTH/2)-50),y=((HEIGHT/2)-50))
        prev = new
        timer = 0
    ###
    window.update()
    time.sleep(0.01)
    timer += 1
window.mainloop()

