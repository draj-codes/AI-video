import streamlit as st
import os
import backend
import database

# --- 1. CONFIGURATION ---
st.set_page_config(
    page_title="Smart Video AI",
    page_icon="🎬",
    layout="wide",  # This makes it look like a real dashboard
    initial_sidebar_state="expanded"
)

# Initialize Database
database.init_db()

# --- 2. CUSTOM STYLING (CSS) ---
# This hides the default 'Streamlit' menu to make it look like a standalone app
st.markdown("""
    <style>
    .main {
        padding-top: 2rem;
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        background-color: #FF4B4B;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR: HISTORY ---
with st.sidebar:
    st.header("Recent Activity")
    st.markdown("---")
    
    if st.button("Refresh History"):
        st.rerun()

    history = database.get_history()
    if history:
        for row in history[:5]: # Show only last 5
            # row format: (id, filename, original_len, summary_len, date)
            with st.expander(f" {row[1]}"):
                st.caption(f"{row[4]}")
                st.metric("Time Saved", f"{row[2] - row[3]:.1f}s")
    else:
        st.info("No videos processed yet.")

    st.markdown("---")
    st.markdown("### Tech Stack")
    st.code("Python 3.9+\nOpenAI Whisper\nTransformers (BART)\nMoviePy\nStreamlit", language="text")

# --- 4. MAIN HEADER ---
st.title(" AI-Powered Video Summarizer")
st.markdown("""
###  Turn Long Videos into Concise Highlights
Welcome to the **AI Video Summarizer**. This tool uses advanced Artificial Intelligence to understand, analyze, and summarize your video content automatically.

**How it works:**
1.  **Upload** your video file (Lecture, News, or Meeting).
2.  **AI Analysis:** The system listens to the audio (using OpenAI Whisper) and understands the context.
3.  **Smart Cutting:** It identifies the most meaningful sentences and cuts out the filler.
4.  **Download:** Get a fully edited summary video in minutes!

*Built with Python, OpenAI Whisper, and MoviePy.*
""")
st.markdown("---")

# --- 5. MAIN CONTENT AREA ---
# Create a centered upload area
uploaded_file = st.file_uploader("Drag and drop your video here (MP4, AVI, MOV)", type=["mp4", "mov", "avi"])

if uploaded_file is not None:
    # Save temp file
    temp_path = f"temp_{uploaded_file.name}"
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # --- SPLIT LAYOUT (Left: Video, Right: Controls) ---
    col1, col2 = st.columns([1.5, 1], gap="large")

    with col1:
        st.subheader("📺 Original Video")
        st.video(temp_path)
        st.caption(f"Filename: `{uploaded_file.name}`")

    with col2:
        st.subheader("⚙️ Intelligence Panel")
        
        # Use Tabs for cleaner look
        tab_summary, tab_search = st.tabs(["📉 Auto-Summary", "🔍 Keyword Search"])

        # --- TAB 1: Auto Summary ---
        with tab_summary:
            st.info(" The AI will analyze audio patterns to keep the top **30% most important moments**.")
            
            if st.button(" Generate Summary", key="btn_summary"):
                with st.spinner(" Transcribing & Analyzing..."):
                    segments = backend.transcribe_video(temp_path)
                    highlights = backend.extract_highlights(segments, retention_ratio=0.30)
                    output_file, orig_len, summ_len = backend.generate_summary_video(temp_path, highlights)
                
                if output_file:
                    st.success(" Summary Ready!")
                    
                    # Metrics Row
                    m1, m2, m3 = st.columns(3)
                    m1.metric("Original", f"{orig_len:.0f}s")
                    m2.metric("Summary", f"{summ_len:.0f}s")
                    m3.metric("Compressed", f"{int((1 - summ_len/orig_len)*100)}%")
                    
                    st.video(output_file)
                    database.add_video_record(uploaded_file.name, orig_len, summ_len)
                else:
                    st.error(" Failed to process video.")

        # --- TAB 2: Keyword Search ---
        with tab_search:
            st.info(" Find every exact moment a specific word is spoken.")
            search_term = st.text_input("Enter Keyword:", placeholder="e.g. 'project', 'error', 'python'")
            
            if st.button(" Find & Clip", key="btn_search"):
                if not search_term:
                    st.warning(" Please enter a keyword first.")
                else:
                    with st.spinner(f" Scanning for '{search_term}'..."):
                        segments = backend.transcribe_video(temp_path)
                        highlights = backend.extract_keyword_highlights(segments, search_term)
                        
                        if highlights:
                            st.success(f" Found {len(highlights)} mentions!")
                            output_file, orig_len, summ_len = backend.generate_summary_video(temp_path, highlights)
                            st.video(output_file)
                            database.add_video_record(f"Search: {search_term}", orig_len, summ_len)
                        else:
                            st.error(f" No mentions of '{search_term}' found.")

else:
    # Placeholder when no file is uploaded
    st.info("Please upload a video file to begin analysis.")
    
    # Optional: Add an 'About' section at the bottom
    with st.expander("How does this work?"):
        st.markdown("""
        1. **Audio Extraction:** We use **FFmpeg** to strip audio from your video.
        2. **Transcription:** **OpenAI Whisper** converts speech to text with timestamps.
        3. **NLP Analysis:** We rank sentences by importance (Summary Mode) or match keywords (Search Mode).
        4. **Video Stitching:** **MoviePy** cuts the original video at those exact timestamps and merges them.

        """)


