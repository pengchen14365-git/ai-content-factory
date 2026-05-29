#!/usr/bin/env python3
"""
技能包装脚本 - 将技能目录打包为可分发的格式
"""

import argparse
import os
import shutil
import json
import zipfile
from datetime import datetime
from pathlib import Path


def validate_skill(skill_dir):
    """验证技能目录结构是否完整"""
    required_files = ['SKILL.md']
    optional_files = ['scripts/', 'references/', 'assets/']

    # 检查必需文件
    for file in required_files:
        file_path = os.path.join(skill_dir, file)
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"缺少必需文件: {file}")

    # 检查可选目录
    for dir_name in optional_files:
        dir_path = os.path.join(skill_dir, dir_name)
        if not os.path.exists(dir_path):
            print(f"警告: 缺少可选目录: {dir_name}")

    print("✅ 技能目录结构验证通过")
    return True


def create_skill_package(skill_dir, output_dir=None):
    """创建技能包"""
    # 验证技能目录
    validate_skill(skill_dir)

    # 设置输出目录
    if output_dir is None:
        output_dir = os.path.dirname(skill_dir)

    # 创建技能包信息
    skill_info = {
        "name": os.path.basename(skill_dir),
        "version": "1.0.0",
        "created_date": datetime.now().isoformat(),
        "description": "有效产品需求文档创建技能",
        "author": "Claude AI",
        "files": []
    }

    # 收集文件信息
    for root, dirs, files in os.walk(skill_dir):
        for file in files:
            file_path = os.path.join(root, file)
            rel_path = os.path.relpath(file_path, skill_dir)
            skill_info["files"].append({
                "path": rel_path,
                "size": os.path.getsize(file_path),
                "modified": datetime.fromtimestamp(os.path.getmtime(file_path)).isoformat()
            })

    # 创建技能包
    package_name = f"{skill_info['name']}.skill"
    package_path = os.path.join(output_dir, package_name)

    with zipfile.ZipFile(package_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # 添加所有文件
        for root, dirs, files in os.walk(skill_dir):
            for file in files:
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, skill_dir)
                zipf.write(file_path, rel_path)

        # 添加技能包信息文件
        info_content = json.dumps(skill_info, indent=2, ensure_ascii=False)
        zipf.writestr('skill-info.json', info_content)

    print(f"✅ 技能包创建成功: {package_path}")
    print(f"📦 包含文件数: {len(skill_info['files'])}")
    print(f"📊 总大小: {sum(f['size'] for f in skill_info['files'])} bytes")

    return package_path, skill_info


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='创建技能包')
    parser.add_argument('skill_dir', help='技能目录路径')
    parser.add_argument('--output', help='输出目录 (默认为技能目录的父目录)')
    parser.add_argument('--validate-only', action='store_true', help='只验证不创建包')

    args = parser.parse_args()

    if not os.path.exists(args.skill_dir):
        print(f"❌ 技能目录不存在: {args.skill_dir}")
        return 1

    try:
        if args.validate_only:
            validate_skill(args.skill_dir)
            print("✅ 技能验证完成")
        else:
            package_path, skill_info = create_skill_package(args.skill_dir, args.output)
            print(f"\n🎉 技能包创建完成!")
            print(f"📁 包文件: {package_path}")
            print(f"📋 技能名称: {skill_info['name']}")
            print(f"🏷️  版本: {skill_info['version']}")
            print(f"📅 创建时间: {skill_info['created_date']}")
            print(f"📂 文件数: {len(skill_info['files'])}")

        return 0

    except Exception as e:
        print(f"❌ 创建技能包失败: {e}")
        return 1


if __name__ == "__main__":
    main()