---
name: tooluniverse-literature-deep-research
description: Use when conducting comprehensive literature research, target profiling, or verifying scientific claims. MUST use for biological target research requiring ID resolution, evidence grading, and structured theme extraction. Triggers on literature review, target analysis, drug discovery research, or mechanistic investigations.
license: MIT
---

# Literature Deep Research

A systematic approach to comprehensive literature research that **starts with target disambiguation**, uses **evidence grading**, and produces **evidence-graded reports** with mandatory completeness sections.

## Key Principles

1. **Target disambiguation FIRST** - Resolve IDs, synonyms, naming collisions before literature search
2. **Right-size the deliverable** - Factoid Mode for single questions; Full Report for deep research
3. **Evidence grading** - Grade every claim (★★★ primary to ☆☆☆ review-only)
4. **Mandatory completeness** - All 15 sections must exist, even if "limited evidence"
5. **English-first queries** - Use English for all searches; respond in user's language

---

## Workflow Overview

```
User Query
  ↓
Phase 0: MODE SELECT (factoid vs deep report)
  ↓
Phase 1: TARGET DISAMBIGUATION
  ├─ Resolve official IDs (Ensembl, UniProt)
  ├─ Gather synonyms + naming collisions
  ├─ Protein architecture, localization, expression
  └─ GO terms, pathways
  ↓
Phase 2: LITERATURE SEARCH
  ├─ High-precision seed queries
  ├─ Citation network expansion
  ├─ Collision-filtered broad queries
  └─ Theme clustering + evidence grading
  ↓
Phase 3: REPORT SYNTHESIS
  ├─ Progressive writing to [topic]_report.md
  ├─ 15-section mandatory template
  └─ Biological model + testable hypotheses
```

---

## Phase 0: Mode Selection (CRITICAL)

Pick exactly one mode:

| Mode | Use Case | Deliverable |
|------|----------|-------------|
| **Factoid** | Single concrete question | `[topic]_factcheck_report.md` (≤1 page) |
| **Mini-review** | Narrow topic | 1-3 pages synthesis |
| **Full Deep-Research** | Comprehensive review | 15-section full report |

**Heuristic**:
- "Which antibiotic?" → **Factoid Mode**
- "What does literature say about X?" → **Full Deep-Research Mode**

---

## Phase 1: Target Disambiguation

**Default ON for biological targets** (genes/proteins)

See [references/phase1-target-disambiguation.md](references/phase1-target-disambiguation.md) for detailed procedures.

### Key Outputs

| Section | Data Source |
|---------|-------------|
| Official Identifiers | UniProt, Ensembl, NCBI |
| Naming Collisions | PubMed title search analysis |
| Protein Architecture | InterPro, UniProt |
| Subcellular Location | Human Protein Atlas, UniProt |
| Expression Profile | GTEx, HPA |
| Pathways | GO, Reactome, KEGG |

---

## Phase 2: Literature Search

See [references/phase2-literature-search.md](references/phase2-literature-search.md) for detailed methodology.

### Evidence Grading

| Tier | Grade | Definition |
|------|-------|------------|
| T1 | ★★★ | Primary experimental (Results/Methods) |
| T2 | ★★☆ | Strong indirect (review citing primary) |
| T3 | ★☆☆ | Weak (screen hit, text-mined) |
| T4 | ☆☆☆ | Review only |

### Theme Extraction

- Extract keywords from titles/abstracts
- Cluster semantically similar papers
- Require **≥3 papers** per theme
- Label with standardized names

---

## Phase 3: Report Synthesis

See [references/phase3-report-template.md](references/phase3-report-template.md) for complete 15-section template.

### Output Files

1. `[topic]_report.md` - Main narrative report (Full Mode)
2. `[topic]_factcheck_report.md` - Short verification (Factoid Mode)
3. `[topic]_bibliography.json` + `.csv` - Full bibliography
4. `methods_appendix.md` - Methodology (ONLY if requested)

### Report Sections (All 15 Required)

1. Target Identity & Aliases
2. Protein Architecture (or N/A)
3. Complexes & Interaction Partners
4. Subcellular Localization
5. Expression Profile
6. Core Mechanisms
7. Model Organism Evidence
8. Human Genetics & Variants
9. Disease Links
10. Pathogen Involvement (or "None")
11. Key Assays & Readouts
12. Research Themes
13. Open Questions & Research Gaps
14. Biological Model & Testable Hypotheses
15. Conclusions & Recommendations

---

## Completeness Checklist

See [references/completeness-checklist.md](references/completeness-checklist.md) for full checklist.

### Critical Items

- [ ] Official identifiers resolved
- [ ] Naming collisions identified
- [ ] Evidence grades applied throughout
- [ ] ≥3 papers per theme (or "limited evidence")
- [ ] ≥3 testable hypotheses
- [ ] Bibliography generated
- [ ] Data limitations documented

---

## Quick Tool Reference

### Literature
`PubMed_search_articles`, `EuropePMC_search_articles`, `openalex_literature_search`, `SemanticScholar_search_papers`

### Citation
`PubMed_get_cited_by`, `EuropePMC_get_citations`

### Protein/Gene
`UniProt_get_entry_by_accession`, `InterPro_get_protein_domains`, `ensembl_lookup_gene`

### Expression
`GTEx_get_median_gene_expression`, `HPA_get_subcellular_location`

### Disease
`gnomad_get_gene_constraints`, `clinvar_search_variants`, `OpenTargets_get_diseases_phenotypes_by_target_ensembl`

### Pathway
`GO_get_annotations_for_gene`, `Reactome_map_uniprot_to_pathways`, `kegg_get_gene_info`

---

## Communication Guidelines

**During research** (brief updates):
- "Resolving target identifiers and gathering baseline profile..."
- "Building core paper set with high-precision queries..."
- "Clustering into themes and grading evidence..."

**DO NOT expose**:
- Raw tool outputs
- Deduplication counts
- Search round details
- Database-by-database results

**The report is the deliverable. Methodology stays internal.**

---

## Summary

This skill produces comprehensive, evidence-graded research reports that:

1. **Start with disambiguation** to prevent naming collisions
2. **Use annotation tools** to fill gaps when literature is sparse
3. **Grade all evidence** to separate signal from noise
4. **Require completeness** even if stating "limited evidence"
5. **Synthesize into biological models** with testable hypotheses
6. **Keep methodology internal** unless explicitly requested

---

## References

- [Phase 1: Target Disambiguation](references/phase1-target-disambiguation.md)
- [Phase 2: Literature Search](references/phase2-literature-search.md)
- [Phase 3: Report Template](references/phase3-report-template.md)
- [Completeness Checklist](references/completeness-checklist.md)
