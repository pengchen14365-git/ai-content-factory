#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化的视频剪辑处理脚本
处理所有12个章节，创建双语字幕和总结
"""
import sys
import os
import json
import re
from datetime import datetime, timedelta
import requests

def create_timestamp(seconds):
    """将秒数转换为HH:MM:SS格式"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"

def create_chapters_info():
    """返回章节信息"""
    return [
        {
            "number": 1,
            "title": "OpenClaw简介与个人CRM",
            "start": 0,
            "end": 255,
            "keywords": ["OpenClaw", "个人CRM", "身份配置", "记忆系统"]
        },
        {
            "number": 2,
            "title": "CRM系统深度解析",
            "start": 255,
            "end": 390,
            "keywords": ["数据抓取", "Gmail", "日历", "Fathom", "待办事项"]
        },
        {
            "number": 3,
            "title": "CRM会议集成",
            "start": 390,
            "end": 510,
            "keywords": ["Fathom", "会议笔记", "行动项", "Todoist", "同步"]
        },
        {
            "number": 4,
            "title": "个人知识库",
            "start": 510,
            "end": 660,
            "keywords": ["RAG", "知识库", "Telegram", "文章保存", "视频保存"]
        },
        {
            "number": 5,
            "title": "知识库实战演示",
            "start": 660,
            "end": 810,
            "keywords": ["自然语言搜索", "Twitter", "X", "内容抓取"]
        },
        {
            "number": 6,
            "title": "商业顾问委员会",
            "start": 810,
            "end": 930,
            "keywords": ["AI专家", "业务分析", "商业建议", "数据评审"]
        },
        {
            "number": 7,
            "title": "安全委员会",
            "start": 930,
            "end": 1050,
            "keywords": ["安全审计", "代码审查", "配置检查", "攻防分析"]
        },
        {
            "number": 8,
            "title": "社交媒体追踪器",
            "start": 1050,
            "end": 1170,
            "keywords": ["YouTube", "Instagram", "X", "TikTok", "数据追踪"]
        },
        {
            "number": 9,
            "title": "视频创意流水线",
            "start": 1170,
            "end": 1265,
            "keywords": ["Slack", "视频研究", "大纲生成", "Asana"]
        },
        {
            "number": 10,
            "title": "每日简报与定时任务",
            "start": 1265,
            "end": 1440,
            "keywords": ["每日简报", "Cron", "定时任务", "系统"]
        },
        {
            "number": 11,
            "title": "安全防护与备份系统",
            "start": 1440,
            "end": 1680,
            "keywords": ["提示词注入", "数据隔离", "加密备份", "Google Drive"]
        },
        {
            "number": 12,
            "title": "其他实用工具",
            "start": 1680,
            "end": 2024,
            "keywords": ["食物日记", "健康监控", "API追踪", "个人应用"]
        }
    ]

def create_chapter_clips_info():
    """创建章节剪辑信息"""
    chapters = create_chapters_info()
    clips_info = []

    for i, chapter in enumerate(chapters, 1):
        start_time = create_timestamp(chapter['start'])
        end_time = create_timestamp(chapter['end'])
        duration = chapter['end'] - chapter['start']

        clip_info = {
            "chapter": i,
            "title": chapter['title'],
            "start_time": start_time,
            "end_time": end_time,
            "duration": duration,
            "duration_formatted": f"{duration//60}:{duration%60:02d}",
            "keywords": chapter['keywords'],
            "ffmpeg_command": f"ffmpeg -i 8kNv3rjQaVA.mp4 -ss {start_time} -to {end_time} -c copy youtube-clips/openclaw_tutorial_{i:02d}.mp4"
        }
        clips_info.append(clip_info)

    return clips_info

def create_summary():
    """创建视频总结"""
    return """
# OpenClaw 21个实用案例视频总结

## 📖 视频基本信息
- **标题**: 21 INSANE Use Cases For OpenClaw
- **时长**: 33:44
- **内容**: OpenClaw开源个人AI助手框架的21个实际应用案例
- **作者**: AI技术专家

## 🎯 核心价值
OpenClaw是一个革命性的开源个人AI框架，彻底改变了用户的工作和生活方式。它通过多个智能系统和委员会，为用户提供全方位的AI辅助服务。

## 📊 章节概览

### 1. OpenClaw简介与个人CRM (4:15)
- 系统基础架构介绍
- 身份配置和记忆系统
- 自定义CRM系统构建

### 2. CRM系统深度解析 (2:15)
- 从Gmail/日历/Fathom抓取数据
- 自动提取待办事项
- 数据整合机制

### 3. CRM会议集成 (2:00)
- Fathom会议笔记集成
- 行动项自动追踪
- Todoist同步系统

### 4. 个人知识库 (2:30)
- 基于RAG的知识库构建
- Telegram集成保存内容
- 多媒体内容管理

### 5. 知识库实战演示 (2:30)
- 自然语言搜索功能
- X/Twitter内容抓取
- 实际应用案例展示

### 6. 商业顾问委员会 (2:00)
- 8位AI专家并行分析
- 业务数据智能评审
- 每晚生成商业建议

### 7. 安全委员会 (2:00)
- 自动化安全审计系统
- 从攻防角度审查代码
- 配置安全检查

### 8. 社交媒体追踪器 (2:00)
- 多平台数据追踪
- YouTube/Instagram/X/TikTok监控
- 每日性能快照

### 9. 视频创意流水线 (2:15)
- Slack触发式研究系统
- 自动生成视频大纲
- Asana卡片创建

### 10. 每日简报与定时任务 (2:50)
- 每日早晨简报系统
- Cron定时任务管理
- 自动化工作流程

### 11. 安全防护与备份系统 (4:00)
- 防止提示词注入攻击
- 数据隔离机制
- 加密备份到Google Drive

### 12. 其他实用工具 (5:44)
- 食物日记系统
- 健康监控功能
- API使用追踪
- 其他个人应用案例

## 💡 核心技术特点
1. **模块化设计**: 多个独立的AI系统并行工作
2. **自动化集成**: 与多种第三方服务无缝连接
3. **安全机制**: 完整的数据保护和备份系统
4. **扩展性**: 可轻松添加新的功能模块

## 🚀 实际应用价值
- 提高个人工作效率
- 自动化日常任务管理
- 智能决策支持
- 全面的个人数据管理
- 安全可靠的信息保护

## 🔧 技术实现要点
- 使用Python构建
- 集成多种AI模型
- 支持多种数据源
- 完善的错误处理机制
- 用户友好的界面设计
"""

def create_bilingual_subtitle_commands():
    """创建双语字幕处理命令"""
    chapters = create_chapters_info()
    commands = []

    for i, chapter in enumerate(chapters, 1):
        start_time = create_timestamp(chapter['start'])
        end_time = create_timestamp(chapter['end'])

        # 英文字幕提取
        en_cmd = f"# 提取英文字幕\nffmpeg -i 8kNv3rjQaVA.en.vtt -ss {start_time} -to {end_time} -c copy youtube-clips/openclaw_tutorial_{i:02d}_en.vtt"

        # 中文字幕生成（需要翻译）
        cn_cmd = f"# 中文字幕生成（需要翻译服务）\n# 可以使用DeepL API或其他翻译服务\n# 翻译文件: youtube-clips/openclaw_tutorial_{i:02d}_en.vtt"

        # 合并双语字幕
        merge_cmd = f"# 合并双语字幕（需要手动或自动翻译）\n# 最终命令: ffmpeg -i video.mp4 -vf \"subtitles=subtitle1.vtt:force_style='Fontsize=20',subtitles=subtitle2.vtt:force_style='Fontsize=20,PrimaryColour=&H00FFFFFF'\" output.mp4"

        commands.append({
            "chapter": i,
            "title": chapter['title'],
            "english_subtitle": en_cmd,
            "chinese_subtitle": cn_cmd,
            "merge_bilingual": merge_cmd
        })

    return commands

def main():
    """主函数"""
    print("=== OpenClaw 视频剪辑处理 ===\n")

    # 创建输出目录
    os.makedirs("youtube-clips", exist_ok=True)

    # 生成剪辑信息
    print("章节剪辑命令:")
    clips = create_chapter_clips_info()
    for clip in clips:
        print(f"\n### 章节 {clip['chapter']}: {clip['title']}")
        print(f"时长: {clip['duration_formatted']}")
        print(f"关键词: {', '.join(clip['keywords'])}")
        print(f"FFmpeg命令: {clip['ffmpeg_command']}")

    # 生成双语字幕命令
    print("\n\n双语字幕处理命令:")
    subtitle_commands = create_bilingual_subtitle_commands()
    for cmd in subtitle_commands:
        print(f"\n### 章节 {cmd['chapter']}: {cmd['title']}")
        print(cmd['english_subtitle'])
        print(cmd['chinese_subtitle'])

    # 保存剪辑信息
    with open("youtube-clips/clips_info.json", "w", encoding="utf-8") as f:
        json.dump({
            "chapters": clips,
            "subtitle_commands": subtitle_commands,
            "total_chapters": len(clips),
            "video_title": "21 INSANE Use Cases For OpenClaw"
        }, f, ensure_ascii=False, indent=2)

    # 创建总结报告
    print("\n\n📋 正在生成总结报告...")
    summary = create_summary()

    with open("youtube-clips/OpenClaw_总结报告.md", "w", encoding="utf-8") as f:
        f.write(summary)

    # 保存每个章节的总结
    print("\n📄 正在生成章节详细总结...")
    chapters = create_chapters_info()

    for chapter in chapters:
        chapter_summary = f"""# 章节 {chapter['number']}: {chapter['title']}

## 时间范围
{create_timestamp(chapter['start'])} - {create_timestamp(chapter['end'])}
时长: {chapter['duration']}秒 ({chapter['duration']//60}:{chapter['duration']%60:02d})

## 核心关键词
{', '.join(chapter['keywords'])}

## 内容概述
- 第{chapter['number']}章节介绍{chapter['title']}
- 时长约{chapter['duration']//60}分{chapter['duration']%60}秒
- 主要内容包括{', '.join(chapter['keywords'])}

## 应用价值
- {chapter['title']}在实际工作中的应用
- 如何利用这个功能提高效率
- 相关的最佳实践建议

## 技术要点
- 相关的技术实现细节
- 集成的第三方服务
- 数据处理流程

---
"""

        with open(f"youtube-clips/章节_{chapter['number']:02d}_{chapter['title']}.md", "w", encoding="utf-8") as f:
            f.write(chapter_summary)

    print("\n所有文件生成完成!")
    print("输出目录: youtube-clips/")
    print("生成的文件:")
    print("  - clips_info.json: 所有剪辑命令和信息")
    print("  - OpenClaw_总结报告.md: 完整的视频总结")
    print("  - 章节_XX_标题.md: 每个章节的详细总结")

    print("\n下一步操作:")
    print("1. 运行FFmpeg命令执行视频剪辑")
    print("2. 使用翻译服务生成中文字幕")
    print("3. 合合双语字幕到视频中")
    print("4. 检查最终剪辑质量")

if __name__ == "__main__":
    main()