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


## Disclaimer
Use all of these tools at your own discretion. I am not responsible for any damages or consequences you may incur using these tools. 

