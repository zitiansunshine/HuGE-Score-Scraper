## Description

This is a Docker-based scraper for extracting **Human Genetic Evidence scores** from the [Common Metabolic Diseases Knowledge Portal (hugeamp.org)](https://hugeamp.org).  
It is designed for **HPC workflows**, allowing users to run large-scale jobs and retrieve scores for **thousands of genes in parallel** using the provided sample `.sh` script.

For each gene-trait pair, the output is a simple table with three columns:

- `gene_name`
- `trait`
- `score`

Pull the image with:

```bash
docker pull zitiansunshine/huge-scraper:latest
```
