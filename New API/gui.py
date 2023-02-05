# generate tkinter template

import tkinter as tk
import customtkinter

# create the main window
root = tk.Tk()
root.title('My Tkinter App')
root.geometry('1080x680')

# create a label widget 
label = tk.Label(root, text="Hello World!") 
label.pack() 
  
# run the main loop 
root.mainloop()