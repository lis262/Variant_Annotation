#!/usr/bin/env nextflow

/* ----------- define parameters ---------------------
*/
// (1) check environment resource
ava_mem = (double) (Runtime.getRuntime().freeMemory())
ava_cpu = Runtime.getRuntime().availableProcessors()

if (params.cpu != null && ava_cpu > params.cpu) {
    ava_cpu = params.cpu
}

if (params.mem != null && ava_mem > params.mem) {
    ava_mem = params.mem
}



// (2) related files
ref_fa   =  file(params.genome_fa)
ref_fai  =  ref_fa + '.fai'
ref_dict =  ref_fa.parent / ref_fa.baseName + '.dict'
if (!ref_fa.exists()) exit 1, "Reference genome not found: ${ref_fa}"


vcfs = params.vcf_path + '/*.vcf.gz'
vcfs_index = params.vcf_path + '/*.vcf.gz.tbi'

vcf_files = Channel.fromPath(vcfs, checkIfExists: true)
                    .map {file -> [file.simpleName, file]}

vcf_indexes = Channel.fromPath(vcfs_index, checkIfExists: true)
                    .map {file -> [file.simpleName, file]}

vcf_files
     .combine(vcf_indexes, by: 0) // format: [sample, vcf, vcf_idx]
     .set {vcf_and_idx}

// get all of the chromosomes
Channel
    .from(1..22)
    .map {'chr' + it.toString()}
    .set {chr_idx}

other = Channel.from('chrX','chrY','chrM')
chr_idx
     .concat(other)
     .into {chroms; chroms_for_merge}

// cross all vcf files with all chromosomes
vcf_and_idx
     .combine(chroms)
     .set {vcf_for_pass} // format: [sample,vcf,vcf_idx,chrom]



/*------------------ get passed variants ----------------------
*/
process ExtractPassVariants {
     tag "${sample}.${chrom}"

     publishDir pattern: "*.{gz,tbi}",
        path: {params.vcf_path + "/f01_pass_chr_vcf"},
        mode: 'copy', overwrite: true

     input:
     set val(sample), file(vcf), file(vcf_idx), val(chrom) from vcf_for_pass

     output:
     set val(sample), file("${sample}.${chrom}.pass.vcf.gz"), file("${sample}.${chrom}.pass.vcf.gz.tbi"), val(chrom) into vcf_for_normalize

     script:
     """
     bcftools view -i 'FILTER="PASS"' -r ${chrom} ${vcf} -O z -o ${sample}.${chrom}.pass.vcf.gz
     tabix ${sample}.${chrom}.pass.vcf.gz
     """
}

/*------------------ normalize vcf ------------------------------
*/
process NormalizeVCF {
     tag "${sample}.${chrom}"

     publishDir pattern: "*.{gz,tbi}",
        path: {params.vcf_path + "/f02_norm_chr_vcf"},
        mode: 'copy', overwrite: true

     input:
     file ref_fa
     file ref_fai
     file ref_dict
     set val(sample), file(vcf), file(vcf_idx), val(chrom) from vcf_for_normalize

     output:
     set val(sample), file("${sample}.${chrom}.norm.vcf.gz"), file("${sample}.${chrom}.norm.vcf.gz.tbi"), val(chrom) into vcf_for_vep

     script:
     """
     vt decompose -s ${vcf} | vt normalize -r ${ref_fa} - | bgzip > ${sample}.${chrom}.norm.vcf.gz
     tabix ${sample}.${chrom}.norm.vcf.gz
     echo ${sample}.${chrom}.norm.vcf.gz.tbi
     """
}


loftee = params.loftee_path
vep_db = params.vep_db
ref_path = ref_fa.parent
CADD_SNV = file(params.CADD_SNV)
CADD_SNV_idx = CADD_SNV + '.tbi'
CADD_INDEL = file(params.CADD_INDEL)
CADD_INDEL_idx = CADD_INDEL + '.tbi'
CADD_path = CADD_SNV.parent
/*------------------- annotate vcf --------------------
*/
process VEP_annotate {
     tag "${sample}.${chrom}"

     publishDir pattern: "*.{gz,tbi}",
        path: {params.vcf_path + "/f03_vep_chr_vcf"},
        mode: 'copy', overwrite: true

     input:
     set val(sample), file(vcf), file(vcf_idx), val(chrom) from vcf_for_vep
     file ref_fa
     file ref_fai
     file ref_dict
     val loftee
     val vep_db
     file CADD_SNV
     file CADD_SNV_idx
     file CADD_INDEL
     file CADD_INDEL_idx
     val CADD_path

     output:
     set val(sample), file("${sample}.${chrom}.vep.vcf.gz"), file("${sample}.${chrom}.vep.vcf.gz.tbi")

     script:
     """
     if singularity run -B /:/media ${params.singularity} vep -i ${vcf} --plugin LoF,loftee_path:/media/${loftee},human_ancestor_fa:/media/${loftee}/human_ancestor_fa.gz,gerp_bigwig:/media/${loftee}/gerp_conservation_scores.homo_sapiens.GRCh38.bw,conservation_file:/media/${loftee}/phylocsf_gerp.sql --dir_plugins /media/${loftee} --plugin Carol --plugin Condel,:/opt/.vep/Plugins/config/Condel/config,b --plugin ExACpLI,/opt/gnomad.v2.1.1.oe_lof.by_gene.txt --plugin LoFtool,/opt/.vep/Plugins/LoFtool_scores.txt --plugin CADD,${CADD_SNV},${CADD_INDEL} -o ${sample}.${chrom}.vep.vcf.gz --cache --force_overwrite --buffer_size 10000 --species homo_sapiens --assembly GRCh38 --dir /media/${vep_db} --offline --fork 1 --hgvs -e --fa ${ref_fa} --minimal --allele_number --check_existing --vcf --compress_output bgzip; then 
          tabix ${sample}.${chrom}.vep.vcf.gz
          echo ${sample}.${chrom}.vep.vcf.gz.tbi
     else
          echo "${sample}.${chrom} annotation failed"
          cp ${vcf} ${sample}.${chrom}.vep.vcf.gz
          cp ${vcf_idx} ${sample}.${chrom}.vep.vcf.gz.tbi
     fi
     """
}
