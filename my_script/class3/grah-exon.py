import time
import re
from collections import OrderedDict
start = time.clock()

def count_gtf_gene(file_path, buffer_size=1024*1024):
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

def write_to_csv(gtf_gene_dict,file_save):   
    c = []
    for a,b in gtf_gene_dict.items():
        for i in b.keys():
            c.append(i)
    c = set(c)
    file_raw = 'Chromsome'
    file_raw += ',' + 'all_gene' + ',' + 'protein_coding'
    for i in c:
        if i not in ['all_gene', 'protein_coding']:
            file_raw += ',' + i
    for chr_id in list(range(1,23))+['X','Y','MT']:
        chr_id = str(chr_id)
        file_raw += '\nchr_'+ chr_id
        file_raw += ',' + str(gtf_gene_dict[chr_id]['all_gene']) +',' + str(gtf_gene_dict[chr_id]['protein_coding'])
        for i in c:
            if i not in ['all_gene', 'protein_coding']:
                i = str(i)
                try:
                    file_raw += ',' + str(gtf_gene_dict[chr_id][i])
                except:
                    file_raw += ',' + str(0)
    file_raw_list = file_raw.split('\n')[1:]
    i_list = file_raw_list[1].split(',')[1:]
    SUM = list(range(len(i_list)))
    for j in range(len(i_list)):
        SUM[j] = 0
    for i in file_raw_list:
        i_list = i.split(',')[1:]
        for j in range(len(i_list)):
            SUM[j] += int(i_list[j])
    file_raw += '\nSUM'
    for i in SUM:
        file_raw += ',' + str(i)
    with open(file_save,'w') as f:
        f.write(file_raw)
    return re.sub(',', '\t', file_raw)

def count_transcript_and_exon(file_path):
    transcript = []
    exon = []
    with open(file_path, 'r') as f:
        for i in f:
            if not i.startswith('#'):
                i_list = i.split('\t')
                feature = i_list[2]
                if feature == 'gene':
                    try:
                        transcript.append(transcript_num)
                    except:
                        transcript_num = 0
                    transcript_num = 0
                elif feature == 'transcript':
                    try:
                        exon.append(exon_num)
                    except:
                        exon_num = 0
                    transcript_num += 1
                    exon_num = 0
                elif feature == 'exon':
                    exon_num += 1 
        try:
            transcript.append(transcipt_num)
        except:
            pass
        try:
            exon.apend(exon_num)
        except:
            pass
                    
    return (transcript, exon)

    
file_path_human = r'E:\r\biotrainee_demo\class3\Homo_sapiens.GRCh38.87.chr.gtf'
#gtf_gene_dict1 = count_gtf_gene(file_path1)
#file_to_write1 = write_to_csv(gtf_gene_dict, file_save = 'gtf_analysis.csv')
file_path_cat = r'F:\tmp\Felis_catus.Felis_catus_6.2.87.chr.gtf\Felis_catus.Felis_catus_6.2.87.chr.gtf'
#print('Used %.4f s'%(time.clock()-start))   
file_path_zeb = r'F:\tmp\Danio_rerio.GRCz10.87.chr.gtf\Danio_rerio.GRCz10.87.chr.gtf'
file_path_mus = r'F:\tmp\Mus_musculus.GRCm38.87.chr.gtf\Mus_musculus.GRCm38.87.chr.gtf'

transcript_human, exon_human = count_transcript_and_exon(file_path_human)
transcript_cat, exon_cat = count_transcript_and_exon(file_path_cat)
transcript_zeb, exon_zeb = count_transcript_and_exon(file_path_zeb)
transcript_mus, exon_mus = count_transcript_and_exon(file_path_mus)

exon_hub = [exon_human, exon_cat, exon_zeb, exon_mus]


def list_to_freq(exon):
    exon_range = [0]
    exon_freq = [0]
    for i in set(exon):
        exon_range.append(i)
        exon_freq.append(exon.count(i)/len(exon)*100)
    return (exon_range, exon_freq)

import numpy as np
import matplotlib
from pylab import *
import matplotlib.pyplot as plt
myfont = matplotlib.font_manager.FontProperties(fname='C:/Windows/Fonts/msyh.ttf') 
mpl.rcParams['axes.unicode_minus'] = False 
plt.style.use('seaborn-white')
plt.xlim(0,15)
plt.ylim(0, 30)
plt.ylabel('百分比(%)',fontproperties=myfont)
plt.xlabel(u'外显子数目',fontproperties=myfont)
plt.title(u'不同物种基因外显子数目频率统计图', fontproperties=myfont)
i = -1

for exon_item in exon_hub:
    i += 1
    labels = ['Human','cat','zebrafish', 'mouse']
    colors = ['r', 'g', 'm', 'b']
    exon_range, exon_freq = list_to_freq(exon_item)
    plt.plot(exon_range, exon_freq, colors[i], alpha=1, label=labels[i])
    plt.xticks(exon_range[0:15])
    plt.plot((median(exon_item)+i/100,median(exon_item)+i/100), (0,30), colors[i]+'--', alpha=1)
    plt.text(median(exon_item)-0.5+i/10,2,u'中位数', ha='left', color= colors[i], fontproperties=myfont, alpha=0.8)

plt.legend(loc='upper right')
plt.savefig('F:\\1.png', dpi=600)
plt.show()
