# YouTube剪辑工具安装脚本
Write-Host "正在安装YouTube视频剪辑所需工具..." -ForegroundColor Green

# 1. 安装 Chocolatey（如果还没有）
if (-not (Get-Command choco -ErrorAction SilentlyContinue)) {
    Write-Host "安装 Chocolatey 包管理器..." -ForegroundColor Yellow
    Set-ExecutionPolicy Bypass -Scope Process -Force
    [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
    iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
}

# 2. 安装 FFmpeg
Write-Host "安装 FFmpeg..." -ForegroundColor Yellow
choco install ffmpeg -y

# 3. 安装 yt-dlp
Write-Host "安装 yt-dlp..." -ForegroundColor Yellow
choco install yt-dlp -y

# 4. 安装 Python
Write-Host "安装 Python..." -ForegroundColor Yellow
choco install python -y

# 5. 安装 Python依赖
Write-Host "安装Python依赖包..." -ForegroundColor Yellow
pip install pysrt python-dotenv

Write-Host "所有工具安装完成！请重新启动终端。" -ForegroundColor Green
Write-Host "验证安装:"
Write-Host "ffmpeg -version"
Write-Host "yt-dlp --version"
Write-Host "python -c 'import pysrt; print(pysrt installed)'"