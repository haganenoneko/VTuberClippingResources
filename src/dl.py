import os
import argparse
from subprocess import Popen

import tkinter as tk 
from tkinter import messagebox as mbox 

import validators
from typing import Tuple, Dict, Union 

import re 
from datetime import datetime

def removeNonNumeric(s: str) -> str:
	return re.sub("[^0-9]*", '', s)

def getTimestamp(s: str) -> datetime.time:
	try:
		s = removeNonNumeric(s)
		t = datetime.strptime(s, "%H%M%S")
		return datetime.strftime(t, "%H:%M:%S")
	except ValueError:
		return None 

class BadFormat(ValueError):
	def __init__(self, *args: object) -> None:
		super().__init__(*args)

class MultiInput:
	def __init__(self, defaults: Dict[str, Union[str, int]]={}) -> None:
		
		self.box_kw = dict(fill='x', expand=True)

		self.setup()
		self.createVariables()
		self.createBox()
		self.createEntryFields(defaults=defaults)
		self.createButton()
		self.root.mainloop()
		
	def setup(self):
		self.root = tk.Tk()
		self.root.geometry("300x280")
		self.root.resizable(False, False)
		self.root.title('Enter video information')
	
	def createVariables(self):
		self.url = tk.StringVar()
		self.start = tk.StringVar()
		self.stop = tk.StringVar()
		self.fmt = tk.IntVar()

	def getVariables(self) -> Tuple[str, int]:
		return (
			self.url.get(),
			self.start.get(),
			self.stop.get(),
			self.fmt.get(),
		)
			
	def createBox(self):
		self.box = tk.Frame(self.root)
		self.box.pack(padx=10, pady=10, **self.box_kw)	

	@staticmethod
	def _validateFields(url: str, start: str, stop: str, fmt: int) -> Tuple[str, int]:
		if not validators.url(url):
			raise ValueError(f"{url} is not a valid URL")
		
		try:
			times = [getTimestamp(t) for t in [start, stop]]
		except Exception as e:
			print(f'Input: {start}, {stop}')
			raise e

		try:
			fmt = int(fmt)
		except AssertionError:
			raise BadFormat(f"Format {fmt} must be an integer")

		return url, times[0], times[1], fmt 

	def clicked(self):
		""" callback when the login button clicked
		"""
		# validate inputs 
		url, start, stop, fmt = self._validateFields(*self.getVariables())

		# store inputs for later use 
		self.contents = [url, start, stop, fmt]

		msg = f'You entered URL:{url}\nStart: {start}\nEnd: {stop}\nFormat: {fmt}'
		mbox.showinfo(title='Information', message=msg)

		# exit the window 
		self.root.quit()
	
	def _createEntryField(self, label: str=None, default=None):
		if not isinstance(label, str):
			raise ValueError(f"{label} must be a str")		
		# label 
		name = tk.Label(self.box, text=label)
		name.pack(**self.box_kw)
		
		# entry box 
		entry = tk.Entry(self.box, textvariable=self.__dict__[label])
		if default:
			entry.insert(0, str(default))
			self.__dict__[label].set(default)

		entry.pack(**self.box_kw)
		entry.focus()

	def createEntryFields(
		self, defaults: Dict[str, Union[str, int]]={}
	):
		for label in ['url', 'start', 'stop', 'fmt']:
			if label in defaults:
				self._createEntryField(
					label=label, default=defaults[label]
				)
			else:
				self._createEntryField(label=label)
	
	def createButton(self):
		button = tk.Button(self.box, text='Run', command=self.clicked)
		button.pack(pady=10, **self.box_kw)

try:
	parser = argparse.ArgumentParser(description="Add clip information")
	parser.add_argument("URL", type=str, help="Youtube URL")
	parser.add_argument("--start", type=str, help="Start time")
	parser.add_argument("--end", type=str, help="End time")
	parser.add_argument("--format", type=str, help="youtube-dl format", default=22)
	args = parser.parse_args()
	url, start, stop, fmt = args.URL, args.start, args.end, args.format 
except:
	form = MultiInput({'fmt' : 22})

	try:
		url, start, stop, fmt = form.contents
	except AttributeError:
		raise AttributeError("No valid inputs.")
	except BadFormat:
		url, start, stop, _ = form.getVariables()

		print("List of available formats:\n")
		cmd = f"yt-dlp -F {url}"
		Popen(cmd)

		form = MultiInput(
			dict(url=url, start=start, stop=stop)
		)

		fmt = form.contents[-1] 

if start and stop:
	ffmpeg_cmd = f"--external-downloader ffmpeg --external-downloader-args \"ffmpeg_i:-ss {start} -to {stop}\""
else:
	ffmpeg_cmd = ""

cmd = f"yt-dlp -f {fmt} {ffmpeg_cmd} {url}"
print(f"\n\nffmpeg cmd:\n{cmd}")

Popen(cmd)
