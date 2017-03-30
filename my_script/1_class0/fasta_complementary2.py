def complementary_seq(file, buffer=3096*2048):
    base_list = ['A','T','C','G','U','N', '\n']
    base_comp_list = ['T','A','G','C','A','N','\n']
    comp_dict = dict(zip(base_list, base_comp_list))
    with open(file, 'r') as f:
        seq = 1
        front = '\n'
        while True:
            raw_tmp = f.read(buffer)
            for i in raw_tmp:
                if i == '>' and front == '\n':
                    seq = -1
                elif i == '\n' and seq == -1:
                    seq = 1
                front = i
                if seq == 1:
                    print(comp_dict[i.upper()],end = '')
                else:
                    print(i, end = '')
            if not raw_tmp:
                break
    return(0)

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('file', help = 'The fastq file_path')
parser.add_argument('-C', '--comp',action="store_true",help="fasta to complementary fasta")
args = parser.parse_args()
if args.comp:
    complementary_seq(args.file)
