@echo off
echo Starting OpenClaw subtitle extraction...

REM Extract English subtitles for all chapters

echo Extracting Chapter 1 subtitles...
"C:\Program Files\FFmpeg\bin\ffmpeg.exe" -i 8kNv3rjQaVA.en.vtt -ss 00:00:00 -to 00:04:15 -c copy youtube-clips/openclaw_tutorial_01_en.vtt

echo Extracting Chapter 2 subtitles...
"C:\Program Files\FFmpeg\bin\ffmpeg.exe" -i 8kNv3rjQaVA.en.vtt -ss 00:04:15 -to 00:06:30 -c copy youtube-clips/openclaw_tutorial_02_en.vtt

echo Extracting Chapter 3 subtitles...
"C:\Program Files\FFmpeg\bin\ffmpeg.exe" -i 8kNv3rjQaVA.en.vtt -ss 00:06:30 -to 00:08:30 -c copy youtube-clips/openclaw_tutorial_03_en.vtt

echo Extracting Chapter 4 subtitles...
"C:\Program Files\FFmpeg\bin\ffmpeg.exe" -i 8kNv3rjQaVA.en.vtt -ss 00:08:30 -to 00:11:00 -c copy youtube-clips/openclaw_tutorial_04_en.vtt

echo Extracting Chapter 5 subtitles...
"C:\Program Files\FFmpeg\bin\ffmpeg.exe" -i 8kNv3rjQaVA.en.vtt -ss 00:11:00 -to 00:13:30 -c copy youtube-clips/openclaw_tutorial_05_en.vtt

echo Extracting Chapter 6 subtitles...
"C:\Program Files\FFmpeg\bin\ffmpeg.exe" -i 8kNv3rjQaVA.en.vtt -ss 00:13:30 -to 00:15:30 -c copy youtube-clips/openclaw_tutorial_06_en.vtt

echo Extracting Chapter 7 subtitles...
"C:\Program Files\FFmpeg\bin\ffmpeg.exe" -i 8kNv3rjQaVA.en.vtt -ss 00:15:30 -to 00:17:30 -c copy youtube-clips/openclaw_tutorial_07_en.vtt

echo Extracting Chapter 8 subtitles...
"C:\Program Files\FFmpeg\bin\ffmpeg.exe" -i 8kNv3rjQaVA.en.vtt -ss 00:17:30 -to 00:19:30 -c copy youtube-clips/openclaw_tutorial_08_en.vtt

echo Extracting Chapter 9 subtitles...
"C:\Program Files\FFmpeg\bin\ffmpeg.exe" -i 8kNv3rjQaVA.en.vtt -ss 00:19:30 -to 00:21:05 -c copy youtube-clips/openclaw_tutorial_09_en.vtt

echo Extracting Chapter 10 subtitles...
"C:\Program Files\FFmpeg\bin\ffmpeg.exe" -i 8kNv3rjQaVA.en.vtt -ss 00:21:05 -to 00:24:00 -c copy youtube-clips/openclaw_tutorial_10_en.vtt

echo Extracting Chapter 11 subtitles...
"C:\Program Files\FFmpeg\bin\ffmpeg.exe" -i 8kNv3rjQaVA.en.vtt -ss 00:24:00 -to 00:28:00 -c copy youtube-clips/openclaw_tutorial_11_en.vtt

echo Extracting Chapter 12 subtitles...
"C:\Program Files\FFmpeg\bin\ffmpeg.exe" -i 8kNv3rjQaVA.en.vtt -ss 00:28:00 -to 00:33:44 -c copy youtube-clips/openclaw_tutorial_12_en.vtt

echo All subtitles extracted!
echo Next steps:
echo 1. Translate .vtt files to Chinese using DeepL or other translation service
echo 2. Merge bilingual subtitles to videos
echo 3. Check final quality

pause