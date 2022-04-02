import moviepy.editor
from tkinter.filedialog import askopenfilename
from tkinter import *

def mp3():
    global root
    root=Tk()
    video1 = askopenfilename()
    try:
        video = moviepy.editor.VideoFileClip(video1)
        audio = video.audio

        audio.write_audiofile("presets/samples/sample.wav",codec='pcm_s16le')
        print("Completed!")
        try:
            closeroot()
        except:
            None
        return True
    except:
        print("File Could not be found")
        try:
            closeroot()
        except:
            None
        return False


def closeroot():
    root.destroy()

if __name__=="__main__":
    mp3()