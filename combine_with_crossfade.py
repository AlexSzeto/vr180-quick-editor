import os
import subprocess
from moviepy import VideoFileClip, concatenate_videoclips, vfx, afx

def get_video_bitrate(video_path):
    try:
        # Run the ffmpeg command to get video file info
        result = subprocess.run(
            ["ffmpeg", "-i", video_path],
            stderr=subprocess.PIPE,  # ffmpeg writes output to stderr
            universal_newlines=True,
        )
        output = result.stderr

        # Extract bitrate from the output
        for line in output.splitlines():
            if "bitrate" in line:
                bitrate_line = line
                break
        else:
            return "Bitrate not found"

        # Extract the bitrate value
        bitrate_info = bitrate_line.split("bitrate:")[-1].strip().split(" ")[0]
        return bitrate_info
    except Exception as e:
        return str(e)

bitrate = "6000"

def combine_videos_with_crossfade(input_folder, output_file, crossfade_duration=1):
    # List to store video clips
    video_clips = []
    
    video_filenames = sorted(os.listdir(input_folder))
    # Get all .mp4 files in the input folder
    for index, filename in enumerate(video_filenames):  # Sorted for a logical order
        if filename.endswith(".mp4"):
            file_path = os.path.join(input_folder, filename)
            if index == 0:                
                bitrate = get_video_bitrate(file_path)
                print(f"Using bitrate: {bitrate}")
            append_effects = [afx.AudioFadeOut(crossfade_duration)]
            if index > 0:
                append_effects.append(vfx.CrossFadeIn(crossfade_duration))
                append_effects.append(afx.AudioFadeIn(crossfade_duration))
            if index == len(video_filenames) - 1:
                append_effects.append(vfx.FadeOut(crossfade_duration))
            video_clips.append(VideoFileClip(file_path).with_effects(append_effects))
    
    # Ensure there are enough clips to combine
    if len(video_clips) < 2:
        print("Not enough videos to combine. Need at least two.")
        return (False, "Not enough videos to combine. Need at least two.")

    # Add crossfade transition
    final_video = concatenate_videoclips(
        video_clips, 
        method="compose",  # Ensures clips are aligned correctly
        padding=-crossfade_duration  # Add padding for the crossfade transition
    )

    # Write the final video to a file
    final_video.write_videofile(output_file, 
                                codec="libx264",
                                threads=12,
                                bitrate=f"{bitrate}k")
    print(f"Combined video saved as {output_file}")
    return (True, f"Combined video saved as {output_file}")
