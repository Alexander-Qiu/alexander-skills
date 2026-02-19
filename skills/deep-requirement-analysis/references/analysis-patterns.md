# Analysis Patterns

Common patterns for different types of technical analysis.

## Pattern 1: Technology Comparison

Use when comparing frameworks, libraries, or tools.

### Dimensions to Analyze
1. **Architecture**: Design philosophy, component structure
2. **Performance**: Throughput, latency, resource usage
3. **Features**: Capabilities, limitations
4. **Ecosystem**: Community, documentation, plugins
5. **Maturity**: Stability, version history, breaking changes
6. **Integration**: Compatibility with existing stack

### Verification Steps
- [ ] Check official documentation for claims
- [ ] Verify version numbers and release dates
- [ ] Look for recent GitHub issues/PRs
- [ ] Check if examples still work with latest version

### Output Format
```markdown
## Comparison: [Tech A] vs [Tech B]

### Quick Summary
| Aspect | [Tech A] | [Tech B] | Winner |
|--------|----------|----------|--------|
| [Aspect] | | | |

### Detailed Analysis

#### 1. Architecture
**[Tech A]**:
- 

**[Tech B]**:
- 

#### 2. Performance
[Benchmark results with methodology]

#### 3. Feature Matrix
| Feature | A | B | Notes |
|---------|---|---|-------|

### Recommendation
[Clear recommendation with rationale]
```

## Pattern 2: Code Review / Refactoring

Use when reviewing or refactoring existing code.

### Analysis Steps
1. **Understand the code**: What does it do? What's the intent?
2. **Identify issues**: Bugs, smells, performance issues
3. **Check context**: How is it used? What are the constraints?
4. **Evaluate alternatives**: What are better ways to do this?
5. **Assess risk**: What could break? How to test?

### Checklist
- [ ] Correctness: Does it handle edge cases?
- [ ] Performance: Any obvious bottlenecks?
- [ ] Readability: Is the intent clear?
- [ ] Maintainability: Easy to modify?
- [ ] Testing: How is it tested? Coverage?
- [ ] Documentation: Are there comments/docs?

## Pattern 3: System Design

Use when designing new systems or architectures.

### Key Questions
1. **Scale**: Expected load (QPS, data volume, users)?
2. **Latency**: Response time requirements?
3. **Availability**: Uptime requirements? Maintenance windows?
4. **Consistency**: Strong consistency required? Can tolerate eventual?
5. **Security**: Authentication, authorization, data protection?
6. **Observability**: Logging, metrics, tracing, alerting?

### Trade-off Analysis
Document key trade-offs:
- Consistency vs Availability
- Latency vs Throughput
- Complexity vs Performance
- Build vs Buy

## Pattern 4: Root Cause Analysis

Use when debugging or investigating issues.

### 5 Whys Method
1. Start with the problem
2. Ask "Why?" repeatedly (5 times)
3. Distinguish symptoms from root causes
4. Verify the root cause

### Fishbone Diagram Categories
- **People**: Knowledge, training, communication
- **Process**: Procedures, workflows, documentation
- **Technology**: Tools, libraries, infrastructure
- **Environment**: External dependencies, constraints

## Pattern 5: Requirements Analysis

Use when gathering or clarifying requirements.

### User Story Template
```
As a [type of user],
I want [some goal],
So that [some reason/benefit].
```

### INVEST Criteria
- **I**ndependent: Can be developed separately
- **N**egotiable: Details can be discussed
- **V**aluable: Delivers value to users
- **E**stimable: Can estimate effort
- **S**mall: Can be done in one sprint
- **T**estable: Has acceptance criteria

### Acceptance Criteria
Given [context],
When [action],
Then [expected outcome].
