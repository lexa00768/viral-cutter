import os
import subprocess
from scenedetect import VideoManager, SceneManager
from scenedetect.detectors import ContentDetector

def download_video(url, output="video.mp4"):
    subprocess.run(["yt-dlp", "-f", "mp4", "-o", output, url])
    return output

def detect_scenes(video_path):
    video_manager = VideoManager([video_path])
    scene_manager = SceneManager()
    scene_manager.add_detector(ContentDetector(threshold=30.0))
    video_manager.set_downscale_factor()
    video_manager.start()
    scene_manager.detect_scenes(frame_source=video_manager)
    scenes = scene_manager.get_scene_list()
    return [(start.get_seconds(), end.get_seconds()) for start, end in scenes]

def select_top_scenes(scenes, top_n=10):
    scenes = sorted(scenes, key=lambda x: x[1] - x[0], reverse=True)
    return scenes[:top_n]

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

    print("[2] Ищем сцены...")
    scenes = detect_scenes(video_path)

    print("[3] Выбираем топ-10 сцен...")
    top_scenes = select_top_scenes(scenes)

    os.makedirs("clips", exist_ok=True)
    for i, (start, end) in enumerate(top_scenes, 1):
        out_file = f"clips/clip_{i}.mp4"
        print(f"[4] Нарезаем клип {i}: {start:.2f} - {end:.2f} сек")
        crop_vertical(video_path, start, end, out_file)

    print("Готово! Клипы в папке clips/")

if __name__ == "__main__":
    url = input("Вставь ссылку на YouTube: ").strip()
    process_video(url)
