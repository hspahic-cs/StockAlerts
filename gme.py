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
WIDTH = 1000
HEIGHT = 700
xVelocity = 3
yVelocity = 2
window = Tk()
canvas = Canvas(window,width=WIDTH,height=HEIGHT)
canvas.pack()


andromeda = PhotoImage(file='Images/Andromeda.png')
background = canvas.create_image(0,0,image=andromeda,anchor=NW)
wsb = PhotoImage(file='Images/wsb.png')
myImage = canvas.create_image(0,0,image=wsb,anchor=NW)

IMG_W = wsb.width()
IMG_H = wsb.height()

GME = Stock("GME")
timer = 0 
while True:
    coordinates = canvas.coords(myImage)
    print(coordinates)
    if (coordinates[0] >= (WIDTH-IMG_W) or coordinates[0]<0):
        xVelocity *= -1
    if (coordinates[1] >= (HEIGHT-IMG_H) or coordinates[1]<0):
        yVelocity *= -1 
    canvas.move(myImage,xVelocity,yVelocity)
    #Code for discplaying price
    if (timer == 180):
        x = GME.getPrice()
        price = Label(text=x,bg="black",fg="green",font=("Helvetica",36))
        price.place(height=150,width=150,x=((WIDTH/2)-50),y=((HEIGHT/2)-50))
        timer = 0
    ###
    window.update()
    time.sleep(0.01)
    timer += 1
window.mainloop()

