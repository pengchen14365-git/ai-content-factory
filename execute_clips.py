#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
视频剪辑执行脚本
执行所有12个章节的剪辑和字幕处理
"""
import os
import json
import subprocess
import sys
from datetime import datetime

def load_clips_info():
    """加载剪辑信息"""
    with open('youtube-clips/clips_info.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def execute_ffmpeg_command(command, chapter_info):
    """执行FFmpeg命令"""
    print(f"\n=== 执行章节 {chapter_info['chapter']}: {chapter_info['title']} ===")
    print(f"命令: {command}")
    print(f"时长: {chapter_info['duration_formatted']}")

    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=300)

        if result.returncode == 0:
            print("剪辑成功!")

            # 提取字幕
            extract_subtitle_command = f"ffmpeg -i 8kNv3rjQaVA.en.vtt -ss {chapter_info['start_time']} -to {chapter_info['end_time']} -c copy youtube-clips/openclaw_tutorial_{chapter_info['chapter']:02d}_en.vtt"
            print(f"提取字幕: {extract_subtitle_command}")

            subtitle_result = subprocess.run(extract_subtitle_command, shell=True, capture_output=True, text=True, timeout=60)

            if subtitle_result.returncode == 0:
                print("字幕提取成功!")
            else:
                print(f"字幕提取失败: {subtitle_result.stderr}")

        else:
            print(f"剪辑失败: {result.stderr}")

    except subprocess.TimeoutExpired:
        print("命令超时")
    except Exception as e:
        print(f"执行错误: {e}")

def main():
    """主函数"""
    print("=== OpenClaw 视频剪辑执行 ===")
    print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # 加载剪辑信息
    clips_info = load_clips_info()
    chapters = clips_info['chapters']

    print(f"总章节数: {len(chapters)}")
    print("执行以下剪辑命令:")

    # 显示所有剪辑信息
    for chapter in chapters:
        print(f"\n章节 {chapter['chapter']}: {chapter['title']}")
        print(f"时间: {chapter['start_time']} - {chapter['end_time']}")
        print(f"时长: {chapter['duration_formatted']}")
        print(f"关键词: {', '.join(chapter['keywords'])}")

    print(f"\n{'='*50}")
    print("开始执行剪辑...")

    # 逐个执行剪辑
    for i, chapter in enumerate(chapters, 1):
        print(f"\n进度: {i}/{len(chapters)}")

        # 检查文件是否已存在
        video_file = f"youtube-clips/openclaw_tutorial_{chapter['chapter']:02d}.mp4"
        subtitle_file = f"youtube-clips/openclaw_tutorial_{chapter['chapter']:02d}_en.vtt"

        if os.path.exists(video_file):
            print(f"视频文件已存在: {video_file}")
            if os.path.exists(subtitle_file):
                print(f"字幕文件已存在: {subtitle_file}")
                continue

        # 执行剪辑命令
        execute_ffmpeg_command(chapter['ffmpeg_command'], chapter)

    print(f"\n{'='*50}")
    print("剪辑执行完成!")
    print(f"完成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # 显示生成的文件
    print(f"\n生成的文件:")
    video_files = [f for f in os.listdir('youtube-clips') if f.endswith('.mp4')]
    subtitle_files = [f for f in os.listdir('youtube-clips') if f.endswith('_en.vtt')]

    print(f"视频文件: {len(video_files)} 个")
    for f in video_files:
        print(f"  - {f}")

    print(f"字幕文件: {len(subtitle_files)} 个")
    for f in subtitle_files:
        print(f"  - {f}")

if __name__ == "__main__":
    main()