import os
import tkinter
import tkinter.filedialog
import threading
import time
import random
import pygame

folder = '/Users/apple/Desktop/雜物/'

def play():
    global folder
    global get_pos
    global get_busy
    global nextMusic
    global end_time
    #musics = [folder+''+music for music in os.listdir(folder) if music.endswith(('.mp3','.wave','.ogg'))]
    pygame.mixer.init()
    while playing:
        if get_busy==0:
            #nextMusic = random.choice(musics)
            pygame.mixer.music.load(nextMusic.encode())
            pygame.mixer.music.play(loops=0,start=int(1+get_pos/1000))
            get_busy = 1
            musicName.set('playing...'+nextMusic)
        else:
            time.sleep(0.3)
    get_pos=pygame.mixer.music.get_pos() 
    end_time=pygame.mixer.music.get_endevent()
root = tkinter.Tk()
root.title('music')
root.geometry('280x150+400+300')
root.resizable(False, False)     

def closeWindow():
    global playing
    playing = False
    try:
        pygame.mixer.music.stop()
        pygame.mixer.quit()
    except:
        pass
    root.destroy()
root.protocol('VW_DELETE_WINDOW',closeWindow)

pause_resume = tkinter.StringVar(root, value='NotSet')
playing = False

def buttonPlayClick():
    global folder
    global get_pos
    global get_busy
    global nextMusic
    get_pos = 0
    get_busy = 0
    musics = [folder+''+music for music in os.listdir(folder) if music.endswith(('.mp3','.wave','.ogg'))]
    nextMusic = random.choice(musics)
    if not folder:
        folder = tkinter.filedialog.askdirectory()
    if not folder:
        return
    global playing
    playing = True
    t = threading.Thread(target=play)  
    t.start()
    buttonPlay['state'] = 'disabled'
    buttonStop['state'] = 'normal'
    buttonPause['state'] = 'normal'
    buttonNext['state'] = 'normal'
    buttonBack['state'] = 'normal'
    buttonFront['state'] = 'normal'
    pause_resume.set('Pause') 
buttonPlay = tkinter.Button(root, text='Play', command=buttonPlayClick)
buttonPlay.place(x=20,y=120,width=50,height=20)

def buttonBackClick():
    global get_pos
    global get_busy
    playing = False
    pygame.mixer.music.stop()
    if get_pos < 5000:
        get_pos = 0
    else:
        get_pos = get_pos - 5000
    get_busy = 0
    playing = True
buttonBack = tkinter.Button(root, text='<<', command=buttonBackClick)
buttonBack.place(x=20,y=50,width=50,height=20)       
buttonBack['state'] = 'disabled'   

def buttonFrontClick():
    global get_pos
    global get_busy
    global end_time
    playing = False
    pygame.mixer.music.stop()
    if get_pos < 180000:
        get_pos = get_pos + 5000
    else:
        get_pos = get_pos + 5000
    get_busy = 0
    playing = True
buttonFront = tkinter.Button(root, text='>>', command=buttonFrontClick)
buttonFront.place(x=210,y=50,width=50,height=20)
buttonFront['state'] = 'disabled' 

def buttonStopClick():
    global playing
    playing = False
    pygame.mixer.music.stop()
    musicName.set('no music')
    buttonPlay['state'] = 'normal'
    buttonStop['state'] = 'disabled'
    buttonPause['state'] = 'disabled'
    buttonBack['state'] = 'disabled'
    buttonFront['state'] = 'disabled'
buttonStop = tkinter.Button(root, text='Stop', command=buttonStopClick)
buttonStop.place(x=110,y=120,width=50,height=20)
buttonStop['state'] = 'disabled'

def buttonPauseClick():
    global playing
    if pause_resume.get() == 'Pause':
        pygame.mixer.music.pause()
        pause_resume.set('Resume')
    elif pause_resume.get() == 'Resume':
        pygame.mixer.music.unpause()
        pause_resume.set('Pause')
buttonPause = tkinter.Button(root, textvariable=pause_resume, command=buttonPauseClick)
buttonPause.place(x=90,y=40,width=100,height=40)
buttonPause['state'] = 'disabled'

def buttonNextClick():
    global playing
    playing = False
    pygame.mixer.music.stop()
    pygame.mixer.quit()
    buttonPlayClick()
buttonNext = tkinter.Button(root, text='Next', command=buttonNextClick)
buttonNext.place(x=200,y=120,width=50,height=20)
buttonNext['state'] = 'disabled'
#labelTime = tkinter.Label(root, textvariable=get_pos)
#labelTime.place(x=50,y=80,width=50,height=10)

musicName = tkinter.StringVar(root,value='no music now...')
labelName = tkinter.Label(root, textvariable=musicName)
labelName.place(x=0,y=100,width=270,height=20)
root.mainloop()