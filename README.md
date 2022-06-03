# VTuberClippingResources
Scripts and resources to help with clipping

- [VTuberClippingResources](#vtuberclippingresources)
  - [Contents](#contents)
  - [Dependencies](#dependencies)
  - [Instructions](#instructions)
    - [Downloading YouTube clips with `src/download.py`](#downloading-youtube-clips-with-srcdownloadpy)
    - [Burning `.ass` subtitles with `src/hardcode.py`](#burning-ass-subtitles-with-srchardcodepy)
  - [Disclaimer](#disclaimer)

## Contents
These files represent the minimal full spectrum of tools required for clipping: 
1. Downloading videos from YouTube with `src/dl.py`
2. Creating subtitles with Aegisub (examples in `selected_ass_files`)
3. Creating thumbnails (PSD files for many thumbnails and VTuber icons in `thumbnails`)
4. Burning subtitles with `src/burn.py`

## Dependencies
These are software/tools you will need to install before using the scripts below.

- `Python 3.10.1`
- `yt-dlp`
- `ffmpeg`

Python packages. Install these by typing 

```batch
py -3 -m pip install [PACKAGE_NAME]
```

- tkinter
- validators

If you are new to Python and encounter errors, you should first make sure that Python has been properly added to your `PATH` variables. If so, you should be able to open a terminal such as `cmd.exe` and see the following output if you type in `python --version`:

```batch
> python --version
Python 3.10.1
```

## Instructions
The scripts in the `./src/` folder can be used to download videos from YouTube and hardcode subtitles. 

### Downloading YouTube clips with `src/download.py`
This should work out of the box, unless you're missing packages, and will download videos to the folder containing the script. 

### Burning `.ass` subtitles with `src/hardcode.py`
Open the file and edit the lines 

```python
YOUR_RAW_VIDEO_DIRECTORY = "..."
YOUR_SUBTITLE_DIRECTORY = "..."
```

These should be folders in the same directory that contains `burn.py`. 


(Edit 03/06/2022) 
There are actually two ways to run `dl.py`. 
1. The first is by double-clicking the script, which should open a GUI where you can input things like URLs, start and stop times, and download formats. 
2. The second is via the command line. To do this, open the folder containing `dl.py` in `cmd.exe`, `powershell.exe`, or whatever terminal you have. Then, type in `python dl.py --help` to see what commands you can use. 

```bash
> python dl.py --help
usage: dl.py [-h] [--start START] [--end END] [--format FORMAT] URL

Add clip information

positional arguments:
  URL              Youtube URL

options:
  -h, --help       show this help message and exit
  --start START    Start time
  --end END        End time
  --format FORMAT  youtube-dl format
```

For example, the following command downloads 720p video from `https://youtu.be/4UeyWzQFgJU` betwen times `1:03:10` and `1:05:10`. 
```bash
> ptyhon dl.py --start 01:03:10 --end 01:05:10 --format 22 https://youtu.be/4UeyWzQFgJU
```

**A word of caution.** Whichever way you open `dl.py`, make you sure you input 'zero-padded' timestamps, ie write `01:00:00` for one hour, not `1:00:00`, and `00:30:00` for 30 minutes, not `30:00`. This is because I was too lazy to add code to format arbitrary input. 

## Disclaimer
Use all of these tools at your own discretion. I am not responsible for any damages or consequences you may incur using these tools. 

