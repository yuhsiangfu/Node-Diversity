"""
Read write pos file of network
Crate on 2013/12/14
@auth: Yu-Hsiang Fu
"""
# ###
# 1.Define functions
# ###
def read_pos_file(filename):
    import numpy as np

    # Read and strip each line of file
    pos = {}
    with open(filename, mode="r") as f:
        for line in f:
            pos_items   = line.strip().split(' ')
            pos_id      = int(pos_items[0])
            pos[pos_id] = np.array([float(l) for l in pos_items[1:3]])
        f.close()
    return pos

def write_pos_file(filename, pos):
    with open(filename, mode="w") as f:
        for i in pos.keys():
            pos_id = str(i)
            pos_x  = str(pos[i][0])
            pos_y  = str(pos[i][1])
            f.write(pos_id+' '+pos_x+' '+pos_y+'\n')
            f.flush()
        f.close()
