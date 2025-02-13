# requires moviepy, subprocess 
import csv
import sys
import os
from moviepy import VideoFileClip
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import subprocess

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

# Example usage
video_path = "example.mp4"

# Define a function to read the CSV file and convert it to an array of objects
def read_csv_to_objects(filename):
    video_data = []
    
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)  # Automatically handles header row
        for row in reader:
            # Convert each row into a dictionary (object) with modified fields
            video_data.append({
                "Filename": row["Clip Name"],
                "Description": row["Description"],
                "Motion": row["Motion"],
                "Keep": row["Keep"] == "TRUE",
                "Start": int(row["Start"]) if row["Start"] else None,
                "End": int(row["End"]) if row["End"] else None,
                "Family": row["Family"] == "TRUE"
            })
    
    return video_data

# Define a function to filter video data based on arguments
def filter_video_data(video_data, args):
    filters = {}
    for arg in args:
        if '=' in arg:
            key, value = arg.split('=', 1)
            filters[key] = value

    # Apply filters to the video data
    filtered_data = [
        video for video in video_data
        if all(str(video.get(key)) == value for key, value in filters.items())
    ]
    return filtered_data

# Define a function to trim and save videos
def trim_videos(input_folder, video_data, output_folder="output"):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    processed_videos = []
    for video in video_data:
        filename = video["Filename"]
        description = video["Description"]
        start = video["Start"]
        end = video["End"]
        
        # Display the current file being processed and its description
        print(f"Processing: {filename} ({description})")
        
        # Open and trim the video file
        try:
            file_path = os.path.join(input_folder, filename)
            bitrate = get_video_bitrate(file_path).replace("kb/s", "").strip()
            with VideoFileClip(file_path) as clip:
                output_path = os.path.join(output_folder, filename)
                # Check if the file already exists in the output path
                if os.path.exists(output_path):
                    print(f"File {output_path} already exists. Skipping.")
                    continue
                # Skip if start or end is None
                if start is None or end is None:
                    print(f"Skipping {filename} due to missing start or end time.")
                    continue
                # Trim the video between start and end times
                print(f"Trimming video to clip between {start} to {end} seconds.")
                trimmed_clip = clip.subclipped(start, end)
                # Save the trimmed video to the output folder
                trimmed_clip.write_videofile(output_path,
                                            codec="libx264",
                                            threads=12,
                                            bitrate=f"{bitrate}k")
                processed_videos.append((filename, end - start))
        except FileNotFoundError:
            print(f"Error: File {filename} not found.")
            return (False, processed_videos, f"Error: File {filename} not found.")
        except Exception as e:
            print(f"Error processing {filename}: {e}")
            return (False, processed_videos, f"Error processing {filename}: {e}")
        
    return (True, processed_videos, "Videos trimmed successfully.")

# Main program
def trim_and_move_files(video_folder, csv_path, filters, output_folder):
    # Read video data
    video_data = read_csv_to_objects(csv_path)
    
    # Get command-line arguments for filtering
    if len(filters) == 0:
        filters.append("Keep=True")
    filtered_data = filter_video_data(video_data, filters)
    
    # Trim and save videos
    return_data = trim_videos(video_folder, filtered_data, output_folder)
    
    return return_data