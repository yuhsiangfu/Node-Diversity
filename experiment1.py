"""
Experiment1: propagation by top-k nodes
Crate: 2014/03/16
Check: 2016/05/01
@auth: Yu-Hsiang Fu
"""
# ###
# 1.Import packages
# ###
import matplotlib.pyplot as plt
import networkx          as nx
import numpy             as np
import sys
import time

# Import modules
import util.sir_model            as sir
import util.read_write_edgelist  as elrw
import util.read_write_pickle    as pkrw

# ###
# 2.Const variables
# ###
# Color
COLOR_BLACK   = 'k'
COLOR_GRAY    = 'gray'
COLOR_ORANGE  = 'orange'
COLOR_YELLOW  = 'y'
COLOR_BLUE    = 'b'
COLOR_CYAN    = 'c'
COLOR_MAGENTA = 'm'
COLOR_RED     = 'r'
COLOR_LIST    = [COLOR_GRAY, COLOR_ORANGE, COLOR_YELLOW, COLOR_BLUE, COLOR_CYAN, COLOR_MAGENTA, COLOR_RED, COLOR_BLACK]

# Marker
MARKER_CIRCLE      = 'o'
MARKER_TRIANGLE_UP = '^'
MARKER_SQUARE      = 's'
MARKER_HEXAGON     = 'h'
MARKER_X           = 'x'
MARKER_PLUS        = '+'
MARKER_POINT       = '.'
MARKER_STAR        = '*'
MARKER_LIST        = [MARKER_CIRCLE, MARKER_TRIANGLE_UP, MARKER_SQUARE, MARKER_HEXAGON, MARKER_X, MARKER_PLUS, MARKER_POINT, MARKER_STAR]

# Plot
PLOT_X_SIZE = 8
PLOT_Y_SIZE = 8

# SIR model: Kitsak et al (2010): rate_infection=0.08, rate_recovery=1.0; Hang et al (2008): round=30, time_step=120
RATE_INFECTION = 0.02
RATE_RECOVERY  = 1
#
NUM_ROUND      = 1000
NUM_TIME_STEP  = 50
NUM_TOPK       = 1
NUM_TOPP       = 0.01

# ###
# 3.Define functions
# ###
def retrieve_topk_nodes(network_attr=None, specified_attr='', top_k=1):
    if specified_attr is '': return
    if top_k < 1:            return

    # Sort the netowrk_attr by specified_arrt
    sorted_list = sorted(network_attr.items(), key=lambda x:x[1][str(specified_attr)], reverse=True)
    node_topk   = []
    for i in range(0, top_k):
        node_topk.append(sorted_list[i][1]['node_id'])
    return node_topk

def network_propagation(G, net_attr=None, measurement_list=None, model=None, top_k=1, top_p=0.1, mode=1, progress=False):
    if net_attr is None:                          return
    if measurement_list is None:                  return
    if model is None:                             return
    if (top_k < 1) or (top_p < 0) or (top_p > 1): return

    propagation_result = {}
    for i in range(0, len(measurement_list)):
        if progress: print(' -['+str(i+1)+'/'+str(len(measurement_list))+']:'+str(measurement_list[i]))
        if progress: start_time = time.time()

        node_initial = []
        if mode is 1: # Mode 1: initial nodes by top_k
            node_initial = retrieve_topk_nodes(net_attr, measurement_list[i], top_k)
        else:         # Mode 2: initial nodes by top_p
            num_initial_nodes = int(np.multiply(len(G.nodes()), top_p))
            node_initial      = retrieve_topk_nodes(net_attr, measurement_list[i], num_initial_nodes)

        # Propagate by node_initial
        result_key   = measurement_list[i]
        result_value = model.propagation(G, node_initial, NUM_ROUND, NUM_TIME_STEP, RATE_INFECTION, RATE_RECOVERY, progress=True)
        propagation_result[result_key] = result_value

        if progress: print('  -'+str(round(time.time() - start_time, 4))+' seconds')
    return propagation_result

def write_propagation_result(filename='', propagation_result=None):
    if filename        is ''     : return
    if propagation_result is None: return

    with open(filename, mode="w") as f:
        for i in sorted(propagation_result.keys()):
            f.write(str(i)+' ')
            for j in range(0, len(propagation_result[i])):
                f.write(str(propagation_result[i][j])+' ')
            f.write('\n')
        f.close

def draw_propagation_result(propagation_result, title, image_path='', image_show=False, image_save=False):
    if np.multiply(3, 3) < len(propagation_result.keys()): return # Return when plot size < length of propagation_result

    # Plot setting: position, size, title and so on
    fig = plt.figure(figsize=(PLOT_X_SIZE, PLOT_Y_SIZE), facecolor='w')
    fig.canvas.set_window_title(title)
    ax_cols = 9
    ax_rows = 9
    ax_main = plt.subplot2grid((ax_rows,ax_cols), (0,0),  colspan=9, rowspan=9)

    # Setting of main plot and sub-plots
    ax_main.grid()
    ax_main.set_title(title, fontdict={'fontsize': 12})
    ax_main.set_xlabel('time-step')
    ax_main.set_ylabel('% infected nodes')

    # Draw plots of propagation result:
    cm_index = 0
    legen_text  = []
    for i in sorted(propagation_result.keys()):
        # Draw main plot: avg_infected
        ax_main.plot(propagation_result[i], color=COLOR_LIST[cm_index]) #, marker=MARKER_LIST[cm_index], markersize=8, fillstyle='none')

        if i is 'node_mv17':
            method = 'proposed'
        else:
            method = i.split('_')[1]
        legen_text.append(method)
        cm_index += 1

    # Draw legend of main plot: loc=1 (ur), loc=2 (ul), loc=4 (lr), fontsize: medium, small, x-small
    ax_main.legend(legen_text, loc=4, fontsize='small')

    # Save and show the plot
    plt.tight_layout()
    if image_save: plt.savefig(image_path)
    if image_show: plt.show()
    plt.close(fig)

# ###
# 4.Main function
# ###
def main_function():
    total_time      = time.time()
    folder_edgelist = 'edgelist/'
    folder_file     = 'file/'
    folder_image    = 'image/'
    # file_name       = 'ca_astroph_gcc'     # N=17903,  E=196972,  MAX_CORE=56  ,v 1000, b=0.02, 0.025 0,03
    # file_name       = 'ca_condmat_gcc'     # N=21363,  E=91286,   MAX_CORE=25  ,v 1000, b=0.05, 0.08
    # file_name       = 'ca_grqc_gcc'        # N=4158,   E=13422,   MAX_CORE=43  ,v 1000, b=0.1, 0.13, 0.15
    # file_name       = 'ca_hepph_gcc'       # N=11204,  E=117619,  MAX_CORE=238 ,v 1000, b=0.02, 0.05
    # file_name       = 'ca_hepth_gcc'       # N=8638,   E=24806,   MAX_CORE=31  ,v 1000, b=0.1, 0.12, 0.13, 0.15
    # file_name       = 'email_contacts_gcc' # N=12625,  E=20362,   MAX_CORE=23  ,v 1000, b=0.03, 0.05
    # file_name       = 'email_enron_gcc'    # N=33696,  E=180811,  MAX_CORE=43  ,v 1000, b=0.05
    # file_name       = 'jazz_musicians_gcc' #                                   ,v 1000, b=0.02~0.05
    # file_name       = 'wiki_vote_gcc'      # N=7066,   E=100736,  MAX_CORE=53  , 1000, b=0.01, 0.02, 0.03
    #
    # file_name       = 'celegansneural_gcc' #                                   ,v 1000, b=0.06
    # file_name       = 'dolphins_gcc'       #                                   ,v 1000, b=0.15, 0.2
    # file_name       = 'lesmis_gcc'         #                                   ,v 1000, b=0.08
    # file_name       = 'netscience_gcc'     # N=379,    E=914,     MAX_CORE=8   ,v 1000, b=0.2~0.25
    file_name       = 'polblogs_gcc'       # N=1222,   E=16714,   MAX_CORE=36  ,v 1000, b=0.02

    print('1.Load edgelist of network.')
    start_time       = total_time
    network_edgelist = elrw.read_edge_list(folder_edgelist+file_name+'.txt')
    G = nx.parse_edgelist(network_edgelist, nodetype=int)
    print(' -', round(time.time() - start_time, 4), 'seconds')

    print('2.Read node attributes from the file: *.pickle file.')
    start_time   = time.time()
    network_attr = pkrw.read_pickle_file(folder_file+file_name+'-attr.pickle')
    print(' -', round(time.time() - start_time, 4), 'seconds')

    print("3.Propagation by top-k node of the measurement.")
    start_time         = time.time()
    measurement_list   = sorted(['node_degree', 'node_betweenness', 'node_closeness', 'node_k-core', 'node_neighbor-core', 'node_pagerank', 'node_mv17'])
    propagation_result = network_propagation(G, network_attr, measurement_list, sir, NUM_TOPK, NUM_TOPP, mode=1, progress=True)
    print(' -', round(time.time() - start_time, 4), 'seconds')

    print('4.Write propagation result to file.')
    start_time = time.time()
    parameters = ',net='+str(file_name)+',round='+str(NUM_ROUND)+',t='+str(NUM_TIME_STEP)+',topk='+str(NUM_TOPK)+',b='+str(RATE_INFECTION)+',r='+str(RATE_RECOVERY)
    propagate_path = folder_image+'propagation_result'+parameters+'.txt'
    write_propagation_result(propagate_path, propagation_result)
    print(' -', round(time.time() - start_time, 4), 'seconds')

    print("5.Draw and save figure of propagation result.")
    start_time = time.time()
    plot_title = '' # 'Result of network propagation: '+str(file_name)+'.'
    image_path = folder_image+'network_propagation'+parameters+'.png'
    draw_propagation_result(propagation_result, plot_title, image_path, image_save=True, image_show=False)
    print(' -', round(time.time() - start_time, 4), 'seconds')
    print('Done., total of run time:', round(time.time() - total_time, 4), 'seconds')

# ###
# 5.Run main function
# ###
if __name__ == '__main__': main_function()
