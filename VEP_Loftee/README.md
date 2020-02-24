* Dockerfile: commands to build the docker image that have VEP and plugins including LOFTEE.
* gnomad.v2.1.1.oe_lof.by_gene.txt: gnomad recommend to replace ExACpLI loss of
function intolerant score with observed/expected (oe) metric. Details are here:https://macarthurlab.org/2018/10/17/gnomad-v2-1/. So I downloaded the constraint file from gnomad and extract two columns (gene symbol and oe_lof).
* Dockerfile_v1: commands to build the docker image that have VEP and plugins including LOFTEE, replace ExACpLI with gnomad.

Run the vep annotation pipeline in HPC using singularity
--------------------------------------------------------

1. Pull the image using the command: **singularity pull docker://shl198/vep_loftee:97.4_gnomad_pLI**, this will download image file **vep_loftee_97.4_gnomad_pLI.sif**.
2. Download GRCh38 reference genome from ensembl(http://ftp.ensembl.org/pub/release-97/fasta/homo_sapiens/dna/Homo_sapiens.GRCh38.dna.primary_assembly.fa.gz).
3. Check this website 'https://github.com/konradjk/loftee/tree/grch38' and download file **human_ancestor_fa.gz**, and bigwig file **gerp_conservation_scores.homo_sapiens.GRCh38.bw**, and PhyloCSF file **phylocsf_gerp.sql**, then put the files into a loftee folder.
4. In the container run the command:
bsub -q express -o log.txt "singularity run -B **/path/to/your/vcf/folder**:/mnt,**/path/to/loftee**:/opt/loftee,**/path/to/folder/that/have/reference/genome/file**:/media **/path/to/file/vep_loftee_97.4_gnomad_pLI.sif** vep -i **/mnt/vcf.gz** --plugin LoF,loftee_path:/opt/loftee,human_ancestor_fa:/opt/loftee/human_ancestor_fa.gz,gerp_bigwig:/opt/loftee/gerp_conservation_scores.homo_sapiens.GRCh38.bw,conservation_file:/opt/loftee/phylocsf_gerp.sql --dir_plugins /opt/loftee --plugin Carol --plugin Condel,:/opt/.vep/Plugins/config/Condel/config,b --plugin ExACpLI,/opt/gnomad.v2.1.1.oe_lof.by_gene.txt --plugin LoFtool,/opt/.vep/Plugins/LoFtool_scores.txt -o **/output/vcf/file** --cache --force_overwrite --buffer_size 10000 --species homo_sapiens --assembly GRCh38 --dir /media/vep_db_97_GRCH38 --offline --fork 1 --hgvs -e --fa /media/GRCh38_vep97.fa --minimal --allele_number --check_existing --vcf --compress_output gzip"