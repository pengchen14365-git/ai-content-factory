# 环境测试脚本
import sys
import os

print("=== 环境测试 ===")
print(f"Python 版本: {sys.version}")
print(f"Python 路径: {sys.executable}")

# 检查必要的库
try:
    import pysrt
    print("✅ pysrt 已安装")
except ImportError as e:
    print(f"❌ pysrt 未安装: {e}")

try:
    import yt_dlp
    print("✅ yt-dlp 已安装")
except ImportError as e:
    print(f"❌ yt-dlp 未安装: {e}")

try:
    import subprocess
    print("✅ subprocess 可用")
except ImportError as e:
    print(f"❌ subprocess 不可用: {e}")

# 检查外部工具
ffmpeg_path = r"C:\Users\14365\scoop\apps\ffmpeg\current\bin\ffmpeg.exe"
if os.path.exists(ffmpeg_path):
    print(f"✅ FFmpeg 路径: {ffmpeg_path}")
else:
    print("❌ FFmpeg 未找到")

yt_dlp_path = r"C:\Users\14365\scoop\apps\yt-dlp\current\yt-dlp.exe"
if os.path.exists(yt_dlp_path):
    print(f"✅ yt-dlp 路径: {yt_dlp_path}")
else:
    print("❌ yt-dlp 未找到")

print("\n测试完成")