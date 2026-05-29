#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能章节分析脚本
基于字幕内容生成 2-5 分钟粒度的章节
"""
import sys
import io
import re
from datetime import timedelta

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

def analyze_content_keywords(subtitles, start_idx, end_idx):
    """Analyze keywords in a section"""
    text = ' '.join([s['text'] for s in subtitles[start_idx:end_idx+1]]).lower()

    # Common keyword patterns
    keywords = {
        'OpenClaw/OpenAI/assistant': ['openclaw', 'open claw', 'ai assistant', 'personal ai'],
        'CRM/business/contacts': ['crm', 'contact', 'business', 'customer', 'email', 'calendar'],
        'Security/safety': ['security', 'safety', 'protect', 'attack', 'vulnerability', 'prompt injection'],
        'Knowledge base/RAG': ['knowledge', 'rag', 'vector', 'embed', 'search', 'repository', 'ingest'],
        'Business analytics/advisory': ['analytics', 'advisory', 'council', 'expert', 'recommend', 'business'],
        'Social media/content': ['social', 'media', 'twitter', 'x', 'youtube', 'video', 'content', 'post'],
        'Automation/workflow': ['automation', 'workflow', 'pipeline', 'automatic', 'schedule'],
        'Memory/learning': ['memory', 'learn', 'evolve', 'remember', 'preference', 'identity', 'soul']
    }

    scores = {}
    for category, words in keywords.items():
        score = sum(1 for word in words if word in text)
        if score > 0:
            scores[category] = score

    return sorted(scores.items(), key=lambda x: x[1], reverse=True)

def generate_smart_chapters(subtitles):
    """Generate chapters based on content analysis"""
    chapters = []
    total_duration = subtitles[-1]['end']

    # Target chapter length: 2-5 minutes (120-300 seconds)
    min_chapter_length = 120
    max_chapter_length = 300

    current_start = 0
    idx = 0

    while idx < len(subtitles):
        # Find potential chapter end
        chapter_start_time = subtitles[idx]['start']
        best_end_idx = idx
        best_end_time = chapter_start_time + min_chapter_length

        # Look ahead to find natural break points
        for j in range(idx, min(len(subtitles), idx + 300)):  # Look at most ~300 subtitles ahead
            if j >= len(subtitles):
                break

            current_time = subtitles[j]['start']
            chapter_length = current_time - chapter_start_time

            # Check if we've reached minimum length
            if chapter_length >= min_chapter_length:
                # Look for topic transition indicators
                text = subtitles[j]['text'].lower()

                # Transition phrases
                transition_indicators = [
                    'so, next',
                    'okay, so',
                    'all right',
                    'now,',
                    'this next',
                    'moving on',
                    'let\'s talk',
                    'another thing',
                    'also',
                    'by the way',
                    'okay this'
                ]

                is_transition = any(phrase in text for phrase in transition_indicators)

                # Check for content shift by analyzing keywords
                if j > idx + 20:  # Ensure we have enough content
                    current_keywords = analyze_content_keywords(subtitles, idx, j)
                    next_keywords = analyze_content_keywords(subtitles, j, min(j+50, len(subtitles)))

                    # Check if topics are different
                    if current_keywords and next_keywords:
                        if current_keywords[0][0] != next_keywords[0][0]:
                            is_transition = True

                # Update best end if this is a good transition point
                if is_transition or chapter_length >= max_chapter_length:
                    best_end_idx = j
                    best_end_time = current_time
                    break

                # Update minimum end point
                best_end_idx = j
                best_end_time = current_time

        # Create chapter
        chapter_subtitles = subtitles[idx:best_end_idx+1]
        chapter_text = ' '.join([s['text'] for s in chapter_subtitles])

        # Generate chapter title from keywords
        keywords = analyze_content_keywords(subtitles, idx, best_end_idx)
        main_topic = keywords[0][0] if keywords else "General discussion"

        # Clean up topic name
        topic_name = main_topic.split('/')[0] if '/' in main_topic else main_topic
        topic_name = topic_name.replace('_', ' ').title()

        # Create descriptive title
        chapter_title = f"{topic_name}"

        chapters.append({
            'start': chapter_start_time,
            'end': best_end_time,
            'title': chapter_title,
            'summary': chapter_text[:200] + '...' if len(chapter_text) > 200 else chapter_text,
            'keywords': [k[0] for k in keywords[:3]]
        })

        idx = best_end_idx + 1

    return chapters

if __name__ == '__main__':
    vtt_file = '8kNv3rjQaVA.en.vtt'

    print(f"Parsing {vtt_file}...")
    subtitles = parse_vtt(vtt_file)
    print(f"Found {len(subtitles)} subtitles")

    print(f"\nGenerating intelligent chapters...")
    chapters = generate_smart_chapters(subtitles)

    print(f"\n{'='*80}")
    print(f"Generated {len(chapters)} chapters:")
    print(f"{'='*80}\n")

    for i, chapter in enumerate(chapters, 1):
        duration = chapter['end'] - chapter['start']
        print(f"{i}. [{format_time(chapter['start'])} - {format_time(chapter['end'])}] {chapter['title']}")
        print(f"   Duration: {int(duration//60)}:{int(duration%60):02d}")
        print(f"   Keywords: {', '.join(chapter['keywords'])}")
        print(f"   Summary: {chapter['summary'][:150]}...")
        print()

    # Save to file
    with open('chapters.json', 'w', encoding='utf-8') as f:
        import json
        json.dump(chapters, f, indent=2, ensure_ascii=False)
    print(f"Chapters saved to chapters.json")
