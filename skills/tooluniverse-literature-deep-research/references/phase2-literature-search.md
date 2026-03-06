# Phase 2: Literature Search Methodology

**NOTE**: This methodology is internal. The report shows findings, not process.

## 2.1 Query Strategy: Collision-Aware Synonym Plan

### Step 1: High-Precision Seed Queries
Build mechanistic core with specific queries:
```
"[SYMBOL]"[Title/Abstract] AND ("mechanism" OR "function" OR "activity")
```

### Step 2: Citation Network Expansion
- Get papers citing seed papers
- Get papers referenced by seed papers
- Expand to 2nd degree if needed

### Step 3: Collision-Filtered Broader Queries
```
"[SYMBOL]" OR "[alias1]" OR "[alias2]" NOT [collision_term1] NOT [collision_term2]
```

## 2.2 Evidence Grading

| Tier | Grade | Definition |
|------|-------|------------|
| T1 | ★★★ | Primary experimental evidence (Results/Methods) |
| T2 | ★★☆ | Strong indirect evidence (review citing primary) |
| T3 | ★☆☆ | Weak evidence (screen hit, text-mined) |
| T4 | ☆☆☆ | Review only (no primary source identified) |

## 2.3 Theme Extraction

1. **Extract keywords** from titles and abstracts
2. **Cluster into themes** using semantic similarity
3. **Require minimum 3 papers** per theme
4. **Label themes** with standardized names

### Standard Theme Categories
- `function_mechanism` - Core molecular function
- `disease_association` - Disease links
- `regulation_signaling` - Regulatory mechanisms
- `structure_biophysics` - Structural studies
- `therapeutic` - Drug development
- `methodology` - Assays/tools

### Theme Quality Requirements

| Papers | Theme Status |
|--------|--------------|
| ≥10 | Major theme (full section) |
| 3-9 | Minor theme (subsection) |
| <3 | Insufficient (note as "limited evidence") |

## Tool Categories

### Literature Tools
`PubMed_search_articles`, `PMC_search_papers`, `EuropePMC_search_articles`, `openalex_literature_search`, `SemanticScholar_search_papers`

### Citation Tools
`PubMed_get_cited_by`, `EuropePMC_get_citations`, `EuropePMC_get_references`

### OA Tools
Use OA flags from Europe PMC / OpenAlex / Unpaywall
