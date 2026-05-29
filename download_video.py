#!/usr/bin/env python3
"""
YouTube 视频下载脚本
下载视频和英文字幕
"""
import sys
import yt_dlp
import os

def download_video(url):
    """下载 YouTube 视频和字幕"""

    # 设置输出编码为 UTF-8
    import sys
    import io
    if sys.platform == 'win32':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

    # 获取视频信息
    print(f"📥 正在获取视频信息...")
    with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
        info = ydl.extract_info(url, download=False)
        video_id = info.get('id', 'video')
        title = info.get('title', 'Unknown Title')
        duration = info.get('duration', 0)

    print(f"✅ 视频信息:")
    print(f"   标题: {title}")
    print(f"   时长: {duration // 60}:{duration % 60:02d}")
    print(f"   ID: {video_id}")

    # 配置下载选项（单一格式，不需要 FFmpeg）
    ydl_opts = {
        'format': 'best[height<=1080][ext=mp4]/best[height<=1080]',  # 单一格式
        'outtmpl': f'{video_id}.mp4',
        'subtitleslangs': ['en'],
        'writesubtitles': True,
        'writeautomaticsub': True,  # 自动字幕作为备选
        'quiet': False,
        'no_warnings': False,
    }

    # 下载视频和字幕
    print(f"\n📥 开始下载...")
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    # 检查字幕文件
    subtitle_files = []
    for ext in ['en.vtt', 'en.srt', f'{video_id}.en.vtt']:
        if os.path.exists(ext):
            subtitle_files.append(ext)
            break

    # 如果没有找到字幕，尝试查找任何 vtt 文件
    if not subtitle_files:
        for file in os.listdir('.'):
            if file.endswith('.vtt'):
                subtitle_files.append(file)
                break

    # 重命名字幕文件
    final_subtitle = f'{video_id}.en.vtt'
    if subtitle_files and subtitle_files[0] != final_subtitle:
        os.rename(subtitle_files[0], final_subtitle)
        print(f"✅ 字幕已重命名为: {final_subtitle}")

    print(f"\n✅ 下载完成!")
    print(f"   视频: {video_id}.mp4")
    print(f"   字幕: {final_subtitle if os.path.exists(final_subtitle) else '未找到'}")

    return {
        'video_id': video_id,
        'title': title,
        'duration': duration,
        'video_file': f'{video_id}.mp4',
        'subtitle_file': final_subtitle if os.path.exists(final_subtitle) else None
    }

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python download_video.py <youtube_url>")
        sys.exit(1)

    url = sys.argv[1]
    result = download_video(url)

    # 输出结果供后续步骤使用
    print(f"\n📊 视频信息摘要:")
    print(f"ID={result['video_id']}")
    print(f"TITLE={result['title']}")
    print(f"DURATION={result['duration']}")
