import pandas as pd
import numpy as np
import libcluster
import libplot
import collections
import scipy.stats as stats
from matplotlib.collections import LineCollection
from matplotlib.colors import LinearSegmentedColormap
import randomly


def load_monocle_state_clusters(file='monocle_ptime.txt'):
    df = pd.read_csv(file, sep='\t', header=0)
    
    ret = df[['Barcode', 'State']]
    ret = ret.rename(columns={'State' : 'Cluster'})
    ret = ret.set_index('Barcode')
    
    return ret


def sort_clusters_by_exp(df, d, cuttree, colors=None):
    """
    Resort clusters so that expression moves in a gradient left to right
    high to low.
    
    Parameters
    ----------
    df : DataFrame
        Data to be reordered
    d : Dendrogram
        Dendrogram
    cuttree : cuttree object
        Cut tree object
        
    Returns
    -------
    numpy.ndarray
        Array of cells now ordered
        
    """
    
    lidx = np.array(d['leaves'])
    
    if colors is None:
        colors = libcluster.colors()
    
    max_c = np.max(cuttree)
    
    clust_ord_map = collections.defaultdict(lambda: collections.defaultdict(list))
    within_clust_ord_map = collections.defaultdict(lambda: collections.defaultdict(lambda: collections.defaultdict(list)))

    for c in range(1, max_c + 1):
        cidx = np.where(cuttree == c)[0]
        
        # data related to cluster
        dc = df.iloc[cuttree == c, :].values
        
        # Find the max value and its col index from the mean expression 
        # profile of the cluster
        m = dc.mean(axis=0)
        cx = m.max()
        cix = m.argmax()
        
        # if max value occurs on right side, invert x so that we sort from
        # high expression in the middle to high expression at the end to
        # maintain the gradient
        if cix < 50:
            cx = -cx
        
        # sort by position and then expression level 
        clust_ord_map[cix][cx].append(c)
        
        # order within cluster
        
        xs = dc.max(axis=1)
        ixs = dc.argmax(axis=1)
        
        for i in range(0, xs.size):
            x = xs[i]
            ix = ixs[i]
            
            if ix < 50:
                x = -x
        
            within_clust_ord_map[c][ix][x].append(cidx[i])
        
        
        
    
    # New order of clusters
    ordered_cluster_ids = []
    
    for ix in sorted(clust_ord_map):
        # sort within block from highest to lowest
        for x in sorted(clust_ord_map[ix]):
            ordered_cluster_ids.extend(clust_ord_map[ix][x])
    
    idx = []
    
    for c in ordered_cluster_ids:
        # For each cluster, look for the indices for that cluster in cuttree
        # so we know which samples are in the cluster. Next, look up those
        # indices in the sorted leaves so that we can preserve within cluster
        # ordering
        #idx.extend(lidx[np.isin(lidx, np.where(cuttree == c)[0])])
        
        wcom = within_clust_ord_map[c]
        
        for ix in sorted(wcom):
            # sort within block from highest to lowest
            for x in sorted(wcom[ix]):
                idx.extend(wcom[ix][x])
        
    
    idx = np.array(idx)

    labels_idx = []
    
    ordered_clusters = cuttree[idx]
    
    for c in ordered_cluster_ids:
        cidx = np.where(ordered_clusters == c)[0]
        labels_idx.append(cidx[cidx.size // 2])
        
    
    labels = ['Cluster {}'.format(c) for c in ordered_cluster_ids]
    label_colors = [colors[c - 1] for c in ordered_cluster_ids]
    row_colors = [colors[c - 1] for c in ordered_clusters]
    
    return idx, labels_idx, labels, label_colors, row_colors



def pseudo_trace(df, clusters, name, colors=None):
    if colors is None:
        colors = libcluster.colors()
        
    fig, ax = libplot.new_fig(w=10, h=8)
    #fig = libplot.new_base_fig(w=12, h=8)
    
    max_x = np.ceil(df['Pseudotime'].max())
    
    x = np.linspace(0, max_x, 100)
    
    y = 0
    
    cluster_ids = np.array(sorted(set(clusters['Cluster'])))
    
    for c in cluster_ids[::-1]:
        d = df['Pseudotime'][df['Cluster'] == c].values
        
        density = stats.gaussian_kde(d)
        
        p = y + np.clip(density(x), 0, 1)
        
        #axc = libplot.new_ax(fig, root_ax=ax, direction='out')
        
        #libplot.plot(x, p, c=colors[c - 1], label='Cluster {}'.format(c), ax=axc, alpha=0.5)
        
        ax.fill_between(x, p, y, edgecolor='none', facecolor=colors[c - 1], alpha=0.5)
        
        #segments = [((x[i], p[i]), (x[i + 1], p[i + 1])) for i in range(0, x.size - 1)]
        
        #cmap = LinearSegmentedColormap.from_list('c{}'.format(c), [colors[c - 1], libplot.get_tint(colors[c - 1], 0.5)])
        
        #lc = LineCollection(segments, cmap=cmap, norm=plt.Normalize(x.min(), x.max()), linewidth=3)
        # Used by cmap to determine color combined with the norm function
        #lc.set_array(x)
        #axc.add_collection(lc)
        
        #break
        
        y += 1
    
    #libplot.format_legend(ax)
    ax.set_xlabel('Pseudotime')
    #ax.set_ylabel('Cluster')
    ax.spines['left'].set_visible(False)
    ax.set_yticks([])
    ax.set_xlim([0, max_x])
    ax.set_xticks([0, max_x])
    ax.set_xticklabels([0, 1])
    ax.set_ylim([-0.5, len(cluster_ids)])
    ax2 = ax.twinx()
    ax2.set_ylim([-0.5, len(cluster_ids)])
    ax2.set_yticks([i + 0.5 for i in range(0, len(cluster_ids))])
    ax2.set_yticklabels(['Cluster {}'.format(c) for c in cluster_ids[::-1]])
    ax2.tick_params(axis='y', colors='white')
    ax2.spines['left'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.spines['top'].set_visible(False)
    
    # Color the labels
    libplot.color_labels(ax2, colors, len(cluster_ids), color_indices=(cluster_ids[::-1] - 1))
    
    libplot.savefig(fig, 'pseudotime_trace_{}.pdf'.format(name))


def remove_bad_cells(data, genes, gene_index=None):
    """
    Find cells that expression certain genes and flag them for removal
    
    Parameters
    ----------
    data : DataFrame
        count matrix
    genes : list
        genes to check.
    gene_index : optional, list
        list of genes for each row in data.
        
    """
    
    if gene_index is None:
        _, gene_index = data.index.str.split(';').str

    idx = np.where(gene_index.isin(genes))[0]

    gp = collections.defaultdict(set)

    for g in genes:
        idx = np.where(gene_index == g)[0]
    
        exp = data.iloc[idx, :].sum(axis=0)
    
        idx2 = np.where(exp > 0)[0]

        for i in idx2:
            gp[i].add(g)
    
    removed_cols = list(sorted(gp))
    
    # remove the bad cells
    ret = data.iloc[:, np.setxor1d(range(0, data.shape[1]), removed_cols)]
    
    # log what we remove and why
    
    genes = []
    
    for i in removed_cols:
        genes.append(';'.join(sorted(gp[i])))
    
    df = pd.DataFrame({'Barcode':data.columns[removed_cols].values, 'Genes': genes})
    df = df.set_index('Barcode')
    df.to_csv('removed_cells.txt', sep='\t', header=True, index=True)
        
    return ret


def randomly_filter(counts, name, fdr=0.01):
    """
    Use the Randomly package to remove genes that just look like noise
    
    Parameters
    ----------
    counts: df: Pandas dataframe, shape (n_genes, n_cells)
        Counts matrix
    name: str,
        Name to call output files
    fdr: float, optional
        fdr threshold for filtering genes
    """
    
    # Need to transpose for randomly
    cr = counts.T

    model = randomly.Rm()
    model.preprocess(cr, min_tp=0, min_genes_per_cell=0, min_cells_per_gene=0, refined=True)
    model.refining(min_trans_per_gene=7)
    model.fit()
    model.plot_mp(path='{}_mp.pdf'.format(name))
    model.plot_statistics(path='{}_mp_stats.pdf'.format(name))
    
    # get the genes of interest
    cr2 = model.return_cleaned(fdr=fdr).T
    
    # filter counts to include just the genes of interest
    cr3 = counts.loc[counts.index.isin(cr2.index), :]
    print('Randomly filtered size', cr3.shape)
    
    cr3.to_csv('{}_umi.txt.gz'.format(name), sep='\t', header=True, index=True, compression='gzip')
    
    
    # Also create TPM
    
    s = cr3.sum(axis=0)
    
    s = 1000000 / s
    
    cr3 = cr2 * s
    cr3 = (cr3 + 1).apply(np.log2)
    cr3.round(3).to_csv('{}_tpm_log2.txt.gz'.format(name), sep='\t', header=True, index=True, compression='gzip')

