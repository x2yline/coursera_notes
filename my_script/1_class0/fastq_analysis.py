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
                 
 
def fastq2fasta(file, buffer=2048*3069):
    head = ''
    with open(file,'r') as f:
        while True:
            raw_tmp = f.read(buffer)
            tmp = (head + raw_tmp).split('\n@')
            tmp_records = tmp[:-1]
            head = tmp[-1]
            for i in tmp_records:
                if i:
                    if i.strip().startswith('@'):
                        i = i.strip()[1:]
                    fasta = '>'+'\n'.join(i.strip().split('\n')[0:2])
                    print(fasta)
            if not raw_tmp:
                break
        if head:
            for i in head.split('\n@'):
                if i:
                    if i.strip().startswith('@'):
                        i = i.strip()[1:]
                    fasta = '>'+'\n'.join(i.split('\n')[0:2])
                    print(fasta)
 
def length_count(file, buffer=2400*2400):
    length_list = []
    with open(file) as f:
        head = ''
        base_num = 0
        while True:
            a = f.read(buffer)
            raw_list = (head + a).split('\n@')
            deal_list = raw_list[:-1]
            head = raw_list[-1]
            for record in deal_list:
                if record:
                    sequence = record.split('\n')[1].upper().strip()
                    length_list.append(len(sequence))
                    base_num += len(sequence)
            if not len(a):
                break
        if head:
            record = head
            sequence = record.split('\n')[1].upper().strip()
            length_list.append(len(sequence))
            base_num += len(sequence)

    density_plot(length_list, xlabel='length',title='Distribution of length')
    result = ('\nMean length is {0}\nmaxium length is {1}\nminium length is {2}\n'.format(sum(length_list)/len(length_list),max(length_list),min(length_list)))
    print(result)
    return(result)
 
 
def GC_count(file, buffer=2400*3200):
    with open(file) as f:
        head = ''
        gc_list = []
        gc_num = 0
        base_num = 0
        while True:
            a = f.read(buffer)
            raw_list = (head + a).split('\n@')
            deal_list = raw_list[:-1]
            head = raw_list[-1]
            for record in deal_list:
                if record:
                    sequence = record.split('\n')[1].upper().strip()
                    gc_item = sequence.count("G")+sequence.count("C")
                    gc_list.append(gc_item/len(sequence))
                    gc_num += gc_item
                    base_num += len(sequence)
            if not len(a):
                break
        if head:
            record = head
            sequence = record.split('\n')[1].upper().strip()
            gc_item = sequence.count("G")+sequence.count("C")
            gc_list.append(gc_item/len(sequence))
            gc_num += gc_item
            base_num += len(sequence)
    print("\nThe GC count is {0}\nThe number of bases is {1}\nThe number of sequences is {2}".format(gc_num/base_num,base_num,len(gc_list)))
    #print("Ploting...\n")
    density_plot(gc_list, xlabel="Mean GC content",title="GC distribution over all sequences")
    return(0)
 
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
        #print("Waiting for about 20 seconds...\n")
        GC_count(args.file)

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
