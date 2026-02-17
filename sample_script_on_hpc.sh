#!/bin/bash
#$ -cwd
#$ -l h_data=110G,h_rt=16:00:00
#$ -pe shared 1
#$ -j y
#$ -t 1-1000
#$ -m ea


source ~/.bashrc
. /u/local/Modules/default/init/modules.sh
module load anaconda3
micromamba activate
module load apptainer
# Hardcoded input file
gene_list="/PATH/TO/GENE/LIST"

trait="T2D"

export TMPDIR=$SCRATCH

# Verify gene list exists
if [ ! -f "$gene_list" ]; then
    echo "Error: Gene list file $gene_list not found!"
    exit 1
fi

# Read all genes into an array
mapfile -t genes < "$gene_list"

# Calculate array index (SGE_TASK_ID is 1-based)
index=$((SGE_TASK_ID - 1))

# Validate task ID range
if [ $index -lt 0 ] || [ $index -ge ${#genes[@]} ]; then
    echo "Error: Invalid SGE_TASK_ID ($SGE_TASK_ID) for gene list with ${#genes[@]} genes"
    exit 1
fi

# Get current gene
gene="${genes[$index]}"

# Create output directory
output_dir="/PATH/TO/HUGE_${trait}"
mkdir -p "$output_dir"

# Execute and save output
apptainer exec ./HUGE_scraper.sif python /app/scraper.py "$gene" "$trait" > "${output_dir}/${gene}_${trait}_gene.txt"

echo "Processed gene $gene (task $SGE_TASK_ID)"



