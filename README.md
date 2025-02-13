# vr180-quick-editor

A quick and dirty tool for editing VR180 clips

Currently not meant for "public consumption", but you're welcome to try. Requires FFMPEG to be installed (among other things).

Also requires https://github.com/Vargol/spatial-media to be cloned into `spatial-media/` for injecting VR180 metadata.

## SETUP

Edit settings.txt to indicate where your videos are stored. Each "project" is a subfolder inside that main video folder with video files directly inside it (the filenames doesn't matter, part of the editing process would automatically rename the files). The folders must be specifically named using a `YYYY-MM-DD <NAME>` format.

## HOW TO USE

Run editor.py to start the flask server, then:

Select a folder to make it the current project folder, then more or less run the commands from top to bottom. Keep an eye on the command prompt where the flask server is running - there's no progress indicator within the web UI and some parts of the processes takes a long time.

## SAMPLE PROJECT STRUCTURE

```
V:/Video Project
 |
 +-- 2024-03-17 My Summer Vacation Videos
 |  |
 |  +-- 238439_93.mp4
 |  +-- 238439_94.mp4
 |  +-- 23843243_95.mp4
 |
 +-- 2024-05-26 Horrible Time At My Inlaws
 |  |
 |  +-- 238439_93.mp4
 |  +-- 238439_94.mp4
 |  +-- 23843243_95.mp4
```
