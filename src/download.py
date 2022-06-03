import re 
import argparse
from datetime import datetime
from sys import argv 
from subprocess import Popen

import tkinter as tk 
from tkinter import messagebox as mbox
from venv import create 

import validators
from typing import Any, Tuple, Dict, Type, Union 

import logging 
from pathlib import Path 
from common import getTimestamp, BadFormat, create_log, removeNonNumeric

# ---------------------------------------------------------------------------- #
#                                  GUI parser                                  #
# ---------------------------------------------------------------------------- #

class MultiInput:
	def __init__(self, defaults: Dict[str, Union[str, int]]={}) -> None:
		
		self.boxes: List[tk.Frame] = [] 
		self.box_kw = dict(fill='x', expand=True)
		self.frame_kw = dict(padx=10, pady=10, **self.box_kw)	
		
		self.setup()
		self.createVariables()
		self.createEntryFields(defaults=defaults)
		self.createButton()
		self.root.mainloop()
		
	def setup(self):
		self.root = tk.Tk()
		self.root.geometry("300x280")
		self.root.resizable(True, True)
		self.root.title('Enter video information')
	
	def createVariables(self):
		self.url = tk.StringVar()		
		self.start_HH = tk.StringVar()
		self.start_MM = tk.StringVar()
		self.start_SS = tk.StringVar()
		self.stop_HH = tk.StringVar()
		self.stop_MM = tk.StringVar()
		self.stop_SS = tk.StringVar()

		self.fmt = tk.IntVar()

	@staticmethod
	def _validateFields(
		url: str, start: str, stop: str, fmt: int) -> Tuple[str, int]:
		if not validators.url(url):
			raise ValueError(f"{url} is not a valid URL")
		
		try:
			times = [getTimestamp(t) for t in [start, stop]]
		except Exception as e:
			raise ValueError(
				f'Invalid timestamps\nStart:{start:^10}Stop:{stop:^8}')

		try:
			fmt = int(fmt)
		except AssertionError:
			raise BadFormat(f"Format {fmt} must be an integer")

		return url, times[0], times[1], fmt 

	def clicked(self):
		""" callback when the login button clicked
		"""
		# validate inputs 
		url, start, stop, fmt = self._validateFields(
			*self.extractVariables()
		)

		# store inputs for later use 
		self.contents = [url, start, stop, fmt]

		msg = 'You entered:\n'
		msg += f'URL:{url}\nStart: {start}\nEnd: {stop}\nFormat: {fmt}'
		mbox.showinfo(title='Information', message=msg)

		# exit the window 
		self.root.quit()
	
	def _createFrame(self) -> tk.Frame:
		frame = tk.Frame(self.root)
		frame.pack(**self.frame_kw)
		self.boxes.append(frame)
		return frame 

	@staticmethod
	def _format_hms_default(hms: str) -> str:
		if hms is None:
			hms = '0' * 6
		elif isinstance(hms, int):
			hms = str(hms)
		
		hms = removeNonNumeric(hms)
		if len(hms) < 6:
			hms = '0' * (6 - len(hms)) + hms 
		
		return hms 

	def create_hms_box(self, label: str, default: str=None) -> None:
		
		default = self._format_hms_default(default)
		units = ['HH', 'MM', 'SS']
		frame = self._createFrame()

		for i, u in enumerate(units):
			key = f"{label}_{u}"
			var = self.__dict__[key]
			
			if i > 0:
				name = tk.Label(frame, text=u)
			else:
				name = tk.Label(frame, text=f"{label} {u}")
			name.pack(side='left')
			entry = tk.Entry(frame, textvariable=var, width=10)			

			j = 2*i 
			val = default[j:j+2]
			entry.insert(0, val)
			entry.pack(side='left', **self.box_kw)
	
	def _createEntryField(
		self, 
		label: str=None, 
		frame: tk.Frame=None, 
		focus: bool=False,
		default: Union[str, int]=None) -> None:
		
		if not isinstance(label, str):
			raise TypeError(f"{label} must be a str")	

		if not frame:
			frame = self._createFrame()

		name = tk.Label(frame, text=label)
		name.pack(**self.box_kw)
		 
		entry = tk.Entry(frame, textvariable=self.__dict__[label])
		if default:
			entry.insert(0, str(default))
			self.__dict__[label].set(default)

		entry.pack(**self.box_kw)
		
		if focus: 
			entry.focus()

	def createEntryFields(
		self, defaults: Dict[str, Union[str, int]]={}):

		for lab in ['url', 'start', 'stop', 'fmt']:			
			dflt = defaults[lab] if (lab in defaults) else None 
			fcs = True if (lab == 'url') else False 
			
			if lab[0] == 's':
				self.create_hms_box(lab, default=dflt)
			else:
				self._createEntryField(
					lab, focus=fcs, default=dflt)
	
	def createButton(self):
		button = tk.Button(
			self.boxes[-1], text='Run', command=self.clicked)

		button.pack(pady=10, **self.box_kw)

	def extractVariables(self) -> Tuple[str, str, str, int]:
		units = ['HH', 'MM', 'SS']

		start, stop = [
			':'.join([
				self.__dict__[f"{s}_{u}"].get() for u in units
			]) for s in ['start', 'stop']
		]

		return (
			self.url.get(),
			start, 
			stop, 
			self.fmt.get(),
		)


# ---------------------------------------------------------------------------- #
#       Helper functions for parsing CLI arguments and setting up the GUI      #
# ---------------------------------------------------------------------------- #

def extract_cli_args() -> Tuple[str, str, str, int]:
	parser = argparse.ArgumentParser(description="Add clip information")
	parser.add_argument("URL", type=str, help="Youtube URL")
	parser.add_argument("--start", type=str, help="Start time")
	parser.add_argument("--end", type=str, help="End time")
	parser.add_argument(
		"--format", type=str, help="youtube-dl format", default=22)
	
	args = parser.parse_args()

	url, start, stop, fmt = args.URL, args.start, args.end, args.format 
	validators.url(url)

	return url, start, stop, fmt 

def run_ffmpeg(url: str, fmt: int, start: str=None, stop: str=None) -> None:
	
	if start and stop:
		ffmpeg_cmd = f"--external-downloader ffmpeg --external-downloader-args \"ffmpeg_i:-ss {start} -to {stop}\""
	else:
		ffmpeg_cmd = ""	
	
	cmd = f"yt-dlp -f {fmt} {ffmpeg_cmd} {url}"
	print(f"\n\nffmpeg cmd:\n{cmd}")
	Popen(cmd)

def create_gui(defaults: Dict[str, Any]={}) -> Tuple[str, str, str, int]:
	
	form = MultiInput(defaults)

	try:
		url, start, stop, fmt = form.contents
	
	except AttributeError:
		raise AttributeError("No valid inputs.")

	except BadFormat:
		print(f"Unsupported format: {fmt}\nPlease select a format below:")

		url, start, stop, _ = form.extractVariables()
		defaults = dict(url=url, start=start, stop=stop)

		print("List of available formats:\n")
		cmd = f"yt-dlp -F {url}"
		Popen(cmd)

		form = MultiInput(defaults)
		fmt = form.contents[-1] 
	
	return url, start, stop, fmt 

def update_log(
	url: str, start: str, stop: str, fmt: int, 
	logpath="./logs", logmode="append") -> None:
	logmsg = f"""
		Time: {datetime.strftime(datetime.now(), format=r"%Y-%m-%d %H:%M:%S"):^50}
		URL: {url:^50}
		Start:{start:^14}Stop:{stop:^14}Format:{fmt:>4}
	"""
	print(logmsg)
	
	logpath = Path.cwd() if (logpath is None) else Path(logpath)
	if logmode == 'append':
		logpath = logpath / "dl.log" 
	else:
		stem = re.search(r"(?:watch\?v=)(.*)$", url).group(0)
		logpath = logpath / f"{stem}.log"
	
	create_log(logpath)
	logging.info(logmsg)

if __name__ == "__main__":
	if len(argv) >= 3:
		url, start, stop, fmt = extract_cli_args()
	else:
		url, start, stop, fmt = create_gui({'fmt' : 22})

	update_log(url, start, stop, fmt)
	run_ffmpeg(url, fmt, start=start, stop=stop)





