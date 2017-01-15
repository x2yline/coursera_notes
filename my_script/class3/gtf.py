import os
import time
import re
import sys
from collections import OrderedDict
start = time.clock()
file_path = r'E:\r\biotrainee_demo\class3\Homo_sapiens.GRCh38.87.chr.gtf'
#file_path =  r'E:\r\biotrainee_demo\class3\head.txt'
def count_gtf(file_path, buffer_size=1024*1024):
    features = ['gene', 'transcript', 'exon', 'CDS', 'start_codon',\
 'stop_codon', 'five_prime_utr','three_prime_utr','Selenocysteine']
    gtf_count = OrderedDict()
    with open(file_path, 'r') as f:
        chunk = '1'
        while chunk:
            chunk = f.read(buffer_size)
            if '#' in chunk:
                chunk = chunk.split('#!')[-1]
                chunk_list = chunk.split('\n')[1:]
                last = chunk_list[-1]
                chunk_list = chunk_list[:-1]
                for i in chunk_list:
                    i_list = i.split('\t')
                    chromsome = i_list[0]
                    try:   
                        b = gtf_count[chromsome]
                    except:
                        gtf_count[chromsome] = OrderedDict()
                    for j in features:
                        try:
                            gtf_count[chromsome][j] += 0
                        except:
                            gtf_count[chromsome][j] = 0
                    feature = i_list[2]
                    gtf_count[chromsome][feature] += 1
            else:
                chunk = last + chunk
                chunk_list = chunk.split('\n')
                last = chunk_list[-1]
                chunk_list = chunk_list[:-1]
                for i in chunk_list:
                    i_list = i.split('\t')
                    chromsome = i_list[0]
                    try:   
                        b = gtf_count[chromsome]
                    except:
                        gtf_count[chromsome] = OrderedDict()
                    for j in features:
                        try:
                            gtf_count[chromsome][j] += 0
                        except:
                            gtf_count[chromsome][j] = 0
                    feature = i_list[2]
                    gtf_count[chromsome][feature] += 1
           
    return gtf_count
                    
gtf_dict = count_gtf(file_path)
                    
