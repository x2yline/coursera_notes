# /usr/bin/python
# encoding=utf-8
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
import os
 
def density_plot(data_list,xlabel,title):
    fig = plt.figure(1)
    fig.patch.set_facecolor('w')
    ax = fig.add_axes([0.2,0.2,0.5,0.6])
    density = stats.kde.gaussian_kde(data_list)
    data_range = max(data_list) - min(data_list)
    x = np.arange(min(data_list),max(data_list),data_range/40)
    ax.plot(x, density(x),'b-')
    # axis seting
    ax.set_xlim([int(min(data_list)-data_range/10),int(max(data_list)+data_range/10)])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()
    ax.get_xaxis().set_tick_params(direction='out')
    ax.get_yaxis().set_tick_params(direction='out')
    ax.spines['left'].set_position(('outward', 10))
    ax.spines['bottom'].set_position(('outward', 10))
    ax.set_xlabel(xlabel)
    ax.set_xticks(np.linspace(int(min(data_list)-data_range/10),int(max(data_list)+data_range/10),6))
    # text seting
    ax_stats = fig.add_axes([0.76,0.2,0.2,0.6])
    ax_stats.set_axis_off()
    ax_stats.text(0, 0.8,'Mean: {:.3f}'.format(float(np.mean(data_list))), fontsize=12, color='blue')
    ax_stats.text(0, 0.6,'Max: {:.3f}'.format(max(data_list)), fontsize=12, color='red')
    ax_stats.text(0, 0.4,'Min: {:.3f}'.format(min(data_list)), fontsize=12, color='green')
    ax_stats.text(0, 0.2,'Median: {:.3f}'.format(float(np.median(data_list))), fontsize=12,color='blue')
    fig.suptitle('\n\n\n'+title)
    fig.savefig('density_'+xlabel, dpi=150)
    plt.show()
    print('\nFigure saved in {0}\n'.format(str(os.path.join(os.getcwd(),'density_'+xlabel))))
     
def cut_53(file, cut_5, cut_3):
    with open(file, 'r') as f:
        new_file = ''
        while True:
            line1 = f.readline().strip()
            if line1:
                type_id = line1[0]
                if line1.startswith('@') or line1.startswith('+'):
                    line2 = f.readline().strip()
                    line1 = line1[:line1.find('length=')+7] + str(len(line2)-cut_3-cut_5)
                    new_file = new_file + line1 + '\n'
                    if len(line2)-cut_5 <= cut_3:
                        raise ValueError('cut too much')
                    else:
                        line2 = line2[cut_5:-(cut_3)]
                        if type_id:#== '@':
                            print(line1)
                            print(line2)
                        new_file = new_file + line2 + '\n'
            else:
                break
    return(new_file) 
                 
 
def fastq2fasta(file):
    new_file = ''
    with open(file,'r') as f:
        while True:
            line1 = f.readline()
            if line1:
                line2 = f.readline()
                skip = f.readline()
                skip = f.readline()
                print('>'+line1[1:]+line2, end='')
                new_file += '>'+line1[1:]+line2
            else:
                break
    return(new_file)
 
def length_count(file):
    length_list = []
    with open(file,'r') as f:
        print("Waiting for a moment:")
        while True:
            line1 = f.readline()
            if line1.startswith('@'):
                print(line1[1:-1],end='\r')
                line2 = f.readline().strip()
                skip = f.readline()
                skip = f.readline()
                length_list.append(len(line2))
            else:
                break
    print('\n\nPloting...\n')
    density_plot(length_list, xlabel='length',title='Distribution of length')
    result = ('\nmean length is {0}\nmaxium length is {1}\nminium length is {2}\n'.format(sum(length_list)/len(length_list),max(length_list),min(length_list)))
    print(result)
    plt.show()
    return(result)
 
 
def count_GCN(file):
    print("Waiting for a moment:")
    count_dict = {}
    count_dict['GC'] = 0
    count_dict['N'] = 0
    with open(file,'r') as f:
        gc_list = []
        while True:
            line1 = f.readline()
            if line1:
                print(line1[1:-1],end='\r')
                line2 = f.readline().strip().upper()
                skip = f.readline()
                skip = f.readline()
                gc_list.append((line2.count("G")+line2.count("C"))/len(line2))
                count_dict['GC'] += line2.count('G') + line2.count('C')
                count_dict['N'] += len(line2)
            else:
                break
        count_dict['GC'] = count_dict['GC']/count_dict['N']
    print("\n\nThe GC count is {0}\nThe number of bases is {1}".format(count_dict["GC"],count_dict["N"]))
    print("Ploting...\n")
    density_plot(gc_list, xlabel="GC content",title="Distribution of GC content")
    return(count_dict)
 
 
def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('file', help = 'The fastq file_path')
    parser.add_argument('-c3','--cut3',type=int, help="the cut bases in the 3' of the sequences")
    parser.add_argument('-c5','--cut5',type=int,help = "the cut bases in the 5' of the sequences")
    parser.add_argument('-f', '--fasta',action="store_true",help="fastq to fasta")
    parser.add_argument('-gc', '--count',action="store_true",help = "count GC and the number of bases of fastq file")
    parser.add_argument('-l','--length',action="store_true", help="count the length of fastq file")
    args = parser.parse_args()
    if args.fasta:
        fastq2fasta(args.file)
    if args.count:
        count_GCN(args.file)
    if args.length:
        length_count(args.file)
    cut3 = 0
    cut5 = 0
    if args.cut3:
        if args.cut3 >= 0:
            cut3 =args.cut3
        else:
            raise ValueError('cut value can not be negative!!!')
    if args.cut5:
        if args.cut5 >= 0:
            cut5 = args.cut5
        else:
            raise ValueError('cut value can not be negative!!!')
    if cut3 + cut5 != 0:
        cut_53(args.file, cut5,cut3)
 
 
 
 
if __name__ == '__main__':
    main()
