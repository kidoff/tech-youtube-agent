import os
import requests
import asyncio
from google import genai
import edge_tts
from moviepy.editor import VideoFileClip, AudioFileClip, vfx
from playwright.sync_api import sync_playwright

# 1. Setup API Keys
GEMINI_KEY = os.environ.get("GEMINI_API_KEY")
PIXABAY_KEY = os.environ.get("PIXABAY_API_KEY")
YOUTUBE_COOKIES = os.environ.get("YOUTUBE_COOKIES") 

# 2. Generate the Script using the NEW Gemini 2.0 Client
def generate_script():
    print("Generating Script...")
    client = genai.Client(api_key=GEMINI_KEY)
    prompt = "Write a fast-paced, 45-second YouTube Short script about a hidden smartphone trick. No intro, just the script. Make it highly engaging."
    
    response = client.models.generate_content(
        model='gemini-2.0-flash', 
        contents=prompt
    )
    return response.text

# 3. Create Voice using Edge-TTS
async def create_voice(text):
    print("Generating Voice...")
    voice = "en-US-ChristopherNeural" 
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
    
    # Loop the background video
    looped_video = video.fx(vfx.loop, duration=audio.duration)
    
    final_video = looped_video.set_audio(audio)
    final_video.write_videofile("final_youtube_short.mp4", fps=24, codec="libx264", audio_codec="aac")
    print("Video Complete!")

# 6. Upload to YouTube
def upload_to_youtube():
    print("Uploading to YouTube...")
    if not YOUTUBE_COOKIES:
        print("Skipping upload: No cookies found.")
        return
    print("Successfully simulated YouTube Studio login!")

if __name__ == "__main__":
    script = generate_script()
    asyncio.run(create_voice(script))
    get_video()
    make_final_video()
    upload_to_youtube()
