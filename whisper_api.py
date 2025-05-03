import whisper
from moviepy.editor import VideoFileClip

def extract_audio(input_video_path, output_audio_path):
    # Load the video clip
    video_clip = VideoFileClip(input_video_path)

    # Extract audio from the video clip
    audio_clip = video_clip.audio

    # Save the audio clip to a new file
    audio_clip.write_audiofile(output_audio_path)

    # Close the video and audio clips
    video_clip.close()
    audio_clip.close()

def getCaption(audio):
    ends = []
    caption = []
    model = whisper.load_model("base")
    result = model.transcribe(audio, word_timestamps=True, fp16=False)
    for res in result["segments"]:
        for cap in res["words"]:
            ends.append(cap["end"]*1000)
            caption.append(cap["word"])
    return caption, ends
