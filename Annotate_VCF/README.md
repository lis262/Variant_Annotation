This is the pipeline to annotate the vcf file. Start from the gzip vcf file. Steps are:

1. Make sure nextflow is installed and in the pathway.
2. Configure the parameters in file p01_annotate_vcf_parameters.config
3. Run the following command:
     bsub -o log.txt -q short -n 16 -M 41457280 -R "span[ptile=16]" "nextflow run p01_annotate_vcf.nf -c p01_annotate_vcf_Parameters.config  -resume"
4. Files startswith m are for further downstream analysis after vep annotation.