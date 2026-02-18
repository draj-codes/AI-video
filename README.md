🎥 AI-Powered Video Summarizer
Project Description
In an era of information overload, watching hour-long lectures or meetings is inefficient. This project is a Python-based application that automatically generates concise video summaries. Unlike traditional editors that cut based on silence or volume, this tool uses Speech-to-Text (ASR) and Natural Language Processing (NLP) to understand the meaning of the content and retain only the most important segments.

🚀 Key Features

Speech-Aware Editing: Uses OpenAI Whisper to transcribe audio with high accuracy.

Contextual Importance: Uses NLP (Spacy/Transformers) to rank sentences by significance.

Automatic Rendering: Instantly cuts and stitches the video using MoviePy.

No Training Required: Works out-of-the-box on any English video content.

🛠️ Tech Stack

Language: Python 3.9+

AI Models: OpenAI Whisper (Base), Spacy (NLP)

Video Processing: MoviePy, FFmpeg

Frontend: Streamlit
