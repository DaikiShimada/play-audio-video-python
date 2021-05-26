import subprocess
from flask import Flask

app = Flask(__name__)

video_flag = True
python_cmd = 'python'
video_app = 'media/app_for_flask.py'
videos = [
    './A_w480.mp4',
    './test_video2_w480.mp4',
]

if video_flag:
    video_process = subprocess.Popen(
        ' '.join([python_cmd, video_app, '--videos'] + videos), shell=True)

app.run(debug=True, use_reloader=False)
if video_flag:
    video_process.wait()