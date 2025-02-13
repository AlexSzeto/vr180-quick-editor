# requirements: flask, moviepy
from flask import Flask, render_template, redirect, url_for, request, send_file
import os
import re
import csv
from moviepy import VideoFileClip
from trim_from_csv import trim_and_move_files
from move_trimmed_files import move_and_rename_files
from combine_with_crossfade import combine_videos_with_crossfade
from inject_spatial_data import inject_spatial_data
import subprocess

app = Flask(__name__)

def get_filtered_folders():
    """Get folders that match the year-month or year-month-day name format."""
    if os.path.exists("settings.txt"):
        with open("settings.txt", "r") as f:
            current_path = f.read().strip()
    else:
        current_path = os.getcwd()
    all_folders = [name for name in os.listdir(current_path) if os.path.isdir(os.path.join(current_path, name))]
    # Regex to match "YYYY-MM" or "YYYY-MM-DD" formats
    pattern = re.compile(r"^\d{4}-\d{2}(-\d{2})?\s.*")
    return [folder for folder in all_folders if pattern.match(folder)]

@app.route("/<video_file>")
def play_video(video_file):
    """Play the selected video file."""
    if os.path.exists("project.txt"):
        with open("project.txt", "r") as f:
            folder_path = f.read().strip()

    video_path = os.path.join(folder_path, video_file)
    video_url = f"file:///{os.path.abspath(video_path)}"
    
    if not os.path.exists(video_path):
        return f"Video file not found: {video_path}", 404
    return send_file(video_path)

@app.route("/")
def index():
    """Display the current project."""
    if os.path.exists("settings.txt"):
        with open("settings.txt", "r") as f:
            current_path = f.read().strip()    
    if os.path.exists("project.txt"):
        with open("project.txt", "r") as f:
            project_name = os.path.basename(f.read().strip())
    else:
        project_name = "None Selected"
    
    folder_path = os.path.join(current_path, project_name)
    has_renamed = os.path.exists(os.path.join(folder_path, "01.mp4"))
    has_video_details = os.path.exists(os.path.join(folder_path, "video_details.csv"))
    has_trimmed_videos = os.path.exists(os.path.join(folder_path, "trimmed"))
    upscaled_folder = os.path.join(folder_path, "upscaled")
    has_upscaled_videos = os.path.exists(upscaled_folder) and len(os.listdir(upscaled_folder)) > 0
    has_combined_video = os.path.exists(os.path.join(folder_path, f"{os.path.basename(folder_path)}_uninjected.mp4"))
    has_final_output = os.path.exists(os.path.join(folder_path, f"{os.path.basename(folder_path)}.mp4"))

    return render_template("index.html", project_name=project_name, has_renamed=has_renamed, has_video_details=has_video_details, has_trimmed_videos=has_trimmed_videos, has_upscaled_videos=has_upscaled_videos, has_combined_video=has_combined_video, has_final_output=has_final_output)

@app.route("/project")
def project_page():
    """Display the page to change the current project."""
    folders = get_filtered_folders()
    
    if os.path.exists("settings.txt"):
        with open("settings.txt", "r") as f:
            current_path = f.read().strip()
            
    # check if each folder contains video_details.csv
    project_folders = []
    for folder in folders:
        if os.path.exists(os.path.join(current_path, folder, "video_details.csv")):
            print(f"Found video_details.csv in {folder}")
            project_folders.append(folder)
    
    # map folder as object with path and whether it's a project folder
    folders = [{"path": folder, "is_project": folder in project_folders} for folder in folders]

    return render_template("project.html", folders=folders)

@app.route("/save/<folder>")
def save_project(folder):
    """Save the full path of the selected folder to project.txt."""
    """Get folders that match the year-month or year-month-day name format."""
    if os.path.exists("settings.txt"):
        with open("settings.txt", "r") as f:
            current_path = f.read().strip()
    else:
        current_path = os.getcwd()
    folder_path = os.path.join(current_path, folder)
    with open("project.txt", "w") as f:
        f.write(folder_path)
    return redirect(url_for('index'))

@app.route("/open_folder")
def open_folder():
    try:
        if os.path.exists("project.txt"):
            with open("project.txt", "r") as f:
                folder_path = f.read().strip()
        else:
            return redirect(url_for('project_page'))

        subprocess.Popen(f'explorer "{folder_path}"')
        return redirect(url_for('index'))
    except Exception as e:
        return redirect(url_for('index'))
      
@app.route("/rename")
def rename_files():
    """Rename all files in the selected project folder."""
    try:
      if os.path.exists("project.txt"):
          with open("project.txt", "r") as f:
              folder_path = f.read().strip()
      else:
          return redirect(url_for('project_page'))
    
      # Get all files in the current directory
      files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f)) and f.lower().endswith('.mp4')]
      print(os.listdir(folder_path))
      print(files)

      # Sort files alphabetically
      files.sort()

      # Rename files with padded numbers
      rename_files = []
      for i, file in enumerate(files, start=1):
          # Extract file extension
          _, ext = os.path.splitext(file)
          
          # Create the new filename
          new_name = os.path.join(folder_path, f"{i:02}{ext}")
          
          # Rename the file
          os.rename(file, new_name)
          rename_files.append((file, new_name))
      
      return render_template("rename.html", renamed_files=rename_files, message="", success=True)
    except Exception as e:
      return render_template("rename.html", renamed_files=[], message=str(e), success=False)
        
@app.route("/generate_csv")
def generate_csv():
    """Generate a CSV file with video details in the selected project folder."""
    try:
        if os.path.exists("project.txt"):
            with open("project.txt", "r") as f:
                folder_path = f.read().strip()
        else:
            return redirect(url_for('project_page'))
        
        # Get all video files in the current directory
        files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f)) and f.lower().endswith('.mp4')]
        
        # Sort files alphabetically
        files.sort()

        # Prepare CSV data
        csv_data = [["Clip Path", "Clip Name", "Description", "Length", "Motion", "Keep", "Start", "End", "Family", "Notes"]]
        details_list = []
        for file in files:
            # Get clip length using moviepy
            clip = VideoFileClip(file)
            length = int(clip.duration)  # Convert to seconds
            clip.close()
            
            # Extract file name without extension
            file_name = os.path.basename(file)

            # Add row to CSV data
            csv_data.append([file, file_name, "", length, "", "FALSE", "", "", "FALSE", ""])
            details_list.append((file, length))
        
        # Write to CSV file
        csv_file = os.path.join(folder_path, "video_details.csv")
        with open(csv_file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(csv_data)

        return render_template("generate.html", details_list=details_list, message="CSV file generated successfully: video_details.csv", success=True)
    except Exception as e:
        return render_template("generate.html", details_list=[], message=str(e), success=False)

@app.route("/edit_csv", methods=["GET", "POST"])
def edit_csv():
    if os.path.exists("project.txt"):
        with open("project.txt", "r") as f:
            folder_path = f.read().strip()
    else:
        return redirect(url_for('project_page'))
            
    csv_file = os.path.join(folder_path, "video_details.csv")
    if request.method == "POST":
        # Save changes to the CSV file
        data = request.form.to_dict(flat=False)  # Get form data
        print(data)
        
        # Reconstruct CSV data
        updated_data = [
            ["Clip Path", "Clip Name", "Description", "Length", "Motion", "Keep", "Start", "End", "Family", "Notes"]
        ]
        row_count = len(data["Clip Name"])  # Number of rows in the table
        for i in range(row_count):
            updated_data.append([
                data["Clip Path"][i],
                data["Clip Name"][i],
                data["Description"][i],
                data["Length"][i],
                data["Motion"][i],
                "TRUE" if f"Keep_{i}" in data else "FALSE",
                data["Start"][i],
                data["End"][i],
                "TRUE" if f"Family_{i}" in data else "FALSE",
                data["Notes"][i],
            ])
        
        # Write the updated data back to the CSV file
        with open(csv_file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(updated_data)
        
        return redirect(url_for("edit_csv"))  # Reload the page to show updated data
    
    # Read data from the CSV file
    csv_data = []
    with open(csv_file, "r") as f:
        reader = csv.reader(f)
        csv_data = [row for row in reader]

    print(csv_data)

    headers = csv_data[0]  # Column headers
    rows = csv_data[1:]    # Data rows
    return render_template("edit.html", headers=headers, rows=rows)

@app.route("/trim_videos")
def trim_videos():
    if os.path.exists("project.txt"):
        with open("project.txt", "r") as f:
            folder_path = f.read().strip()
    else:
        return redirect(url_for('project_page'))
            
    csv_file = os.path.join(folder_path, "video_details.csv")

    # TODO: update page to GET/POST and create a form to filter videos
    success, video_data, message = trim_and_move_files(folder_path, csv_file, [], os.path.join(folder_path, "trimmed"))
    
    upscaled_folder = os.path.join(folder_path, "upscaled")
    if not os.path.exists(upscaled_folder):
        os.makedirs(upscaled_folder, exist_ok=True)
        
    return render_template("trim.html", success=success, video_data=video_data, message=message)

@app.route("/split_videos", methods=["POST"])
def split_videos():
    if os.path.exists("settings.txt"):
        with open("settings.txt", "r") as f:
            base_path = f.read().strip()
    if os.path.exists("project.txt"):
        with open("project.txt", "r") as f:
            project_path = f.read().strip()
    data = request.get_json()            
    csv_file = os.path.join(project_path, "video_details.csv")
    
    # Read data from the CSV file
    csv_data = []
    with open(csv_file, "r") as f:
        reader = csv.reader(f)
        csv_data = [row for row in reader]
    
    split_rows = []
    # Filter videos based on the selected rows
    for file in data["files"]:
        print(f"Splitting {file}")
        for row in csv_data[1:]:
            if file in row:
                split_rows.append(row)
                
    stay_rows = [row for row in csv_data[1:] if row not in split_rows]
    
    split_rows.insert(0, csv_data[0])  # Add headers
    stay_rows.insert(0, csv_data[0])  # Add headers
    
    # split the date and name portion of the folder path
    pattern = re.compile(r"^(\d{4}-\d{2}(?:-\d{2})?)\s.*")
    folder_date = pattern.match(os.path.basename(project_path)).group(1)
    
    split_folder = os.path.join(base_path, f"{folder_date} {data['folderName']}")
    os.makedirs(split_folder, exist_ok=True)
    
    split_project_csv = os.path.join(split_folder, "video_details.csv")
    with open(split_project_csv, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(split_rows)
        
    stay_project_csv = os.path.join(project_path, "video_details.csv")
    with open(stay_project_csv, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(stay_rows)
        
    # move the split files to the new folder
    clip_path_index = split_rows[0].index("Clip Path")
    split_files = [row[clip_path_index] for row in split_rows[1:]]
    
    for file in split_files:
        file_name = os.path.basename(file)
        new_file = os.path.join(split_folder, file_name)
        os.rename(file, new_file)
        
    return { "success": True }, 200
    
@app.route("/move_trimmed_to_upscaled")
def move_trimmed_to_upscaled():
    if os.path.exists("project.txt"):
        with open("project.txt", "r") as f:
            folder_path = f.read().strip()
    else:
        return redirect(url_for('project_page'))
    
    source_folder = os.path.join(folder_path, "trimmed")
    target_folder = os.path.join(folder_path, "upscaled")
    moved_files = move_and_rename_files(source_folder, target_folder)
    return render_template("move.html", video_data=moved_files)

@app.route("/combine_videos")
def combine_videos():
    if os.path.exists("project.txt"):
        with open("project.txt", "r") as f:
            folder_path = f.read().strip()
    else:
        return redirect(url_for('project_page'))
    
    # Move and rename trimmed files
    # source_folder = os.path.join(folder_path, "trimmed")
    target_folder = os.path.join(folder_path, "upscaled")
    # moved_files = move_and_rename_files(source_folder, target_folder)

    # Combine videos with crossfade
    output_file = os.path.join(folder_path, f"{os.path.basename(folder_path)}_uninjected.mp4")
    success, final_message = combine_videos_with_crossfade(target_folder, output_file)
    return render_template("combine.html", success=success, message=final_message)

@app.route("/inject_video")
def inject_video():
    if os.path.exists("project.txt"):
        with open("project.txt", "r") as f:
            folder_path = f.read().strip()
    else:
        return redirect(url_for('project_page'))
    
    # Inject spatial data into the combined video
    input_video = os.path.join(folder_path, f"{os.path.basename(folder_path)}_uninjected.mp4")
    output_video = os.path.join(folder_path, f"{os.path.basename(folder_path)}.mp4")
    inject_spatial_data(input_video, output_video)
    return render_template("inject.html")

if __name__ == "__main__":
    app.run(debug=True)
