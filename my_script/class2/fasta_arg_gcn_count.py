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
        line1 = f.readline()
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
                        strings_i = i[i.index('\n'):].upper()
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

    
if sys.argv:
    result = OrderedDict()
    for f in sys.argv:
        done = 0
        f= f.strip(''''"''')
        if f.count('.') != 1 or f[-2:] == 'py' or not os.path.exists(f):
            continue
        print(f)
        
        try:
            done = 1
            result = OrderedDict(count_fasta_atcgn(file_path = f, buffer_size = 1024*2048), **result)
        except Exception as e:
            if f.startswith('-'):
                pass
            else:
                print(type(e))
    
    if done == 1:
        file = write_atcg_to_csv(result)
        print(file)
        print('used %.2f s'%(time.clock()-start))
    else:
        print ('\n\nSorry! The command is invalid!\n')
else:
    directory = input('Enter your file: ')
    start = time.clock()
    if directory.count('.') != 1 or directory[-2:] == 'py' or not os.path.exists(directory):
        print('Your file is invalid!')
    else:
        result = count_fasta_atcgn(file_path = directory, buffer_size = 1024*2048)
        file = write_atcg_to_csv(result)
        print('used %.2f s'%(time.clock()-start))
