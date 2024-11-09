from pydub import AudioSegment

def mp4_to_mp3(mp4_file_path, mp3_file_path):
    # Load the MP4 file
    audio = AudioSegment.from_file(mp4_file_path, format="mp4")
    
    # Export as MP3
    audio.export(mp3_file_path, format="mp3")
    print(f"Converted {mp4_file_path} to {mp3_file_path}")

# Example usage
mp4_to_mp3("ghost_sound.mp4", "ghost_sound.mp3")
