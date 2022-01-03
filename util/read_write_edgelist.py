"""
Read write edgelist
Crate on 2013/12/14
@auth: Yu-Hsiang Fu
"""
# ###
# 1.Define functions
# ###
def read_edge_list(filename):
    # Add each edge pair, ex:(start node, end node), in lines of the file
    edge_list = []
    with open(filename, mode="r") as f:
        for line in f:
            # edge_tuple = line.strip().split(' ')
            # edge_pair  = edge_tuple[0]+' '+edge_tuple[1]
            edge_pair = line.strip()
            edge_list.append(edge_pair)
        f.close()
    return edge_list

def write_edge_list(filename, G):
    import networkx as nx
    nx.write_edgelist(G, path=filename, data=False)
