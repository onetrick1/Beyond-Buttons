# Import Module
from tkinter import *
import cursor

is_on = True
def display():
    # Create Object
    root = Tk()
    
    # Add Title
    root.title('Notification')
    
    # Add Geometry
    root.geometry("500x300")
    
    # Keep track of the button state on/off
    #global is_on
    is_on = True
    
    # Create Label
    my_label = Label(root, 
        text = "Notification", 
        fg = "green", 
        font = ("Helvetica", 32))
    
    my_label.pack(pady = 20)
    
    # Define our switch function
    def switch():
        global is_on
        
        # Determine is on or off
        if is_on:
            on_button.config(image = off)
            my_label.config(text = "Notification", 
                            fg = "grey")
            is_on = False
        else:
        
            on_button.config(image = on)
            my_label.config(text = "Notification", fg = "green")
            is_on = True


    # Define Our Images
    on = PhotoImage(file = "images/on.png")
    off = PhotoImage(file = "images/off.png")
    
    # Create A Button
    on_button = Button(root, image = on, bd = 0,
                    command = switch)
    on_button.pack(pady = 50)
    
    # Execute Tkinter
    root.mainloop()