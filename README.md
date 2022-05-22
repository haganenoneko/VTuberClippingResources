# VTuberClippingResources
Scripts and resources to help with clipping

## Contents
These files represent the minimal full spectrum of tools required for clipping: 
1. Downloading videos from YouTube with `src/dl.py`
2. Creating subtitles with Aegisub (examples in `selected_ass_files`)
3. Creating thumbnails (PSD files for many thumbnails and VTuber icons in `thumbnails`)
4. Burning subtitles with `src/burn.py`

## Dependencies
- python 3
- yt-dlp
- ffmpeg

Python packages
- tkinter
- validators

## Instructions
`burn.py`
Open the file and edit the lines 
```python
YOUR_RAW_VIDEO_DIRECTORY = "..."
YOUR_SUBTITLE_DIRECTORY = "..."
```
These should be folders in the same directory that contains `burn.py`. 

`dl.py`
This should work out of the box, unless you're missing packages, and will download videos to the folder containing the script. 

## Disclaimer
Use all of these tools at your own discretion. I am not responsible for any damages or consequences you may incur using these tools. 

