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

def reverse_seq(file, buffer = 3096*2048):
    head = ''
    with open(file, 'r') as f:
        while True:
            raw_tmp = f.read(buffer)
            tmp = (head + raw_tmp)
            if tmp.count('\n>') >=2:
                tmp_list = tmp.split('\n>')
                head = '\n>' + tmp_list[-1]
                tmp_record = tmp_list[:-1]
                for i in tmp_record:
                    if not i:
                        continue
                    seq_head = i.split('\n')[0]
                    seq = ''.join(i.split('\n')[1:])
                    print(seq_head)
                    print(seq[::-1])
            else:
                head = tmp
            if not raw_tmp:
                break
        if head:
                tmp_list = head.split('\n>')
                tmp_record = tmp_list
                for i in tmp_record:
                    if not i:
                        continue
                    seq_head = i.split('\n')[0]
                    seq = ''.join(i.split('\n')[1:])
                    print(seq_head)
                    print(seq[::-1])
    return(0)

def DNA_RNA(file, buffer = 3096*2048):
    base_list = ['T','U']
    base_comp_list = ['U','T']
    comp_dict = dict(zip(base_list, base_comp_list))
    with open(file, 'r') as f:
        head = ''
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
                        if 'U' in i.upper():
                            j = 'U'
                        else:
                            j = 'T'
                        new_seq = i.upper().replace(j,comp_dict[j])
                        print(new_seq, end='\n')
            if not raw_tmp:
                break
        if head:
            if head.startswith('>'):
                print(i, end = '\n')
            else:
                if 'U' in i.upper():
                    j = 'U'
                else:
                    j = 'T'
                new_seq = i.upper().replace(j,comp_dict[j])
                print(new_seq, end='\n')
    return(0)

def ToUpper(file, buffer=3069*2048):
    with open(file, 'r') as f:
        head = ''
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
                        print(i.upper(), end='\n')
            if not raw_tmp:
                break
        if head:
            if head.startswith('>'):
                print(i, end = '\n')
            else:
                print(head.upper(), end='\n')
    return(0)

def ToLower(file, buffer=3069*2048):
    with open(file, 'r') as f:
        head = ''
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
                        print(i.lower(), end='\n')
            if not raw_tmp:
                break
        if head:
            if head.startswith('>'):
                print(i, end = '\n')
            else:
                print(head.lower(), end='\n')
    return(0)

def OutPutLength(file, length, buffer=2048*3096):
    if length > 0:
        with open(file, 'r') as f:
            head = ''
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
                            try:
                                print(i[:length], end='\n')
                            except:
                                print(i)
                if not raw_tmp:
                    break
            if head:
                if head.startswith('>'):
                    print(i, end = '\n')
                else:
                    print(head[:length], end='\n')
    else:
        with open(file, 'r') as f:
            head = ''
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
                            try:
                                print(i[length:], end='\n')
                            except:
                                print(i)
                if not raw_tmp:
                    break
            if head:
                if head.startswith('>'):
                    print(i, end = '\n')
                else:
                    print(head[length:], end='\n')
    return(0)

def seq_order(file, TYPE, buffer=2048*3096):
    fasta_dict = {}
    with open(file, 'r') as f:
        head = ''
        while True:
            raw_tmp = f.read(buffer)
            tmp = (head + raw_tmp).split('\n')
            tmp_records = tmp[:-1]
            head = tmp[-1]
            for i in tmp_records:
                if i:
                    if i.startswith('>'):
                        KEY = i.strip()
                        fasta_dict[KEY] = ''
                    else:
                        fasta_dict[KEY] += i.strip()
            if not raw_tmp:
                break
        if head:
            if head.startswith('>'):
                KEY = head.strip()
                fasta_dict[KEY] = ''
            else:
                fasta_dict[KEY] += head.strip()
    if TYPE.lower() == 'l+':
        SORT = sorted(fasta_dict.items(), key=lambda e:len(e[1]), reverse=False)
        for item in SORT:
            print(item[0]+'\n'+item[1])
    elif TYPE.lower() == 'l-':
        SORT = sorted(fasta_dict.items(), key=lambda e:len(e[1]), reverse=True)
        for item in SORT:
            print(item[0]+'\n'+item[1])
    elif TYPE.lower() == 'n+':
        SORT = sorted(fasta_dict.items(), key=lambda e:e[0][1:], reverse=False)
        for item in SORT:
            print(item[0]+'\n'+item[1])
    elif TYPE.lower() == 'n-':
        SORT = sorted(fasta_dict.items(), key=lambda e:e[0][1:], reverse=True)
        for item in SORT:
            print(item[0]+'\n'+item[1])
    return(0)

def extract_from_id(file, ID, buffer=2048*3096):
    next_id = False
    found = False
    if ID.startswith('>'):
        ID = ID[1:]
    with open(file, 'r') as f:
        head = ''
        while True:
            raw_tmp = f.read(buffer)
            tmp = (head + raw_tmp).split('\n')
            tmp_records = tmp[:-1]
            head = tmp[-1]
            tmp_text = '\n'.join(tmp_records)
            if ID+'\n' in tmp_text:
                found = True
                if '>' in tmp_text[tmp_text.find(ID):]:
                    next_id = True
                    break
                while True:
                    raw_tmp = f.read(buffer)
                    tmp = (head + raw_tmp).split('\n')
                    tmp_records = tmp[:-1]
                    head = tmp[-1]
                    if '>' in  '\n'.join(tmp_records):
                        next_id = True
                        tmp_text += '\n'.join(tmp_records).split('>')[0]
                        break
                    else:
                        tmp_text += '\n'.join(tmp_records)
                    if not raw_tmp:
                        break
                break
            if not raw_tmp:
                break
    if found:
        all_text = tmp_text[tmp_text.find(ID):]
        if not next_id:
            all_text += '\n' + head
        if '>' in all_text:
            print('>'+all_text[:all_text.find('>')])

        else:
            print('>' + all_text)
    else:
        print('Not found!!!!!!!!!!!!!!!!!!!!!!!!!')

    return(0)

def random_seq(file, buffer=2048*3096):
    fasta_dict = {}
    with open(file, 'r') as f:
        head = ''
        while True:
            raw_tmp = f.read(buffer)
            tmp = (head + raw_tmp).split('\n')
            tmp_records = tmp[:-1]
            head = tmp[-1]
            for i in tmp_records:
                if i:
                    if i.startswith('>'):
                        KEY = i.strip()
                        fasta_dict[KEY] = ''
                    else:
                        fasta_dict[KEY] += i.strip()
            if not raw_tmp:
                break
        if head:
            if head.startswith('>'):
                KEY = head.strip()
                fasta_dict[KEY] = ''
            else:
                fasta_dict[KEY] += head.strip()
    import random
    KEY = random.choice(list(fasta_dict.keys()))
    print(KEY)
    print(fasta_dict[KEY])
    return(0)

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('file', help = 'The fastq file_path')
    parser.add_argument('-c', '--comp',action="store_true",help="fasta to complementary fasta")
    parser.add_argument('-r', '--reverse', action="store_true",help="fasta to reverse fasta")
    parser.add_argument('-d', '--D_R', action="store_true",help="switch between DNA and RNA fasta")
    parser.add_argument('-u', '--upper', action='store_true',help='fasta to upper fasta')
    parser.add_argument('-l', '--lower', action='store_true',help='fasta to lower fasta')
    parser.add_argument('-s', '--selection', type=int, help='select length to output, length can either be positive or negative')
    parser.add_argument('-o', '--order', help ='order the fasta file by name for n+ or n-, order the fasta file by length for l+ or l-')
    parser.add_argument('-f', '--find', help = 'find the sequence for a fasta file')
    parser.add_argument('-m', '--randm', action='store_true', help = 'extract a random sequence from a fasta file')
    args = parser.parse_args()

    if args.reverse:
        reverse_seq(args.file)
    if args.comp:
        complementary_seq(args.file)
    if args.D_R:
        DNA_RNA(args.file)
    if args.lower:
        ToLower(args.file)
    if args.upper:
        ToUpper(args.file)
    if args.selection:
        OutPutLength(args.file, args.selection, buffer=2048*3096)
    if args.order:
        seq_order(args.file, args.order, buffer=2048*3096)
    if args.find:
        extract_from_id(args.file, args.find, buffer=2048*3096)
    if args.randm:
        random_seq(args.file, buffer=2048*3096)
if __name__ == '__main__':
    main()
