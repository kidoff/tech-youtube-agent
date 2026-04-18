import os
import requests
import google.generativeai as genai
import edge_tts
import asyncio
from moviepy.editor import VideoFileClip, AudioFileClip

# 1. Setup API Keys securely from GitHub Secrets
GEMINI_KEY = os.environ.get("GEMINI_API_KEY")
PIXABAY_KEY = os.environ.get("PIXABAY_API_KEY")
genai.configure(api_key=GEMINI_KEY)

# 2. Generate the Script using Gemini
def generate_script():
    print("Generating Script...")
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = "Write a fast-paced, 45-second YouTube Short script about a hidden smartphone trick. No intro, just the script. Make it highly engaging."
    response = model.generate_content(prompt)
    return response.text

# 3. Create Voice using Edge-TTS
async def create_voice(text):
    print("Generating Voice...")
    voice = "en-US-ChristopherNeural" # Deep, professional male voice
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save("voiceover.mp3")

# 4. Download Background Video from Pixabay
def get_video():
    print("Downloading Video...")
    url = f"https://pixabay.com/api/videos/?key={PIXABAY_KEY}&q=smartphone+technology&per_page=3"
    response = requests.get(url).json()
    video_url = response['hits'][0]['videos']['medium']['url']
    
    vid_data = requests.get(video_url).content
    with open("background.mp4", "wb") as f:
        f.write(vid_data)

# 5. Merge Audio and Video
def make_final_video():
    print("Editing Video...")
    video = VideoFileClip("background.mp4")
    audio = AudioFileClip("voiceover.mp3")
    
    # Loop video to match audio length
    final_video = video.set_audio(audio).subclip(0, audio.duration)
    final_video.write_videofile("final_youtube_short.mp4", fps=24)
    print("Video Complete!")

# Run the Bot
if __name__ == "__main__":
    script = generate_script()
    asyncio.run(create_voice(script))
    get_video()
    make_final_video()
    
    # NOTE: To upload automatically, you will connect your YouTube channel cookies here later!
