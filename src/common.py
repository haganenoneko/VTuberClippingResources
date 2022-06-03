import re 
import logging 
from pathlib import Path 
from datetime import datetime

# ---------------------------------------------------------------------------- #
#                    Common helper functions and exceptions                    #
# ---------------------------------------------------------------------------- #

def create_log(path: Path):
    if not path.parent.is_dir():
        path.parent.mkdir()
    
    logging.basicConfig(
        filename=path, encoding='utf-8', level=logging.INFO)

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