import os
import subprocess
import whisper

def download_video(url, output="video.mp4"):
    subprocess.run(["yt-dlp", "-f", "mp4", "-o", output, url])
    return output

def extract_audio(video_path, audio_path="audio.wav"):
    subprocess.run(["ffmpeg", "-y", "-i", video_path, "-vn", "-acodec", "pcm_s16le", "-ar", "16000", audio_path])
    return audio_path

def transcribe(audio_path):
    model = whisper.load_model("base")
    result = model.transcribe(audio_path)
    return result

def select_highlights(transcription, keywords, top_n=10):
    clips = []
    for segment in transcription['segments']:
        text = segment['text'].lower()
        if any(keyword.lower() in text for keyword in keywords):
            clips.append((segment['start'], segment['end'], segment['text']))
    clips = sorted(clips, key=lambda x: x[1] - x[0], reverse=True)
    return clips[:top_n]

def crop_vertical(input_file, start, end, output_file):
    cmd = [
        "ffmpeg", "-y",
        "-i", input_file,
        "-ss", str(start),
        "-to", str(end),
        "-filter:v", "crop=ih*9/16:ih:(iw-(ih*9/16))/2:0",
        "-c:a", "copy",
        output_file
    ]
    subprocess.run(cmd)

def process_video(url):
    print("[1] Скачиваем видео...")
    video_path = download_video(url)

    print("[2] Извлекаем аудио...")
    audio_path = extract_audio(video_path)

    print("[3] Распознаём речь (Whisper)...")
    transcription = transcribe(audio_path)

    keywords = ["смех", "ожидания", "мои мысли", "прикол", "вот это", "офигеть", "неожиданно", "реакция", "вирус", "шок"]
    print("[4] Ищем вирусные фразы...")
    highlights = select_highlights(transcription, keywords)

    os.makedirs("ai_clips", exist_ok=True)
    for i, (start, end, text) in enumerate(highlights, 1):
        out_file = f"ai_clips/clip_{i}.mp4"
        print(f"[5] Клип {i}: {start:.1f}-{end:.1f} — {text[:40]}...")
        crop_vertical(video_path, start, end, out_file)

    print("Готово! Клип в папке ai_clips/")

if __name__ == "__main__":
    url = input("Вставь ссылку на YouTube: ").strip()
    process_video(url)
