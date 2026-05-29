@echo off
setlocal enabledelayedexpansion

:: YouTube 视频章节批量处理脚本
:: 用于剪辑所有章节并生成带字幕的版本

set videoPath=D:\wenjian\Obsidian仓库\8kNv3rjQaVA.mp4
set subtitlesPath=D:\wenjian\Obsidian仓库\8kNv3rjQaVA.en.vtt
set chaptersPath=D:\wenjian\Obsidian仓库\chapters_analysis.json

:: 输出目录
set outputBaseDir=D:\wenjian\Obsidian仓库\youtube-clips
for /f "tokens=1-3 delims=/ " %%a in ('date /t') do set today=%%c%%a%%b
for /f "tokens=1-2 delims=: " %%a in ('time /t') do set now=%%a%%b
set timestamp=%today%_%now%
set outputDir=%outputBaseDir%\%timestamp%

:: 创建输出目录
if not exist %outputBaseDir% mkdir %outputBaseDir%
mkdir %outputDir%

echo ========================================
echo === YouTube 视频章节批量处理脚本 ===
echo ========================================
echo.
echo 输出目录: %outputDir%
echo.

:: 读取章节分析文件并处理
for /f "tokens=2 delims=:," %%a in ('findstr "title" %chaptersPath%') do (
    set title=%%a
    set title=!title": "=!
    set title=!title!"!
    set title=!title:,=!

    for /f "tokens=2 delims=:," %%b in ('findstr "start_time" %chaptersPath%') do (
        set startTime=%%b
        set startTime=!startTime": "=!
        set startTime=!startTime!"!
    )

    for /f "tokens=2 delims=:," %%c in ('findstr "end_time" %chaptersPath%') do (
        set endTime=%%c
        set endTime=!endTime": "=!
        set endTime=!endTime!"!
    )

    for /f "tokens=2 delims=:" %%d in ('findstr "summary" %chaptersPath%') do (
        set summary=%%d
        set summary=!summary!"!
    )

    for /f "tokens=2 delims=:]" %%e in ('findstr "index" %chaptersPath%') do (
        set index=%%e
        set index=!index",=!
    )

    echo 正在处理章节 !index!: !title!

    :: 创建章节目录
    set chapterDir=%outputDir%\!index!_!title!
    mkdir !chapterDir!

    :: 1. 剪辑原始视频片段
    set clipPath=!chapterDir!\!title!_clip.mp4
    ffmpeg -y -i "%videoPath%" -ss %startTime% -to %endTime% -c:v libx264 -c:a aac -strict experimental "%clipPath%"
    echo   [完成] 剪辑视频

    :: 2. 提取对应时间段的字幕
    set subPath=!chapterDir!\!title!_sub.vtt
    ffmpeg -y -i "%subtitlesPath%" -ss %startTime% -to %endTime% -c copy "%subPath%"

    :: 3. VTT转SRT
    set srtPath=!chapterDir!\!title!.srt
    powershell -Command "$content = Get-Content '%subPath%' -Raw; $content = $content -replace 'WEBVTT.*?`r?`n`r?`n', ''; $content = $content -replace '<[^>]*>', ''; $content = $content -replace '\{[^}]*\}', ''; $lines = $content -split '`r?`n'; $out = ''; $num = 1; foreach ($line in $lines) { $line = $line.Trim(); if ($line -match '(\d{2}:\d{2}:\d{2}\.\d{3}) --> (\d{2}:\d{2}:\d{2}\.\d{3})') { $out += $num + '`r`n' + $matches[1].Replace('.',',') + ' --> ' + $matches[2].Replace('.',',') + '`r`n'; $num++ } elseif ($line -ne '') { $out += $line + ' ' } else { if ($out -notmatch '`r?`n`r?`n$') { $out += '`r`n`r`n' } } }; $out | Out-File '%srtPath%' -Encoding UTF8"
    echo   [完成] 字幕转换

    :: 4. 创建双语字幕文件
    set bilingualPath=!chapterDir!\!title!_bilingual.srt
    copy "%srtPath%" "%bilingualPath%"
    echo   [完成] 创建双语字幕

    :: 5. 烧录字幕到视频
    set subtitleClipPath=!chapterDir!\!title!_with_subtitles.mp4
    ffmpeg -y -i "%clipPath%" -vf "subtitles='%srtPath'" -c:a copy "%subtitleClipPath%"
    echo   [完成] 添加硬字幕

    :: 6. 生成总结文案
    set summaryPath=!chapterDir!\!title!_summary.md
    # !title! > "%summaryPath%"
    echo ## 时间戳 >> "%summaryPath%"
    echo %startTime% - %endTime% >> "%summaryPath%"
    echo ## 内容总结 >> "%summaryPath%"
    echo !summary! >> "%summaryPath%"
    echo ## 处理时间 >> "%summaryPath%"
    echo %date% %time% >> "%summaryPath%"
    echo   [完成] 生成总结

    echo   [成功] 章节 !index! 处理完成!
    echo.
)

echo ========================================
echo 所有章节处理完成!
echo 输出目录: %outputDir%
echo ========================================

pause