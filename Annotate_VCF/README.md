This is the pipeline to annotate the vcf file. Start from the gzip vcf file. Steps are:
1. split vcf file into chromosomes
2. normalize vcf file using vt (left align).
3. annotate vc file using VEP. 
4. Use m01_vcf2tab.py to transfer VEP from vcf format to table format.