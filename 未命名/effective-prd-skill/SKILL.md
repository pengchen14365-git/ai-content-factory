---
name: effective-product-requirements-document
description: Comprehensive product requirements document (PRD) creation, analysis, and optimization with support for different product types, methodologies (agile, waterfall), writing guidance, template generation, quality assurance, and collaborative workflows. Use when Claude needs to work with product requirements documents for: (1) Creating new PRD from scratch, (2) Analyzing existing PRD quality, (3) Generating templates for specific product types, (4) Providing writing guidance and best practices, (5) Conducting PRD reviews and quality checks, (6) Collaborating on PRD development with team members, (7) Converting between different methodologies (agile to waterfall, etc.)
---

# Effective Product Requirements Document (PRD) Creation

## Quick Start

Create a comprehensive PRD from scratch:

```bash
scripts/generate_prd.py --product-name "Product Name" --product-type web-app --methodology agile
```

## Core Features

### 1. PRD Template Generation
- **Supports multiple product types**: Web applications, mobile apps, SaaS products, e-commerce platforms
- **Multiple methodologies**: Agile, Scrum, Waterfall, MVP
- **Customizable templates**: Based on your specific industry and requirements
- **Auto-generation**: Create complete PRD structure with placeholders

### 2. PRD Quality Analysis
- **Structure validation**: Ensure all required sections are present
- **Clarity scoring**: Assess readability and comprehensiveness
- **Completeness check**: Verify all requirements are well-defined
- **Consistency analysis**: Check for conflicts or ambiguities

### 3. Writing Guidance
- **Best practices**: Industry-standard PRD writing guidelines
- **Common pitfalls**: Avoid typical PRD mistakes
- **Success criteria**: How to write effective acceptance criteria
- **User stories**: Techniques for crafting compelling user stories

### 4. Collaboration Features
- **Version tracking**: Manage PRD iterations and changes
- **Team collaboration**: Multi-user editing and review
- **Review workflows**: Structured review and approval processes
- **Stakeholder alignment**: Ensure all parties understand requirements

## Usage Patterns

### Creating a New PRD
```bash
# Generate basic PRD template
scripts/generate_prd.py --product-name "E-commerce Platform" --product-type web-app

# Generate agile PRD with user stories
scripts/generate_prd.py --product-name "Mobile App" --product-type mobile-app --methodology agile --with-user-stories

# Generate MVP PRD focused on core features
scripts/generate_prd.py --product-name "Startup Product" --product-type saas --methodology mvp
```

### Analyzing Existing PRD
```bash
# Check PRD quality
scripts/analyze_prd.py --file "existing-prd.md"

# Generate improvement suggestions
scripts/improve_prd.py --file "existing-prd.md" --focus readability

# Validate PRD completeness
scripts/validate_prd.py --file "existing-prd.md" --checklist completeness
```

### Collaborative Review
```bash
# Create review checklist
scripts/create_review_checklist.py --template comprehensive

# Track changes and versions
scripts/version_tracker.py --file "prd.md" --action create-version
```

## Methodology Support

### Agile Methodology
- User story format and prioritization
- Sprint planning integration
- Feature breakdown and iteration planning
- Acceptance criteria definition

### Waterfall Methodology
- Comprehensive requirements specification
- Detailed technical requirements
- Phased development approach
- Complete documentation requirements

### MVP Approach
- Core feature identification
- Minimum viable scope definition
- Risk assessment and mitigation
- Go-to-market strategy

## Reference Documentation

For detailed guidance on specific PRD components and methodologies:

- **[writing-guidance.md](writing-guidance.md)** - Writing techniques and best practices
- **[template-library.md](template-library.md)** - Available templates for different product types
- **[quality-checklist.md](quality-checklist.md)** - Quality validation criteria
- **[collaboration-workflows.md](collaboration-workflows.md)** - Team collaboration processes
- **[methodologies.md](methodologies.md)** - Different approach methodologies

## Supported File Formats

- Markdown (.md) - Primary format for PRD
- Word document (.docx) - For formal documentation
- PDF (.pdf) - For sharing and distribution
- JSON (.json) - For structured data and API integration

## Quality Assurance

The PRD skill includes comprehensive quality checks:

- **Structural integrity**: All required sections present and properly organized
- **Clarity and readability**: Clear, concise language without ambiguity
- **Completeness**: All aspects of the product requirements are covered
- **Consistency**: No conflicting requirements or specifications
- **Actionability**: Requirements are testable and implementable

## Getting Started

1. **Choose your product type**: Web app, mobile app, SaaS, etc.
2. **Select methodology**: Agile, Waterfall, MVP
3. **Generate template**: Use the appropriate script
4. **Customize content**: Fill in specific requirements
5. **Review and validate**: Ensure quality and completeness
6. **Collaborate**: Share with stakeholders for feedback

For detailed guidance on each component, refer to the reference documentation or use the specific analysis tools.