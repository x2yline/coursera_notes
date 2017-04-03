# /bin/python
# encoding=utf-8
 
 
"""
简介： fastq文件数据处理工具
作者： dongye
时间： 2017年3月18日01:11:16
"""
 
 
from optparse import OptionParser
import sys
 
args = sys.argv
 
def cut_fastq(filename, cut_5=0, cut_3=0):
    """
    从5'端,3'端截掉几个碱基
 
    :param filename: fastq文件名
    :param cut_5: 5'端截掉碱基数, 大于0
    :param cut_3: 3'端截掉碱基数, 大于0
    :return:
    """
 
    if cut_3 < 0:
        raise ValueError('cut_3: %s < 0' % cut_3)
    if cut_5 < 0:
        raise ValueError('cut_5: %s < 0' % cut_5)
 
    with open(filename) as if_fq:
        while if_fq:
            line_1 = if_fq.readline().strip('\n')
            if not (if_fq and line_1):
                break
            line_2 = if_fq.readline().strip('\n')
            line_3 = if_fq.readline().strip('\n')
            line_4 = if_fq.readline().strip('\n')
 
            print(line_1)
            print(line_2[cut_5:][:-cut_3])
            print(line_3)
            print(line_4[cut_5:][:-cut_3])
 
 
def length_distribution(filename):
    """
    统计fastq文件reads长度分布
 
    :param filename: fastq文件名
    :return:
    """
 
    reads_len = {}
    with open(filename) as if_fq:
        while if_fq:
            line_1 = if_fq.readline().strip('\n')
            if not (if_fq and line_1):
                break
            line_2 = if_fq.readline().strip('\n')
            line_3 = if_fq.readline().strip('\n')
            line_4 = if_fq.readline().strip('\n')
 
            length = len(line_2)
            if not length in reads_len:
                reads_len[length] = 0
            reads_len[length] = 1
 
    for length, num in reads_len.items():
        print("%s\t%s" % (length, num))
    return reads_len
 
 
def fq_2_fa(filename):
    """
    将fastq格式文件转换为fasta格式
 
    :param filename: fastq文件
    :return:
    """

 
    with open(filename) as if_fq:
        while if_fq:
            line_1 = if_fq.readline().strip('\n')
            if not (if_fq and line_1):
                break
            line_2 = if_fq.readline().strip('\n')
            line_3 = if_fq.readline().strip('\n')
            line_4 = if_fq.readline().strip('\n')
 
            print ('>'+line_1)
            print (line_2)
 
 
def fq_length(filename):
    """
    统计fastq文件中碱基数量(reads总长度)
 
    :param filename: fastq文件
    :return:
    """
 
    num = 0
    with open(filename) as if_fq:
        while if_fq:
            line_1 = if_fq.readline().strip('\n')
            if not (if_fq and line_1):
                break
            line_2 = if_fq.readline().strip('\n')
            line_3 = if_fq.readline().strip('\n')
            line_4 = if_fq.readline().strip('\n')
 
            num += len(line_2)
    print(num)
    return num
 
 
def count_gc(filename):
    """
    统计fastq文件中reads的GC含量
 
    :param filename: fastq文件
    :return:
    """
 
    GC = 0
    with open(filename) as if_fq:
        while if_fq:
            line_1 = if_fq.readline().strip('\n')
            if not (if_fq and line_1):
                break
            line_2 = if_fq.readline().strip('\n').upper()
            line_3 = if_fq.readline().strip('\n')
            line_4 = if_fq.readline().strip('\n')
            GC += line_2.count('G') + line_2.count('C')
 
    # 函数的好处
    SUM = fq_length(filename)
    print ("GC : %s" % (GC * 1.0 / SUM))
    return (GC * 1.0 / SUM)
 
 
def main(args):
    parser = OptionParser()
    parser.add_option("-f", "--fastq", dest="filename",
                      help="fastq filename", metavar="FILE")
 
    parser.add_option("--cut", "--cut-fastq", dest="cut",
                      help="cut fastq file", action="store_true",
                      default=False)
    parser.add_option("-5", "--cut-5", dest="cut_5", type=int,
                      help="cut fastq N(N>0) bases from 5'", metavar="INT", default=0)
    parser.add_option("-3", "--cut-3", dest="cut_3", type=int,
                      help="cut fastq N(N>0) bases from 3'", metavar="INT", default=0)
 
    parser.add_option("--len-dis", dest="len_dis",
                      help="sequence length distribution", action="store_true",
                      default=False)
 
    parser.add_option("--fasta", "--fastq2fasta", dest="fasta",
                      help="convert fastq to fasta", action="store_true",
                      default=False)
 
    parser.add_option("--len", "--fastq-length", dest="fq_len",
                      help="total reads number", action="store_true",
                      default=False)
 
    parser.add_option("--gc", "--count-gc", dest="gc",
                      help="print GC%", action="store_true",
                      default=False)
 
    (options, args) = parser.parse_args()
    if not options.filename:
        parser.print_help()
    filename = options.filename
 
    if options.cut:
        cut_5 = options.cut_5
        cut_3 = options.cut_3
        cut_fastq(filename, cut_5, cut_3)
 
    if options.len_dis:
        length_distribution(filename)
 
    if options.fq_len:
        fq_length(filename)
 
    if options.fasta:
        fq_2_fa(filename)
 
    if options.gc:
        count_gc(filename)
 
import time
time1 = time.time()
 
if __name__ == '__main__':
    main(args)
    #print('\nUsed %s s'%(time.time()-time1))