#!/usr/bin/env python3
"""
字幕分析脚本
解析 VTT 字幕并生成结构化数据
"""
import sys
import re
from datetime import timedelta

def parse_vtt_time(time_str):
    # 设置输出编码为 UTF-8（Windows）
    import sys
    import io
    if sys.platform == 'win32':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

    """将 VTT 时间戳转换为秒数"""
    # 格式: 00:00:00.000 或 00:00.000
    parts = time_str.split(':')
    if len(parts) == 3:
        h, m, s = parts
        return int(h) * 3600 + int(m) * 60 + float(s)
    elif len(parts) == 2:
        m, s = parts
        return int(m) * 60 + float(s)
    return 0

def format_time(seconds):
    """将秒数格式化为 HH:MM:SS"""
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    return f"{h:02d}:{m:02d}:{s:02d}"

def parse_vtt(file_path):
    """解析 VTT 字幕文件"""
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    subtitles = []
    current_time = None
    current_text = []

    for line in lines:
        line = line.strip()
        # 跳过空行和 VTT 头部
        if not line or line.startswith('WEBVTT') or line.startswith('Kind:') or line.startswith('Language:'):
            continue

        # 检测时间戳行
        time_match = re.match(r'(\d{2}:\d{2}:\d{2}\.\d{3}) --> (\d{2}:\d{2}:\d{2}\.\d{3})', line)
        if time_match:
            # 保存上一条字幕
            if current_time and current_text:
                subtitles.append({
                    'start': current_time[0],
                    'end': current_time[1],
                    'text': ' '.join(current_text)
                })
            # 开始新字幕
            start = parse_vtt_time(time_match.group(1))
            end = parse_vtt_time(time_match.group(2))
            current_time = (start, end)
            current_text = []
        elif current_time is not None:
            # 移除 VTT 标签
            text = re.sub(r'<[^>]+>', '', line)
            if text:
                current_text.append(text)

    # 保存最后一条字幕
    if current_time and current_text:
        subtitles.append({
            'start': current_time[0],
            'end': current_time[1],
            'text': ' '.join(current_text)
        })

    return subtitles

def analyze_subtitles(subtitles):
    """分析字幕内容"""
    if not subtitles:
        return None

    total_duration = subtitles[-1]['end']
    total_subtitles = len(subtitles)

    # 提取完整文本
    full_text = '\n'.join([f"[{format_time(s['start'])}] {s['text']}" for s in subtitles])

    return {
        'total_duration': total_duration,
        'total_subtitles': total_subtitles,
        'subtitles': subtitles,
        'full_text': full_text
    }

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python analyze_subtitles.py <subtitle_file>")
        sys.exit(1)

    vtt_file = sys.argv[1]

    print(f"📖 正在解析字幕文件: {vtt_file}")
    subtitles = parse_vtt(vtt_file)
    analysis = analyze_subtitles(subtitles)

    if analysis:
        print(f"\n✅ 字幕解析完成!")
        print(f"   总时长: {format_time(analysis['total_duration'])}")
        print(f"   字幕条数: {analysis['total_subtitles']}")

        # 输出前 5000 字符用于 AI 分析
        print(f"\n📝 字幕文本（前 5000 字符）:")
        print("=" * 80)
        print(analysis['full_text'][:5000])
        print("=" * 80)
        if len(analysis['full_text']) > 5000:
            print(f"\n... (还有 {len(analysis['full_text']) - 5000} 字符)")
