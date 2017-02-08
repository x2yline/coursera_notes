

import os
from collections import OrderedDict

def untar(fname, untar_path):
    import tarfile
    if not untar_path:
        untar_path = ''.join(fname.split('.')[:-1])
    t = tarfile.open(fname, 'r')
    t.extractall(path = untar_path)
    t.close()
     
    
    
    
fname = r'G:\GSE48213_RAW.tar'
untar_path = r'G:\GSE48213_RAW'



untar(fname, untar_path)
file_list = []
for j in os.listdir(r'G:\GSE48213_RAW'):
    if j[-3:] == '.gz':
        file_list.append(j)

def merge_array(file_list, dirs = '.' ):
    my_dict = OrderedDict()
    counts = -1
    for i in file_list:
        counts += 1
        if i[-3:] == '.gz':
            import gzip
            with gzip.open(os.path.join(dirs, i),'r') as f:
                for line in f:
                    item = line.split('\t')
                    if item[0] in my_dict:
                        my_dict[item[0]] += (counts - len(my_dict[item[0]]))*[''] + [item[1][:-1]]
                    else:
                        my_dict[item[0]] = counts*[''] + [item[1][:-1]]
        else:
            with open(os.path.join(dirs, i),'r') as f:
                for line in f:
                    item = line.split('\t')
                    if item[0] in my_dict:
                        my_dict[item[0]] += (counts - len(my_dict[item[0]]))*[''] + [item[1][:-1]]
                    else:
                        my_dict[item[0]] = counts*[''] + [item[1][:-1]]
    return my_dict

def write_dict_to_csv(my_dict, path = '.\\merged.csv'):
    content = ''
    for i in my_dict.keys():
        content += i + ','
        content += ','.join(my_dict[i]) + '\n'
    with open(path,'a') as f:
        f.write(content)
        
my_dict = merge_array(file_list, dirs = untar_path)
write_dict_to_csv(my_dict, path = 'G:\\1.csv')
