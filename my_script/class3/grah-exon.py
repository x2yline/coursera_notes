# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

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
    print(file_path)
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
 
     
file_path_human = r'F:\genome\Homo_sapiens.GRCh38.87.chr.gtf\Homo_sapiens.GRCh38.87.chr.gtf'
#gtf_gene_dict1 = count_gtf_gene(file_path1)
#file_to_write1 = write_to_csv(gtf_gene_dict, file_save = 'gtf_analysis.csv')
file_path_cat = r'F:\genome\Felis_catus.Felis_catus_6.2.87.chr.gtf\Felis_catus.Felis_catus_6.2.87.chr.gtf'
#print('Used %.4f s'%(time.clock()-start))   
file_path_gorilla = r'F:\genome\Gorilla_gorilla.gorGor3.1.87.chr.gtf\Gorilla_gorilla.gorGor3.1.87.chr.gtf'
file_path_mus = r'F:\genome\Mus_musculus.GRCm38.87.chr.gtf\Mus_musculus.GRCm38.87.chr.gtf'
file_path_zeb = r'F:\genome\Danio_rerio.GRCz10.87.chr.gtf\Danio_rerio.GRCz10.87.chr.gtf'
file_path_chicken = r'F:\genome\Gallus_gallus.Gallus_gallus-5.0.87.chr.gtf\Gallus_gallus.Gallus_gallus-5.0.87.chr.gtf'
file_path_elephant = r'F:\genome\Caenorhabditis_elegans.WBcel235.87.gtf\Caenorhabditis_elegans.WBcel235.87.gtf'
file_path_fluitfly = r'F:\genome\Drosophila_melanogaster.BDGP6.87.chr.gtf\Drosophila_melanogaster.BDGP6.87.chr.gtf'
file_path_pig = r'F:\genome\Sus_scrofa.Sscrofa10.2.87.chr.gtf\Sus_scrofa.Sscrofa10.2.87.chr.gtf'
file_path_dog = r'F:\genome\Canis_familiaris.CanFam3.1.87.chr.gtf\Canis_familiaris.CanFam3.1.87.chr.gtf'
file_path_horse = r'F:\genome\Equus_caballus.EquCab2.87.chr.gtf\Equus_caballus.EquCab2.87.chr.gtf'

transcript_human, exon_human = count_transcript_and_exon(file_path_human)
transcript_cat, exon_cat = count_transcript_and_exon(file_path_cat)
transcript_zeb, exon_zeb = count_transcript_and_exon(file_path_zeb)
transcript_gorilla, exon_gorilla = count_transcript_and_exon(file_path_gorilla)
transcript_mus, exon_mus = count_transcript_and_exon(file_path_mus)
transcript_pig, exon_pig = count_transcript_and_exon(file_path_pig)
transcript_fluitfly, exon_fluitfly = count_transcript_and_exon(file_path_fluitfly)
transcript_dog, exon_dog = count_transcript_and_exon(file_path_dog)
transcript_chicken, exon_chicken = count_transcript_and_exon(file_path_chicken)
transcript_horse, exon_horse = count_transcript_and_exon(file_path_horse)
transcript_elephant, exon_elephant = count_transcript_and_exon(file_path_elephant)
exon_hub = [exon_human, exon_gorilla, exon_elephant, exon_horse, exon_pig, exon_dog, exon_cat,  exon_mus, exon_zeb, exon_fluitfly]

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

plt.figure(1)
plt.style.use('seaborn-white')
plt.xlim(0,15)
plt.ylim(0, 50)
plt.ylabel('百分比(%)',fontproperties=myfont)
plt.xlabel(u'外显子数目',fontproperties=myfont)
plt.title(u'不同物种基因外显子数目频率统计图', fontproperties=myfont)
i = -1
colors = ['#00FF00','#006400','blue','#9400D3','#800000','#191970','#CD853F','#FF0000','#FFFF00','#FFA500']
for exon_item in exon_hub:
    i += 1
    labels = ['Human','gorilla','elephant', 'horse', 'pig', 'dog', 'cat',  'mus', 'zebrafish', 'fluitfly' ]
    #colors = ['r', 'g', 'k', 'b','r', 'g', 'k', 'b', 'r', 'b']
    exon_range, exon_freq = list_to_freq(exon_item)
    plt.plot(exon_range, exon_freq, color=colors[i], alpha=.61, label=labels[i])
    #plt.xticks(exon_range[0:15])
    plt.plot((median(exon_item)+i/100,median(exon_item)+i/100), (0,50), colors[i],ls = '--', alpha=1)
    #plt.text(median(exon_item)-0.5+i/10,2,u'中位数', ha='left', color= colors[i], fontproperties=myfont, alpha=0.8)
 
plt.legend(loc='upper right')
plt.savefig('F:\\1.png', dpi=600)
plt.show()


plt.figure(2)
plt.style.use('ggplot')
plt.boxplot(exon_hub)
plt.ylim(0, 35)
plt.yticks(range(1,36,2))
plt.xticks(range(1,11),labels, fontsize=9)
plt.savefig('F:\\2.png', dpi=600)
plt.title('exons of different specieces')

plt.show()
