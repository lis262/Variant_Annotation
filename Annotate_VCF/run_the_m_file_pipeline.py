# # 1. transfer vep to table
# import glob, os
# from natsort import natsorted
# py_file = '/home/lis262/Code/Variant_Analysis/Annotate_VCF/m01_vcf2tab.py'

# path = '/hpc/grid/wip_drm_targetsciences/users/shangzhong/NIH_UDP/p01_FSGS_cohort'
# vep_path = path + '/f03_vep_chr_vcf'

# vep_files = natsorted(glob.glob(vep_path + '/*.vcf.gz'))
# tab_path = path + '/f04_vep_chr_tab'

# if not os.path.exists(tab_path):
#     os.mkdir(tab_path)

# for vep_file in vep_files:
#     chrom = vep_file.split('.')[-4]
#     tab_file = tab_path + '/' + vep_file.split('/')[-1][:-6] + 'tsv.gz'
#     cmd = ('bsub -q short -J {job} -o {log} \"python {py} -i {vep} -o {tab} \"').format(log=tab_path+'/log.'+chrom, py=py_file,vep=vep_file,tab=tab_file,job=chrom)
#     os.system(cmd)

# #--------------------------------------------------------
# # 2. transfer tab to spl
# import glob,os
# from natsort import natsorted
# py_file = '/home/lis262/Code/Variant_Analysis/Annotate_VCF/m02_tab2sql.py'


# path = '/hpc/grid/wip_drm_targetsciences/users/shangzhong/NIH_UDP/p01_FSGS_cohort'

# tab_path = path + '/f04_vep_chr_tab'
# tab_files = natsorted(glob.glob(tab_path + '/*.tsv.gz'))

# sql_path = path + '/f05_vep_chr_sql'
# varcards_path = '/hpc/grid/wip_drm_targetsciences/projects/VEP_plugin/Varcards_GRCh38'
# varcards_files = natsorted(glob.glob(varcards_path + '/*.gz'))

# if not os.path.exists(sql_path):
#     os.mkdir(sql_path)

# for tab_file in tab_files:
#     chrom = tab_file.split('.')[-4]
#     try:
#         varcards_file = [i for i in varcards_files if '.'+chrom+'.' in i][0]
#         print()
#     except:
#         print('doesnot find varcard files')
#         continue
#     sql_file = sql_path + '/' + tab_file.split('/')[-1][:-6] + 'sql'
#     cmd = ('bsub -q short -J {job} -o {log} \"python {py} -t {tab} -s {sql} -d {db}\"').format(py=py_file,
#                     tab = tab_file,sql=sql_file,db=varcards_file,
#                     log=sql_path+'/log.'+chrom,job=chrom)
#     os.system(cmd)

#--------------------------------------------------------------------
# # 3. OVERLAP FSGS TABLE WITH VARCARDS TABLE
# import glob,os
# from natsort import natsorted

# path = '/hpc/grid/wip_drm_targetsciences/users/shangzhong/NIH_UDP/p01_FSGS_cohort'
# sql_path = path + '/f05_vep_chr_sql'
# out_path = path + '/f06_vep_chr_varcards_tab'

# if not os.path.exists(out_path):
#     os.mkdir(out_path)

# sql_files = natsorted(glob.glob(sql_path + '/*.sql'))[12:16]

# py_file = '/home/lis262/Code/Variant_Analysis/Annotate_VCF/m03_vcf_sql_overlap.py'

# for sql in sql_files:
#     chrom = sql.split('.')[-3]
#     log = out_path + '/log.' + sql.split('.')[1]
#     cmd = 'bsub -o {log} -J {job} \"python {py} -i {sql} -o {out_dir}\"'.format(
#         py=py_file,log=log,job=chrom,sql=sql,out_dir=out_path)
#     os.system(cmd)
    
#--------------------------------------------------------------
# # 4. add gnomad v3 NFE frequency
# import glob, os
# from natsort import natsorted


# path = '/hpc/grid/wip_drm_targetsciences/users/shangzhong/NIH_UDP/p01_FSGS_cohort'
# ovrelap_path = path + '/f06_vep_chr_varcards_tab'
# out_path = path + '/f07_add_gnomadV3_tab'
# if not os.path.exists(out_path):
#     os.mkdir(out_path)

# py_file = '/home/lis262/Code/Variant_Analysis/Annotate_VCF/m04_add_gnomad_v3.py'
# gnomad_v3_path = '/hpc/grid/wip_drm_targetsciences/projects/gnomAD/gnomad_v3'

# overlap_files = natsorted(glob.glob(ovrelap_path + '/*.tsv.gz'))
# for overlap_fn in overlap_files[13:17]:
#     chrom = overlap_fn.split('.')[-4]
#     out_file = out_path + '/' + overlap_fn.split('/')[-1]
#     log = out_path + '/log.' + chrom
#     cmd = 'bsub -o {log} -J {chrom} -q short \"python {py} -i {tab} -o {out} -g {gnomad}\"'.format(log=log,chrom=chrom,py=py_file,tab=overlap_fn,out=out_file,gnomad=gnomad_v3_path)
#     os.system(cmd)
