#!/usr/bin/env python3
"""
Product Requirements Document (PRD) Validator

This script validates PRD files against specific checklists,
standards, and quality criteria for different methodologies.
"""

import argparse
import json
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class PRDValidator:
    """PRD validator with comprehensive validation checklists and standards."""

    def __init__(self):
        self.validation_standards = {
            "agile": {
                "name": "Agile Development Methodology",
                "checklist": self._get_agile_checklist(),
                "weightings": {
                    "user_stories": 0.3,
                    "acceptance_criteria": 0.25,
                    "iteration_planning": 0.2,
                    "metrics": 0.15,
                    "adaptability": 0.1
                }
            },
            "waterfall": {
                "name": "Waterfall Development Methodology",
                "checklist": self._get_waterfall_checklist(),
                "weightings": {
                    "comprehensive_requirements": 0.3,
                    "technical_specifications": 0.25,
                    "detailed_planning": 0.2,
                    "risk_management": 0.15,
                    "documentation": 0.1
                }
            },
            "mvp": {
                "name": "MVP Development Methodology",
                "checklist": self._get_mvp_checklist(),
                "weightings": {
                    "core_feature_identification": 0.35,
                    "market_validation": 0.25,
                    "resource_efficiency": 0.2,
                    "go_to_market": 0.15,
                    "iteration_planning": 0.05
                }
            }
        }

        self.quality_gates = {
            "completeness": {
                "threshold": 80,
                "description": "Overall document completeness"
            },
            "clarity": {
                "threshold": 75,
                "description": "Document clarity and readability"
            },
            "actionability": {
                "threshold": 85,
                "description": "Requirements are actionable and testable"
            },
            "consistency": {
                "threshold": 80,
                "description": "Document consistency and coherence"
            }
        }

    def validate_prd(self, prd_file: str, methodology: str = "agile",
                    checklist: Optional[str] = None, quality_gates: bool = True) -> Dict:
        """Validate a PRD against specified standards and checklists."""

        if not os.path.exists(prd_file):
            raise FileNotFoundError(f"PRD file not found: {prd_file}")

        if methodology not in self.validation_standards:
            raise ValueError(f"Unsupported methodology: {methodology}")

        # Read the PRD file
        with open(prd_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Perform validation
        validation = {
            "file_path": prd_file,
            "methodology": methodology,
            "validation_date": datetime.now().isoformat(),
            "checklist_results": {},
            "methodology_compliance": {},
            "quality_gates": {},
            "overall_score": 0,
            "status": "pending"
        }

        # Run checklist validation
        validation["checklist_results"] = self._run_checklist_validation(content, methodology)

        # Run methodology compliance
        validation["methodology_compliance"] = self._validate_methodology_compliance(content, methodology)

        # Run quality gates
        if quality_gates:
            validation["quality_gates"] = self._run_quality_gates(content)

        # Calculate overall score
        validation["overall_score"] = self._calculate_overall_score(validation)

        # Determine status
        validation["status"] = self._determine_status(validation)

        return validation

    def _run_checklist_validation(self, content: str, methodology: str) -> Dict:
        """Run checklist validation against methodology standards."""
        checklist = self.validation_standards[methodology]["checklist"]
        results = {}

        for category, items in checklist.items():
            category_results = {
                "items": items,
                "completed": 0,
                "total": len(items),
                "percentage": 0,
                "details": []
            }

            for item in items:
                if self._check_item_completion(content, item):
                    category_results["completed"] += 1
                    category_results["details"].append({
                        "item": item,
                        "status": "completed",
                        "notes": "✓ Completed"
                    })
                else:
                    category_results["details"].append({
                        "item": item,
                        "status": "missing",
                        "notes": "✗ Missing or incomplete"
                    })

            category_results["percentage"] = (category_results["completed"] / category_results["total"]) * 100
            results[category] = category_results

        return results

    def _check_item_completion(self, content: str, item: str) -> bool:
        """Check if a checklist item is completed in the PRD."""
        content_lower = content.lower()

        # Different types of items
        if "user story" in item.lower():
            # Check for user story format
            user_story_pattern = r'as a .* i want .* so that'
            return bool(re.search(user_story_pattern, content_lower, re.IGNORECASE))

        elif "acceptance criteria" in item.lower():
            # Check for acceptance criteria format
            ac_pattern = r'- \[ \] .*'
            return bool(re.search(ac_pattern, content))

        elif "risk assessment" in item.lower():
            # Check for risk content
            risk_patterns = [r'risk', 'challenge', 'issue', 'concern']
            return any(pattern in content_lower for pattern in risk_patterns)

        elif "technical specification" in item.lower():
            # Check for technical content
            tech_patterns = [r'api', 'database', 'infrastructure', 'architecture', 'deployment']
            return any(pattern in content_lower for pattern in tech_patterns)

        elif "success metric" in item.lower():
            # Check for metrics content
            metric_patterns = [r'metric', 'kpi', 'goal', 'target', 'objective']
            return any(pattern in content_lower for pattern in metric_patterns)

        elif "iteration planning" in item.lower():
            # Check for iteration content
            iteration_patterns = [r'sprint', 'iteration', 'backlog', 'planning']
            return any(pattern in content_lower for pattern in iteration_patterns)

        elif "core feature" in item.lower():
            # Check for core feature identification
            core_patterns = [r'core.*feature', 'essential.*feature', 'minimum.*viable']
            return any(pattern in content_lower for pattern in core_patterns)

        elif "market validation" in item.lower():
            # Check for market validation content
            market_patterns = [r'market', 'customer', 'user', 'feedback', 'validation']
            return any(pattern in content_lower for pattern in market_patterns)

        elif "go-to-market" in item.lower():
            # Check for go-to-market content
            gt_patterns = [r'launch', 'market', 'strategy', 'promotion', 'release']
            return any(pattern in content_lower for pattern in gt_patterns)

        else:
            # Generic check for presence of keywords
            keywords = item.lower().split()
            if len(keywords) > 2:
                # Use the main keywords for checking
                main_keywords = keywords[:2]  # First two words usually most important
                return all(keyword in content_lower for keyword in main_keywords)

        return False

    def _validate_methodology_compliance(self, content: str, methodology: str) -> Dict:
        """Validate compliance with specific methodology requirements."""
        compliance = {
            "methodology": self.validation_standards[methodology]["name"],
            "compliance_score": 0,
            "specific_requirements": {},
            "alignment_score": 0
        }

        if methodology == "agile":
            requirements = {
                "user_stories_present": self._has_user_stories(content),
                "acceptance_criteria_present": self._has_acceptance_criteria(content),
                "iterative_approach": self._has_iterative_approach(content),
                "flexible_requirements": self._has_flexible_requirements(content),
                "team_collaboration": self._has_team_collaboration(content)
            }

        elif methodology == "waterfall":
            requirements = {
                "comprehensive_requirements": self._has_comprehensive_requirements(content),
                "detailed_planning": self._has_detailed_planning(content),
                "phase_boundaries": self._has_phase_boundaries(content),
                "documentation_focus": self._has_documentation_focus(content),
                "change_management": self._has_change_management(content)
            }

        elif methodology == "mvp":
            requirements = {
                "core_features_focused": self._has_core_features_focused(content),
                "market_validation_focus": self._has_market_validation_focus(content),
                "resource_efficiency": self._has_resource_efficiency(content),
                "rapid_deployment": self._has_rapid_deployment(content),
                "feedback_loops": self._has_feedback_loops(content)
            }

        compliance["specific_requirements"] = requirements

        # Calculate alignment score
        satisfied_requirements = sum(1 for satisfied in requirements.values() if satisfied)
        compliance["alignment_score"] = (satisfied_requirements / len(requirements)) * 100
        compliance["compliance_score"] = compliance["alignment_score"]

        return compliance

    def _has_user_stories(self, content: str) -> bool:
        """Check if user stories are present."""
        pattern = r'as a .* i want .* so that'
        return bool(re.search(pattern, content.lower(), re.IGNORECASE))

    def _has_acceptance_criteria(self, content: str) -> bool:
        """Check if acceptance criteria are present."""
        pattern = r'- \[ \] .*'
        return bool(re.search(pattern, content))

    def _has_iterative_approach(self, content: str) -> bool:
        """Check if iterative approach is mentioned."""
        patterns = [r'sprint', 'iteration', 'backlog', 'agile', 'scrum']
        return any(pattern in content.lower() for pattern in patterns)

    def _has_flexible_requirements(self, content: str) -> bool:
        """Check if flexible requirements are mentioned."""
        patterns = [r'flexible', 'adaptable', 'change', 'evolve', 'adjust']
        return any(pattern in content.lower() for pattern in patterns)

    def _has_team_collaboration(self, content: str) -> bool:
        """Check if team collaboration is mentioned."""
        patterns = [r'team', 'collaboration', 'stakeholder', 'communication']
        return any(pattern in content.lower() for pattern in patterns)

    def _has_comprehensive_requirements(self, content: str) -> bool:
        """Check if comprehensive requirements are present."""
        sections = re.findall(r'^##\s+(.+)$', content, re.MULTILINE)
        return len(sections) >= 8  # Should have many detailed sections

    def _has_detailed_planning(self, content: str) -> bool:
        """Check if detailed planning is present."""
        patterns = [r'detailed.*plan', 'comprehensive.*plan', 'step.*step', 'phased']
        return any(pattern in content.lower() for pattern in patterns)

    def _has_phase_boundaries(self, content: str) -> bool:
        """Check if phase boundaries are defined."""
        patterns = [r'phase\s*\d+', 'stage\s*\d+', 'milestone']
        return any(pattern in content.lower() for pattern in patterns)

    def _has_documentation_focus(self, content: str) -> bool:
        """Check if documentation focus is present."""
        patterns = [r'document', 'specification', 'procedure', 'protocol']
        return any(pattern in content.lower() for pattern in patterns)

    def _has_change_management(self, content: str) -> bool:
        """Check if change management is mentioned."""
        patterns = [r'change.*control', 'change.*management', 'change.*request']
        return any(pattern in content.lower() for pattern in patterns)

    def _has_core_features_focused(self, content: str) -> bool:
        """Check if core features are focused."""
        patterns = [r'core.*feature', 'essential.*feature', 'critical.*feature', 'minimum.*viable']
        return any(pattern in content.lower() for pattern in patterns)

    def _has_market_validation_focus(self, content: str) -> bool:
        """Check if market validation focus is present."""
        patterns = [r'market.*valid', 'customer.*valid', 'user.*test', 'pilot']
        return any(pattern in content.lower() for pattern in patterns)

    def _has_resource_efficiency(self, content: str) -> bool:
        """Check if resource efficiency is mentioned."""
        patterns = [r'resource.*effici', 'cost.*effect', 'budget.*control', 'resource.*optim']
        return any(pattern in content.lower() for pattern in patterns)

    def _has_rapid_deployment(self, content: str) -> bool:
        """Check if rapid deployment is mentioned."""
        patterns = [r'rapid.*deploy', 'quick.*launch', 'fast.*time.*market', 'accelerated']
        return any(pattern in content.lower() for pattern in patterns)

    def _has_feedback_loops(self, content: str) -> bool:
        """Check if feedback loops are mentioned."""
        patterns = [r'feedback.*loop', 'iterative.*feedback', 'continuous.*feedback']
        return any(pattern in content.lower() for pattern in patterns)

    def _run_quality_gates(self, content: str) -> Dict:
        """Run quality gate validation."""
        quality_gates = {}

        for gate, criteria in self.quality_gates.items():
            score = self._calculate_quality_gate_score(content, gate)
            status = "pass" if score >= criteria["threshold"] else "fail"

            quality_gates[gate] = {
                "name": criteria["description"],
                "score": score,
                "threshold": criteria["threshold"],
                "status": status,
                "difference": score - criteria["threshold"]
            }

        return quality_gates

    def _calculate_quality_gate_score(self, content: str, gate: str) -> float:
        """Calculate quality gate score for a specific gate."""
        content_lower = content.lower()

        if gate == "completeness":
            # Calculate completeness based on section coverage
            sections = re.findall(r'^##\s+(.+)$', content, re.MULTILINE)
            return min(len(sections) * 10, 100)

        elif gate == "clarity":
            # Calculate clarity based on language quality
            sentences = re.findall(r'[.!?]\s*[A-Z][^.]+[.!?]', content)
            long_sentences = len([s for s in sentences if len(s) > 150])
            clarity_score = max(0, 100 - (long_sentences * 5))
            return clarity_score

        elif gate == "actionability":
            # Calculate actionability based on testable requirements
            acceptance_criteria = re.findall(r'- \[ \] .*', content)
            testable_criteria = len([c for c in acceptance_criteria if any(term in c.lower() for term in ['<', '>', '=', '%', 'time', 'seconds', 'minutes', 'days'])])
            return (testable_criteria / len(acceptance_criteria)) * 100 if acceptance_criteria else 0

        elif gate == "consistency":
            # Calculate consistency based on terminology consistency
            # Simple heuristic: count different terms that could be synonyms
            synonyms = [("user", "customer"), ("feature", "function"), ("requirement", "specification")]
            inconsistencies = 0
            for term1, term2 in synonyms:
                if term1 in content_lower and term2 in content_lower:
                    inconsistencies += 1
            return max(0, 100 - inconsistencies * 20)

        return 0

    def _calculate_overall_score(self, validation: Dict) -> float:
        """Calculate overall validation score."""
        scores = []

        # Checklist scores
        for category, result in validation["checklist_results"].items():
            scores.append(result["percentage"])

        # Methodology compliance
        scores.append(validation["methodology_compliance"]["compliance_score"])

        # Quality gates
        for gate, result in validation["quality_gates"].items():
            scores.append(result["score"])

        return sum(scores) / len(scores)

    def _determine_status(self, validation: Dict) -> str:
        """Determine overall validation status."""
        overall_score = validation["overall_score"]
        quality_gates = validation["quality_gates"]

        if overall_score >= 90:
            return "excellent"
        elif overall_score >= 80:
            return "good"
        elif overall_score >= 70:
            return "satisfactory"
        elif overall_score >= 60:
            return "needs_improvement"
        else:
            return "failing"

    def _get_agile_checklist(self) -> Dict:
        """Get agile methodology checklist."""
        return {
            "user_stories": [
                "User stories follow the 'As a I want so that' format",
                "User stories are prioritized",
                "User stories are sized appropriately",
                "User stories have clear acceptance criteria",
                "User stories are testable"
            ],
            "acceptance_criteria": [
                "Acceptance criteria are specific and measurable",
                "Acceptance criteria follow the Given-When-Then format",
                "Acceptance criteria cover edge cases",
                "Acceptance criteria are agreed upon by stakeholders",
                "Acceptance criteria are testable"
            ],
            "iteration_planning": [
                "Iterations are time-boxed",
                "Iteration goals are defined",
                "Iteration capacity is planned",
                "Iteration reviews are scheduled",
                "Iteration retrospectives are planned"
            ],
            "metrics": [
                "Success metrics are defined",
                "Metrics are aligned with business goals",
                "Metrics are measurable",
                "Metrics are tracked regularly",
                "Metrics are reviewed and adjusted"
            ],
            "adaptability": [
                "Requirements can be adjusted",
                "Change process is defined",
                "Risk management is in place",
                "Team can adapt to change",
                "Continuous improvement is planned"
            ]
        }

    def _get_waterfall_checklist(self) -> Dict:
        """Get waterfall methodology checklist."""
        return {
            "comprehensive_requirements": [
                "All requirements are documented",
                "Requirements are detailed and specific",
                "Requirements are approved by stakeholders",
                "Requirements are prioritized",
                "Requirements are traceable"
            ],
            "technical_specifications": [
                "Technical architecture is defined",
                "Technical requirements are specified",
                "Data models are documented",
                "API specifications are provided",
                "Security requirements are defined"
            ],
            "detailed_planning": [
                "Project timeline is detailed",
                "Resource allocation is planned",
                "Milestones are defined",
                "Dependencies are identified",
                "Risks are assessed and mitigated"
            ],
            "risk_management": [
                "Risks are identified",
                "Risk assessments are performed",
                "Mitigation strategies are defined",
                "Contingency plans are in place",
                "Risk monitoring is planned"
            ],
            "documentation": [
                "All documentation is complete",
                "Documentation is version controlled",
                "Documentation is accessible to team",
                "Documentation is reviewed",
                "Documentation standards are followed"
            ]
        }

    def _get_mvp_checklist(self) -> Dict:
        """Get MVP methodology checklist."""
        return {
            "core_feature_identification": [
                "Core features are identified",
                "Features are essential for MVP",
                "Features provide value to users",
                "Features can be implemented quickly",
                "Features differentiate the product"
            ],
            "market_validation": [
                "Target market is defined",
                "User needs are validated",
                "Problem-solution fit is established",
                "Competitive analysis is performed",
                "User feedback is incorporated"
            ],
            "resource_efficiency": [
                "Resource usage is optimized",
                "Development time is minimized",
                "Budget is controlled",
                "Team size is appropriate",
                "Technical complexity is reduced"
            ],
            "go_to_market": [
                "Go-to-market strategy is defined",
                "Launch timeline is planned",
                "Marketing approach is outlined",
                "Distribution channels are identified",
                "Success metrics are established"
            ],
            "iteration_planning": [
                "Post-MVP features are prioritized",
                "Feedback loops are established",
                "Improvement cycles are planned",
                "Scaling strategy is outlined",
                "Long-term vision is defined"
            ]
        }

    def generate_validation_report(self, validation: Dict, output_format: str = "text") -> str:
        """Generate a comprehensive validation report."""
        if output_format == "json":
            return json.dumps(validation, indent=2)

        report = f"""# PRD Validation Report

**File**: {validation['file_path']}
**Methodology**: {validation['methodology'].upper()}
**Validation Date**: {validation['validation_date']}

## Overall Status: {validation['status'].upper()}
**Overall Score**: {validation['overall_score']:.1f}/100

## Methodology Compliance: {validation['methodology_compliance']['methodology']}
**Compliance Score**: {validation['methodology_compliance']['compliance_score']:.1f}/100

### Specific Requirements
"""

        for requirement, satisfied in validation['methodology_compliance']['specific_requirements'].items():
            status = "✓" if satisfied else "✗"
            requirement_name = requirement.replace('_', ' ').title()
            report += f"- {status} {requirement_name}\n"

        report += f"**Alignment Score**: {validation['methodology_compliance']['alignment_score']:.1f}%\n\n"

        # Quality Gates
        if validation['quality_gates']:
            report += "## Quality Gates\n\n"
            for gate, result in validation['quality_gates'].items():
                status_icon = "✓" if result['status'] == 'pass' else "✗"
                report += f"**{gate.title()}** ({result['name']})\n"
                report += f"- {status_icon} Score: {result['score']:.1f}/{result['threshold']} (Diff: {result['difference']:+.1f})\n\n"

        # Checklist Results
        report += "## Checklist Results\n\n"
        for category, result in validation['checklist_results'].items():
            category_title = category.replace('_', ' ').title()
            status_icon = "✓" if result['percentage'] >= 80 else "⚠" if result['percentage'] >= 60 else "✗"
            report += f"**{category_title}**: {status_icon} {result['percentage']:.1f}% ({result['completed']}/{result['total']})\n"

            if result['details']:
                report += "  - Items:\n"
                for detail in result['details'][:3]:  # Show first 3 items
                    status_icon = "✓" if detail['status'] == 'completed' else "✗"
                    report += f"    {status_icon} {detail['item']}\n"

        return report


def main():
    """Main function for command-line interface."""
    parser = argparse.ArgumentParser(description='Validate Product Requirements Document (PRD)')

    parser.add_argument('file', help='Path to the PRD file to validate')
    parser.add_argument('--methodology', choices=['agile', 'waterfall', 'mvp'], default='agile',
                       help='Development methodology to validate against')
    parser.add_argument('--checklist', help='Custom checklist file')
    parser.add_argument('--quality-gates', action='store_true', default=True,
                       help='Run quality gate validation')
    parser.add_argument('--output', choices=['text', 'json'], default='text',
                       help='Output format for the validation report')
    parser.add_argument('--output-file',
                       help='Output file for the validation report')

    args = parser.parse_args()

    validator = PRDValidator()

    try:
        validation = validator.validate_prd(
            args.file,
            args.methodology,
            args.checklist,
            args.quality_gates
        )

        # Generate and save report
        report = validator.generate_validation_report(validation, args.output)

        if args.output_file:
            with open(args.output_file, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"✅ Validation report saved to: {args.output_file}")
        else:
            print(report)

        print(f"✅ PRD validation completed for: {args.file}")
        print(f"📊 Overall Score: {validation['overall_score']:.1f}/100")
        print(f"🎯 Status: {validation['status'].upper()}")

    except Exception as e:
        print(f"❌ Error validating PRD: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    main()