#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
YouTube 视频章节批量处理脚本
用于剪辑所有章节并生成带字幕的版本
"""

import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

def main():
    # 文件路径配置
    video_path = Path("D:/wenjian/Obsidian仓库/8kNv3rjQaVA.mp4")
    subtitles_path = Path("D:/wenjian/Obsidian仓库/8kNv3rjQaVA.en.vtt")
    chapters_path = Path("D:/wenjian/Obsidian仓库/chapters_analysis.json")

    # 输出目录
    output_base_dir = Path("D:/wenjian/Obsidian仓库/youtube-clips")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = output_base_dir / timestamp

    # 创建输出目录
    output_base_dir.mkdir(exist_ok=True)
    output_dir.mkdir(exist_ok=True)
    temp_dir = output_dir / "temp"
    temp_dir.mkdir(exist_ok=True)

    print("=" * 50)
    print("=== YouTube 视频章节批量处理脚本 ===")
    print("=" * 50)
    print(f"输出目录: {output_dir}")
    print()

    # 读取章节分析
    with open(chapters_path, 'r', encoding='utf-8') as f:
        chapters_data = json.load(f)

    total_chapters = len(chapters_data['chapters'])
    print(f"开始处理 {total_chapters} 个章节...")
    print("-" * 50)

    # 处理每个章节
    for i, chapter in enumerate(chapters_data['chapters'], 1):
        chapter_index = chapter['index']
        chapter_title = chapter['title']
        start_time = chapter['start_time']
        end_time = chapter['end_time']
        summary = chapter['summary']
        keywords = chapter['keywords']

        print(f"处理章节 {i}/{total_chapters}: {chapter_title}")

        # 创建章节目录
        chapter_dir = output_dir / f"{chapter_index:02d}_{chapter_title}"
        chapter_dir.mkdir(exist_ok=True)

        # 1. 剪辑原始视频片段
        clip_path = chapter_dir / f"{chapter_title}_clip.mp4"
        cmd = [
            'ffmpeg', '-y', '-i', str(video_path),
            '-ss', start_time, '-to', end_time,
            '-c:v', 'libx264', '-c:a', 'aac',
            '-strict', 'experimental', str(clip_path)
        ]
        subprocess.run(cmd, check=True)
        print("  ✓ 剪辑视频完成")

        # 2. 提取对应时间段的字幕
        temp_sub_path = temp_dir / f"chapter_{chapter_index}.vtt"
        cmd = [
            'ffmpeg', '-y', '-i', str(subtitles_path),
            '-ss', start_time, '-to', end_time,
            '-c', 'copy', str(temp_sub_path)
        ]
        subprocess.run(cmd, check=True)

        # 3. 将 VTT 转换为 SRT
        srt_path = temp_dir / f"chapter_{chapter_index}.srt"
        vtt_to_srt(temp_sub_path, srt_path)
        print("  ✓ 字幕转换完成")

        # 4. 创建双语字幕文件
        bilingual_srt_path = chapter_dir / f"{chapter_title}_bilingual.srt"
        create_bilingual_subtitles(srt_path, bilingual_srt_path)
        print("  ✓ 创建双语字幕完成")

        # 5. 烧录字幕到视频（硬字幕版本）
        subtitle_clip_path = chapter_dir / f"{chapter_title}_with_subtitles.mp4"
        cmd = [
            'ffmpeg', '-y', '-i', str(clip_path),
            '-vf', f"subtitles='{srt_path}'",
            '-c:a', 'copy', str(subtitle_clip_path)
        ]
        subprocess.run(cmd, check=True)
        print("  ✓ 添加硬字幕完成")

        # 6. 生成总结文案
        summary_path = chapter_dir / f"{chapter_title}_summary.md"
        summary_content = f"""# {chapter_title}

## 时间戳
{start_time} - {end_time}

## 内容总结
{summary}

## 关键词
{', '.join(keywords)}

## 处理时间
{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write(summary_content)
        print("  ✓ 生成总结文案完成")

        print(f"  ✅ 章节 {chapter_index} 处理完成!")
        print()

    # 清理临时文件
    import shutil
    shutil.rmtree(temp_dir)

    print("-" * 50)
    print("所有章节处理完成!")
    print(f"输出目录: {output_dir}")
    print(f"总处理章节: {total_chapters} 个")
    print(f"总耗时: {(datetime.now() - start_time).total_seconds():.1f} 秒")

    # 显示目录结构
    print()
    print("生成的文件结构:")
    for item in output_dir.rglob('*'):
        if item.is_file():
            relative_path = item.relative_to(output_dir)
            print(f"  {relative_path}")

def vtt_to_srt(vtt_path, srt_path):
    """将 VTT 转换为 SRT 格式"""
    with open(vtt_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 移除 WEBVTT 头和格式标记
    content = content.replace('WEBVTT\nKind: captions\nLanguage: en\n\n', '')
    content = content.replace('<c>', '').replace('</c>', '')
    content = content.replace('{', '').replace('}', '')
    content = content.replace('align:start position:0%', '')

    # 处理时间格式和行号
    lines = content.split('\n')
    srt_content = ""
    line_number = 1

    i = 0
    while i < len(lines):
        line = lines[i].strip()

        if '-->' in line:
            # 时间戳行
            start_time, end_time = line.split(' --> ')
            # 转换为 SRT 格式
            start_time = start_time.replace('.', ',')
            end_time = end_time.replace('.', ',')
            srt_content += f"{line_number}\n{start_time} --> {end_time}\n"
            line_number += 1
            i += 1

            # 处理字幕文本
            subtitle_text = ""
            while i < len(lines) and lines[i].strip() != '':
                subtitle_text += lines[i] + '\n'
                i += 1
            srt_content += subtitle_text + '\n'
        else:
            i += 1

    with open(srt_path, 'w', encoding='utf-8') as f:
        f.write(srt_content)

def create_bilingual_subtitles(srt_path, bilingual_path):
    """创建双语字幕文件"""
    with open(srt_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 这里简化处理，实际应该集成翻译服务
    bilingual_content = ""
    entries = content.split('\n\n')

    for entry in entries:
        if entry.strip():
            lines = entry.split('\n')
            if len(lines) >= 3:
                index = lines[0]
                time = lines[1]
                text = '\n'.join(lines[2:])

                # 模拟翻译
                chinese_text = get_chinese_translation(text)

                bilingual_content += f"{index}\n{time}\n英文: {text}\n中文: {chinese_text}\n\n"

    with open(bilingual_path, 'w', encoding='utf-8') as f:
        f.write(bilingual_content)

def get_chinese_translation(text):
    """模拟中文翻译（简化版本）"""
    # 这里只是一个简单的映射，实际应该使用翻译API
    translation_map = {
        "OpenClaw is the most important AI software I have ever used.": "OpenClaw 是我用过的最重要的 AI 软件。",
        "It has fundamentally changed how not only I work, but I live.": "它从根本上改变了我工作和生活方式。",
        "infiltrated every aspect of my life": "渗透到我生活的方方面面",
        "allowed me to be hyper productive": "让我变得超级高效",
        "and really": "并且真的",
    }

    for key, value in translation_map.items():
        if key in text:
            return text.replace(key, value)

    return f"[翻译待完成] {text}"

if __name__ == "__main__":
    start_time = datetime.now()
    main()