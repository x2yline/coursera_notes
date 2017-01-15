import os
import time
import sys
from collections import OrderedDict
start = time.clock()
file_path = r'E:\r\biotrainee_demo\class3\Homo_sapiens.GRCh38.87.chr.gtf'
#file_path =  r'E:\r\biotrainee_demo\class3\head.txt'
def count_gtf(file_path, buffer_size=1024*1024):
    #features = ['gene', 'transcript', 'exon', 'CDS', 'start_codon',\
 #'stop_codon', 'five_prime_utr','three_prime_utr','Selenocysteine']
    gtf_count = OrderedDict()
    with open(file_path, 'r') as f:
        #print(type(f))
        for i in f:
            if not i.startswith('#'):
                i_list = i.split('\t')
                CHR = i_list[0]
                feature = i_list[2]
                if CHR not in gtf_count.keys():
                    gtf_count[CHR] = OrderedDict()
                    gtf_count[CHR]['all_gene'] = 0
                    gtf_count[CHR]['CDS_gene'] = 0
                if feature == 'gene':
                    gtf_count[CHR]['all_gene'] += 1
                    gene_count_CDS = 0
                elif feature == 'CDS':
                    if gene_count_CDS == 0:
                        gtf_count[CHR]['CDS_gene'] += 1
                    gene_count_CDS =1
    return gtf_count
gtf_dict = count_gtf(file_path)
print('used %.4f s'%(time.clock()-start))          
