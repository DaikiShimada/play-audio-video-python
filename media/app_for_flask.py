import argparse
import threading
import time
import tkinter

import video_preload as video
import audio

# for black display
import numpy as np
from PIL import ImageTk, Image

class BlackDisplay():
    def __init__(self, width, height, frame):
        black = np.zeros((height, width, 3), dtype=np.uint8)
        self.frame = frame
        self.frame_image = ImageTk.PhotoImage(Image.fromarray(black))
        self.display = False
        self.quit = False

    def play(self):
        self.video_thread = threading.Thread(target=self._stream)
        self.video_thread.start()
    
    def _stream(self):
        while not self.quit:
            if self.display:
                self.frame.config(image=self.frame_image)
                self.frame.image = self.frame_image
                time.sleep(0.3)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--videos', '-v',
        type=str,
        nargs='+',
        help='path to input video')
    args = parser.parse_args()

    root = tkinter.Tk()
    root.frame = tkinter.Label(root)
    root.frame.pack()

    # prepare videos
    channels = {
        c + 1: (video.VideoPL(v, root.frame), audio.Audio(v)) 
        for c, v in enumerate(args.videos)}
    # define change channel function
    def change_ch(ch):
        print('called change_ch', ch)
        for ch_no, (v, a) in channels.items():
            v.display = ch == ch_no
            # TODO: audio change
        
    for c in channels.keys():
        key = chr(ord('a') + c - 1)
        print('bind key: {} -> change_ch({})'.format(key, c))
        root.frame.bind(key, lambda event, c=c: change_ch(c))

    # prepare black display
    black = BlackDisplay(480, 270, root.frame)
    channels[0] = (black, None) # TODO: dummy audio class
    # define turning off function
    def turn_off():
        print('called turn_off')
        for ch_no, (v, a) in channels.items():
            if ch_no == 0:
                v.display = True
            else:
                v.display = False
                # TODO: turining off audio
    # define exit function
    def exit_app():
        print('called exit_app')
        for ch_no, (v, a) in channels.items():
            v.quit = True
    root.frame.bind('q', lambda event: turn_off())
    root.frame.bind('@', lambda event: exit_app())

    # play videos
    for c, (v, a) in channels.items():
        v.play()
        #a.play()
    change_ch(1) # start from turned off

    root.frame.focus_set()
    root.mainloop()

if __name__ == '__main__':
    main()