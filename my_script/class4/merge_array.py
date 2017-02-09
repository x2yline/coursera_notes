import os
from collections import OrderedDict

def untar(fname, untar_path):
    ''' 函数输入为fname为tar或gz文件的绝对路，
    untar_path为解文件放置路径，不存在时可以自动新建文件夹，
    utar_path若为空，则默认为fname的同级新建目录'''
    import tarfile
    if not untar_path:
        untar_path = ''.join(fname.split('.')[:-1])
    t = tarfile.open(fname, 'r')
    t.extractall(path = untar_path)
    t.close()

def merge_array(file_list, dirs = '.' ):
    '''函数输入file_list为要和并的距阵文件名列表，可以是txt或gz文件
    dirs为文所在的路径，默认为当前路径
    输出为有序字典，keys为行名，values为对应行的数值列表'''
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
    with open(path, 'w') as f:
        pass
    with open(path,'a') as f:
        for i in my_dict.keys():
            content = i + ','
            content += ','.join(my_dict[i]) + '\n'
            f.write(content)
    with open(path, 'r') as f:
        content = f.read().replace(",", "\t")
    return content
# fname为GSE48213_RAW.tar所在绝对路径
# untar_path为解压后文件所在路径，可任意设定
fname = r'G:\GSE48213_RAW.tar'
untar_path = r'G:\GSE48213_RAW'

untar(fname, untar_path)
file_list = []
for j in os.listdir(r'G:\GSE48213_RAW'):
    if j[-3:] == '.gz':
        file_list.append(j)
        
my_dict = merge_array(file_list, dirs = untar_path)
content = write_dict_to_csv(my_dict, path = 'E:\\merged_array.csv')
