# Video-Tamper-Detect
VidTamperDetect is a lightweight Python-based tool designed to detect potential tampering in CCTV and surveillance footage. It uses Optical Character Recognition (OCR) to extract embedded timestamps from video frames and analyzes scene transitions to identify sudden changes or cuts that could indicate manipulation.

## 🔍 Core Features

**Timestamp-Based Detection**  
Extracts visible timestamps using Tesseract OCR and detects jumps exceeding a configurable threshold (default: 30 seconds). This helps identify missing or altered footage segments.

**Scene Change Analysis**  
When timestamps are not available, the tool analyzes frame-to-frame differences in grayscale pixel intensity to detect abrupt visual cuts or transitions—useful for uncovering suspicious edits.

**Dual Detection Modes**  
Automatically switches between timestamp analysis and scene cut detection based on video content, ensuring reliable results across different formats and quality levels.

**No Metadata Dependency**  
Operates purely on frame content, making it suitable for analyzing footage where metadata is missing or unreliable.

---

## 🧠 Ideal For

- Digital forensics investigations  
- Authenticating security footage  
- Detecting tampering in video evidence  
- Educational or research projects in video forensics and cybersecurity

## 📂 Add Your Video File

In the script `forensic_video_analyzer.py`, go to **line 91** and update the file path:

```python
video_file = "E:\\dissertation 2\\edit2.mp4"  # Replace with your video file path
