import os
import sys
import tempfile
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware


project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from model import analyze_image


app = FastAPI(title="Mood-Based Music Recommender")

app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*']
)

MOOD_SONGS = {
    "happy": ["Happy Song 1", "Happy Song 2"],
    "sad": ["Sad Song 1", "Sad Song 2"],
    "angry": ["Angry Song 1", "Angry Song 2"],
    "surprise": ["Surprise Song 1"],
    "neutral": ["Neutral Song 1", "Neutral Song 2"]
}

@app.post("/detect-mood")
async def detect_mood(file: UploadFile = File(...)):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp:
            tmp.write(await file.read())
            image_path = tmp.name
    except Exception as e:
        return {"error": f"Failed to save uploaded image: {e}"}
    
    mood, full_result, saved_path = analyze_image(image_path, save_json=True)
    
    song = MOOD_SONGS.get(mood.lower(), [])

    return{
        "mood": mood,
        "songs": song,
        "full_result": full_result
    }