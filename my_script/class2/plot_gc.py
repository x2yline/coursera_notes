import os
import time
import re
import sys
from collections import OrderedDict
start = time.clock()
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
 
def write_atcg_to_csv(ATCG_analysis, file_path = '.'):
    file = os.path.join(file_path,'atcg_analysis.csv')
    csv_content = 'chromsome\tGC_content\tN_content\tLength\tN\tA\tT\tC\tG\n'
    for chr_id, atcg_count in ATCG_analysis.items():
        GC = atcg_count['G'] + atcg_count['C']
        N = atcg_count['N']
        Length = sum(atcg_count.values())
        GC_content = GC*1.0/(Length-N)
        N_content = N*1.0/Length
        csv_content += chr_id + '\t' + '%.4f'%GC_content + '\t' + '%.4f'%N_content + '\t' + str(Length) + '\t' + str(atcg_count['N']) +'\t' + str(atcg_count['A']) + '\t' + str(atcg_count['T']) + '\t' + str(atcg_count['C'])+'\t'+ str(atcg_count['G'])+ '\n'
    with open(file, 'w') as f:
        csv_file_content = re.sub('\t', ',', csv_content)
        f.write(csv_file_content)
    print(u'File have been saved in '+ file)
    return csv_content
    
file_path = 'F:\genome\chromFa\hg19.fa'


ATCG_analysis = count_fasta_atcgn(file_path, buffer_size=1024*1024)
cg_list = []
chr_id_list = list(range(1,23)) + ['X','Y','M']
for i in chr_id_list:
    cg_list.append((ATCG_analysis['CHR'+str(i)]['G']+ATCG_analysis['CHR'+str(i)]['C'])/(ATCG_analysis['CHR'+str(i)]['N']+ATCG_analysis['CHR'+str(i)]['A']+ATCG_analysis['CHR'+str(i)]['T']+ATCG_analysis['CHR'+str(i)]['C']+ATCG_analysis['CHR'+str(i)]['G'])*100)
import matplotlib.pyplot as plt
plt.bar(left = range(25), height = cg_list, color='k')
for i in range(len(cg_list)):
    plt.text( x=i, y=cg_list[i]+.35,s=str(round(cg_list[i])))
plt.title('GC content for hg19 genome')
plt.ylabel('GC content (%)')
pos = []
for i in range(len(chr_id_list)):
    pos.append(i + 0.35)
plt.xticks(pos, list(range(1,23)) + ['X','Y','MT'], fontsize=8)
plt.xlim(-0.35, )
plt.ylim(0, 100)
plt.savefig('F:\gc.png',dpi=600)
plt.show()
