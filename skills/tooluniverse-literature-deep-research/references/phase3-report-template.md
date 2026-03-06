# Phase 3: Report Template (15 Sections)

**CRITICAL**: All 15 sections must exist, even if marked "N/A" or "Limited evidence"

## Output Files
1. `[topic]_report.md` - Main narrative report (Full Deep-Research Mode)
2. `[topic]_factcheck_report.md` - Short verification (Factoid Mode)
3. `[topic]_bibliography.json` - Full deduplicated bibliography
4. `methods_appendix.md` - Methodology (ONLY if requested)

## Report Structure

```markdown
# [TARGET/TOPIC]: Comprehensive Research Report

*Generated: [Date]*
*Total unique papers: [N]*

## Executive Summary
[2-3 paragraphs synthesizing key findings]
**Bottom Line**: [One-sentence actionable conclusion]

## 1. Target Identity & Aliases
### 1.1 Official Identifiers
### 1.2 Synonyms and Aliases
### 1.3 Known Naming Collisions

## 2. Protein Architecture
*[N/A for non-protein targets]*
### 2.1 Domain Structure
### 2.2 Isoforms
### 2.3 Key Structural Features

## 3. Complexes & Interaction Partners
## 4. Subcellular Localization
## 5. Expression Profile
## 6. Core Mechanisms
### 6.1 Molecular Function
### 6.2 Biological Role
### 6.3 Key Pathways
### 6.4 Regulation

## 7. Model Organism Evidence
## 8. Human Genetics & Variants
## 9. Disease Links
### 9.1 Strong Evidence (Genetic + Functional)
### 9.2 Moderate Evidence (Association + Mechanism)
### 9.3 Weak Evidence (Association Only)

## 10. Pathogen Involvement
*[State "None identified" if not applicable]*

## 11. Key Assays & Readouts
## 12. Research Themes
### 12.1 [Theme 1] (N papers)
### 12.2 [Theme 2] (N papers)
*[Require ≥3 papers per theme, or state "limited evidence"]*

## 13. Open Questions & Research Gaps
## 14. Biological Model & Testable Hypotheses
### 14.1 Integrated Biological Model
### 14.2 Testable Hypotheses Table
### 14.3 Suggested Experiments

## 15. Conclusions & Recommendations
### 15.1 Key Takeaways
### 15.2 Confidence Assessment
### 15.3 Recommended Next Steps

## References
### Key Papers (Must-Read)
1. [Citation] - [Why important] [Grade: ★★★]

## Data Limitations
```

## Factoid Mode (Fast Path)

For single-answer questions:

```markdown
# [TOPIC]: Fact-check Report

## Question
[User question]

## Answer
**[One-sentence answer]** [Evidence: ★★★/★★☆/★☆☆]

## Source(s)
- [Primary paper citation]

## Verification Notes
- [Where in paper: Abstract/Results/Methods]

## Limitations
- [If full text not available]
```
