import os
os.chdir(r'E:\r\biotrainee_demo\class7')
import pandas as pd

#模拟差异基因
diff_gene_list = []
with open(r'E:\r\biotrainee_demo\class7\GDS4511.soft\GDS4511.soft','r') as f:
    for line in f:
        if not line[0] in ['#','!','^']:
            gene = line.split()[1]
            diff_gene_list.append(gene)
diff_gene_list = diff_gene_list[0:800]


def analysis_kegg(file_path):
    kegg_dict={}
    with open(file_path,'r') as f:
        for line in f:
            if line.startswith('C'):
                try:
                    path_num = line.split()[1]
#                    if len(path_num) > 10:
#                        print(line)
                    kegg_dict[path_num]= []
                except:
                    print('Warning: '+line)
            elif line.startswith('D'):
                try:
                    gene_name = line[:line.find(';')].split()[-1]
                    kegg_dict[path_num].append(gene_name)
                except:
                    print('Warning: '+line)
                    
    non_empty_path = []
    all_gene = []
    for keys in kegg_dict.keys():
        if kegg_dict[keys]:
           non_empty_path.append(keys)
           all_gene += kegg_dict[keys]
    return(kegg_dict, all_gene)
#kegg文件解析
kegg_dict, all_kegg_gene = analysis_kegg(r'E:\r\biotrainee_demo\class7\hsa00001.keg')

# 计算p值
DEGs = []
for i in diff_gene_list:
    if i in all_kegg_gene:
        DEGs.append(i)

DEGs=list(set(DEGs))
popTotal = len(set(all_kegg_gene))
listTotal = len(DEGs)


from scipy.stats import hypergeom

keggEnrich = {}
for ke, val in kegg_dict.items():
    hits = [gene for gene in val if gene in DEGs]
    hitCount =len(hits)
    popHits = len(val)
    
    if hitCount == 0:
        print(ke,end=' is not in hits\n')
    else:
        pVal = hypergeom.sf(hitCount-1, popTotal, popHits, listTotal)
        keggEnrich[ke] = [hitCount, listTotal, popHits, popTotal, pVal, ':'.join(hits)]
        
keggOutput = pd.DataFrame.from_dict(keggEnrich, orient='columns',dtype=None)
keggOutput = pd.DataFrame.transpose(keggOutput)
keggOutput.columns=['Count','List Total', 'pop Hits', 'pop Total', 'p-Val','genes']

# 计算FDR值
p = keggOutput['p-Val']
plist = [i for i in p]
length = len(plist)
psort = [i for i in plist]
psort.sort()
psort.reverse()
FDR = []
for i in plist:
    q = i*length/(psort.index(i)+1)
    FDR.append(q)
    
keggOutput['FDR']=FDR     
