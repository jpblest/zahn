import os
from datetime import datetime
import soundfile as sf

def save_audio_file(audio_data, file_format="wav"):
    """
    Save audio data to a file using soundfile.

    Args:
        audio_data (bytes): The audio data to save.
        file_format (str): The format of the audio file (e.g., "wav").

    Returns:
        str: The filename of the saved audio file.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"recorded_audio_{timestamp}.{file_format}"
    filepath = os.path.join("app/static/recordings", filename)

    # Ensure the directory exists
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    # Save the audio data using soundfile
    audio_data, samplerate = sf.read(io.BytesIO(audio_data))
    sf.write(filepath, audio_data, samplerate)

    return filename

