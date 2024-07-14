#Import the required library
from tkinter import *

#SCROLL
def display(SCROLL_MODE):
    #Create an instance of tkinter frame
    win = Tk()
    #Set the geometry
    win.geometry("500x280")
    if SCROLL_MODE == TRUE:
        canvas= Canvas(win, width= 500, height= 280, bg="Green")
        canvas.create_text(200, 150, text="Scroll Mode ON", fill="black", font=('Helvetica 15 bold'))
        canvas.pack()

    else:
        canvas2= Canvas(win, width= 500, height= 280, bg="Red")
        canvas2.create_text(200, 150, text="Scroll Mode OFF", fill="black", font=('Helvetica 15 bold'))
        canvas2.pack()

    win.after(1000,lambda:win.destroy())
    win.mainloop()
