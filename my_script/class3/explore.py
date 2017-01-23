import time
import re
from collections import OrderedDict
start = time.clock()
  
def count_gtf_gene(file_path, buffer_size=1024*1024):
    print(file_path.split('.')[-1])
    gtf_count = OrderedDict()
    with open(file_path, 'r') as f:
        for i in f:
            if not i.startswith('#'):
                i_list = i.split('\t')
                CHR = i_list[0]
                feature = i_list[2]
                if CHR not in gtf_count.keys():
                    gtf_count[CHR] = OrderedDict()
                    gtf_count[CHR]['all_gene'] = 0
                if feature == 'gene':
                    gtf_count[CHR]['all_gene'] += 1
                    TYPE = re.search('gene_biotype "(.*?)";',i_list[-1]).group(1)
                    try:
                        gtf_count[CHR][TYPE] += 1
                    except:
                        gtf_count[CHR][TYPE] = 1
    return gtf_count
      
file_path_human = r'F:\genome\Homo_sapiens.GRCh38.87.chr.gtf\Homo_sapiens.GRCh38.87.chr.gtf'

hg38_gene = count_gtf_gene(file_path_human)
chr_id_list = list(range(1,23)) + ['X','Y','MT']
gene_num_list = []
for i in chr_id_list:
    gene_num_list.append(hg38_gene[str(i)]['all_gene'])

import matplotlib.pyplot as plt
plt.figure(1)
plt.style.use('seaborn-white')
plt.bar(left = range(25), height = gene_num_list, color='k')
for i in range(len(gene_num_list)):
    plt.text( x= i , y=gene_num_list[i]+35,s=str(round(gene_num_list[i])), fontsize = 5)
plt.title('Gene distribution of hg38 genome')
plt.ylabel('Gene number of chromosome')
pos = []
for i in range(len(chr_id_list)):
    pos.append(i + 0.35)
plt.xticks(pos, list(range(1,23)) + ['X','Y','MT'], fontsize=8)
plt.xlim(-0.2, )
plt.savefig('F:\gene_distribution.png',dpi=600)
plt.show()




plt.figure(2)
plt.style.use('seaborn-white')
import os
from collections import OrderedDict

def count_fasta_atcgn(file_path, buffer_size=1024*1024):
    bases = ['N', 'A', 'T', 'C', 'G']
    ATCG_analysis = OrderedDict()
    with open(file_path, 'r') as f:
        line1 = f.readline().upper()
        chr_i = re.split('\s', line1)[0][1:]
        print(chr_i)
        ATCG_analysis[chr_i] = OrderedDict()
        for base in bases:
            ATCG_analysis[chr_i][base] = 0
        while True:
            chunk = f.read(buffer_size).upper()
            if '>' in chunk:
                chromsome = re.split('>',chunk)
                if chromsome[0]:
                    for base in bases:
                        ATCG_analysis[chr_i][base] += chromsome[0].count(base)
                for i in chromsome[1:]:
                    if i:
                        chr_i = re.split('\s', i[0:i.index('\n')])[0]
                        print(chr_i)
                        strings_i = i[i.index('\n'):]
                        ATCG_analysis[chr_i] = OrderedDict()
                        for base in bases:
                            ATCG_analysis[chr_i][base] = strings_i.count(base)
            else:
                for base in bases:
                    ATCG_analysis[chr_i][base] += chunk.count(base)
            if not chunk:
                break
    return ATCG_analysis
 
file_path = r'F:\genome\hg38.chromFa\chroms\hg38.fa'

ATCG_analysis = count_fasta_atcgn(file_path, buffer_size=1024*1024)
cg_list = []
chr_id_list = list(range(1,23)) + ['X','Y','M']
for i in chr_id_list:
    cg_list.append((ATCG_analysis['CHR'+str(i)]['G']+ATCG_analysis['CHR'+str(i)]['C'])/(ATCG_analysis['CHR'+str(i)]['A']+ATCG_analysis['CHR'+str(i)]['T']+ATCG_analysis['CHR'+str(i)]['C']+ATCG_analysis['CHR'+str(i)]['G'])*100)

plt.bar(left = range(25), height = cg_list, color='k')
for i in range(len(cg_list)):
    plt.text( x=i -.1, y=cg_list[i]+.35,s=str(round(cg_list[i])))
plt.title('GC content for hg38 genome')
plt.ylabel('GC content (%)')
pos = []
for i in range(len(chr_id_list)):
    pos.append(i + 0.35)
plt.xticks(pos, list(range(1,23)) + ['X','Y','MT'], fontsize=8)
plt.xlim(-0.2, )
plt.ylim(0, 100)
plt.savefig('F:\hg38_gc.png',dpi=600)
plt.show()
