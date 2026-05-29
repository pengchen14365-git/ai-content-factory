#!/usr/bin/env python3
"""
Product Requirements Document (PRD) Improver

This script analyzes existing PRD files and suggests improvements
based on best practices, quality standards, and common pitfalls.
"""

import argparse
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class PRDImprover:
    """PRD improvement tool with targeted enhancement suggestions."""

    def __init__(self):
        self.improvement_categories = {
            "structure": {
                "title": "Document Structure Improvements",
                "weight": 0.2,
                "checks": self._structure_checks
            },
            "clarity": {
                "title": "Clarity and Readability Improvements",
                "weight": 0.25,
                "checks": self._clarity_checks
            },
            "completeness": {
                "title": "Completeness Improvements",
                "weight": 0.2,
                "checks": self._completeness_checks
            },
            "consistency": {
                "title": "Consistency Improvements",
                "weight": 0.15,
                "checks": self._consistency_checks
            },
            "actionability": {
                "title": "Actionability Improvements",
                "weight": 0.2,
                "checks": self._actionability_checks
            }
        }

        self.common_issues = {
            "vague_language": {
                "patterns": [r'\b(some|several|various|many|few|often|sometimes|approximately|about)\b'],
                "suggestions": "Replace vague terms with specific, measurable language"
            },
            "long_sentences": {
                "patterns": [r'[.!?]\s*[A-Z][^.]{25,}[.!?]'],
                "suggestions": "Break long sentences into shorter, clearer ones"
            },
            "passive_voice": {
                "patterns": [r'\b(am|is|are|was|were|been|be)\s+\w+(?:\s+by|\s+to\s+\w+)'],
                "suggestions": "Use active voice for clearer, more direct requirements"
            },
            "unc Acceptance Criteria": {
                "patterns": [r'- \[ \] .*[^\d\%\<\>].*'],
                "suggestions": "Acceptance criteria should be specific and measurable"
            }
        }

    def improve_prd(self, prd_file: str, focus_area: Optional[str] = None,
                   output_file: Optional[str] = None, backup: bool = True) -> Dict:
        """Improve a PRD file with targeted enhancements."""

        if not os.path.exists(prd_file):
            raise FileNotFoundError(f"PRD file not found: {prd_file}")

        # Create backup if requested
        if backup:
            backup_file = f"{prd_file}.backup.{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            with open(prd_file, 'r', encoding='utf-8') as src, open(backup_file, 'w', encoding='utf-8') as dst:
                dst.write(src.read())
            print(f"Backup created: {backup_file}")

        # Read the PRD file
        with open(prd_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Perform improvements
        improvements = {
            "original_file": prd_file,
            "backup_file": backup_file if backup else None,
            "improvement_date": datetime.now().isoformat(),
            "focus_area": focus_area,
            "categories": {}
        }

        # Apply improvements based on focus area or all areas
        if focus_area:
            if focus_area in self.improvement_categories:
                improvements["categories"][focus_area] = self._apply_improvements(
                    content, focus_area
                )
        else:
            for category in self.improvement_categories:
                improvements["categories"][category] = self._apply_improvements(
                    content, category
                )

        # Generate improved content
        improved_content = content
        for category, data in improvements["categories"].items():
            if data["improvements"]:
                improved_content = data["improved_content"]

        # Write improved content
        if output_file:
            final_file = output_file
        else:
            final_file = prd_file

        with open(final_file, 'w', encoding='utf-8') as f:
            f.write(improved_content)

        improvements["final_file"] = final_file

        return improvements

    def _apply_improvements(self, content: str, category: str) -> Dict:
        """Apply improvements for a specific category."""
        checks = self.improvement_categories[category]["checks"]
        improvements = []
        improved_content = content

        for check_func in checks:
            result = check_func(improved_content)
            if result["issues_found"]:
                improvements.append(result)
                improved_content = result["improved_content"]

        return {
            "category": category,
            "improvements": improvements,
            "issues_found": len(improvements) > 0,
            "improved_content": improved_content
        }

    def _structure_checks(self, content: str) -> Dict:
        """Check and improve document structure."""
        issues = []
        improved = content

        # Check for proper section hierarchy
        sections = re.findall(r'^##\s+(.+)$', improved, re.MULTILINE)
        subsections = re.findall(r'^###\s+(.+)$', improved, re.MULTILINE)

        if sections and not subsections:
            # Add subsections to main sections
            for section in sections[:3]:  # First 3 sections as example
                section_pattern = re.escape(section)
                section_match = re.search(rf'^##\s*{section_pattern}$', improved, re.MULTILINE)
                if section_match:
                    section_pos = section_match.end()
                    next_section = re.search(r'^##\s+.+$', improved[section_pos:], re.MULTILINE)
                    if next_section:
                        next_pos = section_pos + next_section.start()
                        subsection = f"\n### Key Points\n\n- Main point 1\n- Main point 2\n- Main point 3\n"
                        improved = improved[:next_pos] + subsection + improved[next_pos:]
                        issues.append({
                            "type": "added_subsections",
                            "description": f"Added subsection to '{section}' section",
                            "location": "section_hierarchy"
                        })

        # Check for consistent formatting
        checklists = re.findall(r'^- \[ \] ', improved, re.MULTILINE)
        if len(checklists) > 5:  # Many checklists should be consistent
            improved = re.sub(
                r'- \[ \] .*$',
                lambda m: '- [ ] ' + m.group(0)[5:].strip(),
                improved,
                flags=re.MULTILINE
            )
            issues.append({
                "type": "formatting_standardization",
                "description": "Standardized checklist formatting",
                "location": "formatting"
            })

        return {
            "check_type": "structure",
            "issues_found": len(issues) > 0,
            "issues": issues,
            "improved_content": improved
        }

    def _clarity_checks(self, content: str) -> Dict:
        """Check and improve clarity and readability."""
        issues = []
        improved = content

        # Check and fix long sentences
        long_sentences = re.findall(r'[.!?]\s*[A-Z][^.]{25,}[.!?]', improved)
        if long_sentences:
            # Simple sentence breaking
            improved = re.sub(
                r'([.!?])\s*([A-Z][^.]{20,})',
                lambda m: m.group(1) + ' ' + m.group(2).replace(' and ', '. ') + m.group(1),
                improved
            )
            issues.append({
                "type": "long_sentences",
                "description": "Broke down long sentences for better readability",
                "location": "sentence_structure"
            })

        # Check for passive voice
        passive_patterns = re.findall(r'\b(am|is|are|was|were|been|be)\s+\w+(?:\s+by|\s+to\s+\w+)', improved, re.IGNORECASE)
        if passive_patterns:
            # Simple passive to active conversion
            improved = re.sub(
                r'\b(am|is|are|was|were|been|be)\s+(\w+)(?:\s+by\s+(\w+))?',
                lambda m: f"{m.group(3) if m.group(3) else 'We'} {m.group(2)}{' by ' + m.group(3) if m.group(3) else ''}" if m.group(3) else f"{m.group(3) if m.group(3) else 'You'} {m.group(2)}",
                improved,
                flags=re.IGNORECASE
            )
            issues.append({
                "type": "passive_voice",
                "description": "Converted passive voice to active voice",
                "location": "voice"
            })

        return {
            "check_type": "clarity",
            "issues_found": len(issues) > 0,
            "issues": issues,
            "improved_content": improved
        }

    def _completeness_checks(self, content: str) -> Dict:
        """Check and improve completeness."""
        issues = []
        improved = content

        # Check for missing key sections
        required_sections = [
            "Success Metrics", "Risk Assessment", "Dependencies", "Assumptions"
        ]

        for section in required_sections:
            if section not in improved:
                # Add missing section
                if section == "Risk Assessment":
                    section_content = f"\n## {section}\n\n- **Technical Risks**: [Identify potential technical challenges]\n- **Market Risks**: [Identify potential market challenges]\n- **Resource Risks**: [Identify potential resource constraints]\n- **Mitigation Strategies**: [How to address each risk]\n"
                elif section == "Dependencies":
                    section_content = f"\n## {section}\n\n- **External Dependencies**: [List external systems/services]\n- **Internal Dependencies**: [List internal team dependencies]\n- **Timeline Dependencies**: [Dependencies on other projects]\n"
                elif section == "Assumptions":
                    section_content = f"\n## {section}\n\n- **Technical Assumptions**: [Assumptions about technology]\n- **Business Assumptions**: [Assumptions about market/users]\n- **Resource Assumptions**: [Assumptions about available resources]\n"
                else:  # Success Metrics
                    section_content = f"\n## {section}\n\n- **Business Metrics**: [Key business indicators]\n- **User Metrics**: [Key user engagement metrics]\n- **Technical Metrics**: [Key technical performance metrics]\n- **Timeline**: [Measurement schedule]\n"

                # Insert before Acceptance Criteria
                ac_match = re.search(r'^##\s*Acceptance Criteria$', improved, re.MULTILINE)
                if ac_match:
                    improved = improved[:ac_match.start()] + section_content + improved[ac_match.start():]
                    issues.append({
                        "type": "missing_section",
                        "description": f"Added missing '{section}' section",
                        "location": "section_completeness"
                    })

        return {
            "check_type": "completeness",
            "issues_found": len(issues) > 0,
            "issues": issues,
            "improved_content": improved
        }

    def _consistency_checks(self, content: str) -> Dict:
        """Check and improve consistency."""
        issues = []
        improved = content

        # Check for inconsistent terminology
        if 'user' in improved.lower() and 'customer' in improved.lower():
            # Standardize to 'user' for consistency
            improved = re.sub(r'\bcustomer\b', 'user', improved, flags=re.IGNORECASE)
            issues.append({
                "type": "terminology_standardization",
                "description": "Standardized terminology to 'user'",
                "location": "terminology"
            })

        # Check for inconsistent priority formatting
        priorities = re.findall(r'- \[ \] .*[Hh]igh|[Mm]edium|[Ll]ow', improved)
        if priorities:
            # Standardize priority formatting
            improved = re.sub(
                r'- \[ \] .*([Hh]igh|[Mm]edium|[Ll]ow)',
                lambda m: f"- [ ] [{m.group(1).upper()} Priority]",
                improved,
                flags=re.IGNORECASE
            )
            issues.append({
                "type": "priority_formatting",
                "description": "Standardized priority formatting",
                "location": "formatting"
            })

        return {
            "check_type": "consistency",
            "issues_found": len(issues) > 0,
            "issues": issues,
            "improved_content": improved
        }

    def _actionability_checks(self, content: str) -> Dict:
        """Check and improve actionability."""
        issues = []
        improved = content

        # Check for untestable acceptance criteria
        acceptance_criteria = re.findall(r'- \[ \] .*', improved)
        for i, criterion in enumerate(acceptance_criteria):
            if not any(term in criterion.lower() for term in ['<', '>', '=', '%', 'time', 'seconds', 'minutes', 'days']):
                # Make it more testable
                criterion_text = criterion[5:].strip()
                improved_criterion = f"- [ ] {criterion_text} (must be measurable and testable)"

                # Replace the criterion
                criterion_start = improved.find(criterion)
                if criterion_start != -1:
                    improved = improved[:criterion_start] + improved_criterion + improved[criterion_start + len(criterion):]
                    issues.append({
                        "type": "testability_improvement",
                        "description": f"Made acceptance criterion more testable: '{criterion_text[:50]}...'",
                        "location": "acceptance_criteria"
                    })

        return {
            "check_type": "actionability",
            "issues_found": len(issues) > 0,
            "issues": issues,
            "improved_content": improved
        }

    def generate_improvement_report(self, improvements: Dict) -> str:
        """Generate a comprehensive improvement report."""
        report = f"""# PRD Improvement Report

**Original File**: {improvements['original_file']}
**Backup File**: {improvements['backup_file'] if improvements['backup_file'] else 'None'}
**Improvement Date**: {improvements['improvement_date']}

## Summary
"""

        total_improvements = 0
        for category, data in improvements['categories'].items():
            if data['issues_found']:
                total_improvements += len(data['improvements'])
                weight = self.improvement_categories[category]['weight']
                report += f"- **{category.title()}**: {len(data['improvements'])} improvements (weight: {weight*100:.0f}%)\n"

        report += f"**Total Improvements**: {total_improvements}\n\n"

        if total_improvements == 0:
            report += "✅ No improvements needed - PRD is already well-structured!\n\n"
        else:
            report += "## Detailed Improvements\n\n"

            for category, data in improvements['categories'].items():
                if data['issues_found']:
                    category_title = self.improvement_categories[category]['title']
                    weight = self.improvement_categories[category]['weight']

                    report += f"### {category_title} ({weight*100:.0f}% weight)\n"

                    for improvement in data['improvements']:
                        report += f"**{improvement['type'].replace('_', ' ').title()}**\n"
                        report += f"- {improvement['description']}\n"
                        report += f"  Location: {improvement['location'].replace('_', ' ').title()}\n\n"

        report += f"**Final File**: {improvements['final_file']}\n"

        return report


def main():
    """Main function for command-line interface."""
    parser = argparse.ArgumentParser(description='Improve Product Requirements Document (PRD) quality')

    parser.add_argument('file', help='Path to the PRD file to improve')
    parser.add_argument('--focus', choices=['structure', 'clarity', 'completeness', 'consistency', 'actionability'],
                       help='Focus improvements on specific area')
    parser.add_argument('--output-file',
                       help='Output file for the improved PRD (default: modifies original)')
    parser.add_argument('--no-backup', action='store_true',
                       help='Skip creating backup of original file')
    parser.add_argument('--report-file',
                       help='Output file for the improvement report')

    args = parser.parse_args()

    improver = PRDImprover()

    try:
        improvements = improver.improve_prd(
            args.file,
            focus_area=args.focus,
            output_file=args.output_file,
            backup=not args.no_backup
        )

        # Generate and save report
        report = improver.generate_improvement_report(improvements)

        if args.report_file:
            with open(args.report_file, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"✅ Improvement report saved to: {args.report_file}")
        else:
            print(report)

        print(f"✅ PRD improved successfully: {improvements['final_file']}")
        if args.focus:
            print(f"🎯 Focus area: {args.focus}")
        else:
            print("🎯 All improvement areas applied")

    except Exception as e:
        print(f"❌ Error improving PRD: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    main()