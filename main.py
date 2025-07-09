from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from generator import generate_music_clip
from uploader import upload_to_s3
import os

app = FastAPI()

# CORS setup (adjust for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, set your frontend domain here
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PromptRequest(BaseModel):
    name: str

@app.post("/generate-audio")
async def audio_generation_api(prompt_request: PromptRequest):
    try:
        prompt = prompt_request.name.strip()
        print(f"🎤 Received prompt: {prompt}")  # ✅ Print incoming prompt

        if not prompt:
            return {"success": False, "error": "Missing 'name' prompt"}

        # ✅ Generate the audio
        local_file, sample_rate = generate_music_clip(prompt)
        print(f"🎶 Generated file: {local_file} @ {sample_rate}Hz")

        # ✅ Upload to S3
        s3_key = f"generated_audio/{os.path.basename(local_file)}"
        s3_url = upload_to_s3(local_file, s3_key)
        print(f"☁️ Uploaded to S3: {s3_url}")

        return {
            "success": True,
            "message": "Audio generated successfully",
            "file_url": s3_url,
            "local_file": local_file,
            "sample_rate": sample_rate,
            "prompt": prompt
        }

    except Exception as e:
        print(f"❌ Exception occurred: {e}")
        return {"success": False, "error": str(e)}