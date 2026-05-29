# PRD Writing Guidance and Best Practices

## Core Writing Principles

### 1. Clarity and Conciseness
- **Use clear, straightforward language**
- **Avoid jargon and technical terms when possible**
- **Be specific and concrete**
- **Write in the active voice**
- **Keep sentences short (ideally under 20 words)**

### 2. Completeness and Thoroughness
- **Cover all aspects of the product**
- **Include all stakeholders' requirements**
- **Address both functional and non-functional needs**
- **Consider edge cases and exceptions**

### 3. Consistency and Standardization
- **Use consistent terminology throughout**
- **Follow standard formatting and structure**
- **Maintain consistent priority levels**
- **Use standardized templates and formats**

### 4. Actionability and Testability
- **Write requirements that can be implemented**
- **Include measurable acceptance criteria**
- **Define clear success metrics**
- **Provide specific examples when needed**

## Language Usage Guidelines

### Active vs. Passive Voice
**Good (Active):**
- "The system shall process user requests within 2 seconds"
- "Users can search for products using filters"

**Avoid (Passive):**
- "User requests should be processed within 2 seconds"
- "Search functionality is provided for products"

### Specific vs. Vague Language
**Good (Specific):**
- "The system shall support 10,000 concurrent users"
- "Search results shall load within 1.5 seconds"
- "Users shall be able to filter products by price range ($0-$1000)"

**Avoid (Vague):**
- "The system should support many users"
- "Search should be fast"
- "Users can filter products by price"

### Measurable Language
**Good (Measurable):**
- "System availability shall be 99.9%"
- "Error rate shall be less than 0.1%"
- "Response time shall be under 500ms"

**Avoid (Unmeasurable):**
- "The system should be reliable"
- "Errors should be minimal"
- "Performance should be good"

## Requirement Writing Patterns

### User Stories
**Standard Format:**
```
As a [user role]
I want [functionality]
So that [benefit]
```

**Examples:**
```
As a registered user
I want to reset my password
So that I can regain access to my account

As a shopper
I want to filter products by price range
So that I can find products within my budget
```

### Acceptance Criteria
**Structure:**
- Use bullet points with checkboxes
- Start with "Given-When-Then" format for scenarios
- Include both positive and negative cases

**Examples:**
```
Given I am a registered user
When I enter my email address
And I request a password reset
Then I receive a reset link via email

Given I am not a registered user
When I request a password reset
Then I receive an error message
```

### Functional Requirements
**Template:**
```
[Feature Name]
- Description: [Clear description of what the feature does]
- Priority: [High/Medium/Low]
- Acceptance Criteria:
  - [ ] [Specific testable criteria]
  - [ ] [Another testable criteria]
- Dependencies: [Any dependencies on other features]
- Constraints: [Any technical or business constraints]
```

### Non-Functional Requirements
**Template:**
```
[Requirement Type]
- Metric: [Specific metric with value]
- Measurement Method: [How to measure this]
- Target Value: [Specific target]
- Testing Approach: [How to test this requirement]
```

## Common Writing Pitfalls and How to Avoid Them

### 1. Ambiguous Requirements
**Problem:** Vague language that can be interpreted in multiple ways
**Solution:** Use specific, measurable language and examples

**Bad:** "The system should be user-friendly"
**Good:** "The system shall have a navigation structure that allows users to complete common tasks within 3 clicks"

### 2. Unrealistic Requirements
**Problem:** Requirements that are technically impossible or impractical
**Solution:** Consult with technical team to validate feasibility

**Bad:** "The system shall respond instantly to all requests"
**Good:** "The system shall respond to requests within 100ms for 95% of transactions"

### 3. Missing Requirements
**Problem:** Critical requirements are overlooked
**Solution:** Use checklists and involve all stakeholders

**Checklist:**
- [ ] User roles and permissions defined
- [ ] Error handling specified
- [ ] Performance targets defined
- [ ] Security requirements specified
- [ ] Integration requirements defined
- [ ] Success metrics defined

### 4. Over-specified Requirements
**Problem:** Too much detail that limits flexibility
**Solution:** Focus on "what" not "how"

**Bad:** "The system shall use React with TypeScript and Redux to manage state"
**Good:** "The system shall maintain user state across page refreshes"

### 5. Conflicting Requirements
**Problem:** Requirements that contradict each other
**Solution:** Review requirements for consistency and resolve conflicts

**Bad:** "The system shall be highly secure" and "The system shall allow easy access for all users"
**Good:** "The system shall use role-based access control to balance security and usability"

## Document Structure Guidelines

### Standard PRD Structure
```
1. Document Information
   - Title, version, dates, team members

2. Product Overview
   - Vision, goals, success metrics

3. User Analysis
   - Target users, personas, journey

4. Functional Requirements
   - Features, user stories, acceptance criteria

5. Non-Functional Requirements
   - Performance, security, usability

6. Technical Requirements
   - Architecture, technology stack

7. Project Plan
   - Timeline, resources, risks

8. Acceptance Criteria
   - Testing approach, success criteria

9. Appendix
   - Terms, references, related docs
```

### Section Writing Guidelines
**Product Overview:**
- Start with the "why" - the problem you're solving
- Define clear, measurable goals
- Include business context and opportunity

**User Analysis:**
- Be specific about target users
- Include demographic and behavioral data
- Map user journeys and pain points

**Functional Requirements:**
- Prioritize features clearly
- Write user stories for complex features
- Include acceptance criteria for each feature

**Non-Functional Requirements:**
- Be specific about performance targets
- Define security requirements clearly
- Include accessibility and compliance needs

## Quality Review Checklist

### Before Final Review
- [ ] All sections are complete
- [ ] Language is clear and concise
- [ ] Requirements are measurable and testable
- [ ] Terminology is consistent
- [ ] Priorities are clearly defined
- [ ] Dependencies and constraints are identified
- [ ] Success metrics are established
- [ ] All stakeholders have reviewed

### Common Issues to Watch For
- **Vague language**: Replace with specific terms
- **Long sentences**: Break into shorter ones
- **Passive voice**: Convert to active voice
- **Unmeasurable requirements**: Add specific metrics
- **Missing edge cases**: Consider boundary conditions
- **Inconsistent priorities**: Standardize the approach

## Writing Tools and Resources

### Recommended Tools
- **Markdown editors**: Visual Studio Code, Typora, Obsidian
- **Collaboration tools**: Google Docs, Confluence, Notion
- **Diagram tools**: Draw.io, Lucidchart, Miro
- **Version control**: Git, GitHub, GitLab

### Templates and Examples
- Use standardized templates for consistency
- Reference examples for complex sections
- Maintain a library of well-written requirements
- Create style guides for your organization

### Review Process
1. **Self-review**: Check for clarity and completeness
2. **Peer review**: Have team members review
3. **Stakeholder review**: Get input from all stakeholders
4. **Technical validation**: Ensure feasibility
5. **Final approval**: Get sign-off from decision-makers

## Continuous Improvement

### Gather Feedback
- Collect feedback from reviewers
- Track common issues and patterns
- Maintain an issue log and improvement plan

### Update Templates
- Regularly update templates based on feedback
- Incorporate industry best practices
- Share lessons learned with the team

### Measure Quality
- Track time spent on reviews
- Measure number of revisions
- Monitor requirement stability
- Track defect rates traced to requirements

By following these guidelines, you'll create PRDs that are clear, comprehensive, and actionable, leading to better product outcomes and reduced development risks.