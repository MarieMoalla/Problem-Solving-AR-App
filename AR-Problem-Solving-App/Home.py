# -*- coding: utf-8 -*-
import tkinter as tk
from PIL import Image, ImageTk
import os

root = tk.Tk()

canvas = tk.Canvas(root, width=600, height=200)
canvas.grid(columnspan=3, rowspan=4)
#canvas.config(bg="white")


#logo
logo = Image.open('logo.png')
logo = logo.resize( (200, 200)) 
logo = ImageTk.PhotoImage(logo)
logo_label = tk.Label(image=logo)
logo_label.image = logo
logo_label.grid(column=1, row=0)


#download bdf button
browse_text = tk.StringVar()
browse_btn = tk.Button(root, textvariable=browse_text,command=lambda:open_file(), font="Raleway", bg="orange", fg="white", height=1, width=20)
browse_text.set(" Download Documentation ")
browse_btn.grid(column=1, row=2)

#download bdf button
browse_text = tk.StringVar()
browse_btn = tk.Button(root, textvariable=browse_text,command=lambda:open_team_view(), font="Raleway", bg="orange", fg="white", height=1, width=20)
browse_text.set(" Team Info")
browse_btn.grid(column=1, row=3)


#instructions
instructions = tk.Label(root, text="Welcome! To Tunisian Collegiate Programming Contest ", font="Raleway")
instructions.grid(columnspan=3, column=0, row=1)

canvas = tk.Canvas(root, width=600, height=250)
canvas.grid(columnspan=3)

def open_file():
    browse_text.set("loading...")
    

def open_team_view():
    try:
        from QrCodeScanner import main
    except:
        print("window already open!")
    
    
    
root.mainloop()