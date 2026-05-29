#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Final Chapter Processing Script
Process all chapters and generate clips with subtitles
"""

import json
import os
import subprocess
from datetime import datetime
from pathlib import Path

def main():
    # File paths
    video_path = Path("D:/wenjian/Obsidian仓库/8kNv3rjQaVA.mp4")
    subtitles_path = Path("D:/wenjian/Obsidian仓库/8kNv3rjQaVA.en.vtt")
    chapters_path = Path("D:/wenjian/Obsidian仓库/chapters_analysis.json")

    # Output directory
    output_base_dir = Path("D:/wenjian/Obsidian仓库/youtube-clips")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = output_base_dir / timestamp
    temp_dir = output_dir / "temp"

    # Create output directories
    output_base_dir.mkdir(exist_ok=True)
    output_dir.mkdir(exist_ok=True)
    temp_dir.mkdir(exist_ok=True)

    print("=" * 60)
    print("=== YouTube Video Chapter Processing Script - Final Version ===")
    print("=" * 60)
    print(f"Output directory: {output_dir}")
    print()

    # Read chapters analysis
    with open(chapters_path, 'r', encoding='utf-8') as f:
        chapters_data = json.load(f)

    total_chapters = len(chapters_data['chapters'])
    print(f"Processing {total_chapters} chapters...")
    print("-" * 60)

    # Process each chapter
    success_count = 0
    for i, chapter in enumerate(chapters_data['chapters'], 1):
        chapter_index = chapter['index']
        chapter_title = chapter['title']
        start_time = chapter['start_time']
        end_time = chapter['end_time']
        summary = chapter['summary']
        keywords = chapter['keywords']

        # Create safe filename
        safe_title = chapter_title.replace(" ", "_").replace("(", "").replace(")", "").replace("，", "_").replace("。", "")
        safe_title = "".join(c for c in safe_title if c.isalnum() or c in "_").rstrip("_")

        print(f"\nProcessing chapter {i}/{total_chapters}: {chapter_title}")

        try:
            # Create chapter directory
            chapter_dir = output_dir / f"{chapter_index:02d}_{safe_title}"
            chapter_dir.mkdir(exist_ok=True)

            # 1. Clip original video
            clip_path = chapter_dir / f"chapter_{chapter_index}_clip.mp4"
            cmd = [
                'ffmpeg', '-y', '-i', str(video_path),
                '-ss', start_time, '-to', end_time,
                '-c:v', 'libx264', '-c:a', 'aac',
                '-strict', 'experimental', str(clip_path)
            ]
            subprocess.run(cmd, check=True, capture_output=True)
            print("  [OK] Video clipping completed")

            # 2. Extract subtitles for this chapter
            temp_sub_path = temp_dir / f"chapter_{chapter_index}.vtt"
            cmd = [
                'ffmpeg', '-y', '-i', str(subtitles_path),
                '-ss', start_time, '-to', end_time,
                '-c', 'copy', str(temp_sub_path)
            ]
            subprocess.run(cmd, check=True, capture_output=True)

            # 3. Convert VTT to SRT
            srt_path = temp_dir / f"chapter_{chapter_index}.srt"
            vtt_to_srt(temp_sub_path, srt_path)
            print("  [OK] Subtitle conversion completed")

            # 4. Create bilingual subtitles
            bilingual_srt_path = chapter_dir / f"chapter_{chapter_index}_bilingual.srt"
            create_bilingual_subtitles(srt_path, bilingual_srt_path)
            print("  [OK] Bilingual subtitles created")

            # 5. Try to burn subtitles to video (hard subtitles)
            try:
                subtitle_clip_path = chapter_dir / f"chapter_{chapter_index}_with_subtitles.mp4"
                cmd = [
                    'ffmpeg', '-y', '-i', str(clip_path),
                    '-vf', f"subtitles='{srt_path}'",
                    '-c:a', 'copy', str(subtitle_clip_path)
                ]
                subprocess.run(cmd, check=True, capture_output=True, timeout=60)
                print("  [OK] Hard subtitles added")
            except subprocess.TimeoutExpired:
                print("  [!] Hard subtitles timeout, skipping")
                subtitle_clip_path = clip_path
            except subprocess.CalledProcessError:
                print("  [!] Hard subtitles failed, using original video")
                subtitle_clip_path = clip_path

            # 6. Generate summary document
            summary_path = chapter_dir / f"chapter_{chapter_index}_summary.md"
            summary_content = f"""# {chapter_title}

## Timestamp
{start_time} - {end_time}

## Content Summary
{summary}

## Keywords
{', '.join(keywords)}

## Processing Time
{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Generated Files
- Clip: chapter_{chapter_index}_clip.mp4
- With Subtitles: chapter_{chapter_index}_with_subtitles.mp4
- Bilingual Subtitles: chapter_{chapter_index}_bilingual.srt
- Summary: chapter_{chapter_index}_summary.md
"""
            with open(summary_path, 'w', encoding='utf-8') as f:
                f.write(summary_content)
            print("  [OK] Summary generated")

            success_count += 1
            print(f"  [SUCCESS] Chapter {chapter_index} completed!")

        except Exception as e:
            print(f"  [FAILED] Chapter {chapter_index} failed: {str(e)}")

        print("-" * 40)

    # Clean up temporary files
    import shutil
    shutil.rmtree(temp_dir)

    # Print summary
    print("\n" + "=" * 60)
    print("Processing Summary")
    print("=" * 60)
    print(f"Total chapters: {total_chapters}")
    print(f"Successfully processed: {success_count}")
    print(f"Failed: {total_chapters - success_count}")
    print(f"Output directory: {output_dir}")
    print(f"Total time: {(datetime.now() - start_time).total_seconds():.1f} seconds")

    # Show generated files
    print("\nGenerated files structure:")
    print("-" * 40)
    for item in output_dir.rglob('*.mp4'):
        size_mb = item.stat().st_size / (1024 * 1024)
        print(f"  📹 {item.name} ({size_mb:.1f} MB)")

    for item in output_dir.rglob('*.srt'):
        print(f"  📝 {item.name}")

    for item in output_dir.rglob('*.md'):
        print(f"  📄 {item.name}")

    print("\n🎉 Batch processing completed!")

def vtt_to_srt(vtt_path, srt_path):
    """Convert VTT to SRT format"""
    with open(vtt_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Remove WEBVTT header and format tags
    content = content.replace('WEBVTT\nKind: captions\nLanguage: en\n\n', '')
    content = content.replace('<c>', '').replace('</c>', '')
    content = content.replace('{', '').replace('}', '')
    content = content.replace('align:start position:0%', '')

    # Process time format and line numbers
    lines = content.split('\n')
    srt_content = ""
    line_number = 1

    i = 0
    while i < len(lines):
        line = lines[i].strip()

        if '-->' in line:
            # Time stamp line
            start_time, end_time = line.split(' --> ')
            # Convert to SRT format
            start_time = start_time.replace('.', ',')
            end_time = end_time.replace('.', ',')
            srt_content += f"{line_number}\n{start_time} --> {end_time}\n"
            line_number += 1
            i += 1

            # Process subtitle text
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
    """Create bilingual subtitles file"""
    with open(srt_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Simplified bilingual subtitles, in practice should integrate translation API
    bilingual_content = ""
    entries = content.split('\n\n')

    for entry in entries:
        if entry.strip():
            lines = entry.split('\n')
            if len(lines) >= 3:
                index = lines[0]
                time = lines[1]
                text = '\n'.join(lines[2:])

                # Simulate translation
                chinese_text = get_chinese_translation(text)

                bilingual_content += f"{index}\n{time}\nEnglish: {text}\nChinese: {chinese_text}\n\n"

    with open(bilingual_path, 'w', encoding='utf-8') as f:
        f.write(bilingual_content)

def get_chinese_translation(text):
    """Simulate Chinese translation (simplified version)"""
    # This is just a simple mapping, in practice should use translation API
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

    return f"[Translation pending] {text}"

if __name__ == "__main__":
    start_time = datetime.now()
    main()