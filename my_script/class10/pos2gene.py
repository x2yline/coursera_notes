import os
import re

def get_chr_info(file, chromosome):
    with open(file, 'r') as f:
        head = ''
        chr_info = ''
        get = 0
        while(True):
            buffer = head + f.read(2048*2048)
            print(buffer[buffer.find('\n')+1:buffer.find('\n')+3],end='\r')
            head = buffer[buffer.rfind('\n'):]
            buffer_handle = buffer[:buffer.rfind('\n')]
            if buffer == head:
                buffer_handle = head
            if ('\n'+ str(chromosome)+'\t') in buffer_handle:
                get = 1
                chr_info += buffer_handle[buffer_handle.find(str(chromosome)+'\t'):]
            else:
                if get == 1:
                    break
    return(chr_info)


def find_target_data(gene_name, chr_info):
        target_data = {} 
        header = ['chr','db','record','start','end','tmp','strand','tmp','info']
        buffer_list = chr_info.split('\n')
        for line in buffer_list:
            if  ('gene_name "'+ gene_name.upper() + '"') in line:
                line_list = line.split('\t')
                for i in range(9):
                    try:
                        target_data[header[i]].append(line_list[i])
                    except:
                        target_data[header[i]] = [line_list[i]]

        if not target_data:
            print('\n\n There is some wrong with your gene name!\n')
            raise NameError('your gene_name is not exit')
        print ("\nHave got the gene information!")
        return(target_data)
        
def draw_gene_structure(gene_name,target_data, pos_start, pos_end, png_path='',line_width=5):
    gene_symbol = gene_name.upper()
    if not png_path:
        png_path = gene_symbol+'.png'
    #定义颜色的字典
    tmp_colors = ['lime','red', 'blue', 'yellow','yellow','w','lightgray']
    names_tmp_colors = [ 'gene','CDS','exon','three_prime_utr','five_prime_utr','stop_codon']
    colors_legend_name = ['gene','CDS_exon', 'non_CDS_exon', 'UTR_exon',str(pos_start)+'-'+str(pos_end)]
    color_dict = dict(zip(names_tmp_colors,tmp_colors))
    # 提取转录本名称
    import re
    transcript_list = []
    for i in target_data['info']:
        try:
            transcript_name = re.findall('transcript_name "(.*?)"',i)[0]
            if transcript_name not in transcript_list:
                transcript_list.append(transcript_name)
        except:
            pass
    # 计算转录本数目
    transcript_num = 0
    for i in target_data['record']:
        if i =='transcript':
           transcript_num += 1
 
    import numpy as np
    import matplotlib.patches as mpatches
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
    import matplotlib.lines as lines
    import matplotlib.transforms as transforms
    fig = plt.figure(1)
    # 设置不透明度，默认为1
    fig.patch.set_alpha(1)
    fig.patch.set_facecolor('w')
    num = 0#当前转录本数目标志
    warnings = []
    for i in range(len(target_data['record'])):
        if target_data['record'][i] == 'gene':
            #判断正反链
            if target_data['strand'][i] == '+':
                arr = '->'
            else:
                arr = '<-'
            #图的第一个区域
            # add_axes 是在一张图上指定特定区域作图，第一个数字为从左边%20处，下面20%处开始，宽50%，高60%区域作图
            ax = fig.add_axes([0.2,0.2,0.5,0.6])
            # 定义基因方向箭头
            arrow= mpatches.FancyArrowPatch(
            (int(target_data['start'][i]), 0.1),
            (int(target_data['end'][i]), 0.1),
            arrowstyle= arr,
            mutation_scale=25, lw=1, color='lime',antialiased=True)#antialiased默认为True，边缘平滑处理
            # 画箭头
            ax.add_patch(arrow)
            # 坐标轴标签
            ax.set_xlim([int(target_data['start'][i]), int(target_data['end'][i])])
            ax.set_ylim([-0.5, transcript_num+1])
            ax.set_xticks(np.linspace(int(target_data['start'][i]),int(target_data['end'][i]),5))
            ax.set_yticks([0.1]+list(range(1,transcript_num +1)))
            ax.set_yticklabels(['gene']+transcript_list)
            ax.set_xticklabels([int(i) for i in np.linspace(int(target_data['start'][i]),int(target_data['end'][i]),5)])
            # 坐标轴显示
            ax.spines['top'].set_visible(False)
            ax.spines['left'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.get_xaxis().tick_bottom()
            ax.get_yaxis().tick_left()
            ax.get_xaxis().set_tick_params(direction='out')
            ax.tick_params(axis=u'y', which=u'both',length=0)
            # 坐标轴字体大小
            for tick in ax.xaxis.get_major_ticks():
                tick.label.set_fontsize(6) 
            for tick in ax.yaxis.get_major_ticks():
                tick.label.set_fontsize(6) 
        elif target_data['record'][i] == 'transcript':
            num += 1 # 转录本所有区域计数作图
            line1 = [(int(target_data['start'][i]),num), (int(target_data['end'][i]),num)]
            (line1_xs, line1_ys) = zip(*line1)
            ax.add_line(lines.Line2D(line1_xs, line1_ys, linewidth=0.2,
                                     solid_capstyle = 'butt',solid_joinstyle='miter',
                                     antialiased=False,color='black'))
        elif target_data['record'][i] in color_dict.keys():
            # 添加结构图
            line2 = [(int(target_data['start'][i])-0.5,num), (int(target_data['end'][i])+0.5,num)]
            (line2_xs, line2_ys) = zip(*line2)
            ax.add_line(lines.Line2D(line2_xs, line2_ys, 
                                solid_capstyle = 'butt',solid_joinstyle='miter',
                                linewidth=int(line_width), alpha = 1,
                                color=color_dict[target_data['record'][i]],
                                antialiased=False))
        else:
            warnings.append(target_data['record'][i])
    trans = transforms.blended_transform_factory(
        ax.transData, ax.transAxes)
    rect = patches.Rectangle((pos_start,0), width=pos_end-pos_start, height=1,
                              transform=trans, color='gray', alpha=0.2)
    ax.add_patch(rect)
    if warnings:
        print('\nTips: ')
        print(' and '.join([i for i in set(warnings)]) + ' is not in our consideration!!!!!!')
 
    
    # 做图例
    # add_axes 是在一张图上指定特定区域作图，第一个数字为从左边%74处，下面20%处开始，宽20%，高60%区域作图
    ax_legend = fig.add_axes([0.76,0.2,0.2,0.6])
    #ax_legend.set_xticks([])
    #ax_legend.set_yticks([])
    tmp_colors = ['lime','red', 'blue', 'yellow','lightgray','w','lightgray']
    names_tmp_colors = [ 'gene','CDS','exon','three_prime_utr','five_prime_utr','stop_codon']
    colors_legend_name = ['gene','CDS_exon', 'non_CDS_exon', 'UTR_exon',str(pos_start)+'-'+str(pos_end)]
    color_dict = dict(zip(names_tmp_colors,tmp_colors))
    for i in range(len(colors_legend_name)):
        line3 = [(0, (9-i)*0.1),(0.1, (9-i)*0.1)]
        (line3_xs, line3_ys) = zip(*line3)
        ax_legend.add_line(lines.Line2D(line3_xs, line3_ys, linewidth=5,
                                color=color_dict[names_tmp_colors[i]],
                                solid_capstyle = 'butt',solid_joinstyle='miter',
                                antialiased=False))
        ax_legend.text(0.2, (8.9-i)*0.1,colors_legend_name[i] , fontsize=6)
    ax_legend.set_axis_off()
    # 加标题
    fig.suptitle('\n\n\nchr' + str(target_data['chr'][0])+ ': ' + gene_symbol, fontsize=10)
    # 保存图片
    fig.savefig(png_path, dpi=150)
    plt.show()
    print('\nThe picture file is completed: ' + png_path)
    print("All transcripts of " + gene_name + ':\n' + " ".join(sorted(transcript_list)))
    return(png_path)

def find_overlap_gene_list(chr_info, chromosome, pos_start, pos_end):
    gene_list = re.findall(str(chromosome)+'\t.*?\t(.*?)\t(.*?)\t(.*?)\t.*?\t(.*?)\t.*?gene_name "(.*?)"',chr_info)
    target_list = []
    target_gene_list = []
    for i in gene_list:
        if (int(i[1])>=pos_start and int(i[1]) <= pos_end) or (int(i[2])>=pos_start and int(i[2])<=pos_end) or (int(i[1])<=pos_start and int(i[2])>=pos_end):
            target_list.append(i)
            target_gene_list.append(i[-1])
    target_gene_list = list(set(target_gene_list))
    if len(target_gene_list) == 0:
        print('\nThese is no genes in the positon\n')
    return(target_gene_list)


def draw_pos_gene(overlap_genes, chr_info, pos_start, pos_end, chromosome):
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    import re
    import numpy as np
    import matplotlib.patches as patches
    import matplotlib.transforms as transforms
    if len(overlap_genes) > 0:
        gene_info_list = []
        for i in overlap_genes:
            print(i)
            gene_i = re.search(str(chromosome)+'\t.*?\tgene\t(.*?)\t(.*?)\t.*?\t(.*?)\t.*?gene_name "'+i+'";',chr_info)
            gene_info_list.append(chr_info[slice(gene_i.span()[0], gene_i.span()[1])].split('\t')[3:5]+chr_info[slice(gene_i.span()[0], gene_i.span()[1])].split('\t')[6:7]+[i])
        max_x = max([int(i[1]) for i in gene_info_list]+[int(i[0]) for i in gene_info_list]+[pos_start, pos_end])
        min_x = min([int(i[1]) for i in gene_info_list]+[int(i[0]) for i in gene_info_list]+[pos_start, pos_end])
        fig = plt.figure(1)
        fig.patch.set_alpha(1)
        fig.patch.set_facecolor('w')
        ax = fig.add_axes([0.2,0.2,0.6,0.6])
        y = 0
        ax.set_ylim([0, (len(overlap_genes)+1)*0.1])
        ax.spines['top'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.get_yaxis().set_visible(False)
        ax.get_xaxis().tick_bottom()
        ax.get_yaxis().tick_left()
        ax.set_xlim([min_x,max_x])
        ax.set_xticks([int(k) for k in np.linspace(min_x,max_x, 4)])
        ax.set_xticklabels([int(k) for k in np.linspace(min_x,max_x, 4)])
        ax.get_xaxis().set_tick_params(direction='out')
        ax.tick_params(axis=u'y', which=u'both',length=0)
        trans = transforms.blended_transform_factory(
        ax.transData, ax.transAxes)
        rect = patches.Rectangle((pos_start,0), width=pos_end-pos_start, height=1,
                              transform=trans, color='yellow', alpha=0.5)
        ax.add_patch(rect)
        ax.tick_params(axis='x', colors='gray')
        ax.spines['bottom'].set_color('gray')
        for i in gene_info_list:
            if i[2] == '+':
                arr = '->'
                text_x = i[0]
                ha = 'right'
            else:
                arr = '<-'
                text_x = i[1]
                ha = 'left'
                
            y += 0.1
            # define arrow for genes
            arrow= mpatches.FancyArrowPatch(
                (int(i[0]), y),
                (int(i[1]), y),
                arrowstyle= arr,
                mutation_scale=25, lw=1, color='blue',antialiased=True, alpha=0.6)
            ax.add_patch(arrow)
            ax.text(text_x,y, i[-1] ,style='italic', ha=ha, va='center', color='blue', fontsize=200*6/(200+len(overlap_genes)*0.1))

    fig.suptitle('\n\n\nchr' + str(chromosome)+ ': ' + str(pos_start) +'-'+str(pos_end), fontsize=10, color='red')
    png_path = str(pos_start)+'-'+str(pos_end)+'.png'
    fig.savefig(png_path, dpi=150)
    return(png_path)








def main(chromosome, pos_start, pos_end):
    os.chdir(r'E:\r\biotrainee_demo\class10')
    file = 'Homo_sapiens.GRCh38.87.chr.gtf'
    chr_info = get_chr_info(file, chromosome)
    overlap_genes = find_overlap_gene_list(chr_info, chromosome, pos_start, pos_end)
    if len(overlap_genes) == 1:
        for i in overlap_genes:
            draw_gene_structure(i,find_target_data(i, chr_info),pos_start,pos_end)
    else:
        draw_pos_gene(overlap_genes, chr_info, int(pos_start), int(pos_end), int(chromosome))
    print('\nThere are %d genes in the position\n'%len(overlap_genes))

if __name__ == '__main__':
    chromosome = input("Please enter the Chromsome number:\n").strip()
    pos_start = input("Please enter the start position:\n").strip()
    pos_end = input("Please enter the stop position:\n").strip()
    if not chromosome:
        chromosome = 1
    if not pos_start:
        pos_start = 2075000
    if not pos_end:
        pos_end = 2930999
    main(int(chromosome), int(pos_start), int(pos_end))
    
    
    