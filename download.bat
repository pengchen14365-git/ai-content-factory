@echo off
chcp 65001 >nul
setlocal

set VIDEO_URL=https://www.youtube.com/watch?v=Le0DLrn7ta0
set OUTPUT_DIR=youtube-clips\temp
set YTDL_PATH=C:\Users\14365\scoop\apps\yt-dlp\current\yt-dlp.exe

echo 🎬 开始下载视频...
echo    URL: %VIDEO_URL%
echo    输出目录: %OUTPUT_DIR%

if not exist "%OUTPUT_DIR%" mkdir "%OUTPUT_DIR%"

"%YTDL_PATH%" -f "bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080][ext=mp4]/best" --write-subs --write-auto-subs --sub-lang en --sub-format vtt -o "%OUTPUT_DIR%\%%(id)s.%%(ext)s" %VIDEO_URL%

echo.
echo ✅ 下载完成！
echo.
echo 📁 下载的文件:
dir /b "%OUTPUT_DIR%"

endlocal
