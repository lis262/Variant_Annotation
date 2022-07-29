from intervaltree import Interval, IntervalTree
import pandas as pd
import sys

gene_pos = {}
for i in range(1,23):
    gene_pos['chr'+ str(i)] = IntervalTree()

pos_fn = '/hpc/grid/wip_drm_targetsciences/projects/Ensembl/gene_pos_GRCh38_release_97.txt'

pos_df = pd.read_csv(pos_fn, sep='\t', header=0)
pos_df['chrom'] = 'chr' + pos_df['chrom'].astype('str')
gene_df = pos_df.groupby('gene_name').agg({'chrom':'first','start':'min','end':'max'}).reset_index()


for idx, row in gene_df.iterrows():
    chrom = row['chrom']
    gene = row['gene_name']
    start = row['start']
    end = row['end']
    try:
        gene_pos[chrom][start:end] = gene
    except:
        pass


def get_50k_genes(row, gene_pos):
    chrom = str(row['chr'])
    if not chrom.startswith('chr'): chrom = 'chr'+chrom
    start = int(row['pos']) - 25000
    end = int(row['pos']) + 25000
    res = []
    if chrom in gene_pos:
        for inter in sorted(gene_pos[chrom][start:end]):
            res.append(inter.data)
        return ','.join(res)
    else:
        return '-'
    
#anno_fn = '/lustre/workspace/projects/BLCA/Results/WES/vcf/anno/anno.vep.tsv.gz'
#out_fn = '/lustre/workspace/projects/BLCA/Results/WES/vcf/anno/anno50k.vep.tsv.gz'
anno_fn = sys.argv[1]
out_fn = sys.argv[2]

head = True
for anno_df in pd.read_csv(anno_fn, sep='\t', header=0, chunksize=1e6):
    anno_df['near_50Kgene'] = anno_df.apply(lambda row: get_50k_genes(row,gene_pos),axis=1)
    columns = [c for c in anno_df.columns if not c.startswith('gt_')]
    anno_df = anno_df[columns]
    if head:
        anno_df.to_csv(out_fn, sep='\t', index=False, compression='gzip')
        head = False
    else:
        anno_df.to_csv(out_fn, sep='\t', index=False, header=None,compression='gzip',mode='a')



