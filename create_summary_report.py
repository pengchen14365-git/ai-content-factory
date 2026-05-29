#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
创建章节总结报告
由于FFmpeg权限问题，先创建详细的章节总结报告
"""
import sys
import io
import json
import os
from datetime import datetime

# Set UTF-8 encoding for Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

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

def safe_filename(filename):
    """清理文件名中的特殊字符"""
    import re
    filename = re.sub(r'[\\/*?:"<>|]', "", filename)
    filename = re.sub(r'\s+', '_', filename)
    return filename[:100]

def create_comprehensive_report():
    """创建综合报告"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = "youtube-clips"
    os.makedirs(output_dir, exist_ok=True)

    report_dir = os.path.join(output_dir, f"openclaw_report_{timestamp}")
    os.makedirs(report_dir, exist_ok=True)

    print(f"📁 输出目录: {report_dir}")

    # 创建主要报告文件
    readme_path = os.path.join(report_dir, "README.md")
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write("# 🎬 OpenClaw 教程章节剪辑报告\n\n")
        f.write(f"**视频**: 21 INSANE Use Cases For OpenClaw\n")
        f.write(f"**总时长**: 33:44\n")
        f.write(f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"**配置**: 所有章节 + 中文翻译总结\n\n")

        f.write("## 📋 章节总览\n\n")

        # 创建章节目录
        chapters_dir = os.path.join(report_dir, "chapters")
        os.makedirs(chapters_dir, exist_ok=True)

        for i, chapter in enumerate(chapters, 1):
            f.write(f"### {i}. {chapter['title']}\n\n")
            f.write(f"- **时长**: {chapter['end'] - chapter['start']} 秒 ({(chapter['end'] - chapter['start'])//60}:{(chapter['end'] - chapter['start'])%60:02d})\n")
            f.write(f"- **关键词**: {', '.join(chapter['keywords'])}\n")
            f.write(f"- **时间范围**: {chapter['start']}s - {chapter['end']}s\n\n")

            # 创建单独的章节文件
            chapter_summary = generate_summary(chapter)
            chapter_filename = f"chapter_{i}_{safe_filename(chapter['title'])}.md"
            chapter_path = os.path.join(chapters_dir, chapter_filename)

            with open(chapter_path, 'w', encoding='utf-8') as chapter_f:
                chapter_f.write(f"# 📖 {chapter['title']}\n\n")
                chapter_f.write(f"**编号**: {i}\n")
                chapter_f.write(f"**时长**: {chapter['end'] - chapter['start']} 秒\n")
                chapter_f.write(f"**关键词**: {', '.join(chapter['keywords'])}\n\n")
                chapter_f.write(f"## 🎯 核心内容\n\n{chapter_summary['content']}\n\n")

                chapter_f.write("## 📱 多平台发布文案\n\n")
                for platform, content in chapter_summary['platforms'].items():
                    chapter_f.write(f"### {platform}\n")
                    chapter_f.write(f"**标题**: {content}\n")
                    chapter_f.write(f"**适用**: {platform}、YouTube Shorts、B站等平台\n\n")

                chapter_f.write("## 🔗 下载链接\n\n")
                chapter_f.write(f"视频片段: `chapter_{i}_{safe_filename(chapter['title'])}_clip.mp4`\n")
                chapter_f.write(f"英文字幕: `chapter_{i}_{safe_filename(chapter['title'])}_original.srt`\n")
                chapter_f.write(f"总结文案: `chapter_{i}_{safe_filename(chapter['title'])}_summary.md`\n\n")

            f.write(f"📄 详细说明: [chapters/{chapter_filename}](chapters/{chapter_filename})\n\n")

        f.write("## 🎯 视频剪辑信息\n\n")
        f.write("### 章节分割策略\n\n")
        f.write("- 每个章节控制在 2-5 分钟内，适合短视频传播\n")
        f.write("- 基于内容主题自然分割，确保信息完整性\n")
        f.write("- 提供中英双语字幕选项，满足不同观众需求\n\n")

        f.write("### 字幕格式\n\n")
        f.write("- **原文字幕**: SRT格式，时间码同步\n")
        f.write("- **双语字幕**: 中文+英文，位置对齐\n")
        f.write("- **硬字幕选项**: 可直接烧录到视频上\n\n")

        f.write("### 文件结构\n\n")
        f.write("```\n")
        f.write(f"📁 {timestamp}/\n")
        f.write("├── 📄 README.md                           # 主报告文件\n")
        f.write("├── 📁 chapters/                           # 章节详细报告\n")
        for i, chapter in enumerate(chapters, 1):
            safe_title = safe_filename(chapter['title'])
            f.write(f"│   ├── 📄 chapter_{i}_{safe_title}.md    # 章节详细报告\n")
        f.write("└── 📁 video_files/                        # 视频文件 (需要手动创建)\n")
        f.write("    ├── 📹 chapter_1_*.mp4                 # 各章节视频文件\n")
        f.write("    ├── 📄 chapter_1_*.srt                 # 各章节字幕文件\n")
        f.write("    └── 📄 chapter_1_*.md                  # 各章节总结文案\n")
        f.write("```\n")

        f.write("## 🚀 使用建议\n\n")
        f.write("### 推荐发布平台\n\n")
        f.write("1. **Bilibili**: 发布完整系列，每个章节单独成片\n")
        f.write("2. **抖音/快手**: 选择精华章节，制作 15-60 短视频\n")
        f.write("3. **YouTube**: 发布双语版本，吸引国际观众\n")
        f.write("4. **知乎专栏**: 发布技术解析文章，配合视频教程\n\n")

        f.write("### 内容优化建议\n\n")
        f.write("- 添加章节开头和结尾的转场效果\n")
        f.write("- 为每个章节添加特色封面和简介\n")
        f.write("- 在描述中提供相关资源和下载链接\n")
        f.write("- 定期更新内容，反映 OpenClaw 的新功能\n\n")

        f.write("## 📞 技术支持\n\n")
        f.write("如果需要帮助进行视频剪辑或有其他技术问题，请查看脚本中的 FFmpeg 配置或联系技术支持。\n\n")

    # 创建章节信息JSON文件
    chapters_info = []
    for i, chapter in enumerate(chapters, 1):
        chapters_info.append({
            'number': i,
            'title': chapter['title'],
            'start_time': chapter['start'],
            'end_time': chapter['end'],
            'duration': chapter['end'] - chapter['start'],
            'keywords': chapter['keywords'],
            'summary': generate_summary(chapter)['content'],
            'platforms': generate_summary(chapter)['platforms']
        })

    json_path = os.path.join(report_dir, "chapters_info.json")
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(chapters_info, f, indent=2, ensure_ascii=False)

    print(f"\n🎉 综合报告创建完成！")
    print(f"📁 主报告: {readme_path}")
    print(f"📊 数据文件: {json_path}")
    print(f"📄 章节详细报告: {chapters_dir}")

    # 显示章节统计
    total_duration = sum(chapter['end'] - chapter['start'] for chapter in chapters)
    print(f"\n📈 统计信息:")
    print(f"   - 总章节数: {len(chapters)}")
    print(f"   - 总时长: {total_duration//60}:{total_duration%60:02d}")
    print(f"   - 平均每章: {total_duration//len(chapters)} 秒 ({(total_duration//len(chapters))//60}:{(total_duration//len(chapters))%60:02d})")

if __name__ == '__main__':
    create_comprehensive_report()