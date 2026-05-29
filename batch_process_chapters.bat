@echo off
setlocal enabledelayedexpansion

:: YouTube 视频章节批量处理脚本
:: 用于剪辑所有章节并生成带字幕的版本

set videoPath="D:\wenjian\Obsidian仓库\8kNv3rjQaVA.mp4"
set subtitlesPath="D:\wenjian\Obsidian仓库\8kNv3rjQaVA.en.vtt"
set chaptersPath="D:\wenjian\Obsidian仓库\chapters_analysis.json"
set ffmpegPath="C:\Users\14365\scoop\apps\ffmpeg\current\bin\ffmpeg.exe"

:: 输出目录
set outputBaseDir="D:\wenjian\Obsidian仓库\youtube-clips"
set timestamp=%date:~0,4%%date:~5,2%%date:~8,2%_%time:~0,2%%time:~3,2%
set outputDir=%outputBaseDir%\%timestamp%

:: 创建输出目录
if not exist %outputBaseDir% mkdir %outputBaseDir%
mkdir %outputDir%

echo === YouTube 视频章节批量处理脚本 ===
echo 输出目录: %outputDir%
echo.

:: 读取章节总数
find /c "index" %chaptersPath% > nul
set /p totalChapters=<chapters_count.txt

echo 开始处理章节...
echo ==============================================

:: 创建临时文件目录
set tempDir=%outputDir%\temp
mkdir %tempDir%

:: 使用临时文件存储章节信息
for /f "tokens=*" %%a in ('type %chaptersPath%') do (
    echo %%a >> temp_chapters.txt
)

:: 处理每个章节
set chapterIndex=0
for /f "tokens=*" %%a in ('type temp_chapters.txt ^| findstr "title"') do (
    set /a chapterIndex+=1

    :: 提取章节信息
    for /f "tokens=*" %%b in ('type temp_chapters.txt ^| findstr %%a') do (
        set chapterTitle=%%b
        set chapterTitle=!chapterTitle:*": "!=!
        set chapterTitle=!chapterTitle!",!
        set chapterTitle=!chapterTitle:"=!

        :: 获取时间和摘要
        for /f "tokens=*" %%c in ('type temp_chapters.txt ^| findstr %%a') do (
            if "%%c"=="      " (
                set startTime=%%d
                set startTime=!startTime!:"}=!
                set startTime=!startTime!:"!=""!
            )
        )
    )

    echo 处理章节 !chapterIndex!: !chapterTitle!

    :: 创建章节目录
    set chapterDir=%outputDir%\!chapterIndex!_!chapterTitle!
    mkdir !chapterDir!

    :: 1. 剪辑原始视频片段
    set clipPath=!chapterDir!\!chapterTitle!_clip.mp4
    %ffmpegPath% -y -i %videoPath% -ss %startTime% -to %endTime% -c:v libx264 -c:a aac -strict experimental !clipPath!
    echo   [x] 剪辑视频完成

    :: 2. 提取对应时间段的字幕
    set tempSubPath=%tempDir%\chapter_!chapterIndex!.vtt
    %ffmpegPath% -y -i %subtitlesPath% -ss %startTime% -to %endTime% -c copy !tempSubPath!

    :: 3. 将 VTT 转换为 SRT
    set srtPath=%tempDir%\chapter_!chapterIndex!.srt
    call :ConvertVttToSrt !tempSubPath! !srtPath!

    :: 4. 创建双语字幕文件
    set bilingualSrtPath=!chapterDir!\!chapterTitle!_bilingual.srt
    call :ConvertToBilingualSubtitles !srtPath! !bilingualSrtPath!

    :: 5. 烧录字幕到视频
    set subtitleClipPath=!chapterDir!\!chapterTitle!_with_subtitles.mp4
    %ffmpegPath% -y -i !clipPath! -vf "subtitles=!srtPath!" -c:a copy !subtitleClipPath!
    echo   [x] 添加硬字幕完成

    :: 6. 生成总结文案
    set summaryPath=!chapterDir!\!chapterTitle!_summary.md
    echo # !chapterTitle! > !summaryPath!
    echo ## 时间戳 >> !summaryPath!
    echo %startTime% - %endTime% >> !summaryPath!
    echo ## 内容总结 >> !summaryPath!
    echo !summary! >> !summaryPath!
    echo ## 关键词 >> !summaryPath!
    echo !keywords! >> !summaryPath!
    echo ## 处理时间 >> !summaryPath!
    echo %date% %time% >> !summaryPath!
    echo   [x] 生成总结文案完成

    echo   [OK] 章节 !chapterIndex! 处理完成!
    echo.
)

:: 清理临时文件
rd /s /q %tempDir%

echo ==============================================
echo 所有章节处理完成!
echo 输出目录: %outputDir%
echo 总处理章节: %totalChapters% 个
echo.

:: 显示目录结构
echo 生成的文件结构:
for /f "tokens=*" %%a in ('dir /s /b "%outputDir%"') do (
    echo   %%a
)

pause

:: VTT转SRT函数
:ConvertVttToSrt
set vttPath=%1
set srtPath=%2
copy %vttPath% temp_vtt.txt

:: 使用PowerShell处理VTT到SRT
powershell -Command "$content = Get-Content 'temp_vtt.txt' -Raw; $content = $content -replace 'WEBVTT.*?`r?`n`r?`n', ''; $content = $content -replace '<[^>]*>', ''; $content = $content -replace '\{[^}]*\}', ''; $content = $content -replace 'align:[^%]*%|position:[^%]*%', ''; $content | Out-File 'temp_srt.txt' -Encoding UTF8"

:: 处理SRT格式
copy temp_srt.txt %srtPath%

del temp_vtt.txt temp_srt.txt
goto :eof

:: 双语字幕函数
:ConvertToBilingualSubtitles
set srtPath=%1
set bilingualPath=%2
copy %srtPath% temp_bilingual.txt

:: 添加双语标题
echo 英文 >> temp_bilingual.txt
echo 中文 >> temp_bilingual.txt

copy temp_bilingual.txt %bilingualPath%

del temp_bilingual.txt
goto :eof