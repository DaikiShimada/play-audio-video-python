import tkinter
from tkinter import ttk
import imageio
from PIL import ImageTk, Image
import time
import threading
import numpy as np
from imageio.plugins.ffmpeg import FfmpegFormat

class VideoPL():
    def __init__(self, file_path, frame, preload=True, debug=False):
        format = FfmpegFormat(
            "ffmpeg",
            "Many video formats and cameras (via ffmpeg)",
            ".mov .avi .mpg .mpeg .mp4 .mkv .wmv .webm",
            "I",
            )
        imageio.formats.add_format(format, True)
        self._file_path = file_path
        self._buffer = None
        self.frame = frame
        self.display = False
        self.quit = False
        self.debug = debug
        if preload:
            print('[log] preloading file:', self._file_path)
            self.openfile(self._file_path)
            self._buffer = self._preload()
            print('[log] complete:', self._file_path)

    def openfile(self, file_path, frame=None):
        if frame is not None:
            self.frame = frame
        try:
            self.video = imageio.get_reader(file_path)
        except imageio.core.fetching.NeedDownloadError:
            imageio.plugins.avbin.download()
            self.video = imageio.get_reader(file_path)

    def play(self):
        self.video_thread = threading.Thread(target=self._stream)
        self.video_thread.start()

    def stop(self):
        self.video_thread.stop()

    def _preload(self):
        #frames = np.array([image for image in self.video.iter_data()])
        frames = [ImageTk.PhotoImage(Image.fromarray(image.copy())) for image in self.video.iter_data()]
        return frames

    def _stream(self):
        while not self.quit:
            start_time=time.time()
            sleeptime = 1 / self.video.get_meta_data()["fps"]
            frame_now = 0
            video_stream = self.video.iter_data() if self._buffer is None else self._buffer
            for image in video_stream:
                _st = time.perf_counter()
                frame_now = frame_now + 1
                if self.debug:
                    print(self.display)
                if self.quit:
                    break
                if frame_now * sleeptime >= time.time() - start_time and self.display:
                    #frame_image = ImageTk.PhotoImage(Image.fromarray(image))
                    #self.frame.config(image=frame_image)
                    #self.frame.image = frame_image
                    self.frame.config(image=image)
                    self.frame.image = image
                    # print performance
                    #print(time.perf_counter() - _st, "sec.")
                    time.sleep(sleeptime)
                else:
                    pass

