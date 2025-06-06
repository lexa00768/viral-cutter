# Termux AI Clip Extractor 🎙️

Новая версия скрипта с использованием Whisper (ИИ от OpenAI):

## Что делает:
1. Скачивает YouTube-видео
2. Распознаёт речь с помощью Whisper
3. Ищет вирусные фразы (например: "офигеть", "смех", "реакция")
4. Нарезает клипы с этими моментами в вертикальном формате

## Установка

```bash
git clone https://github.com/lexa00768/viral-cutter.git
cd viral-cutter
bash setup_termux_ai.sh
python termux_ai_clips.py
```

## Где сохраняются клипы
В папке `ai_clips/`
