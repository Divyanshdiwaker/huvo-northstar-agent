import os
import tempfile
import pyttsx3

os.environ["HF_HUB_DISABLE_SYMLINKS"] = "1"

from faster_whisper import WhisperModel


MODEL_SIZE = os.getenv("WHISPER_MODEL_SIZE", "small")

# Load the model once when the app starts
model = WhisperModel(
    MODEL_SIZE,
    device="cpu",
    compute_type="int8"
)


def speech_to_text(audio_file):
    audio_path = None

    try:
        audio_file.seek(0)
        audio_bytes = audio_file.read()

        if not audio_bytes or len(audio_bytes) < 2000:
            return "", "Recording seems too short or empty. Please try again."

        
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
            tmp_file.write(audio_bytes)
            audio_path = tmp_file.name

        # Transcribe
        segments, info = model.transcribe(
            audio_path,
            language=None,  
            task="transcribe",
            beam_size=10,
            temperature=0,
            vad_filter=True,
            vad_parameters={
                "min_silence_duration_ms": 300
            },
            no_speech_threshold=0.8,
            log_prob_threshold=-1.0,
            compression_ratio_threshold=2.0,
            hallucination_silence_threshold=1.0,
            condition_on_previous_text=False,
            initial_prompt=(
                "Northstar Homes real estate conversation. "
                "The customer is discussing apartments, flats, "
                "1 BHK, 2 BHK, 3 BHK, budget, crore, lakh, "
                "Gurugram, Sector 79, property, site visit, "
                "possession, investment and self use."
            )
        )

        # Convert segments into one string
        transcript = " ".join(
            segment.text.strip()
            for segment in segments
        ).strip()

        if not transcript:
            return "", "No speech detected."

        return transcript, None

    except Exception as error:
        return "", f"STT error: {error}"

    finally:
        if audio_path and os.path.exists(audio_path):
            os.remove(audio_path)

def text_to_speech(text):
    

    try:
        engine = pyttsx3.init()

        engine.setProperty(
            "rate",
            170
        )

        engine.say(text)
        engine.runAndWait()

        return True

    except Exception as error:

        print(f"TTS error: {error}")

        return False