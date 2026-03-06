# Phase 1: Target Disambiguation + Profile

**CRITICAL**: This phase prevents "missing target details" when literature is sparse or noisy.

## 1.1 Resolve Official Identifiers

```
UniProt_search → Get UniProt accession for human protein
UniProt_get_entry_by_accession → Full entry with cross-references
ensembl_lookup_gene → Ensembl gene ID, biotype
MyGene_get_gene_annotation → NCBI Gene ID, aliases, summary
```

**Output**:
```markdown
## Target Identity

| Identifier | Value | Source |
|------------|-------|--------|
| Official Symbol | ATP6V1A | HGNC |
| UniProt | P38606 | UniProt |
| Ensembl Gene | ENSG00000114573 | Ensembl |
```

## 1.2 Identify Naming Collisions

**Examples**:
- **TRAG**: T-cell regulatory gene vs bacterial TraG
- **JAK**: Janus kinase vs Just Another Kinase
- **CAT**: Catalase vs chloramphenicol acetyltransferase

**Detection strategy**:
1. Search PubMed for `"[SYMBOL]"[Title]`
2. If >20% off-topic, identify collision terms
3. Build negative filter: `NOT [collision_term]`

## 1.3 Protein Architecture & Domains

```
InterPro_get_protein_domains → Domain architecture
UniProt_get_ptm_processing_by_accession → PTMs, active sites
```

## 1.4 Subcellular Location

```
HPA_get_subcellular_location → Human Protein Atlas localization
UniProt_get_subcellular_location_by_accession → UniProt annotation
```

## 1.5 Baseline Expression

```
GTEx_get_median_gene_expression → Tissue expression (TPM)
HPA_get_rna_expression_by_source → HPA expression data
```

## 1.6 GO Terms & Pathway Placement

```
GO_get_annotations_for_gene → GO annotations
Reactome_map_uniprot_to_pathways → Reactome pathways
kegg_get_gene_info → KEGG pathways
OpenTargets_get_target_gene_ontology_by_ensemblID → Open Targets GO
```
