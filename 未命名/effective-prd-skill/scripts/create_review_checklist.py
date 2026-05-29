#!/usr/bin/env python3
"""
PRD Review Checklist Creator

This script creates comprehensive review checklists for PRD validation,
collaboration, and quality assurance workflows.
"""

import argparse
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


class PRDReviewChecklistGenerator:
    """Generator for PRD review checklists with multiple review types and workflows."""

    def __init__(self):
        self.review_templates = {
            "comprehensive": {
                "name": "Comprehensive PRD Review",
                "description": "Complete review of all PRD aspects including structure, content, and quality",
                "sections": self._get_comprehensive_sections(),
                "workflow": self._get_comprehensive_workflow()
            },
            "technical": {
                "name": "Technical PRD Review",
                "description": "Focus on technical requirements, specifications, and feasibility",
                "sections": self._get_technical_sections(),
                "workflow": self._get_technical_workflow()
            },
            "business": {
                "name": "Business PRD Review",
                "description": "Focus on business value, market fit, and strategic alignment",
                "sections": self._get_business_sections(),
                "workflow": self._get_business_workflow()
            },
            "user_experience": {
                "name": "User Experience Review",
                "description": "Focus on user needs, usability, and experience design",
                "sections": self._get_ux_sections(),
                "workflow": self._get_ux_workflow()
            },
            "agile": {
                "name": "Agile Methodology Review",
                "description": "Review specific to agile development practices and user stories",
                "sections": self._get_agile_sections(),
                "workflow": self._get_agile_workflow()
            }
        }

        self.review_roles = {
            "product_manager": {
                "name": "Product Manager",
                "responsibilities": [
                    "Business value and strategic alignment",
                    "Market and competitive analysis",
                    "User requirements and stories",
                    "Success metrics and KPIs",
                    "Prioritization and roadmap planning"
                ]
            },
            "technical_lead": {
                "name": "Technical Lead",
                "responsibilities": [
                    "Technical feasibility and architecture",
                    "Implementation approach and complexity",
                    "Integration requirements",
                    "Performance and scalability",
                    "Security and compliance requirements"
                ]
            },
            "design_lead": {
                "name": "Design Lead",
                "responsibilities": [
                    "User interface and experience design",
                    "Design system and consistency",
                    "Accessibility and usability",
                    "Visual design and branding",
                    "User interaction patterns"
                ]
            },
            "qa_lead": {
                "name": "QA Lead",
                "responsibilities": [
                    "Testability and acceptance criteria",
                    "Testing strategy and coverage",
                    "Quality metrics and standards",
                    "Defect tracking and resolution",
                    "Performance and load testing"
                ]
            },
            "stakeholder": {
                "name": "Stakeholder",
                "responsibilities": [
                    "Business requirements validation",
                    "Strategic alignment",
                    "Resource allocation",
                    "Timeline and budget approval",
                    "Risk assessment"
                ]
            }
        }

    def create_checklist(self, template: str = "comprehensive", output_file: Optional[str] = None,
                        custom_sections: Optional[List[str]] = None) -> Dict:
        """Create a review checklist based on the specified template."""

        if template not in self.review_templates:
            raise ValueError(f"Unsupported template: {template}")

        checklist_data = {
            "template": template,
            "template_name": self.review_templates[template]["name"],
            "description": self.review_templates[template]["description"],
            "created_date": datetime.now().isoformat(),
            "version": "1.0",
            "sections": self.review_templates[template]["sections"],
            "workflow": self.review_templates[template]["workflow"],
            "roles": self.review_roles,
            "review_criteria": self._get_review_criteria(),
            "scoring_system": self._get_scoring_system()
        }

        # Add custom sections if provided
        if custom_sections:
            checklist_data["custom_sections"] = custom_sections

        # Save to file if requested
        if output_file:
            self._save_checklist(checklist_data, output_file)
            print(f"✅ Checklist saved to: {output_file}")

        return checklist_data

    def _save_checklist(self, checklist_data: Dict, output_file: str):
        """Save checklist data to file."""
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(checklist_data, f, indent=2, ensure_ascii=False)

    def _get_comprehensive_sections(self) -> List[Dict]:
        """Get comprehensive review sections."""
        return [
            {
                "name": "Document Structure",
                "description": "Review the overall structure and organization of the PRD",
                "items": [
                    "Document has clear title and version information",
                    "All required sections are present",
                    "Sections follow logical order",
                    "Table of contents is included",
                    "Cross-references between sections are present"
                ],
                "priority": "high",
                "reviewer": "all"
            },
            {
                "name": "Product Overview",
                "description": "Review the product vision, goals, and context",
                "items": [
                    "Product vision is clearly defined",
                    "Goals are specific and measurable",
                    "Market background analysis is comprehensive",
                    "Problem statement is accurate",
                    "Business opportunity is well-defined",
                    "Success metrics are appropriate"
                ],
                "priority": "high",
                "reviewer": "product_manager, stakeholder"
            },
            {
                "name": "User Analysis",
                "description": "Review user research and requirements",
                "items": [
                    "Target users are clearly defined",
                    "User personas are realistic and detailed",
                    "User needs are well-understood",
                    "User journey mapping is complete",
                    "Pain points are accurately identified",
                    "User stories follow proper format"
                ],
                "priority": "high",
                "reviewer": "product_manager, ux_designer"
            },
            {
                "name": "Functional Requirements",
                "description": "Review functional specifications and features",
                "items": [
                    "All features are clearly defined",
                    "User stories are complete and testable",
                    "Priority levels are consistent",
                    "Acceptance criteria are specific and measurable",
                    "Feature dependencies are identified",
                    "Edge cases are considered"
                ],
                "priority": "high",
                "reviewer": "product_manager, technical_lead, qa_lead"
            },
            {
                "name": "Non-Functional Requirements",
                "description": "Review non-functional specifications",
                "items": [
                    "Performance requirements are specific",
                    "Security requirements are comprehensive",
                    "Availability targets are realistic",
                    "Compatibility requirements are complete",
                    "Scalability requirements are defined",
                    "Compliance requirements are addressed"
                ],
                "priority": "medium",
                "reviewer": "technical_lead, qa_lead"
            },
            {
                "name": "Technical Requirements",
                "description": "Review technical specifications and architecture",
                "items": [
                    "Technology stack is appropriate",
                    "Architecture is sound and scalable",
                    "Integration requirements are clear",
                    "Data models are well-defined",
                    "API specifications are complete",
                    "Deployment requirements are specified"
                ],
                "priority": "high",
                "reviewer": "technical_lead"
            },
            {
                "name": "Project Plan",
                "description": "Review project planning and execution",
                "items": [
                    "Timeline is realistic and detailed",
                    "Resource allocation is appropriate",
                    "Milestones are clearly defined",
                    "Risk assessment is comprehensive",
                    "Dependencies are identified and planned",
                    "Budget considerations are addressed"
                ],
                "priority": "medium",
                "reviewer": "project_manager, stakeholder"
            },
            {
                "name": "Quality Assurance",
                "description": "Review quality assurance and testing",
                "items": [
                    "Testing strategy is comprehensive",
                    "Test cases are defined and testable",
                    "Quality metrics are established",
                    "Defect management process is defined",
                    "Performance testing is planned",
                    "User acceptance testing is defined"
                ],
                "priority": "medium",
                "reviewer": "qa_lead"
            }
        ]

    def _get_technical_sections(self) -> List[Dict]:
        """Get technical review sections."""
        return [
            {
                "name": "Architecture Review",
                "description": "Technical architecture and design",
                "items": [
                    "Architecture supports scalability requirements",
                    "Technology choices are justified",
                    "Integration points are well-defined",
                    "Data flow is properly designed",
                    "Security architecture is comprehensive"
                ],
                "priority": "high",
                "reviewer": "technical_lead, architect"
            },
            {
                "name": "Implementation Feasibility",
                "description": "Technical implementation assessment",
                "items": [
                    "Requirements are technically feasible",
                    "Implementation complexity is assessed",
                    "Resource requirements are realistic",
                    "Technology constraints are identified",
                    "Risks are properly assessed"
                ],
                "priority": "high",
                "reviewer": "technical_lead, development_team"
            },
            {
                "name": "Integration Requirements",
                "description": "System integration specifications",
                "items": [
                    "External systems integration is defined",
                    "API contracts are complete",
                    "Data synchronization requirements are clear",
                    "Error handling for integrations is specified",
                    "Performance impact is assessed"
                ],
                "priority": "medium",
                "reviewer": "technical_lead, integration_specialist"
            },
            {
                "name": "Performance & Scalability",
                "description": "Performance and scalability requirements",
                "items": [
                    "Performance targets are realistic",
                    "Scalability requirements are defined",
                    "Load testing requirements are specified",
                    "Resource optimization is considered",
                    "Monitoring and alerting are planned"
                ],
                "priority": "medium",
                "reviewer": "technical_lead, performance_engineer"
            }
        ]

    def _get_business_sections(self) -> List[Dict]:
        """Get business review sections."""
        return [
            {
                "name": "Business Value",
                "description": "Business value and ROI assessment",
                "items": [
                    "Business objectives are clearly defined",
                    "Value proposition is compelling",
                    "Market opportunity is assessed",
                    "Competitive advantage is identified",
                    "ROI calculations are provided"
                ],
                "priority": "high",
                "reviewer": "product_manager, stakeholder"
            },
            {
                "name": "Market Analysis",
                "description": "Market and competitive analysis",
                "items": [
                    "Target market is well-defined",
                    "Market size is estimated",
                    "Market trends are analyzed",
                    "Competitive landscape is assessed",
                    "Positioning strategy is clear"
                ],
                "priority": "high",
                "reviewer": "product_manager, marketing_team"
            },
            {
                "name": "Financial Planning",
                "description": "Financial considerations and budget",
                "items": [
                    "Development costs are estimated",
                    "Operational costs are considered",
                    "Pricing strategy is defined",
                    "Revenue projections are realistic",
                    "Budget allocation is appropriate"
                ],
                "priority": "medium",
                "reviewer": "finance_team, stakeholder"
            },
            {
                "name": "Risk Assessment",
                "description": "Business risk analysis and mitigation",
                "items": [
                    "Market risks are identified",
                    "Financial risks are assessed",
                    "Operational risks are considered",
                    "Mitigation strategies are defined",
                    "Risk tolerance is established"
                ],
                "priority": "medium",
                "reviewer": "risk_manager, stakeholder"
            }
        ]

    def _get_ux_sections(self) -> List[Dict]:
        """Get user experience review sections."""
        return [
            {
                "name": "User Requirements",
                "description": "User needs and requirements analysis",
                "items": [
                    "User needs are accurately identified",
                    "User requirements are comprehensive",
                    "User pain points are addressed",
                    "User goals are clear",
                    "User expectations are managed"
                ],
                "priority": "high",
                "reviewer": "product_manager, ux_designer"
            },
            {
                "name": "Design System",
                "description": "Design consistency and system",
                "items": [
                    "Design system is defined and documented",
                    "Components are consistent",
                    "Design guidelines are followed",
                    "Brand guidelines are respected",
                    "Accessibility standards are met"
                ],
                "priority": "medium",
                "reviewer": "design_lead, ux_designer"
            },
            {
                "name": "Interaction Design",
                "description": "Interaction and flow design",
                "items": [
                    "User flows are intuitive",
                    "Navigation is clear and consistent",
                    "Interaction patterns are standard",
                    "Feedback mechanisms are appropriate",
                    "Error handling is user-friendly"
                ],
                "priority": "high",
                "reviewer": "ux_designer, interaction_designer"
            },
            {
                "name": "Usability Testing",
                "description": "Usability testing requirements",
                "items": [
                    "Usability testing is planned",
                    "Test participants are defined",
                    "Test scenarios are realistic",
                    "Success criteria are established",
                    "Improvement process is defined"
                ],
                "priority": "medium",
                "reviewer": "ux_designer, usability_specialist"
            }
        ]

    def _get_agile_sections(self) -> List[Dict]:
        """Get agile methodology review sections."""
        return [
            {
                "name": "User Stories",
                "description": "User story format and content",
                "items": [
                    "User stories follow 'As a I want so that' format",
                    "Roles are clearly defined",
                    "Benefits are specific",
                    "Stories are appropriately sized",
                    "Stories are prioritized"
                ],
                "priority": "high",
                "reviewer": "product_manager, development_team"
            },
            {
                "name": "Acceptance Criteria",
                "description": "Acceptance criteria definition",
                "items": [
                    "Criteria are specific and measurable",
                    "Criteria test the user story",
                    "Edge cases are considered",
                    "Criteria are agreed upon by team",
                    "Criteria are testable"
                ],
                "priority": "high",
                "reviewer": "product_manager, development_team, qa_lead"
            },
            {
                "name": "Iteration Planning",
                "description": "Sprint and iteration planning",
                "items": [
                    "Iteration goals are defined",
                    "Work is broken down into tasks",
                    "Capacity is estimated accurately",
                    "Dependencies are identified",
                    "Review and retrospective are planned"
                ],
                "priority": "medium",
                "reviewer": "scrum_master, development_team"
            },
            {
                "name": "Agile Metrics",
                "description": "Agile performance metrics",
                "items": [
                    "Velocity is tracked",
                    "Burndown charts are maintained",
                    "Cycle time is measured",
                    "Lead time is optimized",
                    "Quality metrics are tracked"
                ],
                "priority": "medium",
                "reviewer": "scrum_master, development_team"
            }
        ]

    def _get_comprehensive_workflow(self) -> Dict:
        """Get comprehensive review workflow."""
        return {
            "name": "Comprehensive Review Workflow",
            "description": "Complete PRD review process",
            "phases": [
                {
                    "name": "Preparation",
                    "description": "Prepare for the review",
                    "activities": [
                        "Read through the entire PRD",
                        "Check for completeness",
                        "Identify areas of concern",
                        "Prepare questions and feedback"
                    ],
                    "duration": "1-2 days"
                },
                {
                    "name": "Initial Review",
                    "description": "Initial review and feedback",
                    "activities": [
                        "Review document structure",
                        "Check product overview",
                        "Review user analysis",
                        "Identify major issues"
                    ],
                    "duration": "3-5 days",
                    "participants": ["product_manager", "technical_lead", "design_lead"]
                },
                {
                    "name": "Detailed Review",
                    "description": "Detailed review of specific areas",
                    "activities": [
                        "Functional requirements review",
                        "Technical requirements review",
                        "Non-functional requirements review",
                        "User experience review"
                    ],
                    "duration": "5-7 days",
                    "participants": ["all_reviewers"]
                },
                {
                    "name": "Stakeholder Review",
                    "description": "Stakeholder review and approval",
                    "activities": [
                        "Business value validation",
                        "Strategic alignment review",
                        "Resource assessment",
                        "Final approval"
                    ],
                    "duration": "2-3 days",
                    "participants": ["stakeholders", "product_manager"]
                },
                {
                    "name": "Resolution",
                    "description": "Resolve issues and finalize",
                    "activities": [
                        "Address feedback and concerns",
                        "Update PRD with changes",
                        "Final validation",
                        "Sign-off"
                    ],
                    "duration": "2-3 days",
                    "participants": ["product_manager", "all_reviewers"]
                }
            ],
            "approval_criteria": {
                "document_complete": True,
                "business_value_approved": True,
                "technical_feasibility_confirmed": True,
                "user_requirements_validated": True,
                "stakeholders_aligned": True
            }
        }

    def _get_technical_workflow(self) -> Dict:
        """Get technical review workflow."""
        return {
            "name": "Technical Review Workflow",
            "description": "Focus on technical aspects and feasibility",
            "phases": [
                {
                    "name": "Architecture Review",
                    "description": "Technical architecture assessment",
                    "duration": "2-3 days",
                    "participants": ["technical_lead", "architect"]
                },
                {
                    "name": "Implementation Assessment",
                    "description": "Implementation feasibility review",
                    "duration": "3-4 days",
                    "participants": ["technical_lead", "development_team"]
                },
                {
                    "name": "Integration Planning",
                    "description": "Integration requirements review",
                    "duration": "2-3 days",
                    "participants": ["technical_lead", "integration_specialist"]
                },
                {
                    "name": "Technical Approval",
                    "description": "Technical approval and sign-off",
                    "duration": "1-2 days",
                    "participants": ["technical_lead", "cto"]
                }
            ]
        }

    def _get_business_workflow(self) -> Dict:
        """Get business review workflow."""
        return {
            "name": "Business Review Workflow",
            "description": "Focus on business value and strategy",
            "phases": [
                {
                    "name": "Market Analysis",
                    "description": "Market and competitive analysis",
                    "duration": "3-5 days",
                    "participants": ["product_manager", "marketing_team"]
                },
                {
                    "name": "Value Assessment",
                    "description": "Business value and ROI assessment",
                    "duration": "2-3 days",
                    "participants": ["product_manager", "finance_team"]
                },
                {
                    "name": "Strategic Review",
                    "description": "Strategic alignment review",
                    "duration": "2-3 days",
                    "participants": ["product_manager", "stakeholders"]
                },
                {
                    "name": "Business Approval",
                    "description": "Business approval and sign-off",
                    "duration": "1-2 days",
                    "participants": ["stakeholders", "executive_team"]
                }
            ]
        }

    def _get_ux_workflow(self) -> Dict:
        """Get user experience review workflow."""
        return {
            "name": "User Experience Review Workflow",
            "description": "Focus on user needs and experience",
            "phases": [
                {
                    "name": "User Research Review",
                    "description": "User research and requirements review",
                    "duration": "2-3 days",
                    "participants": ["ux_designer", "product_manager"]
                },
                {
                    "name": "Design System Review",
                    "description": "Design system and consistency review",
                    "duration": "2-3 days",
                    "participants": ["design_lead", "ux_designer"]
                },
                {
                    "name": "Interaction Design Review",
                    "description": "Interaction and flow design review",
                    "duration": "3-4 days",
                    "participants": ["interaction_designer", "ux_designer"]
                },
                {
                    "name": "Usability Review",
                    "description": "Usability testing and validation",
                    "duration": "3-5 days",
                    "participants": ["usability_specialist", "ux_designer"]
                }
            ]
        }

    def _get_agile_workflow(self) -> Dict:
        """Get agile review workflow."""
        return {
            "name": "Agile Review Workflow",
            "description": "Focus on agile practices and user stories",
            "phases": [
                {
                    "name": "User Story Review",
                    "description": "User story format and content review",
                    "duration": "2-3 days",
                    "participants": ["product_manager", "development_team"]
                },
                {
                    "name": "Acceptance Criteria Review",
                    "description": "Acceptance criteria validation",
                    "duration": "2-3 days",
                    "participants": ["product_manager", "qa_lead", "development_team"]
                },
                {
                    "name": "Iteration Planning",
                    "description": "Sprint planning and backlog grooming",
                    "duration": "1-2 days",
                    "participants": ["scrum_master", "development_team", "product_manager"]
                },
                {
                    "name": "Team Alignment",
                    "description": "Team alignment and commitment",
                    "duration": "1 day",
                    "participants": ["all_team_members"]
                }
            ]
        }

    def _get_review_criteria(self) -> Dict:
        """Get review criteria definitions."""
        return {
            "completeness": {
                "description": "Document completeness and coverage",
                "scoring": "0-100%",
                "weight": 0.3
            },
            "clarity": {
                "description": "Clarity and readability of content",
                "scoring": "0-100%",
                "weight": 0.25
            },
            "consistency": {
                "description": "Internal consistency of requirements",
                "scoring": "0-100%",
                "weight": 0.2
            },
            "actionability": {
                "description": "Requirements are actionable and testable",
                "scoring": "0-100%",
                "weight": 0.15
            },
            "alignment": {
                "description": "Alignment with business and strategic goals",
                "scoring": "0-100%",
                "weight": 0.1
            }
        }

    def _get_scoring_system(self) -> Dict:
        """Get scoring system definitions."""
        return {
            "numeric_scale": {
                "excellent": 90-100,
                "good": 80-89,
                "satisfactory": 70-79,
                "needs_improvement": 60-69,
                "failing": 0-59
            },
            "weighting_system": {
                "high_priority_items": 1.2,
                "medium_priority_items": 1.0,
                "low_priority_items": 0.8
            },
            "approval_thresholds": {
                "major_changes_required": 60,
                "minor_changes_needed": 75,
                "ready_for_approval": 85,
                "excellent": 90
            }
        }

    def generate_review_guide(self, checklist_data: Dict) -> str:
        """Generate a comprehensive review guide from checklist data."""
        guide = f"""# PRD Review Guide: {checklist_data['template_name']}

**Description**: {checklist_data['description']}
**Created**: {checklist_data['created_date']}
**Version**: {checklist_data['version']}

## Review Workflow

### {checklist_data['workflow']['name']}
{checklist_data['workflow']['description']}

#### Review Phases
"""
        for phase in checklist_data['workflow']['phases']:
            guide += f"""
**{phase['name']}**
- **Description**: {phase['description']}
- **Duration**: {phase['duration']}
- **Participants**: {', '.join(phase['participants']) if 'participants' in phase else 'TBD'}
"""
            if 'activities' in phase:
                guide += "- **Activities**:\n"
                for activity in phase['activities']:
                    guide += f"  - {activity}\n"

        guide += f"""
## Review Roles and Responsibilities

"""

        for role_key, role_info in checklist_data['roles'].items():
            guide += f"""
### {role_info['name']}
**Responsibilities**:
"""
            for responsibility in role_info['responsibilities']:
                guide += f"- {responsibility}\n"

        guide += f"""
## Review Criteria

"""

        for criteria_key, criteria_info in checklist_data['review_criteria'].items():
            guide += f"""
### {criteria_key.title()}
- **Description**: {criteria_info['description']}
- **Scoring**: {criteria_info['scoring']}
- **Weight**: {criteria_info['weight']*100:.0f}%
"""

        guide += f"""
## Scoring System

### Numeric Scale
- **Excellent**: 90-100%
- **Good**: 80-89%
- **Satisfactory**: 70-79%
- **Needs Improvement**: 60-69%
- **Failing**: 0-59%

### Weighting System
- **High Priority Items**: 1.2x weight
- **Medium Priority Items**: 1.0x weight
- **Low Priority Items**: 0.8x weight

### Approval Thresholds
- **Major Changes Required**: Below 60%
- **Minor Changes Needed**: 60-75%
- **Ready for Approval**: 75-85%
- **Excellent**: Above 85%

## Review Checklist Sections

"""

        for section in checklist_data['sections']:
            guide += f"""
### {section['name']}
**Description**: {section['description']}
**Priority**: {section['priority'].upper()}
**Reviewer**: {', '.join(section['reviewer']) if 'reviewer' in section else 'All'}

#### Review Items:
"""
            for item in section['items']:
                guide += f"- [ ] {item}\n"

        return guide


def main():
    """Main function for command-line interface."""
    parser = argparse.ArgumentParser(description='Create PRD Review Checklist')

    parser.add_argument('--template', choices=['comprehensive', 'technical', 'business', 'user_experience', 'agile'],
                       default='comprehensive', help='Review template type')
    parser.add_argument('--output-file',
                       help='Output file for the checklist (JSON format)')
    parser.add_argument('--guide-file',
                       help='Output file for the review guide (Markdown format)')
    parser.add_argument('--custom-sections', nargs='+',
                       help='Custom sections to add to the checklist')

    args = parser.parse_args()

    generator = PRDReviewChecklistGenerator()

    try:
        # Create checklist
        checklist = generator.create_checklist(
            template=args.template,
            output_file=args.output_file,
            custom_sections=args.custom_sections
        )

        # Generate guide
        if args.guide_file:
            guide = generator.generate_review_guide(checklist)
            with open(args.guide_file, 'w', encoding='utf-8') as f:
                f.write(guide)
            print(f"✅ Review guide saved to: {args.guide_file}")

        # Print summary
        print(f"✅ Checklist created for: {checklist['template_name']}")
        print(f"📋 Sections: {len(checklist['sections'])}")
        print(f"👥 Review roles: {len(checklist['roles'])}")
        print(f"🔄 Workflow phases: {len(checklist['workflow']['phases'])}")

        if args.output_file:
            print(f"💾 Checklist saved to: {args.output_file}")
        if args.guide_file:
            print(f"📝 Review guide saved to: {args.guide_file}")

    except Exception as e:
        print(f"❌ Error creating checklist: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    main()