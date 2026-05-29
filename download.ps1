# PowerShell 脚本下载 YouTube 视频
$ErrorActionPreference = "Stop"

$videoUrl = "https://www.youtube.com/watch?v=Le0DLrn7ta0"
$outputDir = "youtube-clips/temp"

Write-Host "🎬 开始下载视频..." -ForegroundColor Green
Write-Host "   URL: $videoUrl" -ForegroundColor Cyan
Write-Host "   输出目录: $outputDir" -ForegroundColor Cyan

# 创建输出目录
New-Item -ItemType Directory -Force -Path $outputDir | Out-Null

# 使用 yt-dlp 下载
$ytDlpPath = "C:\Users\14365\scoop\apps\yt-dlp\current\yt-dlp.exe"
& $ytDlpPath -f "bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080][ext=mp4]/best" `
    --write-subs --write-auto-subs --sub-lang en --sub-format vtt `
    -o "$outputDir/%(id)s.%(ext)s" `
    $videoUrl

Write-Host "`n✅ 下载完成！" -ForegroundColor Green

# 列出下载的文件
Write-Host "`n📁 下载的文件:" -ForegroundColor Cyan
Get-ChildItem -Path $outputDir | ForEach-Object {
    Write-Host "   - $($_.Name)" -ForegroundColor White
}
