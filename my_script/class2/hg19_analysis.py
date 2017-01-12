import os
import time
begin = time.time()
os.chdir(r'F:\tmp\chromFa')
def count_n_and_gc(file):
    content = []
    chromsome = []
    g = 0; c = 0; n = 0; a = 0; t = 0
    with open(file) as f:
        raw_list = f.readlines()
        for i in raw_list:
            if not i.startswith('>'):
                i = i.upper()
                n +=  i.count('N')
                g += i.count('G')
                c += i.count('C')
                a += i.count('A')
                t += i.count('T')
            else:
                if  chromsome:
                    content.append((n ,a, t, c, g))
                    g = 0; c = 0; n = 0; a = 0; t = 0
                chromsome.append(i.strip())
        content.append(( n ,a, t, c, g))
    return (content,chromsome)
content = []
chromsome = []
for i in (list(range(1,23)) + ['X','Y']):
    file = 'chr'+ str(i) + '.fa'
    print('Start dealing with ' + file)
    m, n = count_n_and_gc(file)
    content += m
    chromsome += n
all_info = 'chr,GC_ratio,N_ratio,Length,N,A,T,C,G'
for i in range(len(chromsome)):
    data = '\n'+str(chromsome[i]) +',' + "%.5f"%((content[i][-1]+content[i][-2])/sum(content[i][1:])) +','  + "%.5f" %(content[i][0]/(sum(content[i]))) +','  +str((sum(content[i]))) +','  +str((content[i][0])) + ','  +str(content[i][1])+',' +str(content[i][2])+','  +str(content[i][3])+','  +str(content[i][4]) 
    all_info += data
with open('hg19_analysis.csv','w') as f:
    f.write(all_info)
print('Time using:'+ str(time.time() - begin) + ' seconds\n')
