import cv2
import pytesseract
import re
from datetime import datetime
import numpy as np

# Configure Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_timestamp(frame):
    """
    Extract timestamp from a video frame using OCR.
    """
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Convert frame to grayscale
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)  # Apply thresholding
    text = pytesseract.image_to_string(thresh, config='--psm 6')  # Perform OCR

    timestamp_pattern = re.search(r'\d{2}[:\-\/]\d{2}[:\-\/]\d{2}', text)
    
    if timestamp_pattern:
        try:
            return datetime.strptime(timestamp_pattern.group(), "%M:%S:%f")
        except ValueError:
            return None
    return None

def detect_tampering(video_path):
    """
    Analyze the video for timestamp jumps exceeding 1 second.
    """
    cap = cv2.VideoCapture(video_path)
    prev_timestamp = None
    tampering_durations = []
    
    frame_count = 0  # Track frames

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Process every single frame (1-1 frame extraction)
        timestamp = extract_timestamp(frame)

        if timestamp and prev_timestamp:
            time_diff = (timestamp - prev_timestamp).total_seconds()
            if time_diff > 30:
                tampering_durations.append(time_diff)
                print(f"Sudden jump detected: {time_diff} seconds")

        if timestamp:
            prev_timestamp = timestamp

        frame_count += 1

    cap.release()
    return tampering_durations

def analyze_video_without_timestamps(video_path):
    """
    Perform node analysis for videos without timestamps by detecting scene cuts.
    """
    cap = cv2.VideoCapture(video_path)
    prev_frame = None
    tampering_events = []

    frame_count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if prev_frame is not None:
            diff = cv2.absdiff(prev_frame, gray_frame)
            score = np.mean(diff)  # Calculate difference between frames
            
            if score > 50:  # Threshold for sudden scene change
                tampering_events.append((frame_count, score))
                print(f"Scene change detected at frame {frame_count}: Score {score}")

        prev_frame = gray_frame
        frame_count += 1

    cap.release()
    return tampering_events

if __name__ == "__main__":
    video_file = "E:\\dissertation 2\edit2.mp4"  # Replace with actual video file path

    # Step 1: Try detecting tampering using timestamps
    tampering_jumps = detect_tampering(video_file)

    if tampering_jumps:
        print("Tampering Detected via Timestamps! Duration(s) of jumps:", tampering_jumps)
    else:
        print("No timestamp-based tampering detected.")

        # Step 2: If no timestamps detected, try node-based analysis
        scene_changes = analyze_video_without_timestamps(video_file)
        if scene_changes:
            print("Tampering Detected via Scene Change Analysis!")
        else:
            print("No significant tampering detected in video.")
