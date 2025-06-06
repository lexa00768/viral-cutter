#!/data/data/com.termux/files/usr/bin/bash

pkg update -y && pkg upgrade -y
pkg install -y python ffmpeg git wget clang make pkg-config libffi-dev

pip install --upgrade pip
pip install --no-cache-dir yt-dlp
pip install --no-deps git+https://github.com/Breakthrough/PySceneDetect.git
