"""
Read write pairvalue
Crate on 2014/03/16
@auth: Yu-Hsiang Fu
"""
# ###
# 1.Define functions
# ###
def read_pairvalue_file(filename):
    # Add key-value pair, ex:(node id, betweenness, closenesses or other value), in lines of the file
    pairvalue = {}
    with open(filename, mode="r") as f:
        for line in f:
            pair           = line.strip().split(' ')
            key            = int(pair[0])
            value          = float(pair[1])
            pairvalue[key] = value
        f.close()
    return pairvalue

def write_pairvalue_file(filename, G, pairvalue):
    with open(filename, mode="w") as f:
        keys_set = set(pairvalue.keys())
        for n in G.nodes():
            node_id = n
            node_pairvalue = 0
            if n in keys_set: node_pairvalue = pairvalue[node_id]
            f.write(str(node_id)+' '+str(node_pairvalue))
            f.write('\n')
            f.flush()
        f.close()
