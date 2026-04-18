import os
import requests
import asyncio
import google.generativeai as genai
import edge_tts
from moviepy.editor import VideoFileClip, AudioFileClip, vfx
from playwright.sync_api import sync_playwright

# 1. Setup API Keys from GitHub Secrets
GEMINI_KEY = os.environ.get("GEMINI_API_KEY")
PIXABAY_KEY = os.environ.get("PIXABAY_API_KEY")
YOUTUBE_COOKIES = os.environ.get("YOUTUBE_COOKIES") # We will use this later for uploading

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

# 5. Merge Audio and Video (CRASH FIX APPLIED HERE)
def make_final_video():
    print("Editing Video...")
    video = VideoFileClip("background.mp4")
    audio = AudioFileClip("voiceover.mp3")
    
    # FIX: Loop the short Pixabay video so it lasts as long as the Gemini voiceover
    looped_video = video.fx(vfx.loop, duration=audio.duration)
    
    final_video = looped_video.set_audio(audio)
    final_video.write_videofile("final_youtube_short.mp4", fps=24, codec="libx264", audio_codec="aac")
    print("Video Complete!")

# 6. Upload to YouTube (Skeleton setup for cookies)
def upload_to_youtube():
    print("Uploading to YouTube...")
    if not YOUTUBE_COOKIES:
        print("Skipping upload: No cookies found. Video saved as final_youtube_short.mp4")
        return

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        
        # This is where your cookies let the bot log in automatically
        # Note: We will format your cookies properly once you generate them!
        
        page = context.new_page()
        page.goto("https://studio.youtube.com")
        print("Successfully opened YouTube Studio!")
        
        # The exact click instructions go here once cookies are linked.
        browser.close()

# Run the Bot
if __name__ == "__main__":
    script = generate_script()
    asyncio.run(create_voice(script))
    get_video()
    make_final_video()
    upload_to_youtube()
