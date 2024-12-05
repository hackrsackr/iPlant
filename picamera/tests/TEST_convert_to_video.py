import subprocess

def create_timelapse(input_pattern, output_file, fps=30, pix_fmt='yuv420p', codec='libx264'):
    """Creates a timelapse video from a sequence of images."""

    cmd = [
        'ffmpeg',
        '-r', str(fps),  # Set the desired frame rate for the output video
        '-pattern_type', 'glob',  # Use glob pattern matching for input files
        '-i', input_pattern,  # Input image pattern (e.g., '*.jpg')
        '-c:v', codec,  # Specify the video codec (e.g., libx264, h265)
        '-pix_fmt', pix_fmt,  # Set the pixel format (e.g., yuv420p)
        output_file  # Output video file
    ]

    subprocess.run(cmd)

# Example usage
input_folder = "tests/TEST_timelapses/*.jpg"
output_file = "tests/TEST_timelapses/timelapse.mp4"
frame_rate = 30
create_timelapse(input_folder, output_file)