import os
import shutil
import sys

# --- 🚨 SMART FFMPEG SETUP 🚨 ---
# 1. CLOUD MODE: Check if FFmpeg is already installed (Streamlit Cloud does this via packages.txt)
if shutil.which("ffmpeg"):
    print("✅ Cloud/Linux Mode: FFmpeg found in system path!")

# 2. LOCAL WINDOWS MODE: If not found, force the manual path
else:
    print("⚠️ Local Mode: FFmpeg not found in system. Attempting manual path...")
    # Your specific local path
    local_ffmpeg_path = r"C:\ffmpeg\ffmpeg-8.0.1-essentials_build\bin"
    
    # Check if this folder actually exists (Debug Step)
    if os.path.exists(os.path.join(local_ffmpeg_path, "ffmpeg.exe")):
        print(f"✅ Found local FFmpeg at: {local_ffmpeg_path}")
        os.environ["PATH"] += os.pathsep + local_ffmpeg_path
    else:
        print(f"❌ ERROR: Could not find FFmpeg at {local_ffmpeg_path}")
# -------------------------------------------------------

import whisper
from moviepy import VideoFileClip, concatenate_videoclips
from transformers import pipeline

# --- 1. Load Models ---
def load_whisper_model():
    return whisper.load_model("base")

def load_summarizer_model():
    return pipeline("summarization", model="facebook/bart-large-cnn")

# --- 2. Transcription Engine ---
def transcribe_video(video_path):
    print("⏳ Starting Transcription...")
    model = load_whisper_model()
    result = model.transcribe(video_path)
    return result['segments']

# --- 3. Intelligence Layer ---
def extract_highlights(segments, retention_ratio=0.3):
    n_segments = int(len(segments) * retention_ratio)
    sorted_segments = sorted(segments, key=lambda x: len(x['text']), reverse=True)
    top_segments = sorted_segments[:n_segments]
    return sorted(top_segments, key=lambda x: x['start'])

def extract_keyword_highlights(segments, keywords):
    highlight_segments = []
    keyword_list = [k.strip().lower() for k in keywords.split(",")]
    for seg in segments:
        text = seg['text'].lower()
        if any(word in text for word in keyword_list):
            highlight_segments.append(seg)
    return highlight_segments

# --- 4. Video Processing (MoviePy 2.0 Compatible) ---
def generate_summary_video(video_path, selected_segments, output_path="summary_output.mp4"):
    try:
        clip = VideoFileClip(video_path)
        subclips = []
        
        for seg in selected_segments:
            start = seg['start']
            end = seg['end']
            # MoviePy 2.0 uses .subclipped() 
            new_subclip = clip.subclipped(start, end)
            subclips.append(new_subclip)
        
        final_clip = concatenate_videoclips(subclips)
        final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")
        
        clip.close()
        return output_path, clip.duration, final_clip.duration
        
    except Exception as e:
        print(f"Error in video processing: {e}")
        return None, 0, 0