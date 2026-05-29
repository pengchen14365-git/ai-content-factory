#!/usr/bin/env python3
"""
简单的字幕分析工具
解析 VTT 字幕并提取文本内容用于 AI 分析
"""

import re
import json
from pathlib import Path

def parse_vtt(vtt_path):
    """解析 VTT 字幕文件"""
    with open(vtt_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 移除 VTT 头部
    lines = content.split('\n')
    if lines[0].strip() == 'WEBVTT':
        lines = lines[1:]

    # 解析字幕条目
    subtitles = []
    current_subtitle = None

    for line in lines:
        line = line.strip()
        if not line:
            if current_subtitle:
                subtitles.append(current_subtitle)
                current_subtitle = None
            continue

        # 检查是否是时间戳行
        time_pattern = r'(\d{2}:\d{2}:\d{2}\.\d{3}) --> (\d{2}:\d{2}:\d{2}\.\d{3})'
        time_match = re.search(time_pattern, line)
        if time_match:
            current_subtitle = {
                'start': time_match.group(1),
                'end': time_match.group(2),
                'text': []
            }
        elif current_subtitle:
            # 移除字幕标签（如 <font>、<c.colorE5E5E5> 等）
            text = re.sub(r'<[^>]+>', '', line)
            if text and text != '&nbsp;':
                current_subtitle['text'].append(text)

    if current_subtitle:
        subtitles.append(current_subtitle)

    return subtitles

def time_to_seconds(time_str):
    """将时间字符串转换为秒数"""
    h, m, s = time_str.split(':')
    return int(h) * 3600 + int(m) * 60 + float(s)

def seconds_to_time(seconds):
    """将秒数转换为时间字符串 (HH:MM:SS)"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"

def main():
    vtt_path = "8kNv3rjQaVA.en.vtt"

    print("📊 解析字幕文件...")
    subtitles = parse_vtt(vtt_path)

    print(f"✅ 共解析 {len(subtitles)} 条字幕")

    if not subtitles:
        print("❌ 未找到字幕内容")
        return

    # 计算总时长
    total_duration = time_to_seconds(subtitles[-1]['end'])
    print(f"⏱️  总时长: {seconds_to_time(total_duration)} ({total_duration:.0f} 秒)")

    # 输出前 10 条字幕作为预览
    print("\n📝 字幕预览 (前 10 条):")
    for i, sub in enumerate(subtitles[:10], 1):
        print(f"{i}. [{sub['start']} - {sub['end']}] {' '.join(sub['text'])}")

    # 保存完整字幕文本到文件
    output_file = "subtitle_text.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        for sub in subtitles:
            time_range = f"[{sub['start']} - {sub['end']}]"
            text = ' '.join(sub['text'])
            f.write(f"{time_range} {text}\n")

    print(f"\n✅ 完整字幕已保存到: {output_file}")

    # 保存结构化数据
    json_file = "subtitles.json"
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(subtitles, f, ensure_ascii=False, indent=2)

    print(f"✅ 结构化数据已保存到: {json_file}")

if __name__ == "__main__":
    main()
