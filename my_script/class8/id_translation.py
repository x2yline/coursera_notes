def read_trans_file(file, target_column = [1,2]):
    target_dict = {}
    if file.split('\\')[-1][0:3] == 'GPL':
        with open(file) as f:
            for line in f:
                if line:
                    if line[0] not in ['#','!' '^']:
                        break
        target_column[0] = line.strip().split('\t').index('ID')
        target_column[1] = line.strip().split('\t').index('Entrez_Gene_ID')
    with open(file) as f:
        for line in f:
            if line[0] not in ['#','!' '^']:
                line_list = line.strip().split('\t')
                geneid = line_list[target_column[0]]
                gene_trans = line_list[target_column[1]]
                if geneid not in target_dict.keys():
                    target_dict[geneid] = gene_trans
                else:
                    target_dict[geneid] = [gene_trans] + list(target_dict[geneid])
    return(target_dict)

    
    

def column_trans(file, target_dict, column_common, exchange_key_val = False):
    if exchange_key_val:
        target_dict = dict((zip(target_dict.values(), target_dict.keys())))
    with open(file) as f:
        for line in f:
            if line[0] not in ['#','!' '^']:
                line_list = line.strip().split('\t')
                try:
                    line_target = target_dict[line_list[column_common]]
                    new_line = line.strip() + '\t' + line_target
                    print(new_line)
                except:
                    print(line_list[column_common] + ' is not in our dict!!!!!!')
                    break
            else:
                print(line.strip() + '\tnew_col')

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-f1','--file1',help = 'The target file to combine with and print out')
    parser.add_argument('-f2', '--file2',help = 'The infomation of the translation')
    parser.add_argument('-e', '--extract',default = '1, 2',help = 'column of file2 to extract as dict')
    parser.add_argument('-c', '--common', type=int, default=1,help="The target file column share with file2")
    args = parser.parse_args()
    col_trans_dict = read_trans_file(args.file2,[int(i) for i in args.extract.split(',')])
    #print(col_trans_dict)
    column_trans(args.file1, col_trans_dict, column_common = args.common)
if __name__ == '__main__':
    main()


            