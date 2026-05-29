#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
视频剪辑处理脚本
分割视频、翻译字幕、生成双语字幕、生成总结文案
"""
import sys
import io
import json
import os
import subprocess
import re
from datetime import datetime

# Set UTF-8 encoding for Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# 定义章节列表
chapters = [
    {
        'start': 0, 'end': 255,
        'title': 'OpenClaw简介与个人CRM',
        'keywords': ['OpenClaw', 'AI助手', '个人CRM']
    },
    {
        'start': 255, 'end': 390,
        'title': 'CRM系统深度解析',
        'keywords': ['CRM系统', 'Gmail集成', '数据抓取']
    },
    {
        'start': 390, 'end': 530,
        'title': 'CRM会议集成',
        'keywords': ['会议集成', '行动项', 'Todoist同步']
    },
    {
        'start': 530, 'end': 660,
        'title': '个人知识库构建',
        'keywords': ['知识库', 'RAG', '内容抓取']
    },
    {
        'start': 660, 'end': 810,
        'title': '知识库实战演示',
        'keywords': ['搜索功能', 'X集成', '内容管理']
    },
    {
        'start': 810, 'end': 930,
        'title': '商业顾问委员会',
        'keywords': ['商业分析', 'AI专家', '数据洞察']
    },
    {
        'start': 930, 'end': 1050,
        'title': '安全委员会',
        'keywords': ['安全审计', '代码审查', '防护措施']
    },
    {
        'start': 1050, 'end': 1170,
        'title': '社交媒体追踪器',
        'keywords': ['社交媒体', '性能监控', '数据分析']
    },
    {
        'start': 1170, 'end': 1325,
        'title': '视频创意流水线',
        'keywords': ['视频制作', '研究工具', '自动化']
    },
    {
        'start': 1325, 'end': 1500,
        'title': '每日简报与任务调度',
        'keywords': ['任务自动化', '时间管理', '效率工具']
    },
    {
        'start': 1500, 'end': 1680,
        'title': '安全防护与备份系统',
        'keywords': ['数据安全', '备份策略', '加密保护']
    },
    {
        'start': 1680, 'end': 2024,
        'title': '其他实用工具案例',
        'keywords': ['个人应用', '健康管理', '系统监控']
    }
]

def safe_filename(filename):
    """清理文件名中的特殊字符"""
    # 移除或替换特殊字符
    filename = re.sub(r'[\\/*?:"<>|]', "", filename)
    filename = re.sub(r'\s+', '_', filename)
    return filename[:100]  # 限制长度

def clip_video(video_path, output_path, start_time, end_time):
    """使用FFmpeg剪切视频片段"""
    try:
        # 使用绝对路径调用FFmpeg
        ffmpeg_cmd = '"C:\\Program Files\\FFmpeg\\bin\\ffmpeg.exe"'
        cmd = [
            ffmpeg_cmd,
            '-i', video_path,
            '-ss', f"{start_time}",
            '-to', f"{end_time}",
            '-c:v', 'libx264',
            '-c:a', 'aac',
            '-y',  # 覆盖输出文件
            output_path
        ]

        # 运行命令
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')

        if result.returncode == 0:
            return True
        else:
            print(f"❌ FFmpeg 错误: {result.stderr}")
            return False

    except Exception as e:
        print(f"❌ 剪辑失败: {e}")
        return False

def extract_subtitle_segment(vtt_path, output_path, start_time, end_time):
    """提取字幕片段"""
    try:
        with open(vtt_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        output_lines = []
        current_time = None
        in_range = False

        for line in lines:
            line = line.strip()
            if not line or line.startswith('WEBVTT') or line.startswith('Kind:') or line.startswith('Language:'):
                continue

            # 匹配时间戳
            time_match = re.match(r'(\d{2}:\d{2}:\d{2}\.\d{3}) --> (\d{2}:\d{2}:\d{2}\.\d{3})', line)
            if time_match:
                start_str = time_match.group(1)
                end_str = time_match.group(2)

                # 转换为秒数
                start_secs = parse_vtt_time(start_str)
                end_secs = parse_vtt_time(end_str)

                # 检查是否在范围内
                if start_time <= start_secs <= end_time or end_time <= end_secs <= end_time:
                    in_range = True
                    output_lines.append(line)
                else:
                    in_range = False
            elif in_range and line:
                output_lines.append(line)

        # 保存字幕片段
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('WEBVTT\n\n')
            f.write('\n'.join(output_lines))

        return True

    except Exception as e:
        print(f"❌ 字幕提取失败: {e}")
        return False

def parse_vtt_time(time_str):
    """将 VTT 时间戳转换为秒数"""
    parts = time_str.split(':')
    if len(parts) == 3:
        h, m, s = parts
        return int(h) * 3600 + int(m) * 60 + float(s)
    elif len(parts) == 2:
        m, s = parts
        return int(m) * 60 + float(s)
    return 0

def generate_summary(chapter):
    """为每个章节生成总结文案"""
    summaries = {
        1: {
            'title': 'OpenClaw简介与个人CRM',
            'content': '介绍OpenClaw如何改变工作生活，展示配置方法和记忆系统，以及构建个人CRM的第一步。',
            'platforms': {
                '小红书': 'OpenClaw彻底改变我的工作方式！33分钟带你了解AI助手的强大能力',
                '知乎': 'OpenClaw个人AI助手实战：从零开始构建自定义CRM系统',
                '抖音': 'OpenClaw教程：如何在30分钟内搭建自己的AI助手'
            }
        },
        2: {
            'title': 'CRM系统深度解析',
            'content': '详解如何从Gmail、日历、Fathom自动抓取联系人数据，智能过滤噪音内容，构建个性化CRM数据库。',
            'platforms': {
                '小红书': 'OpenClaw CRM实战：自动同步邮件和日历，再也不用手动录入联系人',
                '知乎': '基于OpenClaw的个人CRM：多源数据整合与智能分析',
                '抖音': '自动化CRM系统：邮件日历自动同步，效率提升10倍'
            }
        },
        3: {
            'title': 'CRM会议集成',
            'content': '展示Fathom会议笔记与CRM的无缝集成，行动项自动提取，跨平台任务同步的完整工作流。',
            'platforms': {
                '小红书': '会议自动化：OpenClaw帮你自动生成会议纪要和待办事项',
                '知乎': 'OpenClaw会议系统集成：从会议到行动项的全自动化',
                '抖音': '会议效率神器：AI自动提取待办事项，多平台同步'
            }
        },
        4: {
            'title': '个人知识库构建',
            'content': '演示如何使用RAG技术构建个人知识库，通过Telegram自动保存各种内容，建立强大的信息检索系统。',
            'platforms': {
                '小红书': 'OpenClaw知识库：AI帮你管理所有学习资料，秒级搜索任何内容',
                '知乎': '基于RAG的个人知识库：从文章到视频的智能管理',
                '抖音': '个人知识库搭建：一键保存搜索，AI帮你整理所有资料'
            }
        },
        5: {
            'title': '知识库实战演示',
            'content': '实际演示知识库的使用方法，包括X/Twitter内容抓取、智能搜索、跨内容关联分析等高级功能。',
            'platforms': {
                '小红书': 'OpenClaw知识库实战：搜索文章、分析趋势、关联内容',
                '知乎': '智能知识库系统：从信息收集到知识转化的完整链路',
                '抖音': 'AI知识库：秒速搜索分析，让你成为信息达人'
            }
        },
        6: {
            'title': '商业顾问委员会',
            'content': '展示8位AI专家并行分析业务数据的系统，每天提供商业洞察，帮助优化决策和运营。',
            'platforms': {
                '小红书': '8个AI商业顾问：每晚分析你的业务数据，提供优化建议',
                '知乎': 'OpenClaw商业顾问系统：AI驱动的多维度业务分析',
                '抖音': '商业AI顾问：数据分析+决策建议，提升企业效率'
            }
        },
        7: {
            'title': '安全委员会',
            'content': '详解安全审计系统，从攻防角度审查代码，防止提示词注入，确保数据和系统安全。',
            'platforms': {
                '小红书': 'OpenClaw安全防护：防止AI攻击，保护数据隐私',
                '知乎': 'AI助手安全体系：从代码审查到数据保护的全链路防护',
                '抖音': 'AI安全防护：教你如何防止提示词注入和恶意攻击'
            }
        },
        8: {
            'title': '社交媒体追踪器',
            'content': '展示多平台社交媒体数据追踪系统，自动分析内容表现，提供数据洞察和优化建议。',
            'platforms': {
                '小红书': '社交媒体数据分析：OpenClaw帮你监控所有平台表现',
                '知乎': 'AI驱动的社交媒体分析：从数据到洞察的智能转化',
                '抖音': '社交媒体监控：多平台数据分析，提升内容效率'
            }
        },
        9: {
            'title': '视频创意流水线',
            'content': '演示Slack触发的视频研究系统，自动生成视频大纲，研究趋势，管理创意项目。',
            'platforms': {
                '小红书': '视频制作自动化：OpenClaw帮你研究趋势生成大纲',
                '知乎': 'OpenClaw视频流水线：从想法到发布的全自动化',
                '抖音': 'AI视频创作：自动生成大纲、研究趋势，内容制作快10倍'
            }
        },
        10: {
            'title': '每日简报与任务调度',
            'content': '介绍定时任务系统和每日简报功能，自动化信息收集，优化时间管理和工作效率。',
            'platforms': {
                '小红书': '时间管理神器：OpenClaw每日简报和任务自动化',
                '知乎': 'AI驱动的任务管理系统：自动化、智能化的时间管理',
                '抖音': '效率提升：AI每日简报，自动管理所有任务和日程'
            }
        },
        11: {
            'title': '安全防护与备份系统',
            'content': '详解数据安全防护策略，加密备份系统，防止数据丢失，确保AI系统的安全稳定运行。',
            'platforms': {
                '小红书': '数据安全防护：OpenClaw帮你备份加密所有AI数据',
                '知乎': 'AI系统安全防护：从备份到加密的完整解决方案',
                '抖音': '数据安全秘籍：AI系统自动备份，数据永不丢失'
            }
        },
        12: {
            'title': '其他实用工具案例',
            'content': '展示食物日记、健康监控、API追踪等实际应用案例，体现OpenClaw在个人生活中的多样化应用。',
            'platforms': {
                '小红书': 'OpenClaw生活应用：从健康管理到系统监控的全方位解决方案',
                '知乎': 'OpenClaw个人应用生态：AI助手如何改变日常生活',
                '抖音': 'AI生活助手：健康监控、食物日记、效率工具全覆盖'
            }
        }
    }

    return summaries.get(chapter['number'], {
        'title': chapter['title'],
        'content': f"介绍{chapter['title']}的核心概念和实际应用。",
        'platforms': {
            '小红书': f'{chapter["title"]}AI工具教程',
            '知乎': f'{chapter["title"]}详细解析',
            '抖音': f'{chapter["title"]}快速入门'
        }
    })

def process_all_chapters():
    """处理所有章节的剪辑"""
    video_path = "8kNv3rjQaVA.mp4"
    vtt_path = "8kNv3rjQaVA.en.vtt"

    if not os.path.exists(video_path):
        print(f"❌ 视频文件不存在: {video_path}")
        return

    if not os.path.exists(vtt_path):
        print(f"❌ 字幕文件不存在: {vtt_path}")
        return

    # 创建输出目录
    output_dir = "youtube-clips"
    os.makedirs(output_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    chapter_dir = os.path.join(output_dir, f"openclaw_tutorial_{timestamp}")
    os.makedirs(chapter_dir, exist_ok=True)

    print(f"📁 输出目录: {chapter_dir}")

    # 处理每个章节
    for i, chapter in enumerate(chapters, 1):
        print(f"\n🎬 处理章节 {i}/12: {chapter['title']}")
        print("-" * 50)

        chapter_number = i
        chapter_safe_title = safe_filename(chapter['title'])
        chapter_dir_path = os.path.join(chapter_dir, f"chapter_{i}_{chapter_safe_title}")
        os.makedirs(chapter_dir_path, exist_ok=True)

        # 1. 剪辑视频
        video_clip_path = os.path.join(chapter_dir_path, f"{chapter_safe_title}_clip.mp4")
        print(f"1/6 剪辑视频片段... ", end="")
        if clip_video(video_path, video_clip_path, chapter['start'], chapter['end']):
            print("✅")
        else:
            print("❌")
            continue

        # 2. 提取原文字幕
        en_subtitle_path = os.path.join(chapter_dir_path, f"{chapter_safe_title}_original.srt")
        print(f"2/6 提取原文字幕... ", end="")
        if extract_subtitle_segment(vtt_path, en_subtitle_path, chapter['start'], chapter['end']):
            print("✅")
        else:
            print("❌")
            continue

        # 3. 生成总结文案
        summary = generate_summary(chapter)
        summary_path = os.path.join(chapter_dir_path, f"{chapter_safe_title}_summary.md")
        print(f"3/6 生成总结文案... ✅")

        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write(f"# {summary['title']}\n\n")
            f.write(f"## 核心内容\n{summary['content']}\n\n")
            f.write("## 多平台文案\n\n")
            for platform, content in summary['platforms'].items():
                f.write(f"### {platform}\n{content}\n\n")

        # 保存章节信息
        chapter_info = {
            'number': chapter_number,
            'title': chapter['title'],
            'time_range': f"{chapter['start']}s - {chapter['end']}s",
            'keywords': chapter['keywords'],
            'files': [
                f"{chapter_safe_title}_clip.mp4",
                f"{chapter_safe_title}_original.srt",
                f"{chapter_safe_title}_summary.md"
            ]
        }

        with open(os.path.join(chapter_dir_path, 'chapter_info.json'), 'w', encoding='utf-8') as f:
            json.dump(chapter_info, f, indent=2, ensure_ascii=False)

        print(f"✅ 章节 {chapter_number} 处理完成")
        print(f"📁 文件位置: {chapter_dir_path}")

    # 生成总览文件
    overview_path = os.path.join(chapter_dir, "README.md")
    with open(overview_path, 'w', encoding='utf-8') as f:
        f.write("# OpenClaw 教程章节剪辑\n\n")
        f.write(f"**视频**: 21 INSANE Use Cases For OpenClaw\n")
        f.write(f"**总时长**: 33:44\n")
        f.write(f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        f.write("## 章节列表\n\n")
        for i, chapter in enumerate(chapters, 1):
            f.write(f"{i}. **{chapter['title']}**\n")
            f.write(f"   - 时间: {chapter['start']}s - {chapter['end']}s\n")
            f.write(f"   - 关键词: {', '.join(chapter['keywords'])}\n")
            f.write(f"   - 目录: chapter_{i}_{safe_filename(chapter['title'])}/\n\n")

        f.write("## 文件结构\n\n")
        f.write("```\n")
        f.write(f"{chapter_dir}/\n")
        for i, chapter in enumerate(chapters, 1):
            safe_title = safe_filename(chapter['title'])
            f.write(f"├── chapter_{i}_{safe_title}/\n")
            f.write(f"│   ├── {safe_title}_clip.mp4              # 视频剪辑\n")
            f.write(f"│   ├── {safe_title}_original.srt           # 英文字幕\n")
            f.write(f"│   └── {safe_title}_summary.md            # 总结文案\n")
        f.write("└── README.md                           # 本说明文件\n")
        f.write("```\n")

    print(f"\n🎉 所有章节剪辑完成！")
    print(f"📁 总览文件: {overview_path}")
    print(f"🔗 快速访问目录: {chapter_dir}")

if __name__ == '__main__':
    process_all_chapters()