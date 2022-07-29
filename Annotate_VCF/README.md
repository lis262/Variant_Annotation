This is the pipeline to annotate the vcf file. Start from the gzip vcf file. Steps are:

1. Make sure nextflow is installed and in the pathway.
2. Pull the image using the command: **singularity pull docker://shl198/vep_loftee:101.0_gnomad_pLI**, this will download image file **vep_loftee_101.0_gnomad_pLI.sif**.
3. Configure the parameters in file **p01_annotate_vcf_parameters.config**.
4. Run the following command:
     
		bsub -o log.txt -q short -n 16 -M 41457280 -R "span[ptile=16]" \
		"singularity run -B /:/media /path/to/vep_loftee_101.0_gnomad_pLI.sif \
		nextflow run /media/path/to/p01_annotate_vcf_GRCh38.nf \
		-c /media/path/to/p01_annotate_vcf_Parameters_GRCh38.config \
		-resume \
		-w /media/lustre/workspace/projects/BLCA/Results/WES/vcf/anno/work"
* -c: path to the parameter file
* -resume: this is to make sure the job will pick up from where it failed.
* -w: this is to set the work directory for all of the intermediate files.

5. Files startswith m are for further downstream analysis after vep annotation.

Attention: In the configure file, you can see all file paths have prefix /media/, that's because for singularity we set a parameter -B /:/media. this means the singularity mount the folder / in your local computer to /media in the container, so all the full path of the files in local computer would have a /media prefix in the container.