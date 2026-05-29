# YouTube 视频章节批量处理脚本
# 用于剪辑所有章节并生成带字幕的版本

# 配置变量
$videoPath = "D:\wenjian\Obsidian仓库\8kNv3rjQaVA.mp4"
$subtitlesPath = "D:\wenjian\Obsidian仓库\8kNv3rjQaVA.en.vtt"
$chaptersPath = "D:\wenjian\Obsidian仓库\chapters_analysis.json"
$ffmpegPath = "C:\Users\14365\scoop\apps\ffmpeg\current\bin\ffmpeg.exe"

# 输出目录
$outputBaseDir = "D:\wenjian\Obsidian仓库\youtube-clips"
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$outputDir = Join-Path $outputBaseDir $timestamp

# 创建输出目录
if (-not (Test-Path $outputBaseDir)) {
    New-Item -ItemType Directory -Path $outputBaseDir -Force | Out-Null
}
New-Item -ItemType Directory -Path $outputDir -Force | Out-Null

Write-Host "=== YouTube 视频章节批量处理脚本 ===" -ForegroundColor Green
Write-Host "输出目录: $outputDir"
Write-Host ""

# 加载章节分析
$chapters = Get-Content $chaptersPath | ConvertFrom-Json
$totalChapters = $chapters.chapters.Count

Write-Host "开始处理 $totalChapters 个章节..." -ForegroundColor Cyan
Write-Host "==============================================" -ForegroundColor Cyan

# 创建临时文件目录
$tempDir = Join-Path $outputDir "temp"
New-Item -ItemType Directory -Path $tempDir -Force | Out-Null

# 处理每个章节
for ($i = 0; $i -lt $totalChapters; $i++) {
    $chapter = $chapters.chapters[$i]
    $chapterIndex = $chapter.index
    $chapterTitle = $chapter.title
    $startTime = $chapter.start_time
    $endTime = $chapter.end_time
    $summary = $chapter.summary

    Write-Host "处理章节 $chapterIndex/$totalChapters: $chapterTitle" -ForegroundColor Yellow

    # 创建章节目录
    $chapterDir = Join-Path $outputDir ($chapterIndex.ToString("00") + "_" + $chapterTitle)
    New-Item -ItemType Directory -Path $chapterDir -Force | Out-Null

    # 1. 剪辑原始视频片段
    $clipPath = Join-Path $chapterDir "$chapterTitle`_clip.mp4"
    $ffmpegArgs = "-y -i `"$videoPath`" -ss $startTime -to $endTime -c:v libx264 -c:a aac -strict experimental `"$clipPath`""
    Start-Process $ffmpegPath -ArgumentList $ffmpegArgs -Wait -NoNewWindow
    Write-Host "  [x] 剪辑视频完成" -ForegroundColor Green

    # 2. 提取对应时间段的字幕
    $tempSubPath = Join-Path $tempDir "chapter_$chapterIndex.vtt"
    $ffmpegSubtitleArgs = "-y -i `"$subtitlesPath`" -ss $startTime -to $endTime -c copy `"$tempSubPath`""
    Start-Process $ffmpegPath -ArgumentList $ffmpegSubtitleArgs -Wait -NoNewWindow

    # 3. 将 VTT 转换为 SRT
    $srtPath = Join-Path $tempDir "chapter_$chapterIndex.srt"
    Convert-VttToSrt $tempSubPath $srtPath

    # 4. 创建双语字幕文件（英文 + 中文）
    $bilingualSrtPath = Join-Path $chapterDir "$chapterTitle`_bilingual.srt"
    ConvertTo-BilingualSubtitles $srtPath $bilingualSrtPath

    # 5. 烧录字幕到视频（硬字幕版本）
    $subtitleClipPath = Join-Path $chapterDir "$chapterTitle`_with_subtitles.mp4"
    $ffmpegSubtitleBurnArgs = "-y -i `"$clipPath`" -vf `"subtitles=`"$srtPath`"`" -c:a copy `"$subtitleClipPath`""
    Start-Process $ffmpegPath -ArgumentList $ffmpegSubtitleBurnArgs -Wait -NoNewWindow
    Write-Host "  [x] 添加硬字幕完成" -ForegroundColor Green

    # 6. 生成总结文案
    $summaryPath = Join-Path $chapterDir "$chapterTitle`_summary.md"
    $summaryContent = @"
# $chapterTitle

## 时间戳
$startTime - $endTime

## 内容总结
$summary

## 关键词
$($chapter.keywords -join ", ")

## 处理时间
$(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
"@
    Set-Content -Path $summaryPath -Value $summaryContent
    Write-Host "  [x] 生成总结文案完成" -ForegroundColor Green

    Write-Host "  [OK] 章节 $chapterIndex 处理完成!" -ForegroundColor Green
    Write-Host ""
}

# 清理临时文件
Remove-Item -Path $tempDir -Recurse -Force

Write-Host "==============================================" -ForegroundColor Cyan
Write-Host "所有章节处理完成!" -ForegroundColor Green
Write-Host "输出目录: $outputDir" -ForegroundColor Green
Write-Host "总处理章节: $totalChapters 个" -ForegroundColor Green
Write-Host "总耗时: $((Get-Date) - $scriptStartTime).TotalSeconds 秒" -ForegroundColor Green

# 显示目录结构
Write-Host ""
Write-Host "生成的文件结构:" -ForegroundColor Cyan
Get-ChildItem -Path $outputDir -Recurse | Where-Object { -not $_.PSIsContainer } | ForEach-Object {
    $relativePath = $_.FullName.Substring($outputDir.Length + 1)
    Write-Host "  $relativePath" -ForegroundColor White
}

# 辅助函数：将 VTT 转换为 SRT
function Convert-VttToSrt {
    param($vttPath, $srtPath)

    $content = Get-Content $vttPath -Raw

    # 移除 WEBVTT 头和格式标记
    $content = $content -replace "WEBVTT.*?`r?`n`r?`n", ""
    $content = $content -replace "<[^>]*>", ""
    $content = $content -replace "\{[^}]*\}", ""
    $content = $content -replace "align:[^%]*%|position:[^%]*%", ""

    # 转换时间格式和行号
    $lines = $content -split "`r?`n"
    $srtContent = ""
    $lineNumber = 1

    for ($i = 0; $i -lt $lines.Length; $i++) {
        $line = $lines[$i].Trim()

        if ($line -match "(\d{2}:\d{2}:\d{2}\.\d{3}) --> (\d{2}:\d{2}:\d{2}\.\d{3})") {
            $startTime = $matches[1].Replace(".", ",")
            $endTime = $matches[2].Replace(".", ",")
            $srtContent += "$lineNumber`r`n$startTime --> $endTime`r`n"
        } elseif ($line -ne "") {
            if ($line -match "^[A-Z]") {
                $srtContent += "$line`r`n`r`n"
            } else {
                $srtContent += "$line "
            }
        } else {
            if ($srtContent -ne "" -and $srtContent -notmatch "`r?`n`r?`n$") {
                $srtContent += "`r`n`r`n"
                $lineNumber++
            }
        }
    }

    Set-Content -Path $srtPath -Value $srtContent
}

# 辅助函数：创建双语字幕
function ConvertTo-BilingualSubtitles {
    param($srtPath, $bilingualPath)

    $content = Get-Content $srtPath -Raw

    # 这里简化处理，实际项目中可以集成翻译服务
    $bilingualContent = ""
    $entries = $content -split "`r?`n`r?`n"

    foreach ($entry in $entries) {
        if ($entry.Trim() -ne "") {
            $lines = $entry -split "`r?`n"
            if ($lines.Length -ge 3) {
                $index = $lines[0]
                $time = $lines[1]
                $text = $lines[2..($lines.Length-1)] -join "`n"

                # 模拟翻译（实际应该使用翻译API）
                $chineseText = Get-ChineseTranslation $text

                $bilingualContent += "$index`r`n$time`r`n英文: $text`r`n中文: $chineseText`r`n`r`n"
            }
        }
    }

    Set-Content -Path $bilingualPath -Value $bilingualContent
}

# 辅助函数：模拟中文翻译（简化版本）
function Get-ChineseTranslation {
    param($text)

    # 这里只是一个简单的映射，实际应该使用翻译API
    $translationMap = @{
        "OpenClaw is the most important AI software I have ever used." = "OpenClaw 是我用过的最重要的 AI 软件。"
        "It has fundamentally changed how not only I work, but I live." = "它从根本上改变了我工作和生活方式。"
        "infiltrated every aspect of my life" = "渗透到我生活的方方面面"
        "allowed me to be hyper productive" = "让我变得超级高效"
        "and really" = "并且真的"
    }

    foreach ($key in $translationMap.Keys) {
        if ($text -match $key) {
            return $text -replace $key, $translationMap[$key]
        }
    }

    # 如果没有找到翻译，返回原始文本
    return "[翻译待完成] $text"
}