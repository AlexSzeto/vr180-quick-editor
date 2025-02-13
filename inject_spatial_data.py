import subprocess
import os

def inject_spatial_data(input_video, output_video):
    cwd_path = os.path.join(os.getcwd(), 'spatial-media')
    subprocess.run(["python", "spatialmedia", "-i", "-s", "left-right", "-m", "equirectangular", input_video, output_video], cwd=cwd_path)