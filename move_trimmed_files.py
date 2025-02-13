import os
import shutil

def move_and_rename_files(source_folder, target_folder):
    # Ensure the target folder exists
    os.makedirs(target_folder, exist_ok=True)

    moved_files = []
    # Iterate over the files in the source folder
    for filename in os.listdir(source_folder):
        # Process only .mp4 files with an underscore in the filename
        if filename.endswith(".mp4"):
            # Extract the part of the filename before the underscore
            new_name = filename
            
            # Full paths for source and destination
            source_path = os.path.join(source_folder, filename)
            destination_path = os.path.join(target_folder, new_name)
            
            # Move and rename the file
            shutil.move(source_path, destination_path)
            moved_files.append((filename, new_name))
            print(f"Moved and renamed: {filename} -> {new_name}")

    return moved_files
