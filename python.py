import cv2 # type: ignore
import numpy as np
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import os
from datetime import datetime

def add_noise_to_video(input_path, output_path, noise_std=25):
    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        print("Error: Cannot open video file.")
        return

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_int = frame.astype(np.int16)
        noise = np.random.normal(0, noise_std, frame.shape).astype(np.int16)
        noisy_frame = np.clip(frame_int + noise, 0, 255).astype(np.uint8)

        out.write(noisy_frame)

    cap.release()
    out.release()
    print(f"ur stuff is done saved noisy video to: {output_path}")

def main():
    Tk().withdraw()
    print("select the video file you want to add noise to...")
    input_file = askopenfilename(filetypes=[("Video files", "*.mp4 *.mkv *.avi *.mov")])
    if not input_file:
        print("No file selected, exiting")
        return

    downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(downloads_folder, f"noisy_video_{timestamp}.mp4")

    add_noise_to_video(input_file, output_file)

if __name__ == "__main__":
    main()
