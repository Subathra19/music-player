# Issue: Files are not displayed on listbox

import os
from tkinter import *
from tkinter import filedialog
from pygame import mixer

#=======================================Initialization=======================================
window=Tk()


mixer.init()

#=======================================Variables=======================================
bg_color="black"
control_color="turquoise1"

trackimage=PhotoImage(file="images/trackimage.png")
play=PhotoImage(file="images/play.gif")
pauseimage=PhotoImage(file="images/pause.gif")
previmage=PhotoImage(file="images/previous.gif")
nextimage=PhotoImage(file="images/next.gif")


playlist=[ ]

current = 0
paused = True
played = False

#=======================================Functions=======================================

def enumeratesongs():
    for i, song in enumerate(playlist):
       list.insert(i,os.path.basename(song))

def retrive():
    global playlist
    songlist=[]
    directory=filedialog.askdirectory()
    for root,dir,files, in os.walk(directory):
        #print(dir)
        for file in files:
            if os.path.splitext(file)[1]==".mp3":
                path=(root+'/'+file).replace('\\','/')
                print(path)
                songlist.append(path)
    
    playlist.extend(songlist)
    list.delete(0,END)
    enumeratesongs()
    # Update the number of songs in the tracklist label
    tracklist['text']="Play List-{}".format(len(playlist))
    

def playsong(event=None):
    global playlist
    global paused
    global played
    global current
    if event is not None:
        current=list.curselection()[0]
        for i in range(len(playlist)):
            list.itemconfigure(i,bg="white")
    
    mixer.music.load(playlist[current])
    paused=False
    played=True

    songtrack['anchor']='w'
    list.activate(current)
    list.itemconfigure(current,bg="white")

    pause['image']=play

    
    mixer.music.play()

def pausesong():
    global paused
    global played
    global current
    if not paused:
        paused=True
        mixer.music.pause()
        pause['image']=pauseimage

    else:
        if played==False:
            playsong()

        paused=False
        mixer.music.unpause()
        pause['image']=play

def prevsong():
    global paused
    global played
    global current
    if current>0:
        current=current-1
    else:
        current=0

    list.itemconfigure(current+1, bg="white")
    playsong()    

def nextsong():
    global playlist
    global paused
    global played
    global current
    if current<len(playlist)-1:
        current=current+1
    else:
        current=0

    list.itemconfigure(current-1, bg="white")
    playsong() 


def changevol(event=None):
    v=volume.get()
    mixer.music.set_volume(v/10)


#=======================================GUI Window=======================================

# Change the size of window
window.geometry("600x400")
window.title("Music Player")
window.configure(background=bg_color)


# Divide the screen into three frames
track=LabelFrame(window,text="Song Track",font=("times new roman",15,"bold"),bg=bg_color,fg="white",bd=5,relief=GROOVE)
track.configure(width=410,height=300)
track.grid(row=0,column=0)

tracklist=LabelFrame(window,text="Play List-{}".format(len(playlist)),font=("times new roman",15,"bold"),bg=bg_color,fg="white",bd=5,relief=GROOVE)
tracklist.configure(width=190,height=400)
tracklist.grid(row=0,column=1,rowspan=3)

trackcontrols=LabelFrame(window,font=("times new roman",15,"bold"),bg=bg_color,fg="white",bd=5,relief=GROOVE)
trackcontrols.configure(width=410,height=100)
trackcontrols.grid(row=1,column=0)

#=======================================Widgets=======================================

# Add widgets to Track screen
canvas=Label(track,image=trackimage)
canvas.configure(width=400,height=240)
canvas.grid(row=0,column=0)

songtrack=Label(track,text="CHINU'S MP3 PLAYER",font=("times new roman",15,"bold"),bg=bg_color,fg="white")
songtrack.configure(width=30,height=1)
songtrack.grid(row=1,column=0)

# Add widgets to Control screen
loadsongs=Button(trackcontrols,text="Load Songs",bg=control_color,fg="black",font=10,command=retrive)
loadsongs.grid(row=0,column=0)

prev=Button(trackcontrols,image=previmage,command=prevsong)
prev.grid(row=0,column=1)

pause=Button(trackcontrols,image=pauseimage,command=pausesong)
pause.grid(row=0,column=2)

next=Button(trackcontrols,image=nextimage,command=nextsong)
next.grid(row=0,column=3)

volume=DoubleVar()
slider=Scale(trackcontrols,from_ =0, to=10,orient=HORIZONTAL,command=changevol)
slider['variable']=volume
slider.set(6)
mixer.music.set_volume(0.6)
slider.grid(row=0,column=4)

# Add widgets to Track List
scroll=Scrollbar(tracklist, orient=VERTICAL)
scroll.grid(row=0,column=1,rowspan=5,sticky="ns")

list=Listbox(tracklist,selectmode=SINGLE,bg=control_color,selectbackground="sky blue")
list.configure(height=22,width=25)
enumeratesongs()
list.grid(row=0,column=0,rowspan=5)


list.configure(yscrollcommand=scroll.set)
scroll.configure(command=list.yview)


#==============================================================================
window.mainloop()
