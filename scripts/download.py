import re
import argparse
from sys import argv

from datetime import datetime, timedelta
from subprocess import Popen, PIPE

import tkinter as tk
from tkinter import messagebox as mbox
from venv import create

import validators
from typing import Any, Tuple, Dict, Union

import logging
from pathlib import Path

HOMEDIR = Path.cwd()
LOGPATH = HOMEDIR / 'logs'

# ---------------------------------------------------------------------------- #
#                               Helper functions                               #
# ---------------------------------------------------------------------------- #


def create_log(path: Path):
	if not path.parent.is_dir():
		path.parent.mkdir()

	logging.basicConfig(
		filename=path, encoding='utf-8', level=logging.INFO)


def removeNonNumeric(s: str) -> str:
	return re.sub("[^0-9]*", '', s)


def getTimestamp(h: int, m: int, s: int) -> float:
	try:
		t = timedelta(hours=h, minutes=m, seconds=s).\
			total_seconds()
		return round(t, ndigits=1)
	except ValueError:
		return None


class BadFormat(ValueError):
	def __init__(self, *args: object) -> None:
		super().__init__(*args)


# ---------------------------------------------------------------------------- #
#                                  GUI parser                                  #
# ---------------------------------------------------------------------------- #

class MultiInput:
	def __init__(self, defaults: Dict[str, Union[str, int]] = {}) -> None:

		self.boxes: list[tk.Frame] = []
		self.box_kw = dict(fill='x', expand=True)
		self.frame_kw = dict(padx=10, pady=10, **self.box_kw)

		self.setup()
		self.createVariables()
		self.createEntryFields(defaults=defaults)
		self.createButton()
		self.root.mainloop()

	def setup(self):
		self.root = tk.Tk()
		self.root.geometry("300x380")
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

		self.fmt = tk.StringVar()
		self.desc = tk.StringVar()

	@staticmethod
	def _validateFields(
			url: str, start: list[int], stop: list[int], fmt: str, desc: str) -> Tuple[str, float, float, Union[str, int], str]:
		if not validators.url(url):
			raise ValueError(f"{url} is not a valid URL")

		try:
			times = [getTimestamp(*hms) for hms in [start, stop]]
		except Exception as e:
			raise ValueError(
				f'Invalid timestamps\nStart:{start:^10}Stop:{stop:^8}')

		return url, times[0], times[1], fmt, desc

	def clicked(self):
		""" callback when the button is clicked"""
		# validate inputs
		url, start, stop, fmt, desc = self._validateFields(
			*self.extractVariables()
		)

		# store inputs for later use
		self.contents = [url, start, stop, fmt, desc]

		msg = 'You entered:\n'
		msg += f'URL:{url}\nStart: {start}\nEnd: {stop}\nFormat: {fmt}\nDescription: {desc}'
		mbox.showinfo(title='Information', message=msg)

		# exit the window
		self.root.quit()

	def _createFrame(self) -> tk.Frame:
		frame = tk.Frame(self.root)
		frame.pack(**self.frame_kw)
		self.boxes.append(frame)
		return frame

	def create_hms_box(self, label: str, default: str = None) -> None:
		
		if default is None:
			hms = [0]*3
		else:
			hms = default.split(":")

		units = ['HH', 'MM', 'SS']
		frame = self._createFrame()
		
		for u, val in zip(units, hms):
			key = f"{label}_{u}"
			var = self.__dict__[key]

			if u == 'HH':
				name = tk.Label(frame, text=f"{label} {u}")
			else:
				name = tk.Label(frame, text=u)
			
			name.pack(side='left')
			entry = tk.Entry(frame, textvariable=var, width=10)

			entry.insert(0, f"0{val}" if len(val) < 2 else val)
			entry.pack(side='left', **self.box_kw)

	def _createEntryField(
			self,
			label: str = None,
			frame: tk.Frame = None,
			focus: bool = False,
			default: Union[str, int] = None) -> None:

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
			self, defaults: Dict[str, Union[str, int]] = {}):

		for lab in ['url', 'start', 'stop', 'fmt', 'desc']:
			dflt = defaults[lab] if (lab in defaults) else None
			fcs = True if (lab == 'url') else False

			if lab in ['start', 'stop']:
				self.create_hms_box(lab, default=dflt)
			else:
				self._createEntryField(
					lab, focus=fcs, default=dflt)

	def createButton(self):
		button = tk.Button(
			self.boxes[-1], text='Run', command=self.clicked)

		button.pack(pady=10, **self.box_kw)

	def extractVariables(self) -> Tuple[str, str, str, int]:
		start, stop = [
			[
				int(self.__dict__[f"{s}_{u}"].get())
				for u in ['HH', 'MM', 'SS']
			] for s in ['start', 'stop']
		]

		return (
			self.url.get(),
			start,
			stop,
			self.fmt.get(),
			self.desc.get()
		)


# ---------------------------------------------------------------------------- #
#       Helper functions for parsing CLI arguments and setting up the GUI      #
# ---------------------------------------------------------------------------- #

DFLT_HMS = re.compile(r"(\d{2,}\:\d{2}\:\d{2})|(\d+\.\d)")
def read_default_times(info: str, pat=DFLT_HMS) -> tuple[str, str]:
	times = [
		x[0] if len(x[0]) > 1 else x[1] 
		for x in pat.findall(info)
	]

	if len(times) > 2:
		times = times[1:]

	if ":" in times[0]:
		return times 
	
	str_times: list[str] = [] 
	for t in times:
		secs = float(t)
		h = secs // 3600 
		m = (secs - 3600*h) // 60 
		s = max(0, secs - 3600*h - 60*m)
		
		str_times.append(
			":".join(map(lambda x: str(int(x)), [h, m, s]))
		)

	return str_times 

def get_last_logged_values(
		logpath: Path = LOGPATH,
		time: datetime = None,
		link: str = None,
		desc: str = None,
		encoding='utf-8') -> dict[str, Union[int, str]]:

	logfile = logpath / 'dl.log'
	if not logfile.is_file():
		raise FileNotFoundError(
			f"{logfile} not found. No defaults loaded.")

	lines = Popen(
		['powershell.exe', f"Get-Content \"{logfile}\" -tail 10"],
		stdout=PIPE).\
		communicate()[0].\
		decode(encoding)

	try:
		info = lines.split("INFO:root:")[1]
	except:
		print(lines)
		raise ValueError(
			f"\nUnable to be \"INFO:root:\" in the last 10 lines of the log."
		)

	print("Using the following defaults:", info, sep='\n')
	try:
		start, stop = read_default_times(info)
	except Exception as e:
		raise ValueError(f"Failed to parse start and stop times from {info}")
	
	link = re.search(r"(?:URL\:)\s*([^\s]+)\s", info).group(1)
	defaults = dict(url=link, start=start, stop=stop)
	tmplt = "(?:{field}\:)\s*([^\s]*)"
	for field, key in zip(['Description', 'Format'], ['desc', 'fmt']):
		res = re.search(tmplt.format(field=field), info)

		if res is None:
			continue
		defaults[key] = res.group(1)

	print(defaults)
	return defaults


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


def desc2outname(desc: str) -> str:
	return re.sub(r"[^\w\d\_\-]*", '', desc)


def get_cmd(
		url: str, fmt: int, start: str = None, stop: str = None) -> str:
	if start and stop:
		ffmpeg_cmd = f"--external-downloader ffmpeg --external-downloader-args \"ffmpeg_i:-ss {start} -to {stop}\""
	else:
		print(
			f"Both start and stop are required, but\nStart = {start} and Stop = {stop}"
		)

		cont = input(
			"Continue? The program will not trim the video. [y/n]"
		).lower()

		if cont == 'n':
			raise ValueError("Start and stop were not provided.")
		else:
			ffmpeg_cmd = ""

	cmd = f"yt-dlp -f {fmt} {ffmpeg_cmd} {url}"

	return cmd


def create_gui(defaults: Dict[str, Any] = {}) -> Tuple[str, str, str, int]:

	form = MultiInput(defaults)

	try:
		url, start, stop, fmt, desc = form.contents

	except AttributeError:
		raise AttributeError("No valid inputs.")

	except BadFormat:
		print(f"Unsupported format: {fmt}\nPlease select a format below:")

		url, start, stop, _ = form.extractVariables()
		defaults = dict(url=url, start=start, stop=stop)

		print("List of available formats:\n")
		cmd = f"yt-dlp -F {url}"
		Popen(['powershell', cmd])

		form = MultiInput(defaults)
		fmt = form.contents[-1]

	return url, start, stop, fmt, desc


def update_log(
		url: str, start: str, stop: str, fmt: int,
		description=None, cmd=None,
		logpath=LOGPATH,
		logmode="append") -> None:

	logmsg = f"""
		Time: {datetime.strftime(datetime.now(), format=r"%Y-%m-%d %H:%M:%S"):^50}
		URL: {url:^50}
		Start:{start:^14}Stop:{stop:^14}Format:{fmt:>4}
		Description:{description}
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


def main(
		url: str,
		start: str, stop: str,
		fmt: Union[str, int],
		desc: str,
		outdir: Path = HOMEDIR) -> None:

	cmd = get_cmd(url, fmt, start=start, stop=stop)
	update_log(url, start, stop, fmt, description=desc, cmd=cmd)

	outname = desc2outname(desc) +\
		f"__({url.split('/')[-1]})"

	outname = re.sub(
		r'[^\w\-_\.\s]',
		'', outname
	)

	outpath = outdir / f"{outname}.mp4"

	Popen(['powershell.exe', cmd + f" -o \"{outpath}\""])


if __name__ == "__main__":
	if len(argv) >= 3:
		args = extract_cli_args()
	else:
		try:
			defaults = get_last_logged_values()
		except ValueError as e:
			print(e)
			defaults = dict(fmt=22)

		args = create_gui(defaults=defaults)

	main(*args)
