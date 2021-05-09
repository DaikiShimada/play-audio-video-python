import media.video
import media.audio
import tkinter
import time

# for black display
import numpy as np
from PIL import ImageTk, Image

def black_frame(frame):
    black = np.zeros((1024, 1024, 3), dtype=np.uint8)
    frame_image = ImageTk.PhotoImage(Image.fromarray(black))
    frame.config(image=frame_image)
    frame.image = frame_image

root = tkinter.Tk()
root.frame = tkinter.Label(root)
root.frame.pack()

#ch1
ch1_video = media.video.Video()
ch1_audio = media.audio.Audio()
ch1_video.openfile("./A.mp4", root.frame)
ch1_audio.openfile("./A.mp4")

#ch2
ch2_video = media.video.Video()
ch2_audio = media.audio.Audio()
ch2_video.openfile("./test_video2.mp4", root.frame)
ch2_audio.openfile("./test_video2.mp4")

channels = {
    1: (ch1_video, ch2_audio), 
    2: (ch2_video, ch2_audio)
}

def change_ch(ch):
    for ch_no, (video, audio) in channels.items():
        video.display = ch == ch_no

def finish_video(frame):
    for ch_no, (video, audio) in channels.items():
        video.quit = True
    black_frame(frame)


root.frame.bind('1', lambda event: change_ch(1))
root.frame.bind('2', lambda event: change_ch(2))
root.frame.bind('q', lambda event: finish_video(root.frame))

ch1_video.play()
ch2_video.play()
change_ch(1)
root.frame.focus_set()
root.mainloop()

