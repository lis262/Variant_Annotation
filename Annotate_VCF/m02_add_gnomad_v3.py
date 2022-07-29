import gzip, glob
import tabix,re
from natsort import natsorted

import argparse

parser = argparse.ArgumentParser(description='add gnoamd_v3 frequency')


parser.add_argument('-o','--out',action='store',dest='out',help='output file')
parser.add_argument('-i','--tab',action='store',dest='tab',help='input tab file')
parser.add_argument('-g','--gnomad',action='store',dest='gnomad',help='gnomad v3 path')

args = parser.parse_args()

tab_file = args.tab
out_file = args.out
gnomad_v3_path = args.gnomad

races = ['AF','AF_afr','AF_amr','AF_asj', 'AF_eas','AF_fin',
        'AF_nfe','AF_oth']

def get_gnomad_v3_freq(line,tb,races):
    chrom,pos,ref,alt = line[:4]
    records = tb.query('chr' + chrom, int(pos)-1, int(pos))
    for r in records:       
        if r[3] == ref and r[4] == alt:
            scores = []
            for race in races:
                try:
                    score = float(re.search('(?<={t}=).+?(?=;|$)'.format(t=race),r[-1]).group(0))
                except:
                    score = '-'
        
                scores.append(score)
            return scores
    return ['-'] * len(races)

# overlap_fn = '/hpc/grid/wip_drm_targetsciences/users/shangzhong/NIH_UDP/p01_FSGS_cohort/f06_vep_chr_varcards_tab/fsgs.chrY.vep.tsv.gz'
# out_add_gnomad_fn = '/hpc/grid/wip_drm_targetsciences/users/shangzhong/NIH_UDP/p01_FSGS_cohort/f07_add_gnomadV3_tab/fsgs.chrY.vep.tsv.gz'

gnomad_file = glob.glob(gnomad_v3_path + '/*.vcf.gz')[0]

tb = tabix.open(gnomad_file)
with gzip.open(tab_file,'rt') as in_f, gzip.open(out_file,'wb') as out:
    header = in_f.readline().strip().split('\t') + ['gnomADg_' + r for r in races]
    header_line = '\t'.join(header) + '\n'
    out.write(header_line.encode('utf-8'))
    for line in in_f:
        items = line.strip().split('\t')
        items += [str(s) for s in get_gnomad_v3_freq(items,tb,races)]
        out_line = '\t'.join(items) + '\n'
        out.write(out_line.encode('utf-8'))
