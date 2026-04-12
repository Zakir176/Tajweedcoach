from faster_whisper import WhisperModel
import os

# Initialize the model globally to load it once
# Using 'base' model for a balance between speed and accuracy
# Quantization set to int8 for CPU efficiency
model = WhisperModel("base", device="cpu", compute_type="int8")

async def transcribe(file_path: str) -> str:
    """
    Transcribes an Arabic audio file using faster-whisper.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Audio file not found: {file_path}")

    segments, info = model.transcribe(
        file_path,
        language="ar", # Explicitly set to Arabic
        beam_size=5
    )
    
    text = " ".join([segment.text for segment in segments])
    return text.strip()
