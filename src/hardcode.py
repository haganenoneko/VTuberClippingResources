import os 
import sys
import tkinter as tk
from tkinter import filedialog
from subprocess import Popen

root = tk.Tk()
root.withdraw()

init_dir = os.getcwd()

video_path = filedialog.askopenfilename(
	initialdir = init_dir + f"/{YOUR_RAW_VIDEO_DIRECTORY}/",
	title = "Select input video file"
)

sub_path = filedialog.askopenfilename(
	initialdir = init_dir + f"/{YOUR_SUBTITLE_DIRECTORY}/",
	title = "Select subtitles",
)

out_name = f"{init_dir}/burned/"
if not os.path.isdir(out_name):
	os.mkdir(out_name)

out_name += f"[SUBBED]_{os.path.basename(video_path)}"

sub_path = sub_path.replace("/", "\\\\\\\\").replace(":", "\\:")
cmd = f"ffmpeg -i {video_path} -vf ass='{sub_path}' {out_name}"

print(cmd)
Popen(cmd, close_fds=True)

if not os.path.isfile(out_name):
	print("Command did not run. Try pasting the command into terminal directly.")