from tkinter import *
from tkinter.font import Font
from tkinter.filedialog import askopenfile
from tkinter import filedialog as fd
import os
import webbrowser
from tkinter import scrolledtext
 

##########################__View__###############################
def view_tree():
	os.system("notepad temp/temp_tree.txt")

##########################__Browse/Upload__######################
def browse_file():
	file_n.delete(1.0,END)
	b_file = fd.askopenfilename()
	file_n.insert(INSERT, b_file)
	file_n.pack(side = TOP)
	file_path.set(b_file)
	file_open = open(file_path.get())
	temp_data = file_open.read()
	file_write = open("temp/temp_data.txt", "w")
	file_write.write(temp_data)
	file_write.close()
	
############################__Submit__############################
def submit_file():
	status_message.set("\nRunning Phylobit...\n")
	status.insert(INSERT, status_message.get())
	status.pack(side = TOP)
	os.system("python build_tree.py temp/temp_data.txt")
	status_message.set("\nTree construction complete...\n")
	status.insert(END, status_message.get())
	status.pack(side = TOP)

##########################__PhyloBit__############################
def PhyloBit():
	pb_win = Tk()
	pb_win.geometry("400x300")
	pb_win.maxsize(400,300)
	pb_win.title("PhyloBit")
	Label(pb_win, text = "PhyloBit", font = "Arial 20 bold", bg = "spring green",fg = "black").pack(padx = 20, pady = 20)
	Label(pb_win, 
	text = 
"""
PhyloBit is a Phylogenetic tree making
tool based on Distance-matrix method 
and use GUI(Graphical User Interface) 
as a interface between the user and 
the program.
It is developed by Rajan (M.Sc. Student)
of University of Delhi, Delhi, India.
It has been developed as an independent
project just to learn about phylogenetic
tree.
""", font ="Arial 11 bold", bg = "white").pack(padx = 10, pady = 10)
	mainloop()

###########################__About__#############################
def about():
	about_win = Tk()
	about_win.geometry("300x220")
	about_win.maxsize(300,220)
	about_win.title("About")
	Label(about_win, 
	text = 
"""



    PhyloBit_GUI 1.2    



""", font ="Arial 14 bold", bg = "white").pack(pady = 30,padx = 10)
	mainloop()

############################__Help__#############################
def help():
	webbrowser.open("https://github.com/rajanbit")

###########################__Support__###########################
def support():
	sup_win = Tk()
	sup_win.geometry("300x220")
	sup_win.maxsize(300,220)
	sup_win.title("Support")
	Label(sup_win, 
	text = 
"""


Windows OS

Python 3.7   
        
NumPy [Matrix handling]

Tkinter [G.U.I]


""", font ="Arial 14 bold", bg = "white").pack(pady = 30,padx = 10)
	mainloop()

#################################################################
# Configuration
gui = Tk()
gui.geometry("500x650")
gui.maxsize(500,650)
gui.title("PhyloBit")
menu = Menu(gui)
gui.config(menu=menu)

###############################################################
# Variables
status_message = StringVar(gui,"")
status_message.set(" ")
file_path = StringVar(gui,"")
file_path.set("No file selected...")

##################################################################
# FRAME_1
frame1 = Frame(gui, bg = "ghost white", height = 630, width = 480) 
frame1.pack(side = TOP, pady = 20)
# File Menu
f_menu = Menu(menu, tearoff = 0)
f_menu.add_command(label = "Upload", command = lambda:browse_file())
f_menu.add_separator()
f_menu.add_command(label = "Exit", command = gui.quit)
menu.add_cascade(label = "File",  menu = f_menu)
# Tools Menu
t_menu = Menu(menu, tearoff = 0)
t_menu.add_command(label = "PhyloBit", command =lambda:PhyloBit())
menu.add_cascade(label = "Tools", menu = t_menu)
# Help Menu
h_menu = Menu(menu, tearoff = 0)
h_menu.add_command(label = "Help", command = lambda:help())
h_menu.add_command(label = "Support", command = lambda:support())
menu.add_cascade(label = "Help", menu = h_menu)
# About Menu
a_menu = Menu(menu, tearoff = 0)
a_menu.add_command(label = "About", command = lambda:about())
menu.add_cascade(label = "About", menu = a_menu)
# Header
rt_init = os.getcwd()
rt_images = rt_init
name = PhotoImage(file = rt_images+"/n.png")
logo = PhotoImage(file= rt_images+"/s.png")
Label(frame1,
		image = name).pack(pady = 10)
Label(frame1,
		image = logo).pack()
Label(frame1, 
		 text="""A tool for constructing Phylogenetic Tree
based on Distance-matrix method.""",
		 fg = "black",
		 bg = "ghost white",
		 font = "Arial 12 bold").pack(padx = 20,pady = 10)
# FRAME_2
frame2 = Frame(frame1, bg = "pale green", height = 300, width = 400) 
frame2.pack(side = TOP, pady = 15)
# Upload Button
browse = Button(frame2, text = "Browse", font = "Arial 15 bold", command = lambda:browse_file()).pack(pady = 10, padx = 160)
file_n = Text(frame2, height = 2, width = 50,bg = "white")
file_n.insert(INSERT, file_path.get())
file_n.pack(side = TOP)
# Submit Button
submit = Button(frame2, text = "Submit", font = "Arial 15 bold", command = lambda:submit_file()).pack(pady = 10)
status = scrolledtext.ScrolledText(frame2,height = 5, width = 50,bg = "white")
status.insert(INSERT, status_message.get())
status.pack(side = TOP)
# View Button
view = Button(frame2, text = " View ", font = "Arial 15 bold", command = lambda:view_tree()).pack(pady = 10)
mainloop()

