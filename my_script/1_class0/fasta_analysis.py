# encoding:utf-8
import os
import time
time1 = time.time()
os.chdir(r'E:\r\biotrainee_demo\class0')

file = 'test.fa'
def complementary_seq(file, buffer=1024*2048):
    base_list = ['A','T','C','G','U','N']
    base_comp_list = ['T','A','G','C','A','N']
    comp_dict = dict(zip(base_list, base_comp_list))
    head = ''
    with open(file,'r') as f:
        while True:
            raw_tmp = f.read(buffer)
            tmp = (head + raw_tmp).split('\n>')
            tmp_records = tmp[:-1]
            head = tmp[-1]
            for i in tmp_records:
                if i:
                    if not i.startswith('>'):
                        i = '>' + i
                    seq = ''.join(i.split('\n')[1:]).strip().upper()
                    new_seq = ''
                    for j in seq:
                        new_seq += comp_dict[j]                  
                    print(i.split('\n')[0] + '\n' + new_seq)
            if not raw_tmp:
                break
        if head:
            for i in head.split('\n>'):
                if i:
                    if not i.startswith('>'):
                        i = '>' + i
                    seq = i.split('\n')[1].strip().upper()
                    new_seq = ''
                    for j in seq:
                        new_seq += comp_dict[j]                    
                    print(i.split('\n')[0] + '\n' + new_seq)
    return(0)
complementary_seq(file, buffer = 2048*3069)
