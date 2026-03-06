# Completeness Checklist

**ALL boxes must be checked or marked "N/A" / "Limited evidence"**

## Identity & Context
- [ ] Official identifiers resolved (UniProt, Ensembl, NCBI)
- [ ] All synonyms/aliases documented
- [ ] Naming collisions identified and handled
- [ ] Protein architecture described (or N/A stated)
- [ ] Subcellular localization documented
- [ ] Baseline expression profile included

## Mechanism & Function
- [ ] Core mechanism section with evidence grades
- [ ] Pathway involvement documented
- [ ] Model organism evidence (or "none found")
- [ ] Complexes/interaction partners listed
- [ ] Key assays/readouts described

## Disease & Clinical
- [ ] Human genetic variants documented
- [ ] Constraint scores with interpretation
- [ ] Disease links with evidence strength grades
- [ ] Pathogen involvement (or "none identified")

## Synthesis
- [ ] Research themes clustered with ≥3 papers each
- [ ] Open questions/gaps articulated
- [ ] Biological model synthesized
- [ ] ≥3 testable hypotheses with experiments
- [ ] Conclusions with confidence assessment

## Technical
- [ ] All claims have source attribution
- [ ] Evidence grades applied throughout
- [ ] Bibliography file generated
- [ ] Data limitations documented

## Bibliography Format

**File**: `[topic]_bibliography.json`

```json
{
  "metadata": {
    "generated": "2026-02-04",
    "query": "ATP6V1A",
    "total_papers": 342,
    "unique_after_dedup": 287
  },
  "papers": [
    {
      "pmid": "12345678",
      "doi": "10.1038/xxx",
      "title": "Paper Title",
      "authors": ["Smith A", "Jones B"],
      "year": 2024,
      "journal": "Nature",
      "evidence_tier": "T1",
      "themes": ["lysosomal_acidification"],
      "oa_status": "gold"
    }
  ]
}
```

Also generate `[topic]_bibliography.csv` with same data.
