def complementary_seq(file, buffer=3096*2048):
    base_list = ['A','T','C','G','U','N']
    base_comp_list = ['T','A','G','C','A','N']
    comp_dict = dict(zip(base_list, base_comp_list))
    head = ''
    with open(file, 'r') as f:
        while True:
            raw_tmp = f.read(buffer)
            tmp = (head + raw_tmp).split('\n')
            tmp_records = tmp[:-1]
            head = tmp[-1]
            for i in tmp_records:
                if i:
                    if i.startswith('>'):
                        print(i, end = '\n')
                    else:
                        new_seq = ''
                        for j in i.upper():
                            new_seq += comp_dict[j]
                        print(new_seq, end='\n')
            if not raw_tmp:
                break
        if head:
            if head.startswith('>'):
                print(i, end = '\n')
            else:
                new_seq = ''
                for j in head.upper():
                    new_seq += comp_dict[j]
                print(new_seq, end='\n')
    return(0)

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('file', help = 'The fastq file_path')
parser.add_argument('-C', '--comp',action="store_true",help="fasta to complementary fasta")
args = parser.parse_args()
if args.comp:
    complementary_seq(args.file)
