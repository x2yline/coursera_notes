with open('umf.txt', 'r') as f:
    data = {}
    all_lines = f.readlines()
    line = all_lines[0]
    item_list = line.split()
    for i in item_list:
        data[i] = []
    for line in all_lines[1:]:
        for i in item_list:
            data[i].append(line.split('\t')[item_list.index(i)].strip().strip('"'))
print('Plotting...\n')
def enrichment_plot(data, item_list):
    '''data为字典
    其键为item_list
    item_list的顺序为[pathway_discription,
    hit_gene_number, q_val, rich_factor]'''
    import matplotlib.pyplot as plt
    import numpy as np
    import matplotlib as mpl
    x = [float(i) for i in data[item_list[3]]]
    y = [float(j) for j in range(len(data[item_list[0]]))]
    qvals = [float(i) for i in data[item_list[2]]]

    parameters =  np.linspace(np.min(qvals), np.max(qvals), len(y))
    norm = mpl.colors.Normalize(
        vmin=np.min(parameters),
        vmax=np.max(parameters))
    
    c_m = mpl.cm.autumn#spring
    s_m = mpl.cm.ScalarMappable(cmap=c_m, norm=norm)
    s_m.set_array([])
    fig = plt.figure(figsize=(11,12))
    fig.patch.set_facecolor('w')
    fig.suptitle('KEGG Enrichment', fontsize=24)
    ax = fig.add_axes([0.43, 0.1, 0.5, 0.8])

    ax.set_ylim([np.min(y), np.max(y)])

    ax.set_yticks([ j for j in range(len(data[item_list[0]]))])
    ax.set_yticklabels(data[item_list[0]], fontsize=18, color='k')

    for i in range(len(data[item_list[3]])):
        ax.plot(float(data[item_list[3]][i]), i, 'bo',
                markersize=float(data[item_list[1]][i])*1.2+2 ,clip_on=False,
                color=s_m.to_rgba(qvals[i]),
                 markeredgewidth=0.0)
    ax.set_xlim([np.min(x) - (np.max(x) - np.min(x))/20, np.max(x) + (np.max(x) - np.min(x))/20])
    ax.set_xticks(np.linspace(np.min(x) - (np.max(x) - np.min(x))/20, np.max(x) + (np.max(x) - np.min(x))/20, 5))
    ax.set_xticklabels([round(float(i), 2) for i in np.linspace(np.min(x) - (np.max(x) - np.min(x))/20, np.max(x) + (np.max(x) - np.min(x))/20, 5)])
    ax.get_xaxis().tick_bottom()
    ax.set_xlabel('Rich factor', fontsize=20)
    ax.set_ylabel('Kegg Pathways', fontsize=20)
    ax.get_yaxis().tick_left()
    ax.get_xaxis().set_tick_params(direction='out')
    ax.get_yaxis().set_tick_params(direction='out')
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['left'].set_position(('outward', 10))
    ax.spines['bottom'].set_position(('outward', 30))
    axbar = fig.add_axes([0.85, 0.4, 0.1, 0.3])
    axbar.set_axis_off()
    cb = plt.colorbar(s_m)
    cb.outline.set_visible(False)
    cb.set_label('Q value', labelpad=-20, y=1.07, rotation=0)
    axmarker = fig.add_axes([0.89, 0.75, 0.1, 0.1])
    axmarker.set_axis_off()
    axmarker.text(0, 1.2, 'Gene number', ha='center')
    for i in range(3):
        axmarker.plot(0, i*0.5, 'ko', markersize=(i*5+5)*1.2+2, clip_on=False)
        axmarker.text(0.02, i*0.5, str(i*5+5), clip_on=False, color='k', ha='left', va='center')
    plt.savefig('enrichment.png', dpi=100)
    plt.show()
enrichment_plot(data, item_list)