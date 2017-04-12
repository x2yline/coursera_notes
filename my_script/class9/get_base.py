
file = r'E:\r\biotrainee_demo\class2\hg19.fa'
chromosome = 5#int(input("Please enter the chromosome:\n"))
base_pos = 8397383#int(input("Please enter the base position:\n"))
with open(file, 'r') as f:
    head = ''
    got = 0
    while True:
        base_begin_pos = 0
        buffer = head + f.read(2048*2048)
        if '>' in buffer:
            print(buffer[buffer.find('>')+1:buffer.find('>')+6].strip(), end='\r')
        if buffer.rfind('>') > buffer.rfind('\n'):
            buffer = buffer[:buffer.rfind('>')]
            head = buffer[buffer.rfind('>'):]
        else:
            buffer = buffer
            head = ''
        if ('>chr'+ str(chromosome)) in buffer:
            got = 1
            chr_begin = buffer[buffer.find('>chr'+ str(chromosome))+len('>chr'+ str(chromosome))+1:].replace('\n','').replace(' ','')
            base_begin_pos += len(chr_begin)
            if base_begin_pos >=base_pos:
                end = True
                base_value = chr_begin[base_pos-1]
                break
            else:
                chr_skip1 = f.read(base_pos-base_begin_pos-1).replace('\n','').replace(' ','')
                chr_skip2 = f.read(base_pos-base_begin_pos-1).replace('\n','').replace(' ','')
                base_value = chr_skip2[base_pos-base_begin_pos-len(chr_skip1)-1]
                end = True
                if '>' in chr_skip1 or '>' in chr_skip2[:base_pos-base_begin_pos-len(chr_skip1)]:
                    print("\nThe position do not exist!!!!\n")
                    end = False
                    break
        if got == 1 or len(buffer)==0:
            break
    if end:
        print("\nThe base of chr{}:{} is {}".format(chromosome, base_pos, base_value))
            
            
            
