# *Daphnia* Genome Annotation & Transcriptomics Analysis

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![GitHub issues](https://img.shields.io/github/issues/Aridoge13/Evo-Genomics)
![GitHub last commit](https://img.shields.io/github/last-commit/Aridoge13/Evo-Genomics)

This repository documents the genome annotation and transcriptomic analysis pipeline for *Daphnia magna*, with all steps executed on a local Linux/WSL system. The workflow uses EviAnn for annotation and aims to scale toward transcript quantification, comparative genomics, and functional annotation using modern tools. 

This pipeline is not specific to the *Daphnia magna* and can be used for evolutionary genomics study involving any species.

---

## Project Overview

```mermaid

flowchart TD
    A[Install EviAnn and Dependencies] --> B[Download & Prepare Inputs]
    B --> C[Index Genome\nhisat2-build]
    C --> D[Map RNA-seq Reads\nhisat2]
    D --> E[Convert SAM to BAM & Sort\nsamtools]
    E --> F[Reconstruct Transcripts\nstringtie]
    F --> G[Run EviAnn Pipeline]
    G --> H{Successful?}
    H -- No .gtf files --> I[Debug Transcript Merge Issue]
    I --> F
    H -- Yes --> J[Predict Proteins\nTransDecoder]
    J --> K[Quality Control & Filtering]
    K --> L[Functional Annotation\neggNOG - pending]
    L --> M[Transcript Quantification\nSalmon] 
    M --> N[Comparative Genomics & Visualization]
%% Color definitions
    style A fill:#d32f2f,stroke:#b71c1c,color:#ffffff
    style B fill:#f57c00,stroke:#ff6f00,color:#ffffff
    style C fill:#f57c00,stroke:#1b5e20,color:#ffffff
    style D fill:#f57c00,stroke:#e65100,color:#ffffff
    style E fill:#ffa000,stroke:#b71c1c,color:#ffffff
    style F fill:#ffa000,stroke:#ff6f00,color:#ffffff
    style G fill:#ffa000,stroke:#1b5e20,color:#ffffff
    style H fill:#ffa000,stroke:#e65100,color:#ffffff
    style I fill:#388e3c,stroke:#b71c1c,color:#ffffff
    style J fill:#388e3c,stroke:#ff6f00,color:#ffffff
    style K fill:#388e3c,stroke:#1b5e20,color:#ffffff
    style L fill:#388e3c,stroke:#e65100,color:#ffffff
    style M fill:#1976d2,stroke:#0d47a1,color:#ffffff
    style N fill:#1976d2,stroke:#ff6f00,color:#ffffff
```

---

## Requirements
Tested on Linux (Ubuntu). WSL or HPC systems are recommended for memory-intensive steps.

### Dependencies
|Tool|	Purpose|
|----|---------|
|EviAnn|	Genome annotation core pipeline|
|SRA Toolkit|	FASTQ download from SRA|
|SwissProt|	Homology reference DB|
|hisat2|	RNA-seq alignment|
|samtools|	Format conversion, sorting|
|stringtie|	Transcript reconstruction|
|gffcompare|	GTF comparison and merging|
|TransDecoder|	ORF prediction|
|blastp|	Protein homology search|
|makeblastdb|	BLAST database creation|
|salmon|	Transcript quantification|

> All tools are installed in Tools/ or via conda. See environment.yml for reproducibility.

---
## How to run EviAnn
```bash
./eviann.sh -g path/to/the/genome/fasta/sequence -r path/to/the/paired/reads/text/file -p path/to/the/proteome

```
---

## Issues Faced
- Missing .gtf Files for Transcript Merge
Cause: Incorrect use of stringtie with FASTQ files instead of BAM.
Fix: Corrected by using the appropriate aligned BAM files.

- eggNOG-mapper Alignment Failure (DIAMOND)
eggNOG-mapper was successfully installed and run via Docker. However, it failed at the DIAMOND alignment step with the error:

```bash
Error running diamond: Loading reference sequences... Killed
```

Diagnosis: DIAMOND was terminated by the kernel due to excessive memory usage — a common issue with large protein datasets on machines with <16–32 GB RAM.

Solution: This step requires high-performance compute (HPC) nodes or cloud instances with sufficient RAM (32–64 GB recommended). Either of the following can be attempted:

- Re-run DIAMOND alignment via eggNOG on an HPC cluster.
- Use cloud platforms like AWS/GCP with high-memory instances.
- Try conda/local eggNOG install on a workstation with more RAM. 

---

## Steps Completed
1. ✅ Installed EviAnn pipeline and dependencies.

2. ✅ Indexed genome using hisat2-build.

3. ✅ Aligned paired-end reads using hisat2.

4. ✅ Converted SAM to sorted BAM with samtools.

5. ✅ Attempted transcript reconstruction using stringtie.

6. ⚠️ Merge failure: .gtf files generated, but an error message popped up likely due to evidence mis-specification.

7. ✅ Corrected by replacing .fastq inputs with proper .txt file listing evidence.

8. ✅ Quality Control and Filtering of files obtained from EviAnn annotation.

9. ✅ Re-ran pipeline with improved input handling (pending eggNOG).

10. 🚧 Functional annotation step using eggNOG-mapper failed due to Docker argument bug.

11. ⏳ Transcript quantification with salmon queued up next.

---

## Planned Pipeline Modules

|Step | Completion status|
|-----|------------------|
|Functional Annotation| Currently developing & debugging|
|Transcript Quantification| Upcoming|
|Comparative Genomics| Upcoming|
|Visualization| Upcoming|
|Publication Preparation | Upcoming|

## References
- EviAnn: https://github.com/alekseyzimin/EviAnn_release

## Contact
**Aritra Mukherjee**
- **Email**: aritra.mukherjee98@gmail.com
- **LinkedIn**: https://www.linkedin.com/in/aritra-mukherjee-82b070125/