#!/usr/bin/env python3
"""
Product Requirements Document (PRD) Generator

This script generates comprehensive PRD templates based on different
product types, methodologies, and requirements.
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


class PRDGenerator:
    """PRD template generator with multiple product types and methodologies support."""

    def __init__(self):
        self.templates = self._load_templates()

    def _load_templates(self) -> Dict:
        """Load PRD templates for different product types and methodologies."""
        return {
            "web-app": {
                "agile": self._get_web_app_agile_template(),
                "waterfall": self._get_web_app_waterfall_template(),
                "mvp": self._get_web_app_mvp_template()
            },
            "mobile-app": {
                "agile": self._get_mobile_app_agile_template(),
                "waterfall": self._get_mobile_app_waterfall_template(),
                "mvp": self._get_mobile_app_mvp_template()
            },
            "saas": {
                "agile": self._get_saas_agile_template(),
                "waterfall": self._get_saas_waterfall_template(),
                "mvp": self._get_saas_mvp_template()
            },
            "ecommerce": {
                "agile": self._get_ecommerce_agile_template(),
                "waterfall": self._get_ecommerce_waterfall_template(),
                "mvp": self._get_ecommerce_mvp_template()
            }
        }

    def generate_prd(self, product_name: str, product_type: str, methodology: str,
                    output_file: Optional[str] = None, with_user_stories: bool = False,
                    **kwargs) -> str:
        """Generate a complete PRD based on specifications."""

        if product_type not in self.templates:
            raise ValueError(f"Unsupported product type: {product_type}")

        if methodology not in self.templates[product_type]:
            raise ValueError(f"Unsupported methodology: {methodology}")

        template = self.templates[product_type][methodology]

        # Replace placeholders with actual values
        prd_content = self._replace_placeholders(template, {
            "product_name": product_name,
            "current_date": datetime.now().strftime("%Y-%m-%d"),
            "product_type": product_type.replace("-", " ").title(),
            "methodology": methodology.upper(),
            "version": "1.0",
            "with_user_stories": with_user_stories,
            **kwargs
        })

        # Add user stories if requested
        if with_user_stories and methodology == "agile":
            prd_content += self._generate_user_stories(product_name, product_type)

        # Set output file
        if not output_file:
            output_file = f"{product_name.lower().replace(' ', '-')}-prd.md"

        # Write to file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(prd_content)

        print(f"PRD generated successfully: {output_file}")
        return output_file

    def _replace_placeholders(self, template: str, replacements: Dict) -> str:
        """Replace placeholders in template with actual values."""
        content = template
        for placeholder, value in replacements.items():
            content = content.replace(f"[{placeholder}]", str(value))
        return content

    def _generate_user_stories(self, product_name: str, product_type: str) -> str:
        """Generate sample user stories for agile methodology."""
        return f"""

## User Stories

### Epic: Core Functionality
- **Story 1**: As a user, I want to [core function] so that [benefit]
- **Story 2**: As a user, I want to [another core function] so that [benefit]
- **Story 3**: As a user, I want to [important feature] so that [benefit]

### Epic: User Experience
- **Story 4**: As a user, I want [intuitive navigation] so that [good UX]
- **Story 5**: As a user, I want [responsive design] so that [accessibility]

### Epic: Performance
- **Story 6**: As a user, I want [fast loading] so that [good performance]
- **Story 7**: As a user, I want [reliable service] so that [trust]

## Acceptance Criteria

- All user stories have clear acceptance criteria
- Each acceptance criterion is testable and measurable
- Acceptance criteria align with business objectives
- User acceptance testing is planned
"""

    def _get_web_app_agile_template(self) -> str:
        """Get web app agile template."""
        return """# [product_name] Web Application - PRD

## Document Information
- **Document Title**: [product_name] Web Application Requirements Document
- **Document Version**: v[version]
- **Created Date**: [current_date]
- **Last Updated**: [current_date]
- **Product Manager**: [Name]
- **Development Lead**: [Name]
- **Design Lead**: [Name]
- **Test Lead**: [Name]
- **Stakeholders**: [List stakeholders]

---

## 1. Product Overview

### 1.1 Background & Opportunity
- **Market Background**: [Describe market context and trends]
- **Problem Statement**: [What problem does this solve?]
- **Business Opportunity**: [What business value does this create?]
- **Competitive Landscape**: [Who are the competitors?]

### 1.2 Product Vision & Goals
- **Product Vision**: [What is the ultimate vision for this product?]
- **Short-term Goals (3 months)**: [Specific, measurable goals]
- **Mid-term Goals (6 months)**: [Specific, measurable goals]
- **Long-term Goals (12 months)**: [Specific, measurable goals]

### 1.3 Success Metrics
- **Business Metrics**: [Key business indicators]
- **User Metrics**: [Key user engagement metrics]
- **Technical Metrics**: [Key technical performance metrics]
- **Timeline**: [Target release date]

---

## 2. User Analysis

### 2.1 Target Users
- **Primary User Group**: [Description]
  - Demographics: [Age, occupation, etc.]
  - Technical proficiency: [How tech-savvy are they?]
  - Goals: [What do they want to achieve?]
  - Pain Points: [What problems do they face?]

### 2.2 User Personas
- **Primary Persona**: [Name, role, goals, pain points]
- **Secondary Persona**: [Name, role, goals, pain points]

### 2.3 User Journey
- **Current Flow**: [Describe existing user flow]
- **Pain Points**: [What's broken today?]
- **Improvement Opportunities**: [How can we improve?]

---

## 3. Functional Requirements

### 3.1 Core Features
#### Feature 1: [Feature Name]
- **Description**: [What does this feature do?]
- **User Story**:
  ```
  As a [user role]
  I want [functionality]
  So that [benefit]
  ```
- **Priority**: [High/Medium/Low]
- **Acceptance Criteria**:
  - [ ] [Criteria 1]
  - [ ] [Criteria 2]
  - [ ] [Criteria 3]

### 3.2 Supporting Features
#### Feature 2: [Feature Name]
- **Description**: [What does this feature do?]
- **User Story**:
  ```
  As a [user role]
  I want [functionality]
  So that [benefit]
  ```
- **Priority**: [High/Medium/Low]
- **Acceptance Criteria**:
  - [ ] [Criteria 1]
  - [ ] [Criteria 2]

### 3.3 Feature Priority Matrix
| Feature | Business Value | User Value | Effort | Priority |
|---------|---------------|------------|--------|----------|
| Feature 1 | [Value] | [Value] | [Effort] | [Priority] |
| Feature 2 | [Value] | [Value] | [Effort] | [Priority] |

---

## 4. Non-Functional Requirements

### 4.1 Performance Requirements
- **Response Time**: [Target response time]
- **Concurrent Users**: [Target concurrent users]
- **Data Volume**: [Target data volume]
- **API Performance**: [Target API response times]

### 4.2 Security Requirements
- **Data Encryption**: [Encryption standards]
- **Authentication**: [Authentication methods]
- **Authorization**: [Permission levels]
- **Compliance**: [Regulatory requirements]

### 4.3 Availability Requirements
- **Uptime**: [Target uptime percentage]
- **Error Rate**: [Target error rate]
- **Failover**: [Disaster recovery plan]
- **Backup**: [Backup and recovery procedures]

### 4.4 Compatibility Requirements
- **Browsers**: [Supported browsers]
- **Devices**: [Supported devices]
- **Screen Sizes**: [Responsive design requirements]
- **Network**: [Network connectivity requirements]

---

## 5. User Interface & Experience

### 5.1 Design Principles
- **Simplicity**: [Design philosophy]
- **Consistency**: [Design system approach]
- **Accessibility**: [Accessibility standards]
- **Performance**: [Performance considerations]

### 5.2 Key Interfaces
- **Homepage**: [Layout and functionality]
- **Main Features**: [Core functionality pages]
- **User Profile**: [User management interface]
- **Settings**: [Configuration interface]

### 5.3 Interaction Design
- **Navigation**: [Navigation structure]
- **User Flow**: [Key user flows]
- **Feedback**: [User feedback mechanisms]
- **Error Handling**: [Error handling approach]

---

## 6. Data & Analytics

### 6.1 Data Requirements
- **User Behavior**: [What user data to collect]
- **Business Metrics**: [What business data to track]
- **Technical Metrics**: [What technical data to monitor]
- **Financial Data**: [What financial data to track]

### 6.2 Data Collection
- **Tracking Strategy**: [How to track user interactions]
- **Data Storage**: [Data storage approach]
- **Privacy**: [Privacy protection measures]
- **Analytics**: [Analytics and reporting]

### 6.3 Key Metrics
- **Core Metrics**: [Primary success metrics]
- **Process Metrics**: [Secondary metrics]
- **Business Metrics**: [Business outcomes]
- **User Experience**: [User satisfaction metrics]

---

## 7. Technical Requirements

### 7.1 Technology Stack
- **Frontend**: [Frontend technologies]
- **Backend**: [Backend technologies]
- **Database**: [Database technologies]
- **Infrastructure**: [Infrastructure requirements]
- **DevOps**: [Development operations tools]

### 7.2 APIs & Integration
- **API Standards**: [API design standards]
- **Data Formats**: [Data format standards]
- **Authentication**: [API authentication]
- **Versioning**: [API versioning strategy]

### 7.3 Deployment & Operations
- **Environments**: [Deployment environments]
- **CI/CD**: [Continuous integration and deployment]
- **Monitoring**: [System monitoring]
- **Scaling**: [Scaling strategy]

---

## 8. Project Plan

### 8.1 Milestones
- **Phase 1**: Requirements & Tech Selection ([Duration])
- **Phase 2**: Design & Tech Planning ([Duration])
- **Phase 3**: Core Development ([Duration])
- **Phase 4**: Testing & Optimization ([Duration])
- **Phase 5**: Launch & Operations ([Duration])

### 8.2 Resources
- **Team**: [Team composition]
- **Technology**: [Technology requirements]
- **Budget**: [Budget considerations]
- **Training**: [Training requirements]

### 8.3 Risk Assessment
- **Technical Risks**: [Potential technical challenges]
- **Market Risks**: [Potential market challenges]
- **Resource Risks**: [Potential resource constraints]
- **Timeline Risks**: [Potential timeline issues]

---

## 9. Acceptance Criteria

### 9.1 Functional Acceptance
- [ ] Core features implemented and working
- [ ] User flows work correctly
- [ ] Error handling works properly
- [ ] Performance requirements met

### 9.2 Non-functional Acceptance
- [ ] Performance tests pass
- [ ] Security tests pass
- [ ] Compatibility tests pass
- [ ] Availability tests pass

### 9.3 User Experience Acceptance
- [ ] User testing successful
- [ ] Usability tests pass
- [ ] Accessibility requirements met
- [ ] Design consistency maintained

---

## 10. Appendix

### 10.1 Terminology
- [Term 1]: [Definition]
- [Term 2]: [Definition]

### 10.2 References
- [Reference 1]: [Link]
- [Reference 2]: [Link]

### 10.3 Related Documents
- [Related Document 1]: [Link]
- [Related Document 2]: [Link]

---

## Approval
- **Product Owner**: ________________ (Signature/Date)
- **Tech Lead**: ________________ (Signature/Date)
- **Design Lead**: ________________ (Signature/Date)
- **QA Lead**: ________________ (Signature/Date)
- **Project Sponsor**: ________________ (Signature/Date)
"""

    def _get_web_app_waterfall_template(self) -> str:
        """Get web app waterfall template (more detailed)."""
        template = self._get_web_app_agile_template()
        # Add more detailed sections for waterfall methodology
        return template.replace(
            "### 3.1 Core Features",
            "### 3.1 Core Features\n#### Detailed Requirements"
        ) + """

## 11. Detailed Technical Specifications

### 11.1 System Architecture
- **Architecture Pattern**: [Architecture approach]
- **Component Design**: [Component breakdown]
- **Data Flow**: [Data flow diagrams]
- **Integration Points**: [System integrations]

### 11.2 Database Design
- **Schema Design**: [Database schema]
- **Data Relationships**: [Entity relationships]
- **Indexing Strategy**: [Performance optimization]
- **Backup Strategy**: [Data protection]

### 11.3 API Design
- **API Endpoints**: [Complete API specification]
- **Data Models**: [Data model definitions]
- **Error Handling**: [Error response formats]
- **Rate Limiting**: [Usage limitations]

### 11.4 Security Design
- **Authentication Flow**: [Authentication process]
- **Authorization Model**: [Permission system]
- **Data Protection**: [Security measures]
- **Compliance**: [Regulatory compliance]

## 12. Implementation Plan

### 12.1 Detailed Timeline
- **Week 1-2**: Detailed requirements gathering
- **Week 3-4**: Technical design and architecture
- **Week 5-8**: Core implementation
- **Week 9-10**: Integration and testing
- **Week 11-12**: User acceptance testing
- **Week 13-14**: Deployment and launch

### 12.2 Resource Allocation
- **Week 1-2**: Product Manager, Architect
- **Week 3-4**: Architect, Senior Developers
- **Week 5-8**: Full development team
- **Week 9-10**: Developers, QA Engineers
- **Week 11-12**: QA Engineers, User Testers
- **Week 13-14**: Operations Team, Product Manager

### 12.3 Deliverables
- [ ] Requirements specification document
- [ ] Technical architecture document
- [ ] Database design document
- [ ] API specification document
- [ ] Complete implementation
- [ ] Test reports
- [ ] User acceptance test results
- [ ] Deployment plan

## 13. Quality Assurance Plan

### 13.1 Testing Strategy
- **Unit Testing**: [Unit testing approach]
- **Integration Testing**: [Integration testing approach]
- **System Testing**: [System testing approach]
- **User Acceptance Testing**: [UAT approach]

### 13.2 Test Cases
- [ ] Functional test cases
- [ ] Performance test cases
- [ ] Security test cases
- [ ] Compatibility test cases
- [ ] User acceptance test cases

### 13.3 Quality Metrics
- **Code Coverage**: [Target coverage percentage]
- **Bug Density**: [Target bug rate]
- **Performance Benchmarks**: [Performance targets]
- **User Satisfaction**: [Satisfaction targets]
"""

    def _get_web_app_mvp_template(self) -> str:
        """Get web app MVP template (focused on core features)."""
        template = self._get_web_app_agile_template()
        # Simplify for MVP focus
        return template.replace(
            "## 1. Product Overview",
            "## 1. Product Overview\n\n### 1.1 MVP Scope\n**In Scope for MVP:**\n- [Core Feature 1]\n- [Core Feature 2]\n- [Essential Feature 3]\n\n**Out of Scope for MVP:**\n- [Feature 1 - Post-MVP]\n- [Feature 2 - Post-MVP]\n- [Nice-to-have Feature 3]"
        ) + """

## 14. Go-to-Market Strategy

### 14.1 Launch Strategy
- **Target Audience**: [Primary market segment]
- **Launch Channels**: [Go-to-market channels]
- **Messaging**: [Product positioning]
- **Success Metrics**: [Launch success criteria]

### 14.2 Post-MVP Roadmap
- **Phase 1 (Month 1-2)**: [Post-MVP features]
- **Phase 2 (Month 3-4)**: [Additional features]
- **Phase 3 (Month 5-6)**: [Advanced features]

### 14.3 Feedback Loop
- **User Feedback Collection**: [How to gather feedback]
- **Iterative Improvements**: [Improvement process]
- **Feature Prioritization**: [Prioritization framework]
- **Success Measurement**: [How to measure success]
"""

    def _get_mobile_app_agile_template(self) -> str:
        """Get mobile app agile template."""
        template = self._get_web_app_agile_template()
        return template.replace("Web Application", "Mobile Application").replace(
            "## 4. Compatibility Requirements",
            "## 4. Compatibility Requirements\n\n### 4.1 Mobile Platform Requirements\n- **iOS**: [Supported iOS versions]\n- **Android**: [Supported Android versions]\n- **Devices**: [Supported device types]\n- **Screen Sizes**: [Supported screen resolutions]\n\n### 4.2 Performance Requirements\n- **App Launch Time**: [Target launch time]\n- **Memory Usage**: [Target memory footprint]\n- **Battery Usage**: [Target battery consumption]\n- **Network Resilience**: [Offline capabilities]"
        )

    def _get_mobile_app_waterfall_template(self) -> str:
        """Get mobile app waterfall template."""
        template = self._get_mobile_app_agile_template()
        return self._get_web_app_waterfall_template().replace("Web Application", "Mobile Application")

    def _get_mobile_app_mvp_template(self) -> str:
        """Get mobile app MVP template."""
        template = self._get_mobile_app_agile_template()
        return self._get_web_app_mvp_template().replace("Web Application", "Mobile Application")

    def _get_saas_agile_template(self) -> str:
        """Get SaaS agile template."""
        template = self._get_web_app_agile_template()
        return template.replace("Web Application", "SaaS Platform").replace(
            "## 7. Technical Requirements",
            "## 7. Technical Requirements\n\n### 7.1 Multi-tenant Architecture\n- **Tenant Isolation**: [Data isolation strategy]\n- **Resource Sharing**: [Resource allocation]\n- **Scaling**: [Tenant-specific scaling]\n\n### 7.2 Subscription Management\n- **Billing Integration**: [Payment processing]\n- **Usage Tracking**: [Resource monitoring]\n- **Tier Management**: [Subscription tiers]"
        )

    def _get_saas_waterfall_template(self) -> str:
        """Get SaaS waterfall template."""
        template = self._get_saas_agile_template()
        return self._get_web_app_waterfall_template().replace("Web Application", "SaaS Platform")

    def _get_saas_mvp_template(self) -> str:
        """Get SaaS MVP template."""
        template = self._get_saas_agile_template()
        return self._get_web_app_mvp_template().replace("Web Application", "SaaS Platform")

    def _get_ecommerce_agile_template(self) -> str:
        """Get e-commerce agile template."""
        template = self._get_web_app_agile_template()
        return template.replace("Web Application", "E-commerce Platform").replace(
            "## 3. Functional Requirements",
            "## 3. Functional Requirements\n\n### 3.1 E-commerce Core Features\n#### Product Management\n- **Product Catalog**: [Product display capabilities]\n- **Product Search**: [Search functionality]\n- **Product Filtering**: [Filter and categorization]\n\n#### Shopping Cart\n- **Cart Management**: [Add/remove items]\n- **Price Calculation**: [Tax and shipping]\n- **Cart Persistence**: [Save cart functionality]\n\n#### Checkout Process\n- **Guest Checkout**: [Anonymous purchasing]\n- **User Accounts**: [Registered user checkout]\n- **Payment Processing**: [Payment integration]\n\n#### Order Management\n- **Order Tracking**: [Order status updates]\n- **Order History**: [Past orders]\n- **Returns/Refunds**: [Return processing]"
        )

    def _get_ecommerce_waterfall_template(self) -> str:
        """Get e-commerce waterfall template."""
        template = self._get_ecommerce_agile_template()
        return self._get_web_app_waterfall_template().replace("Web Application", "E-commerce Platform")

    def _get_ecommerce_mvp_template(self) -> str:
        """Get e-commerce MVP template."""
        template = self._get_ecommerce_agile_template()
        return self._get_web_app_mvp_template().replace("Web Application", "E-commerce Platform")


def main():
    """Main function for command-line interface."""
    parser = argparse.ArgumentParser(description='Generate Product Requirements Document (PRD)')

    parser.add_argument('--product-name', required=True,
                       help='Name of the product')
    parser.add_argument('--product-type', required=True, choices=['web-app', 'mobile-app', 'saas', 'ecommerce'],
                       help='Type of product')
    parser.add_argument('--methodology', required=True, choices=['agile', 'waterfall', 'mvp'],
                       help='Development methodology')
    parser.add_argument('--output-file',
                       help='Output file path (default: [product-name]-prd.md)')
    parser.add_argument('--with-user-stories', action='store_true',
                       help='Include user stories for agile methodology')

    # Additional customization options
    parser.add_argument('--pm-name', default='[Name]',
                       help='Product Manager name')
    parser.add_argument('--tech-lead', default='[Name]',
                       help='Technical lead name')
    parser.add_argument('--design-lead', default='[Name]',
                       help='Design lead name')
    parser.add_argument('--test-lead', default='[Name]',
                       help='Test lead name')

    args = parser.parse_args()

    generator = PRDGenerator()

    try:
        output_file = generator.generate_prd(
            product_name=args.product_name,
            product_type=args.product_type,
            methodology=args.methodology,
            output_file=args.output_file,
            with_user_stories=args.with_user_stories,
            pm_name=args.pm_name,
            tech_lead=args.tech_lead,
            design_lead=args.design_lead,
            test_lead=args.test_lead
        )

        print(f"✅ PRD generated successfully: {output_file}")
        print(f"📋 Template type: {args.product_type} ({args.methodology})")
        if args.with_user_stories:
            print("👥 User stories included")

    except Exception as e:
        print(f"❌ Error generating PRD: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()