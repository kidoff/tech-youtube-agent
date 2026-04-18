import os
import requests
import asyncio
from google import genai
import edge_tts
from moviepy import VideoFileClip, AudioFileClip, vfx

# 1. Setup API Keys
GEMINI_KEY = os.environ.get("GEMINI_API_KEY")
PIXABAY_KEY = os.environ.get("PIXABAY_API_KEY")

# 2. Generate Script with Gemini 3 Flash (The 2026 Standard)
def generate_script():
    print("Generating Script with Gemini 3 Flash...")
    client = genai.Client(api_key=GEMINI_KEY)
    prompt = "Write a snappy, 45-second YouTube Short script about a tech tip. No intro. Viral style."
    
    response = client.models.generate_content(
        model='gemini-3-flash', 
        contents=prompt
    )
    return response.text

# 3. Create Voice using Edge-TTS
async def create_voice(text):
    print("Generating Voice...")
    communicate = edge_tts.Communicate(text, "en-US-ChristopherNeural")
    await communicate.save("voiceover.mp3")

# 4. Download Video from Pixabay
def get_video():
    print("Downloading Video...")
    url = f"https://pixabay.com/api/videos/?key={PIXABAY_KEY}&q=technology&per_page=3"
    response = requests.get(url).json()
    video_url = response['hits'][0]['videos']['medium']['url']
    with open("background.mp4", "wb") as f:
        f.write(requests.get(video_url).content)

# 5. Merge (Modern MoviePy Syntax)
def make_final_video():
    print("Editing Video...")
    video = VideoFileClip("background.mp4")
    audio = AudioFileClip("voiceover.mp3")
    
    # Modern looping for 2026 MoviePy
    final_video = video.with_effects([vfx.Loop(duration=audio.duration)])
    final_video = final_video.with_audio(audio)
    
    final_video.write_videofile("final_short.mp4", fps=24)
    print("Video Complete!")

if __name__ == "__main__":
    script = generate_script()
    asyncio.run(create_voice(script))
    get_video()
    make_final_video()
