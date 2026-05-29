#!/usr/bin/env python3
"""
Product Requirements Document (PRD) Analyzer

This script analyzes existing PRD files for quality, completeness,
and provides detailed feedback on improvement opportunities.
"""

import argparse
import json
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class PRDAnalyzer:
    """PRD quality analyzer with comprehensive evaluation metrics."""

    def __init__(self):
        self.quality_metrics = {
            "completeness": {
                "weight": 0.3,
                "description": "Document completeness and coverage"
            },
            "clarity": {
                "weight": 0.25,
                "description": "Clarity and readability of content"
            },
            "consistency": {
                "weight": 0.2,
                "description": "Internal consistency of requirements"
            },
            "actionability": {
                "weight": 0.15,
                "description": "Requirements are actionable and testable"
            },
            "structure": {
                "weight": 0.1,
                "description": "Document structure and organization"
            }
        }

        self.required_sections = [
            "Document Information",
            "Product Overview",
            "User Analysis",
            "Functional Requirements",
            "Non-Functional Requirements",
            "User Interface & Experience",
            "Data & Analytics",
            "Technical Requirements",
            "Project Plan",
            "Acceptance Criteria"
        ]

        self.checklist_items = {
            "completeness": [
                "Clear product vision and goals",
                "Target user analysis",
                "Functional requirements defined",
                "Non-functional requirements specified",
                "Acceptance criteria provided",
                "Success metrics defined",
                "Risk assessment included"
            ],
            "clarity": [
                "Language is clear and concise",
                "No ambiguous terms",
                "Technical terms are defined",
                "User stories follow proper format",
                "Acceptance criteria are testable",
                "Requirements are specific and measurable"
            ],
            "consistency": [
                "No conflicting requirements",
                "Terminology is consistent throughout",
                "Priority levels are consistent",
                "Assumptions are documented",
                "Dependencies are identified"
            ],
            "actionability": [
                "Requirements can be implemented",
                "Acceptance criteria are measurable",
                "Success criteria are defined",
                "Requirements have clear ownership",
                "Implementation approach is specified"
            ],
            "structure": [
                "Logical flow and organization",
                "Proper section hierarchy",
                "Consistent formatting",
                "Visual aids where appropriate",
                "Cross-references between sections"
            ]
        }

    def analyze_prd(self, prd_file: str, focus_area: Optional[str] = None) -> Dict:
        """Analyze a PRD file and return detailed quality assessment."""

        if not os.path.exists(prd_file):
            raise FileNotFoundError(f"PRD file not found: {prd_file}")

        # Read the PRD file
        with open(prd_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Initialize analysis results
        results = {
            "file_path": prd_file,
            "analysis_date": datetime.now().isoformat(),
            "basic_metrics": self._analyze_basic_metrics(content),
            "section_coverage": self._analyze_section_coverage(content),
            "quality_scores": self._calculate_quality_scores(content),
            "improvement_suggestions": self._generate_improvement_suggestions(content),
            "checklist_status": self._analyze_checklist(content),
            "focus_area": focus_area
        }

        return results

    def _analyze_basic_metrics(self, content: str) -> Dict:
        """Analyze basic metrics of the PRD."""
        lines = content.split('\n')
        word_count = len(content.split())
        char_count = len(content)
        sections = re.findall(r'^##\s+(.+)$', content, re.MULTILINE)

        # Count various elements
        user_stories = len(re.findall(r'As a .* I want', content, re.IGNORECASE))
        acceptance_criteria = len(re.findall(r'- \[ \] ', content))
        priority_items = len(re.findall(r'- \[ \] .*[Hh]igh|[Mm]edium|[Ll]ow', content))

        return {
            "word_count": word_count,
            "char_count": char_count,
            "line_count": len(lines),
            "section_count": len(sections),
            "user_story_count": user_stories,
            "acceptance_criteria_count": acceptance_criteria,
            "priority_items_count": priority_items,
            "document_type": self._detect_document_type(content)
        }

    def _analyze_section_coverage(self, content: str) -> Dict:
        """Analyze coverage of required sections."""
        coverage = {}

        for section in self.required_sections:
            # Check if section exists (case-insensitive)
            section_pattern = re.escape(section)
            if re.search(rf'^##\s*{section_pattern}$', content, re.MULTILINE | re.IGNORECASE):
                coverage[section] = True
            else:
                coverage[section] = False

        missing_sections = [section for section, covered in coverage.items() if not covered]
        coverage_percentage = (sum(coverage.values()) / len(coverage)) * 100

        return {
            "sections_present": {section: covered for section, covered in coverage.items() if covered},
            "sections_missing": missing_sections,
            "coverage_percentage": coverage_percentage,
            "completeness_score": coverage_percentage
        }

    def _calculate_quality_scores(self, content: str) -> Dict:
        """Calculate quality scores for different aspects."""
        scores = {}

        # Completeness score
        completeness = self._calculate_completeness_score(content)
        scores["completeness"] = completeness

        # Clarity score
        clarity = self._calculate_clarity_score(content)
        scores["clarity"] = clarity

        # Consistency score
        consistency = self._calculate_consistency_score(content)
        scores["consistency"] = consistency

        # Actionability score
        actionability = self._calculate_actionability_score(content)
        scores["actionability"] = actionability

        # Structure score
        structure = self._calculate_structure_score(content)
        scores["structure"] = structure

        # Overall weighted score
        overall_score = sum(score * metric["weight"] for score, metric in zip(scores.values(), self.quality_metrics.values()))
        scores["overall"] = overall_score

        return scores

    def _calculate_completeness_score(self, content: str) -> float:
        """Calculate completeness score."""
        # Check for presence of key elements
        elements = [
            ("product vision", "Product Vision"),
            ("success metrics", "Success Metrics"),
            ("user analysis", "User Analysis"),
            ("functional requirements", "Functional Requirements"),
            ("non-functional requirements", "Non-Functional Requirements"),
            ("acceptance criteria", "Acceptance Criteria")
        ]

        present_elements = 0
        for pattern, section in elements:
            if pattern in content.lower() and section in content:
                present_elements += 1

        return (present_elements / len(elements)) * 100

    def _calculate_clarity_score(self, content: str) -> float:
        """Calculate clarity score based on language quality."""
        # Check for common clarity issues
        clarity_issues = 0
        total_checks = 0

        # Check for very long sentences (> 25 words)
        long_sentences = re.findall(r'[.!?]\s*[A-Z][^.]{25,}[.!?]', content)
        clarity_issues += len(long_sentences)
        total_checks += len(long_sentences) if len(long_sentences) > 0 else 1

        # Check for passive voice (basic heuristic)
        passive_patterns = re.findall(r'\b(am|is|are|was|were|been|be)\s+\w+(?:\s+by|\s+to\s+\w+)', content, re.IGNORECASE)
        clarity_issues += len(passive_patterns)
        total_checks += len(passive_patterns) if len(passive_patterns) > 0 else 1

        # Check for vague terms
        vague_terms = ['some', 'several', 'various', 'many', 'few', 'often', 'sometimes', 'approximately']
        vague_count = sum(1 for term in vague_terms if term in content.lower())
        clarity_issues += vague_count
        total_checks += len(vague_terms)

        # Calculate clarity (inverse of issues)
        if total_checks > 0:
            clarity = max(0, 100 - (clarity_issues / total_checks) * 100)
        else:
            clarity = 100

        return clarity

    def _calculate_consistency_score(self, content: str) -> float:
        """Calculate consistency score."""
        consistency_issues = 0
        total_checks = 0

        # Check for inconsistent priority levels
        priorities = re.findall(r'- \[ \] .*[Hh]igh|[Mm]edium|[Ll]ow', content)
        if priorities:
            priority_values = [p.lower() for p in priorities]
            if len(set(priority_values)) > 2:  # More than 2 different priority formats
                consistency_issues += 1
        total_checks += 1

        # Check for inconsistent terminology
        if 'user' in content.lower() and 'customer' in content.lower():
            # Check if both terms refer to the same concept
            user_contexts = [s.strip() for s in content.split('.') if 'user' in s.lower()]
            customer_contexts = [s.strip() for s in content.split('.') if 'customer' in s.lower()]

            # Simple heuristic: if both terms are used frequently, check for confusion
            if len(user_contexts) > 5 and len(customer_contexts) > 5:
                consistency_issues += 1
        total_checks += 1

        # Check for conflicting requirements
        conflict_patterns = [
            r'must.*[Nn]ot',
            r'should.*[Nn]ever',
            r'required.*[Ee]xclude',
            r'prohibited.*[Aa]llow'
        ]

        for pattern in conflict_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                consistency_issues += 1
        total_checks += len(conflict_patterns)

        if total_checks > 0:
            consistency = max(0, 100 - (consistency_issues / total_checks) * 100)
        else:
            consistency = 100

        return consistency

    def _calculate_actionability_score(self, content: str) -> float:
        """Calculate actionability score."""
        actionability_score = 0
        total_checks = 0

        # Check for testable acceptance criteria
        acceptance_criteria = re.findall(r'- \[ \] .*', content)
        testable_criteria = 0

        for criterion in acceptance_criteria:
            # Check if criterion has measurable terms
            if any(term in criterion.lower() for term in ['<', '>', '=', '%', 'time', 'seconds', 'minutes', 'days']):
                testable_criteria += 1

        if acceptance_criteria:
            actionability_score += (testable_criteria / len(acceptance_criteria)) * 50
        total_checks += 1

        # Check for clear ownership
        ownership_terms = ['responsible for', 'owner:', 'accountable:', 'developer:', 'designer:']
        ownership_count = sum(1 for term in ownership_terms if term in content.lower())
        actionability_score += min(ownership_count * 10, 50)
        total_checks += 1

        if total_checks > 0:
            return min(actionability_score, 100)
        else:
            return 100

    def _calculate_structure_score(self, content: str) -> float:
        """Calculate structure and organization score."""
        structure_score = 0
        total_checks = 0

        # Check for proper section hierarchy
        sections = re.findall(r'^##\s+(.+)$', content, re.MULTILINE)
        subsections = re.findall(r'^###\s+(.+)$', content, re.MULTILINE)

        if sections:
            structure_score += 40
            total_checks += 1

            if subsections:
                structure_score += 30
                total_checks += 1

        # Check for consistent formatting
        consistent_formatting = True
        checklists = re.findall(r'^- \[ \] ', content, re.MULTILINE)
        numbered_lists = re.findall(r'^\d+\. ', content, re.MULTILINE)

        if checklists and numbered_lists:
            # Check if formatting is consistent within sections
            for i in range(len(checklists) - 1):
                if not re.search(r'- \[ \] ', content[content.find(checklists[i]):content.find(checklists[i+1])]):
                    consistent_formatting = False
                    break

        if consistent_formatting:
            structure_score += 30
        total_checks += 1

        if total_checks > 0:
            return min(structure_score, 100)
        else:
            return 100

    def _detect_document_type(self, content: str) -> str:
        """Detect the type of PRD document."""
        content_lower = content.lower()

        type_indicators = {
            "web app": ["web application", "frontend", "backend", "api"],
            "mobile app": ["mobile", "ios", "android", "app store"],
            "saas": ["saas", "subscription", "multi-tenant", "cloud"],
            "ecommerce": ["ecommerce", "e-commerce", "shopping", "cart", "checkout"],
            "enterprise": ["enterprise", "b2b", "business", "organization"]
        }

        scores = {}
        for doc_type, indicators in type_indicators.items():
            score = sum(1 for indicator in indicators if indicator in content_lower)
            scores[doc_type] = score

        return max(scores, key=scores.get) if scores else "unknown"

    def _generate_improvement_suggestions(self, content: str) -> List[Dict]:
        """Generate improvement suggestions for the PRD."""
        suggestions = []

        # Add missing sections
        section_coverage = self._analyze_section_coverage(content)
        for missing_section in section_coverage["sections_missing"]:
            suggestions.append({
                "category": "completeness",
                "priority": "high",
                "suggestion": f"Add '{missing_section}' section to improve document completeness",
                "details": f"The '{missing_section}' section is missing but is essential for a comprehensive PRD"
            })

        # Add clarity suggestions
        clarity_score = self._calculate_clarity_score(content)
        if clarity_score < 80:
            suggestions.append({
                "category": "clarity",
                "priority": "medium",
                "suggestion": "Improve language clarity and readability",
                "details": f"Clarity score is {clarity_score:.1f}. Consider simplifying complex sentences and reducing vague terminology"
            })

        # Add consistency suggestions
        consistency_score = self._calculate_consistency_score(content)
        if consistency_score < 85:
            suggestions.append({
                "category": "consistency",
                "priority": "medium",
                "suggestion": "Improve consistency in terminology and priority levels",
                "details": f"Consistency score is {consistency_score:.1f}. Standardize terminology and ensure consistent priority assignments"
            })

        # Add actionability suggestions
        actionability_score = self._calculate_actionability_score(content)
        if actionability_score < 75:
            suggestions.append({
                "category": "actionability",
                "priority": "high",
                "suggestion": "Improve testability and clarity of requirements",
                "details": f"Actionability score is {actionability_score:.1f}. Add measurable acceptance criteria and clear ownership"
            })

        # Add structure suggestions
        structure_score = self._calculate_structure_score(content)
        if structure_score < 80:
            suggestions.append({
                "category": "structure",
                "priority": "low",
                "suggestion": "Improve document structure and formatting",
                "details": f"Structure score is {structure_score:.1f}. Ensure consistent formatting and proper section hierarchy"
            })

        return suggestions

    def _analyze_checklist(self, content: str) -> Dict:
        """Analyze checklist compliance."""
        results = {}

        for category, items in self.checklist_items.items():
            category_score = 0
            for item in items:
                # Simple heuristic for checklist completion
                if item.lower().split()[0] in content.lower():
                    category_score += 1

            results[category] = {
                "total_items": len(items),
                "completed_items": category_score,
                "percentage": (category_score / len(items)) * 100 if items else 0
            }

        return results

    def generate_report(self, analysis: Dict, output_format: str = "text") -> str:
        """Generate a comprehensive analysis report."""
        if output_format == "json":
            return json.dumps(analysis, indent=2)

        report = f"""
# PRD Quality Analysis Report

**File**: {analysis['file_path']}
**Analysis Date**: {analysis['analysis_date']}

## Basic Metrics
- **Word Count**: {analysis['basic_metrics']['word_count']:,}
- **Section Count**: {analysis['basic_metrics']['section_count']}
- **User Stories**: {analysis['basic_metrics']['user_story_count']}
- **Acceptance Criteria**: {analysis['basic_metrics']['acceptance_criteria_count']}
- **Document Type**: {analysis['basic_metrics']['document_type']}

## Section Coverage
**Coverage**: {analysis['section_coverage']['coverage_percentage']:.1f}%

### Missing Sections:
{chr(10).join(f"- {section}" for section in analysis['section_coverage']['sections_missing']) if analysis['section_coverage']['sections_missing'] else "✅ All required sections present"}

## Quality Scores
"""

        for aspect, score in analysis['quality_scores'].items():
            metric = self.quality_metrics[aspect]
            report += f"- **{aspect.title()}** ({metric['weight']*100:.0f}% weight): {score:.1f}/100\n"

        report += f"**Overall Score**: {analysis['quality_scores']['overall']:.1f}/100\n\n"

        if analysis['improvement_suggestions']:
            report += "## Improvement Suggestions\n\n"
            for suggestion in analysis['improvement_suggestions']:
                report += f"### {suggestion['category'].title()} - {suggestion['priority'].upper()} Priority\n"
                report += f"- **{suggestion['suggestion']}**\n"
                report += f"  *{suggestion['details']}*\n\n"

        if analysis['checklist_status']:
            report += "## Checklist Status\n\n"
            for category, status in analysis['checklist_status'].items():
                report += f"- **{category.title()}**: {status['completed_items']}/{status['total_items']} items ({status['percentage']:.1f}%)\n"

        return report


def main():
    """Main function for command-line interface."""
    parser = argparse.ArgumentParser(description='Analyze Product Requirements Document (PRD) quality')

    parser.add_argument('file', help='Path to the PRD file to analyze')
    parser.add_argument('--focus', choices=['completeness', 'clarity', 'consistency', 'actionability', 'structure'],
                       help='Focus analysis on specific area')
    parser.add_argument('--output', choices=['text', 'json'], default='text',
                       help='Output format for the analysis')
    parser.add_argument('--output-file',
                       help='Output file for the analysis report')

    args = parser.parse_args()

    analyzer = PRDAnalyzer()

    try:
        analysis = analyzer.analyze_prd(args.file, args.focus)

        # Generate report
        if args.output == 'json':
            report = json.dumps(analysis, indent=2)
        else:
            report = analyzer.generate_report(analysis, args.output)

        # Output report
        if args.output_file:
            with open(args.output_file, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"✅ Analysis report saved to: {args.output_file}")
        else:
            print(report)

    except Exception as e:
        print(f"❌ Error analyzing PRD: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    main()