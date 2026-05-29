#!/usr/bin/env python3
"""
PRD Version Tracker

This script manages PRD versions, tracks changes, and provides
version control functionality for collaborative PRD development.
"""

import argparse
import hashlib
import json
import os
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class PRDVersionTracker:
    """PRD version tracking and change management system."""

    def __init__(self):
        self.version_history = []
        self.change_categories = {
            "content": "Content Changes",
            "structure": "Structure Changes",
            "requirements": "Requirement Changes",
            "technical": "Technical Specification Changes",
            "business": "Business Logic Changes",
            "ui_ux": "User Interface/Experience Changes",
            "performance": "Performance Requirements Changes",
            "security": "Security Requirements Changes"
        }

        self.severity_levels = {
            "minor": "Minor changes that don't affect core functionality",
            "major": "Significant changes that may require re-planning",
            "critical": "Critical changes that impact major decisions",
            "addition": "New content or requirements added",
            "removal": "Content or requirements removed",
            "update": "Existing content modified"
        }

    def create_version(self, prd_file: str, version_notes: str = "",
                     change_category: str = "content", severity: str = "minor",
                     author: str = "Unknown", output_dir: Optional[str] = None) -> Dict:
        """Create a new version of the PRD file."""

        if not os.path.exists(prd_file):
            raise FileNotFoundError(f"PRD file not found: {prd_file}")

        # Generate version identifier
        version_id = self._generate_version_id(prd_file)

        # Create version directory
        if output_dir:
            version_dir = os.path.join(output_dir, f"version_{version_id}")
        else:
            version_dir = os.path.join(os.path.dirname(prd_file), f"versions_{version_id}")

        os.makedirs(version_dir, exist_ok=True)

        # Copy PRD file to version directory
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        version_filename = f"prd_{timestamp}_{version_id}.md"
        version_path = os.path.join(version_dir, version_filename)

        shutil.copy2(prd_file, version_path)

        # Calculate file hash for integrity check
        file_hash = self._calculate_file_hash(version_path)

        # Create version metadata
        version_metadata = {
            "version_id": version_id,
            "version_number": self._get_next_version_number(),
            "created_date": datetime.now().isoformat(),
            "created_by": author,
            "source_file": prd_file,
            "version_file": version_path,
            "file_hash": file_hash,
            "version_notes": version_notes,
            "change_category": change_category,
            "severity": severity,
            "file_size": os.path.getsize(version_path),
            "word_count": self._count_words(version_path)
        }

        # Add to version history
        self.version_history.append(version_metadata)

        # Save version history
        self._save_version_history(version_dir)

        # Create change summary
        change_summary = self._create_change_summary(prd_file, version_path, change_category, severity)

        # Save change summary
        summary_path = os.path.join(version_dir, f"change_summary_{version_id}.md")
        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write(change_summary)

        print(f"✅ Version {version_metadata['version_number']} created successfully")
        print(f"📁 Version file: {version_path}")
        print(f"📋 Change summary: {summary_path}")

        return version_metadata

    def compare_versions(self, version1: str, version2: str, output_file: Optional[str] = None) -> Dict:
        """Compare two PRD versions and show differences."""

        if not os.path.exists(version1):
            raise FileNotFoundError(f"Version 1 file not found: {version1}")
        if not os.path.exists(version2):
            raise FileNotFoundError(f"Version 2 file not found: {version2}")

        # Read both versions
        with open(version1, 'r', encoding='utf-8') as f:
            content1 = f.read()
        with open(version2, 'r', encoding='utf-8') as f:
            content2 = f.read()

        # Calculate differences
        comparison = {
            "version1": {
                "file": version1,
                "hash": self._calculate_file_hash(version1),
                "word_count": self._count_words(version1)
            },
            "version2": {
                "file": version2,
                "hash": self._calculate_file_hash(version2),
                "word_count": self._count_words(version2)
            },
            "comparison_date": datetime.now().isoformat(),
            "differences": self._analyze_differences(content1, content2),
            "change_summary": self._generate_change_summary(content1, content2),
            "impact_assessment": self._assess_impact(content1, content2)
        }

        # Generate comparison report
        report = self._generate_comparison_report(comparison)

        # Save report if requested
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"✅ Comparison report saved to: {output_file}")

        return comparison

    def get_version_history(self, prd_file: Optional[str] = None) -> List[Dict]:
        """Get version history for a PRD file."""
        if prd_file:
            # Filter versions for specific file
            return [v for v in self.version_history if v['source_file'] == prd_file]
        else:
            return self.version_history

    def restore_version(self, version_id: str, target_file: str, backup_original: bool = True) -> Dict:
        """Restore a specific version to the target file."""

        # Find version in history
        version = None
        for v in self.version_history:
            if v['version_id'] == version_id:
                version = v
                break

        if not version:
            raise ValueError(f"Version {version_id} not found in history")

        version_file = version['version_file']
        if not os.path.exists(version_file):
            raise FileNotFoundError(f"Version file not found: {version_file}")

        # Create backup of original if requested
        if backup_original and os.path.exists(target_file):
            backup_path = f"{target_file}.backup.{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            shutil.copy2(target_file, backup_path)
            print(f"📁 Original backed up to: {backup_path}")

        # Restore version
        shutil.copy2(version_file, target_file)

        # Update version metadata
        restore_metadata = {
            "action": "restore",
            "version_id": version_id,
            "target_file": target_file,
            "restore_date": datetime.now().isoformat(),
            "backup_file": backup_path if backup_original else None
        }

        print(f"✅ Version {version_id} restored to: {target_file}")
        return restore_metadata

    def _generate_version_id(self, file_path: str) -> str:
        """Generate unique version ID based on file path and timestamp."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_hash = hashlib.md5(file_path.encode()).hexdigest()[:8]
        return f"{timestamp}_{file_hash}"

    def _get_next_version_number(self) -> str:
        """Get the next version number."""
        if not self.version_history:
            return "1.0.0"

        # Parse existing versions
        versions = []
        for v in self.version_history:
            if 'version_number' in v:
                try:
                    major, minor, patch = map(int, v['version_number'].split('.'))
                    versions.append((major, minor, patch))
                except:
                    continue

        if versions:
            major, minor, patch = max(versions)
            patch += 1
            return f"{major}.{minor}.{patch}"
        else:
            return "1.0.0"

    def _calculate_file_hash(self, file_path: str) -> str:
        """Calculate SHA256 hash of file."""
        hash_sha256 = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha256.update(chunk)
        return hash_sha256.hexdigest()

    def _count_words(self, file_path: str) -> int:
        """Count words in file."""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            return len(content.split())

    def _save_version_history(self, version_dir: str):
        """Save version history to file."""
        history_file = os.path.join(version_dir, "version_history.json")
        with open(history_file, 'w', encoding='utf-8') as f:
            json.dump(self.version_history, f, indent=2, ensure_ascii=False)

    def _create_change_summary(self, old_file: str, new_file: str, category: str, severity: str) -> str:
        """Create change summary document."""
        summary = f"""# PRD Change Summary

**Version**: {self._get_next_version_number()}
**Created**: {datetime.now().isoformat()}
**Change Category**: {category}
**Severity Level**: {severity}
**Author**: Unknown

## Change Overview

This document summarizes the changes made to the Product Requirements Document.

### Change Details
- **File Changed**: {os.path.basename(new_file)}
- **Change Category**: {self.change_categories.get(category, category)}
- **Severity**: {self.severity_levels.get(severity, severity)}
- **Change Notes**: [Add your change notes here]

## Changes Made

### {category.title()} Changes

[Describe the specific changes made in this category]

### Impact Assessment

- **Scope Impact**: [Low/Medium/High]
- **Timeline Impact**: [Low/Medium/High]
- **Resource Impact**: [Low/Medium/High]
- **Risk Level**: [Low/Medium/High]

### Approval Status

- **Product Manager**: ________________ (Date)
- **Technical Lead**: ________________ (Date)
- **Design Lead**: ________________ (Date)
- **Stakeholder**: ________________ (Date)

## Next Steps

[Describe any next steps or actions required]

---
*This change summary was automatically generated on {datetime.now().isoformat()}*
"""
        return summary

    def _analyze_differences(self, content1: str, content2: str) -> Dict:
        """Analyze differences between two PRD versions."""
        lines1 = content1.split('\n')
        lines2 = content2.split('\n')

        differences = {
            "added_lines": [],
            "removed_lines": [],
            "modified_lines": [],
            "added_sections": [],
            "removed_sections": [],
            "total_changes": 0
        }

        # Simple line-by-line comparison
        for i, (line1, line2) in enumerate(zip(lines1, lines2)):
            if line1 != line2:
                differences["modified_lines"].append({
                    "line_number": i + 1,
                    "old_content": line1,
                    "new_content": line2
                })

        # Lines added in version 2
        if len(lines2) > len(lines1):
            for i in range(len(lines1), len(lines2)):
                differences["added_lines"].append({
                    "line_number": i + 1,
                    "content": lines2[i]
                })

        # Lines removed in version 2
        if len(lines1) > len(lines2):
            for i in range(len(lines2), len(lines1)):
                differences["removed_lines"].append({
                    "line_number": i + 1,
                    "content": lines1[i]
                })

        # Count total changes
        differences["total_changes"] = (
            len(differences["added_lines"]) +
            len(differences["removed_lines"]) +
            len(differences["modified_lines"])
        )

        return differences

    def _generate_change_summary(self, content1: str, content2: str) -> Dict:
        """Generate change summary with analysis."""
        categories = {
            "content": 0,
            "structure": 0,
            "requirements": 0,
            "technical": 0,
            "business": 0,
            "ui_ux": 0,
            "performance": 0,
            "security": 0
        }

        # Analyze change categories based on content
        content_lower = content2.lower()

        # Simple keyword-based categorization
        if any(keyword in content_lower for keyword in ['user', 'customer', 'interface']):
            categories["ui_ux"] += 1
        if any(keyword in content_lower for keyword in ['api', 'database', 'infrastructure']):
            categories["technical"] += 1
        if any(keyword in content_lower for keyword in ['business', 'revenue', 'profit']):
            categories["business"] += 1
        if any(keyword in content_lower for keyword in ['requirement', 'specification']):
            categories["requirements"] += 1
        if any(keyword in content_lower for keyword in ['performance', 'speed', 'scalability']):
            categories["performance"] += 1
        if any(keyword in content_lower for keyword in ['security', 'auth', 'privacy']):
            categories["security"] += 1

        return {
            "categories": categories,
            "total_changes": sum(categories.values()),
            "primary_category": max(categories, key=categories.get) if any(categories.values()) else "content"
        }

    def _assess_impact(self, content1: str, content2: str) -> Dict:
        """Assess the impact of changes."""
        word_count1 = len(content1.split())
        word_count2 = len(content2.split())
        word_change = abs(word_count2 - word_count1)

        impact = {
            "size_change": word_change,
            "size_change_percent": (word_change / word_count1) * 100 if word_count1 > 0 else 0,
            "impact_level": "Low",
            "risk_level": "Low",
            "requires_replanning": False,
            "requires_retesting": False
        }

        # Determine impact level
        if word_change > 100:
            impact["impact_level"] = "High"
            impact["risk_level"] = "Medium"
            impact["requires_replanning"] = True
        elif word_change > 50:
            impact["impact_level"] = "Medium"
            impact["risk_level"] = "Low"
            impact["requires_retesting"] = True

        return impact

    def _generate_comparison_report(self, comparison: Dict) -> str:
        """Generate comprehensive comparison report."""
        report = f"""# PRD Version Comparison Report

**Comparison Date**: {comparison['comparison_date']}
**Version 1**: {comparison['version1']['file']}
**Version 2**: {comparison['version2']['file']}

## Summary

- **Total Changes**: {comparison['differences']['total_changes']}
- **Word Count Change**: {comparison['impact_assessment']['size_change']} words ({comparison['impact_assessment']['size_change_percent']:.1f}%)
- **Impact Level**: {comparison['impact_assessment']['impact_level']}
- **Risk Level**: {comparison['impact_assessment']['risk_level']}

## Detailed Differences

### Added Lines ({len(comparison['differences']['added_lines'])})
"""
        for line in comparison['differences']['added_lines'][:10]:  # Show first 10
            report += f"- Line {line['line_number']}: {line['content'][:100]}...\n"

        report += f"""
### Removed Lines ({len(comparison['differences']['removed_lines'])})
"""
        for line in comparison['differences']['removed_lines'][:10]:  # Show first 10
            report += f"- Line {line['line_number']}: {line['content'][:100]}...\n"

        report += f"""
### Modified Lines ({len(comparison['differences']['modified_lines'])})
"""
        for change in comparison['differences']['modified_lines'][:10]:  # Show first 10
            report += f"- Line {change['line_number']}:\n"
            report += f"  Old: {change['old_content'][:100]}...\n"
            report += f"  New: {change['new_content'][:100]}...\n"

        report += f"""
## Change Analysis

### Change Categories
"""
        for category, count in comparison['change_summary']['categories'].items():
            if count > 0:
                report += f"- {category.title()}: {count} changes\n"

        report += f"""
### Primary Change Category: {comparison['change_summary']['primary_category'].title()}

## Impact Assessment

### Size Impact
- Word count changed by {comparison['impact_assessment']['size_change']} words
- Percentage change: {comparison['impact_assessment']['size_change_percent']:.1f}%

### Impact Level
- **Overall Impact**: {comparison['impact_assessment']['impact_level']}
- **Risk Level**: {comparison['impact_assessment']['risk_level']}

### Required Actions
- Requires Re-planning: {comparison['impact_assessment']['requires_replanning']}
- Requires Re-testing: {comparison['impact_assessment']['requires_retesting']}

## Recommendations

{self._generate_recommendations(comparison)}

---
*This comparison report was generated on {datetime.now().isoformat()}*
"""
        return report

    def _generate_recommendations(self, comparison: Dict) -> str:
        """Generate recommendations based on comparison."""
        recommendations = []

        impact = comparison['impact_assessment']

        if impact['requires_replanning']:
            recommendations.append("🔄 **Re-planning Required**: The changes are significant enough to require project replanning.")

        if impact['requires_retesting']:
            recommendations.append("🧪 **Re-testing Required**: The changes require comprehensive testing to ensure functionality.")

        if impact['impact_level'] == 'High':
            recommendations.append("⚠️ **High Impact Changes**: These changes significantly affect the project scope and may require stakeholder approval.")

        if len(comparison['differences']['added_lines']) > 50:
            recommendations.append("➕ **Large Addition**: Consider if all new requirements are necessary or if some can be deferred.")

        if len(comparison['differences']['removed_lines']) > 30:
            recommendations.append("➖ **Significant Removal**: Ensure that removed requirements won't impact critical functionality.")

        if not recommendations:
            recommendations.append("✅ **Minor Changes**: These changes appear to be minor updates that shouldn't significantly impact the project.")

        return "\n".join(recommendations)


def main():
    """Main function for command-line interface."""
    parser = argparse.ArgumentParser(description='PRD Version Tracker')

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Create version command
    create_parser = subparsers.add_parser('create-version', help='Create a new version')
    create_parser.add_argument('file', help='PRD file to version')
    create_parser.add_argument('--notes', default='', help='Version notes')
    create_parser.add_argument('--category', choices=list(PRDVersionTracker().change_categories.keys()),
                             default='content', help='Change category')
    create_parser.add_argument('--severity', choices=list(PRDVersionTracker().severity_levels.keys()),
                             default='minor', help='Change severity')
    create_parser.add_argument('--author', default='Unknown', help='Author name')
    create_parser.add_argument('--output-dir', help='Output directory for versions')

    # Compare versions command
    compare_parser = subparsers.add_parser('compare-versions', help='Compare two versions')
    compare_parser.add_argument('version1', help='First version file')
    compare_parser.add_argument('version2', help='Second version file')
    compare_parser.add_argument('--output', help='Output file for comparison report')

    # Version history command
    history_parser = subparsers.add_parser('version-history', help='Show version history')
    history_parser.add_argument('--file', help='Show history for specific file')

    # Restore version command
    restore_parser = subparsers.add_parser('restore-version', help='Restore a version')
    restore_parser.add_argument('version_id', help='Version ID to restore')
    restore_parser.add_argument('target_file', help='Target file to restore to')
    restore_parser.add_argument('--no-backup', action='store_true', help='Skip backup')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    tracker = PRDVersionTracker()

    try:
        if args.command == 'create-version':
            version = tracker.create_version(
                args.file,
                args.notes,
                args.category,
                args.severity,
                args.author,
                args.output_dir
            )
            print(f"✅ Version {version['version_number']} created successfully")

        elif args.command == 'compare-versions':
            comparison = tracker.compare_versions(args.version1, args.version2, args.output)
            print(f"✅ Comparison completed between {args.version1} and {args.version2}")
            if args.output:
                print(f"📋 Report saved to: {args.output}")

        elif args.command == 'version-history':
            history = tracker.get_version_history(args.file)
            if history:
                print(f"Version History ({len(history)} versions):")
                for version in history[-10:]:  # Show last 10 versions
                    print(f"- {version['version_number']}: {version['created_date'][:10]} "
                          f"({version['change_category']}, {version['severity']})")
            else:
                print("No version history found")

        elif args.command == 'restore-version':
            restore_metadata = tracker.restore_version(
                args.version_id,
                args.target_file,
                not args.no_backup
            )
            print(f"✅ Version {args.version_id} restored to {args.target_file}")

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    main()