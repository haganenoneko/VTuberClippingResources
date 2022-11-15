import os 
import sys
import tkinter as tk
from tkinter import filedialog
from subprocess import Popen

root = tk.Tk()
root.withdraw()

init_dir = os.getcwd()

video_path = filedialog.askopenfilename(
	initialdir = init_dir + "/full_raw/",
	title = "Select input video file"
)

sub_path = filedialog.askopenfilename(
	initialdir = init_dir + "/subs/",
	title = "Select subtitles",
)

out_name = f"{init_dir}/burned/"
if not os.path.isdir(out_name):
	os.mkdir(out_name)

out_name += f"[SUBBED]_{os.path.basename(video_path)}"
sub_path = sub_path.replace("/", "\\\\\\\\").replace(":", "\\:")

#start = input("Start (HH:MM:SS): ")
#stop = input("Stop time (HH:MM:SS): ")

#if len(start) == 8 and len(stop) == 8:
#	cmd_prefix = f"ffmpeg -ss {start} -to {stop}"
#else:
#	cmd_prefix = "ffmpeg"

cmd_prefix = "ffmpeg"
cmd = f"{cmd_prefix} -i {video_path} -vf ass='{sub_path}' {out_name}"
print(cmd)

Popen(cmd, close_fds=True)

if not os.path.isfile(out_name):
	print("Command did not run. Try pasting the command into terminal directly.")