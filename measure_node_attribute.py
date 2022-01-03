"""
Measure node attribute
Crate: 2014/03/17
Check: 2016/05/01
@auth: Yu-Hsiang Fu
"""
# ###
# 1.Import packages
# ###
import networkx as nx
import numpy    as np
# import math
import sys
import time

# Import modules
import util.read_write_edgelist  as elrw
import util.read_write_pairvalue as pvrw
import util.read_write_pos       as psrw
import util.read_write_pickle    as pkrw

# ###
# 2.Const variables
# ###
# Node attributes
NODE_ID    = 'node_id'
NODE_POS_X = 'node_pos_x'
NODE_POS_Y = 'node_pos_y'

# Node measurement: local
NODE_DEGREE          = 'node_degree'
NODE_CC              = 'node_cc'
NODE_NEIGHBOR_DEGREE = 'node_neighbor-degree'
NODE_NEIGHBOR_CORE   = 'node_neighbor-core'

# Node measurement: global
NODE_BETWEENNESS   = 'node_betweenness'
NODE_CLOSENESS     = 'node_closeness'
NODE_KCORE         = 'node_k-core'
NODE_KCORE_ENTROPY = 'node_k-core-entropy'
NODE_PAGERANK      = 'node_pagerank'
NODE_MV17          = 'node_mv17'

# Constant
PAGERANK_ALPHA    = 0.85  # Google uses this value
PAGERANK_MAX_ITER = 100   # It could be enough

# ###
# 3.Define functions
# ###
def append_new_attribute(net_attr, append_attr, new_attr):
    for i in sorted(net_attr.keys()):
        net_attr[i][new_attr] = append_attr[i]
    return net_attr

def create_network(edgelist):
    # Create network
    G = nx.parse_edgelist(edgelist, nodetype=int)

    # Remove self-loop and convert to undirected graph
    G.remove_edges_from(G.selfloop_edges())
    G = G.to_undirected()
    return G

def create_network_attribute(G):
    net_attr = {}
    for ni in G.nodes():
        node_info          = {}
        node_info[NODE_ID] = ni
        net_attr[ni]       = node_info
    return net_attr

def compute_kcore_entropy(G, node_core):
    entropy_dict = {}
    for ni in G:
        neighbor_list = G.neighbors(ni)

        # case 1: entropy > 0, number of neighbor > 1
        if len(neighbor_list) > 1:
            neighbors_core_list = [node_core[x] for x in neighbor_list]
            counts              = np.bincount(neighbors_core_list)
            probs               = np.divide(counts[np.nonzero(counts)], len(neighbors_core_list))
            entropy             = -np.sum([np.multiply(pi, np.log2(pi)) for pi in probs])
            entropy_dict[ni]    = entropy
        # case 2: entropy = 0
        else:
            entropy_dict[ni] = 0
    return entropy_dict

def compute_neighbor_attribute(G, node_attr, specified_attr=NODE_NEIGHBOR_DEGREE):
    neighbor_attr = {}
    for ni in G:
        neighbor_list = list(G.neighbors(ni))
        if specified_attr is NODE_CC:
            if len(neighbor_list) is 0: # case 1: neighbor's cc = 0
                neighbor_attr[ni] = 0
            else:                         # case 2: neighbor's cc > 0
                neighbor_attr_list = [node_attr[n] for n in neighbor_list]
                neighbor_attr[ni]  = np.subtract(1, np.divide(np.sum(neighbor_attr_list), len(neighbor_attr_list)))
        # neighbor's attribute
        elif specified_attr is NODE_NEIGHBOR_DEGREE:
            neighbor_attr_list = [node_attr[n] for n in neighbor_list]
            neighbor_attr[ni]  = np.log2(np.sum(neighbor_attr_list))
        # neighbor's neighbor's attribute: closeness, core, degree, entropy
        else:
            attr_value = 0
            for nj in neighbor_list:
                nj_neighbor_list = G.neighbors(nj)
                attr_value      += np.sum([node_attr[n] for n in nj_neighbor_list])
            neighbor_attr[ni] = np.log2(attr_value) if attr_value > 0 else 0
    return neighbor_attr

def measure_node_attribute(G, net_attr, progress=False):
    # Global attributes: k-core, k-core entropy and pagerank
    if progress: print(" -compute global attributes: k-core, k-core entropy.")
    node_core           = nx.core_number(G)
    node_kcore_entropy  = compute_kcore_entropy(G, node_core)

    if progress: print(' -compute pagerank: alpha='+str(PAGERANK_ALPHA)+', max_iter='+str(PAGERANK_MAX_ITER)+'.')
    node_pagerank = nx.pagerank(G, alpha=PAGERANK_ALPHA, max_iter=PAGERANK_MAX_ITER)

    # Local attributes: c.c and degree
    if progress: print(' -compute local attributes: c.c and degree.')
    node_cc     = nx.clustering(G)
    node_degree = nx.degree(G)

    if progress: print(" -compute local attributes: neighbor's k-core and degree.")
    # neighbor's attributes
    node_neighbor_core   = compute_neighbor_attribute(G, node_core, NODE_NEIGHBOR_CORE)
    node_neighbor_degree = compute_neighbor_attribute(G, node_degree, NODE_NEIGHBOR_DEGREE)

    # Add all attributes of node to node_dict
    if progress: print(' -create node attributes info.')
    for ni in G.nodes():
        # global attributes
        net_attr[ni][NODE_KCORE]           = node_core[ni]
        net_attr[ni][NODE_PAGERANK]        = node_pagerank[ni]
        # local attributes
        net_attr[ni][NODE_CC]              = node_cc[ni]
        net_attr[ni][NODE_DEGREE]          = node_degree[ni]
        # neighbor's neighbor's attributes
        net_attr[ni][NODE_NEIGHBOR_CORE]   = node_neighbor_core[ni]
        
        # proposed attribute
        net_attr[ni][NODE_KCORE_ENTROPY]   = node_kcore_entropy[ni]
        net_attr[ni][NODE_NEIGHBOR_DEGREE] = node_neighbor_degree[ni]
        net_attr[ni][NODE_MV17]            = net_attr[ni][NODE_KCORE_ENTROPY] * net_attr[ni][NODE_NEIGHBOR_DEGREE]
    return net_attr

# ###
# 4.Main function: the input file is assumed as edgelist of gcc (maximum subgraph of network)
# ###
def main_function():
    total_time      = time.time()
    folder_edgelist = 'edgelist/'
    folder_file     = 'file/'
    # collaboration network
    # file_name       = 'ca_astroph_gcc'     # N=17903,  E=196972,  MAX_CORE=56
    # file_name       = 'ca_condmat_gcc'     # N=21363,  E=91286,   MAX_CORE=25
    # file_name       = 'ca_grqc_gcc'        # N=4158,   E=13422,   MAX_CORE=43
    # file_name       = 'ca_hepph_gcc'       # N=11204,  E=117619,  MAX_CORE=238
    # file_name       = 'ca_hepth_gcc'       # N=8638,   E=24806,   MAX_CORE=31
    # file_name       = 'jazz_musicians_gcc' #
    # communication network
    # file_name       = 'email_contacts_gcc' # N=12625,  E=20362,   MAX_CORE=23
    # file_name       = 'email_enron_gcc'    # N=33696,  E=180811,  MAX_CORE=43
    # classical network
    # file_name       = 'celegansneural_gcc' #
    # file_name       = 'dolphins_gcc'       #
    # file_name       = 'lesmis_gcc'         #
    # file_name       = 'netscience_gcc'     # N=379,    E=914,     MAX_CORE=8
    file_name       = 'polblogs_gcc'       # N=1222,   E=16714,   MAX_CORE=36

    print('1.Create a network from edgelist file.')
    start_time       = total_time
    network_edgelist = elrw.read_edge_list(folder_edgelist+file_name+'.txt')
    G = create_network(network_edgelist)
    print(' -', round(time.time() - start_time, 4), 'seconds')

    print('2.Create attribute list from network')
    start_time   = time.time()
    network_attr = create_network_attribute(G)
    print(' -', round(time.time() - start_time, 4), 'seconds')

    print('3.Append new attributes to network.')
    start_time = time.time()
    print(' -Add betweenness as new attribute.')
    betweenness_list = pvrw.read_pairvalue_file(folder_edgelist+file_name+'_tbet.txt')
    network_attr     = append_new_attribute(network_attr, betweenness_list, NODE_BETWEENNESS)
    print(' -Add closeness as new attribute.')
    closeness_list = pvrw.read_pairvalue_file(folder_edgelist+file_name+'_clos.txt')
    network_attr   = append_new_attribute(network_attr, closeness_list, NODE_CLOSENESS)
    print(' -Add pos as new attribute.')
    pos_list     = psrw.read_pos_file(folder_edgelist+file_name+'_pos.txt')
    pos_x        = {k: v[0] for k, v in pos_list.items()} # X-axis
    pos_y        = {k: v[1] for k, v in pos_list.items()} # Y-axis
    network_attr = append_new_attribute(network_attr, pos_x, NODE_POS_X)
    network_attr = append_new_attribute(network_attr, pos_y, NODE_POS_Y)
    print(' -', round(time.time() - start_time, 4), 'seconds')

    print("4.Measurement node's attributes of network.")
    start_time   = time.time()
    network_attr = measure_node_attribute(G, network_attr, progress=True)
    print(' -', round(time.time() - start_time, 4), 'seconds')

    print('4.Write result of measurement to file.')
    start_time = time.time()
    pkrw.write_pickle_file(folder_file+file_name+'-attr.pickle', network_attr)
    print(' -', round(time.time() - start_time, 4), 'seconds')
    print('Done., total of run time:', round(time.time() - total_time, 4), 'seconds')

# ###
# 5.Run main function for testing or useing
# ###
if __name__ == '__main__': main_function()
