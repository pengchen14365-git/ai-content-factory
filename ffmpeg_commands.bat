@echo off
echo Starting OpenClaw video clipping...

REM Chapter 1: OpenClaw简介与个人CRM
echo Processing Chapter 1: OpenClaw简介与个人CRM
"C:\Program Files\FFmpeg\bin\ffmpeg.exe" -i 8kNv3rjQaVA.mp4 -ss 00:00:00 -to 00:04:15 -c copy youtube-clips/openclaw_tutorial_01.mp4
if %errorlevel% equ 0 (
    echo Chapter 1 video: SUCCESS
) else (
    echo Chapter 1 video: FAILED
)

REM Chapter 2: CRM系统深度解析
echo Processing Chapter 2: CRM系统深度解析
"C:\Program Files\FFmpeg\bin\ffmpeg.exe" -i 8kNv3rjQaVA.mp4 -ss 00:04:15 -to 00:06:30 -c copy youtube-clips/openclaw_tutorial_02.mp4
if %errorlevel% equ 0 (
    echo Chapter 2 video: SUCCESS
) else (
    echo Chapter 2 video: FAILED
)

REM Chapter 3: CRM会议集成
echo Processing Chapter 3: CRM会议集成
"C:\Program Files\FFmpeg\bin\ffmpeg.exe" -i 8kNv3rjQaVA.mp4 -ss 00:06:30 -to 00:08:30 -c copy youtube-clips/openclaw_tutorial_03.mp4
if %errorlevel% equ 0 (
    echo Chapter 3 video: SUCCESS
) else (
    echo Chapter 3 video: FAILED
)

REM Chapter 4: 个人知识库
echo Processing Chapter 4: 个人知识库
"C:\Program Files\FFmpeg\bin\ffmpeg.exe" -i 8kNv3rjQaVA.mp4 -ss 00:08:30 -to 00:11:00 -c copy youtube-clips/openclaw_tutorial_04.mp4
if %errorlevel% equ 0 (
    echo Chapter 4 video: SUCCESS
) else (
    echo Chapter 4 video: FAILED
)

REM Chapter 5: 知识库实战演示
echo Processing Chapter 5: 知识库实战演示
"C:\Program Files\FFmpeg\bin\ffmpeg.exe" -i 8kNv3rjQaVA.mp4 -ss 00:11:00 -to 00:13:30 -c copy youtube-clips/openclaw_tutorial_05.mp4
if %errorlevel% equ 0 (
    echo Chapter 5 video: SUCCESS
) else (
    echo Chapter 5 video: FAILED
)

REM Chapter 6: 商业顾问委员会
echo Processing Chapter 6: 商业顾问委员会
"C:\Program Files\FFmpeg\bin\ffmpeg.exe" -i 8kNv3rjQaVA.mp4 -ss 00:13:30 -to 00:15:30 -c copy youtube-clips/openclaw_tutorial_06.mp4
if %errorlevel% equ 0 (
    echo Chapter 6 video: SUCCESS
) else (
    echo Chapter 6 video: FAILED
)

REM Chapter 7: 安全委员会
echo Processing Chapter 7: 安全委员会
"C:\Program Files\FFmpeg\bin\ffmpeg.exe" -i 8kNv3rjQaVA.mp4 -ss 00:15:30 -to 00:17:30 -c copy youtube-clips/openclaw_tutorial_07.mp4
if %errorlevel% equ 0 (
    echo Chapter 7 video: SUCCESS
) else (
    echo Chapter 7 video: FAILED
)

REM Chapter 8: 社交媒体追踪器
echo Processing Chapter 8: 社交媒体追踪器
"C:\Program Files\FFmpeg\bin\ffmpeg.exe" -i 8kNv3rjQaVA.mp4 -ss 00:17:30 -to 00:19:30 -c copy youtube-clips/openclaw_tutorial_08.mp4
if %errorlevel% equ 0 (
    echo Chapter 8 video: SUCCESS
) else (
    echo Chapter 8 video: FAILED
)

REM Chapter 9: 视频创意流水线
echo Processing Chapter 9: 视频创意流水线
"C:\Program Files\FFmpeg\bin\ffmpeg.exe" -i 8kNv3rjQaVA.mp4 -ss 00:19:30 -to 00:21:05 -c copy youtube-clips/openclaw_tutorial_09.mp4
if %errorlevel% equ 0 (
    echo Chapter 9 video: SUCCESS
) else (
    echo Chapter 9 video: FAILED
)

REM Chapter 10: 每日简报与定时任务
echo Processing Chapter 10: 每日简报与定时任务
"C:\Program Files\FFmpeg\bin\ffmpeg.exe" -i 8kNv3rjQaVA.mp4 -ss 00:21:05 -to 00:24:00 -c copy youtube-clips/openclaw_tutorial_10.mp4
if %errorlevel% equ 0 (
    echo Chapter 10 video: SUCCESS
) else (
    echo Chapter 10 video: FAILED
)

REM Chapter 11: 安全防护与备份系统
echo Processing Chapter 11: 安全防护与备份系统
"C:\Program Files\FFmpeg\bin\ffmpeg.exe" -i 8kNv3rjQaVA.mp4 -ss 00:24:00 -to 00:28:00 -c copy youtube-clips/openclaw_tutorial_11.mp4
if %errorlevel% equ 0 (
    echo Chapter 11 video: SUCCESS
) else (
    echo Chapter 11 video: FAILED
)

REM Chapter 12: 其他实用工具
echo Processing Chapter 12: 其他实用工具
"C:\Program Files\FFmpeg\bin\ffmpeg.exe" -i 8kNv3rjQaVA.mp4 -ss 00:28:00 -to 00:33:44 -c copy youtube-clips/openclaw_tutorial_12.mp4
if %errorlevel% equ 0 (
    echo Chapter 12 video: SUCCESS
) else (
    echo Chapter 12 video: FAILED
)

echo All chapters processed!
pause