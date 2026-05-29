#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Subtitle analysis script
Parse VTT subtitles and generate structured data
"""
import sys
import io
import re

# Set UTF-8 encoding for Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

def parse_vtt_time(time_str):
    """Convert VTT timestamp to seconds"""
    parts = time_str.split(':')
    if len(parts) == 3:
        h, m, s = parts
        return int(h) * 3600 + int(m) * 60 + float(s)
    elif len(parts) == 2:
        m, s = parts
        return int(m) * 60 + float(s)
    return 0

def format_time(seconds):
    """Format seconds to HH:MM:SS"""
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    return f"{h:02d}:{m:02d}:{s:02d}"

def parse_vtt(file_path):
    """Parse VTT subtitle file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    subtitles = []
    current_time = None
    current_text = []

    for line in lines:
        line = line.strip()
        if not line or line.startswith('WEBVTT') or line.startswith('Kind:') or line.startswith('Language:'):
            continue

        time_match = re.match(r'(\d{2}:\d{2}:\d{2}\.\d{3}) --> (\d{2}:\d{2}:\d{2}\.\d{3})', line)
        if time_match:
            if current_time and current_text:
                subtitles.append({
                    'start': current_time[0],
                    'end': current_time[1],
                    'text': ' '.join(current_text)
                })
            start = parse_vtt_time(time_match.group(1))
            end = parse_vtt_time(time_match.group(2))
            current_time = (start, end)
            current_text = []
        elif current_time is not None:
            text = re.sub(r'<[^>]+>', '', line)
            if text:
                current_text.append(text)

    if current_time and current_text:
        subtitles.append({
            'start': current_time[0],
            'end': current_time[1],
            'text': ' '.join(current_text)
        })

    return subtitles

def analyze_subtitles(subtitles):
    """Analyze subtitle content"""
    if not subtitles:
        return None

    total_duration = subtitles[-1]['end']
    total_subtitles = len(subtitles)
    full_text = '\n'.join([f"[{format_time(s['start'])}] {s['text']}" for s in subtitles])

    return {
        'total_duration': total_duration,
        'total_subtitles': total_subtitles,
        'subtitles': subtitles,
        'full_text': full_text
    }

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python analyze_subtitles_v2.py <subtitle_file>")
        sys.exit(1)

    vtt_file = sys.argv[1]
    print(f"Parsing subtitle file: {vtt_file}")

    subtitles = parse_vtt(vtt_file)
    analysis = analyze_subtitles(subtitles)

    if analysis:
        print(f"\nSubtitle analysis complete!")
        print(f"Total duration: {format_time(analysis['total_duration'])}")
        print(f"Total subtitles: {analysis['total_subtitles']}")

        # Save full text to file
        output_file = 'subtitle_text.txt'
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(analysis['full_text'])

        print(f"\nFull subtitle text saved to: {output_file}")
        print(f"Text length: {len(analysis['full_text'])} characters")

        # Show first 3000 characters
        print(f"\nFirst 3000 characters:")
        print("=" * 80)
        print(analysis['full_text'][:3000])
        print("=" * 80)
