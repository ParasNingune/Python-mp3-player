import vlc
import os
from time import *
import re
from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import *
from mutagen.mp3 import MP3
from mutagen.id3 import ID3
from threading import Thread
from frames import help, play_from_list, number, play_list
from metadata import Metadata
from PIL import ImageTk, Image 
from io import BytesIO
from pox.shutils import find
import random

w = True

root = Tk()
root.title("MP3 PLAYER")
root.geometry("600x470")
root.config(bg="black")
root.resizable(width = False, height = False)
box = ""

p = "\start.png"
pic = os.getcwd()+p

can = Canvas(root, height=362, width=489, bg="white")
can.place(x=5, y=5)

song = askopenfilenames()

songs = []
a = 0

for x in song:
    songs.append(
        {'no' : a,
            'name' : x
            })
    a = a + 1

b = 0
current = 0

total = a

status = ""
exist = False
is_playing = False
stoped = False
mute = False

def threadmethod():
    elapsed_time = 0
    volume = 70
    global __6, __7, __8, _1, _2, _3, _4, _5, _6
    global status, player, is_playing, songs, size, number, cover
    global instance, current, stoped, total, song, mute, b, p

    while w == True:

        if status == "Play_from":
            if is_playing:
                player.stop()
            try:
                n = int(number[b])-1
                b=b+1
                for x in songs:
                    if n == x['no']:
                        current = n
                        status = "Play"
                        break
                else:
                    messagebox.showinfo(message="Invalid Song number", icon="error")
                    current=0
                    status = "Play"

            except (ValueError):
                messagebox.showinfo(message="Enter the song number", icon="error")
                quit()

        elif status == "Unmute":
            mute = False
            __7.config(text="Mute", command=lambda:join("Mute"))
            player.audio_set_volume(volume)

        elif status == "Resume":
            if is_playing == False:
                is_playing = True
                player.pause()
                status = ""
                _3.config(text="PAUSE", command=lambda:join("Pause"))

            #else:
                #status="Play"

        elif status == "Play":

            elapsed_time = 0
            is_playing = True
            stoped = False
            song = songs[current]['name']
            player = vlc.MediaPlayer(song)
            _3.config(text="PAUSE", command=lambda:join("Pause"))

            try:
                instance = MP3(song)
            except:
                current=current+1
                song = songs[current]['name']
                player = vlc.MediaPlayer(song)
                instance = MP3(song)
            try:
                tags = ID3(song)
                cover = tags.get("APIC:")
            except:
                cover=None
            change()
            cover=""
            size = instance.info.length

            sleep(2)
            track_length = size

            player.audio_set_volume(volume)
            player.play()
            status = ""

        elif status == "Mute":
            __7.config(text="UNMUTE", command=lambda:join("Unmute"))

            if is_playing:
                mute = True
                player.audio_set_volume(0)
                status = ""
            else:
                messagebox.showinfo(message="First play the song.", icon="error")
                status=""

        elif status == "Next":
            if is_playing:
                player.stop()
                sleep(2)
                if current+1 < total:
                    current = current + 1
                
                else:
                    current = 0
                
                song = songs[current]['name']
                player = vlc.MediaPlayer(song)
                instance = MP3(song)
                size = instance.info.length
                status = "Play"
            else:
                messagebox.showinfo(message="First play the song.", icon="error")

        elif status == "Previous":
            if is_playing:
                player.stop()
                sleep(2)
                current = current - 1
                song = songs[current-1]['name']
                player = vlc.MediaPlayer(song)
                instance = MP3(song)
                size = instance.info.length
                status = "Play"
            else:
                messagebox.showinfo(message="First play the song.", icon="error")
        
        elif status == "Pause":
            
            if is_playing:
                _3.config(text="PLAY",  command=lambda:join("Play"))
                is_playing = False
                player.pause()
                status = ""

            else:
                is_playing=False
                messagebox.showinfo(message="First play the song.", icon="error")
                status=""

        elif status == "Stop":
            if is_playing:
                is_playing = False
                change()
                _3.config(text="PLAY", command=lambda:join("Play"))
                stoped = True
                status = ""
                player.stop()
            else:
                is_playing=False
                messagebox.showinfo(message="First play the song.", icon="error")
                status=""

        elif status == "Increase":
            if is_playing:
                volume = volume + 5
                player.audio_set_volume(volume)
                status = ""
            else:
                messagebox.showinfo(message="First play the song.", icon="error")
                status=""

        elif status == "Decrease":
            if is_playing:
                volume = volume - 5
                player.audio_set_volume(volume)
                status = ""
            else:
                messagebox.showinfo(message="First play the song.", icon="error")
                status=""

        if is_playing:
            elapsed_time = elapsed_time + 0.1

            if elapsed_time >= track_length:

                if current+1 < total:
                    current = current + 1
                    
                else:
                    current = 0
                    
                song = songs[current]['name']
                player = vlc.MediaPlayer(song)
                instance = MP3(song)
                size = instance.info.length
                status = "Play"

        sleep(0.1)

def info():
    global song, instance, is_playing
    print(song)
    name = split(song)
    root = Tk()
    root.geometry("300x300")
    root.config(bg="black")
    root.title("SONG INFO")
    root.resizable(width = False, height = False)

    _1 = Label(root, text="Song Info :", width=20, height=3, fg="white", bg="black", font=("Arabia", 12, "bold"))
    _1.place(x=40, y=10)

    can = Canvas(root, height=150, width=325, bg="black")
    can.place(x=10, y=80)

    _2 = Button(root, text="BACK", bd=11, width=8, height=2, fg="white", bg="black", font=("Arabia", 10, "bold"), command=lambda:root.destroy())
    _2.place(x=100, y=240)

    if is_playing:
        try:
            singer = instance['TPE1']

            album = instance['TALB']
            
        except:
            singer = "DATA NOT FOUND"
            album = "DATA NOT FOUND"

    else:
        name = "----------"
        singer = "----------"
        album = "----------"

    name = f"NAME : {name}"
    singer = f"SINGER : {singer}"
    album = f"ALBUM : {album}"

    _1 = Label(can, text=name, font=("Arabia", 14, "bold"), fg="white", bg="black")
    _1.place(x=5, y=5)

    _2 = Label(can, text=album, font=("Arabia", 14, "bold"), fg="white", bg="black")
    _2.place(x=5, y=60)

    _3 = Label(can, text=singer, font=("Arabia", 14, "bold"), fg="white", bg="black")
    _3.place(x=5, y=115)


def split(song):
    global is_playing

    if is_playing:
        x = song
        v=0
        s = re.findall("[/]", song)
        for a in s:
            v = v+1

        s = re.split("[/]", song)
        song_name = s[v]
        return song_name


def change():
    global is_playing, box, can, pic, cover, im1

    if is_playing == False:
        #return
        original = Image.open(pic)
        #return
        im = original.resize((485, 360),Image.ANTIALIAS)
        im1 = ImageTk.PhotoImage(im)
        box = can.create_image(4, 4, anchor=NW, image=im1)
        return

    elif is_playing:
        if cover == None:
            original = Image.open(pic)

        else:
            p = cover.data
            original = Image.open(BytesIO(p))
   
    im = original.resize((485, 360),Image.ANTIALIAS)
    im1 = ImageTk.PhotoImage(im)
    box = can.create_image(4, 4, anchor=NW, image=im1)
    can.update()
    return

def join(operation):
    global exist, status, is_playing, stoped, mute, songs

    if exist == False:
        if operation == "Play_from":
            play_from_list(songs)
            status = operation

        else:
            status = operation
        a = Thread(target=threadmethod)
        a.start()
        exist = True
        a.join(0.1)

    else:
        if operation == "Play_from":
            play_from_list(songs)
            status = operation

        if mute:
            status = "Unmute"

        elif stoped:
            status = "Play"

        elif is_playing == False:
            if operation == "Play":
                status = "Resume"

        else:
            status = operation
 
def shuffle():
    global songs, total, current
    a=0
    count=0
    x=[]
    no = random.sample(range(0, total), total)

    for y in songs:
        n = no[count]
        z = songs[n]['name']
        x.append({
            'no' : a, 
            'name' : z
            })
        a=a+1
        count=count+1

    songs = x
    join("Stop")
    sleep(2)
    current = 0
    join("Play")

def add():
    global songs, total, a

    song = askopenfilenames()

    for x in song:
        for y in songs:
            if x == y['name']:
                break

            else:
                songs.append(
                {'no' : a,
                    'name' : x
                    })
                a = a + 1
                break
    total=a

def main():
    global root, p, __6, __7, __8, _1, _2, _3, _4, _5, _6
    global player, songs, size, current

    
    change()

    can = Canvas(root, height=455, width=90, bg="black")
    can.place(x=505, y=5)

    __0 = Button(can, text="Playlist", height=3, width=8, relief="sunken", bd=11, font=('Arabia', 9, ''), bg="black", fg="white", command=lambda:play_list(songs))
    __0.place(x=7, y=5)

    __2 = Button(can, text="Song\nInfo", height=3, width=8, relief="sunken", bd=11, font=('Arabia', 9, ''), bg="black", fg="white", command=lambda:info())
    __2.place(x=7, y=80)

    __3 = Button(can, text="Play from\nPlaylist", height=3, width=8, bg="black", relief="sunken", bd=11, fg="white", font=('Arabia', 9, ''), command=lambda:join("Play_from"))
    __3.place(x=7,y=155)

    __6 = Button(can, text="Volume\nIncrease", height=3, width=8, bg="black", relief="sunken", bd=11, fg="white", font=("Arabia", 9, ""), command=lambda:join("Increase"))
    __6.place(x=7, y=230)
    
    __7 = Button(can, text="Mute", height=3, width=8, bg="black", relief="sunken", bd=11, fg="white", font=("Arabia", 9, "bold"), command=lambda:join("Mute"))
    __7.place(x=7, y=305)

    __8 = Button(can, text="Volume\nDecrease", height=3, width=8, bg="black", relief="sunken", bd=11, fg="white", font=("Arabia", 9, ""), command=lambda:join("Decrease"))
    __8.place(x=7, y=380)

    can1 = Canvas(root, height=80, width=485, bg="black")
    can1.place(x=5, y=377)

    _1 = Button(can1, text="STOP", height=3, width=8, relief="sunken", bd=9, bg="black", fg="white", font=("Arabia", 9, ""), command=lambda:join("Stop"))
    _1.place(x=5, y=7)

    _2 = Button(can1, text="PREV", height=3, width=8, relief="sunken", bd=9, bg="black", fg="white", font=("Arabia", 9, ""), command=lambda:join("Previous"))
    _2.place(x=85, y=7)

    _3 = Button(can1, text="PLAY", height=3, width=8, relief="sunken", bg="black", bd=9, fg="white", font=("Arabia", 9, ""), command=lambda:join("Play"))
    _3.place(x=165, y=7)

    #_4 = Button(can1, text="PAUSE", height=3, width=8, bg="black", bd=9, fg="white", font=("Arabia", 9, ""), command=lambda:join("Pause"), state=DISABLED)
    #_4.place(x=245, y=7)

    _4 = Button(can1, text="NEXT", height=3, width=8, bg="black", relief="sunken", bd=9, fg="white", font=("Arabia", 9, ""), command=lambda:join("Next"))
    _4.place(x=245, y=7)
    
    _5 = Button(can1, text="SHUFFLE", height=3, width=8, bg="black", relief="sunken", bd=9, fg="white", font=("Arabia", 9, ""), command=lambda:shuffle())
    _5.place(x=325, y=7)

    _6 = Button(can1, text="ADD", height=3, width=8, bg="black", relief="sunken", bd=9, fg="white", font=("Arabia", 9, ""), command=lambda:add())
    _6.place(x=405, y=7)
    
def closing():
    global w, root
    w = False
    root.destroy()

    return

m = Thread(target=main)
p = Thread(target=change)

m.start()
m.join(0.1)
root.protocol("WM_DELETE_WINDOW", closing)
root.mainloop()
