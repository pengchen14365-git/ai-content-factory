# Python 环境检测脚本
import sys

print("=== Python 依赖检测 ===")
print(f"Python 版本: {sys.version}")
print(f"Python 路径: {sys.executable}")

# 检查必要的库
try:
    import pysrt
    print("✅ pysrt 已安装")
except ImportError:
    print("❌ pysrt 未安装，请运行: pip install pysrt")
    sys.exit(1)

try:
    import yt_dlp
    print("✅ yt-dlp 已安装")
except ImportError:
    print("❌ yt-dlp 未安装，请运行: pip install yt-dlp")
    sys.exit(1)

try:
    from dotenv import load_dotenv
    print("✅ python-dotenv 已安装")
except ImportError:
    print("❌ python-dotenv 未安装，请运行: pip install python-dotenv")
    sys.exit(1)

print("\n✅ 所有依赖已满足！")
