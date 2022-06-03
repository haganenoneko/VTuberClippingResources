# VTuberClippingResources

Scripts and resources to help with clipping

- [VTuberClippingResources](#vtuberclippingresources)
  - [Contents](#contents)
  - [Dependencies](#dependencies)
  - [Instructions](#instructions)
    - [Downloading YouTube clips with `scripts/download.py`](#downloading-youtube-clips-with-scriptsdownloadpy)
      - [Where videos will be downloaded](#where-videos-will-be-downloaded)
      - [Using the GUI](#using-the-gui)
      - [Using the command-line](#using-the-command-line)
      - [Notes on inputs](#notes-on-inputs)
    - [Burning `.ass` subtitles with `scripts/hardcode.py`](#burning-ass-subtitles-with-scriptshardcodepy)
  - [Disclaimer](#disclaimer)

## Contents

These files represent the minimal full spectrum of tools required for clipping:

1. Downloading videos from YouTube with `scripts/download.py`
2. Creating subtitles with Aegisub (examples in `selected_ass_files`)
3. Creating thumbnails (PSD files for many thumbnails and VTuber icons in `thumbnails`)
4. Burning subtitles with `scripts/hardcode.py`

## Dependencies

**General software** you will need.

- `Python 3.10.1`
- `yt-dlp`
- `ffmpeg`

**Python packages.** Install these by typing

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

The scripts in the `./scripts/` folder can be used to download videos from YouTube and hardcode subtitles.

### Downloading YouTube clips with `scripts/download.py`

There are two ways to run `scripts/download.py`.

#### Where videos will be downloaded

In both cases, the download location is *where you run the script from*. If you use the GUI, it will be `scripts/`. If you use a terminal, you can call the script from somewhere else, and the videos will be downloaded there instead. Of course, you can move the files to whichever directory you like.

#### Using the GUI

Double-clicking the script should open a GUI in which you can input video information.

It will download videos to `scripts/` (unless you change where you're running the script from) and will also save logs into the `scripts/logs/` folder (which it will create if it doesn't exist already).

```
VTuberClippingResources/
└── scripts/
    ├── download.py
    ├── hardcode.py
    └── logs/
        └── dl.log
```

The log file should be very useful, e.g. you can copy-paste the output into your video descriptions while also keeping track of your sources. Each time you run `download.py`, your input will be appended to the file. For example, the input below downloads the first 30 seconds of [this video](https://www.youtube.com/watch?v=oxcLcNcdZiY) in 720p.

<img src="https://github.com/haganenoneko/VTuberClippingResources/blob/main/scripts/Screenshot%202022-06-03%20163317.png?raw=true" style="display: block; margin-left: auto; margin-right: auto; width: 300px; padding-top: 20px; padding-bottom: 20px">

The log file will then be updated with the following information:

```
INFO:root:
  Time:                2022-06-03 16:06:26                
  URL:    https://www.youtube.com/watch?v=oxcLcNcdZiY    
  Start:   00:00:00   Stop:   00:00:30   Format: 22
```

#### Using the command-line

To use the command-line, open the folder containing `download.py` in whatever terminal you prefer. Then, type in `python download.py --help` to see what commands you can use.

```bash
> python download.py --help
usage: download.py [-h] [--start START] [--end END] [--format FORMAT] URL

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
> python download.py --start 01:03:10 --end 01:05:10 --format 22 https://youtu.be/4UeyWzQFgJU
```

#### Notes on inputs

- If you use the *command-line interface*, make you sure you input 'zero-padded' timestamps, ie write `01:00:00` for one hour, not `1:00:00`, and `00:30:00` for 30 minutes, not `30:00`.
- If you followed the above and still get errors using either the CLI or GUI interfaces, double-check that your timestamps are valid. Invalid timestamps can include things like `75` minutes, `80` seconds, or non-numeric inputs.
- `Format`s should be valid `yt-dl` formats. Although you can use `best-audio` and `best-video` when calling `yt-dl` itself, I find that it is usually better that you know exactly what format/resolution/etc. you are downloading, so the `Format` input must be an integer, e.g. `22` for 720p video, `140` for `.m4a` audio, etc.

I plan to add something that allows you to check/see all available `yt-dl` format codes for a given video, but, currently, you'll just get an error if you give an invalid format.

### Burning `.ass` subtitles with `scripts/hardcode.py`

Open the file and edit the lines

```python
YOUR_RAW_VIDEO_DIRECTORY = "..."
YOUR_SUBTITLE_DIRECTORY = "..."
```

These should be folders in the same directory that contains `hardcode.py`. Once you've done this, you should be able to double-click `hardcode.py` and select your input video `.mp4` and subtitle `.ass` files.

If everything works as intended, the hardcoded video file should be saved in a folder called `burned`, also located in the same working directory. 

**A word of caution.** Sometimes, not often, there will be time delays in the final video. In my experience, this delay is usually around +0.5 to +1.5s. I don't know why it happens, but it does. As such, **always check your videos before you upload**! If you need to, go back into Aegisub and shift all your timings down/up as needed. 


## Disclaimer

Use all of these tools at your own discretion. I am not responsible for any damages or consequences you may incur using these tools.
