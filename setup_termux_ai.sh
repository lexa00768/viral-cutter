#!/data/data/com.termux/files/usr/bin/bash

pkg update -y && pkg upgrade -y
pkg install -y python ffmpeg git wget clang make pkg-config libffi

pip install --upgrade pip setuptools wheel
pip install yt-dlp
pip install torch torchvision torchaudio -f https://download.pytorch.org/whl/cpu/torch_stable.html
pip install git+https://github.com/openai/whisper.git
