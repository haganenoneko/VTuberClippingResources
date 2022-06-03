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

1. Downloading videos from YouTube with `scripts/dl.py`
2. Creating subtitles with Aegisub (examples in `selected_ass_files`)
3. Creating thumbnails (PSD files for many thumbnails and VTuber icons in `thumbnails`)
4. Burning subtitles with `scripts/burn.py`

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

The scripts in the `./scripts/` folder can be used to download videos from YouTube and hardcode subtitles.

### Downloading YouTube clips with `scripts/download.py`

There are two ways to run `scripts/download.py`.

#### Where videos will be downloaded

In both cases, the download location is where you run the script from. If you use the GUI, it will be `scripts/`. If you use a terminal, you can call it from somewhere else, and the videos will be downloaded there instead.

Of course, you can move the files. However, if you move `download.py`, make sure to move `common.py` as well.

#### Using the GUI

The first is by double-clicking the script, which should open a GUI where you can input things like URLs, start and stop times, and download formats.

It will download videos to `scripts/` (unless you change where you're running the script from) and will also save logs into the `scripts/logs/` folder (which it will create if it doesn't exist already).

```
VTuberClippingResources/
└── scripts/
    ├── common.py
    ├── download.py
    ├── hardcode.py
    └── logs/
        └── dl.log
```

The log file should be very useful, e.g. you can copy-paste the output into your video descriptions while also keeping track of your sources. Each time you run `download.py`, your input will be appended to the file. For example, given the input

<img src="https://github.com/haganenoneko/VTuberClippingResources/blob/main/scripts/Screenshot%202022-06-03%20163317.png?raw=true" style="display: block; margin-left: auto; margin-right: auto; width: 300px; padding-top: 20px; padding-bottom: 20px">

The log file will then be updated with the following information:

```
INFO:root:
  Time:                2022-06-03 16:06:26                
  URL:    https://www.youtube.com/watch?v=oxcLcNcdZiY    
  Start:   00:00:00   Stop:   00:01:00   Format: 380
```

#### Using the command-line

The second is via the command line. To do this, open the folder containing `dl.py` in `cmd.exe`, `powershell.exe`, or whatever terminal you have. Then, type in `python dl.py --help` to see what commands you can use.

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

These should be folders in the same directory that contains `burn.py`.

## Disclaimer

Use all of these tools at your own discretion. I am not responsible for any damages or consequences you may incur using these tools.
