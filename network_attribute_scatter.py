"""
Network attribute scatter
Crate: 2014/03/17
Check: 2016/05/01
@auth: Yu-Hsiang Fu
"""
# ###
# 1.Import packages
# ###
import matplotlib.pyplot as plt
import numpy             as np
# import random            as r
import time
import sys
# from  mpl_toolkits.axes_grid1 import make_axes_locatable

# Import modules
import util.read_write_pickle    as pkrw

# ###
# 2.Const variables
# ###
# Plo
COLOR_MAP         = plt.cm.bwr_r
PLOT_DISPLAY_AXIS = [-0.05, 1.05, -0.05, 1.05] # [x_min, x_max, y_min, y_max]
PLOT_NUM_SAMPLE   = 1000
PLOT_MARKER_SIZE  = 10
PLOT_MARKER_ALPHA = 0.5
PLOT_NUM_COLS     = 5
PLOT_NUM_ROWS     = 1
PLOT_X_SIZE       = 15
PLOT_Y_SIZE       = 3
PLOT_DPI          = 1200
PLOT_FORMAT       = 'png'
# PLOT_FORMAT       = 'eps'

# ###
# 3.Define functions
# ###
def draw_plot(ax, net_attr, net_sample, attr_x, attr_y):
    # Data of scatter: calculate by using full data
    scatter_x = [net_attr[n][attr_x] for n in net_attr.keys()]
    scatter_y = [net_attr[n][attr_y] for n in net_attr.keys()]
    cc_z      = np.round(np.corrcoef(scatter_x, scatter_y)[0][1], 4)
    # max_x     = (max(scatter_x)+1) if max(scatter_x) > 1 else 1.01
    # max_y     = (max(scatter_y)+1) if max(scatter_y) > 1 else 1.01
    max_x     = max(scatter_x) + 0.01
    max_y     = max(scatter_y) + 0.01

    # Sample data of scatter: drawing scatter by using net_sample
    # sample_x  = [net_attr[n][attr_x] for n in net_sample]
    # sample_y  = [net_attr[n][attr_y] for n in net_sample]
    # sample_z  = np.multiply(np.ones(len(net_sample)), cc_z)

    # Change x-y axis name
    # x-axis
    if attr_x == 'node_k-core-entropy':
        attr_x = 'global diversity Ei'
    elif attr_x == 'node_neighbor-degree':
        attr_x = 'local features Li'
    # y-axis
    if attr_y == 'node_k-core-entropy':
        attr_y = 'global diversity Ei'
    elif attr_y == 'node_neighbor-degree':
        attr_y = 'local features Li'
    elif attr_y == 'node_closeness':
        attr_y = 'closeness'
    elif attr_y == 'node_k-core':
        attr_y = 'k-shell index'
    elif attr_y == 'node_neighbor-core':
        attr_y = 'coreness'

    # Set and draw scatter
    PLOT_DISPLAY_AXIS = [-0.01, max_x, -0.01, max_y]
    ax.axis(PLOT_DISPLAY_AXIS)
    ax.tick_params(axis='both', labelsize=8)
    ax.set_xlabel(attr_x, fontdict={'fontsize': 10})
    ax.set_ylabel(attr_y, fontdict={'fontsize': 10})
    ax.set_title('correlation coefficient: '+str(cc_z), fontdict={'fontsize': 10})
    ax.scatter(scatter_x, scatter_y, s=PLOT_MARKER_SIZE, marker='+', c='b', alpha=PLOT_MARKER_ALPHA)

def draw_attribute_scatter(net_attr, attr_list, title, image_name='', image_save=False, image_show=False):
    if net_attr  is None: return
    if attr_list is None: return

    # Plot setting: position, size, title and so on
    fig, axes = plt.subplots(nrows=PLOT_NUM_ROWS, ncols=PLOT_NUM_COLS, figsize=(PLOT_X_SIZE, PLOT_Y_SIZE), facecolor='w')
    fig.canvas.set_window_title(title)

    # Draw sub-plots of attributes
    # num_sample = PLOT_NUM_SAMPLE if len(net_attr.keys()) >= PLOT_NUM_SAMPLE else len(net_attr.keys())
    # net_sample = r.sample(sorted(net_attr.keys()), num_sample)
    net_sample = net_attr.keys()

    for i in range(0, len(attr_list)):
        draw_plot(axes[i], net_attr, net_sample, attr_list[i][0], attr_list[i][1])

    # Save and show the plot
    plt.tight_layout()
    if image_save: plt.savefig(image_name, dpi=PLOT_DPI, format=PLOT_FORMAT, bbox_inches='tight', pad_inches=0.02)
    if image_show: plt.show()
    plt.close(fig)

# ###
# 4.Main function: read umsgpack file of network and draw plot of result
# ###
def main_function():
    total_time   = time.time()
    folder_file  = 'file/'
    folder_image = 'image/'
    # file_name       = 'ca_astroph_gcc'        # N=17903,  E=196972,  MAX_CORE=56
    # file_name       = 'ca_condmat_gcc'        # N=21363,  E=91286,   MAX_CORE=25
    # file_name       = 'ca_grqc_gcc'           # N=4158,   E=13422,   MAX_CORE=43
    # file_name       = 'ca_hepph_gcc'          # N=11204,  E=117619,  MAX_CORE=238
    file_name       = 'ca_hepth_gcc'          # N=8638,   E=24806,   MAX_CORE=31
    # file_name       = 'email_contacts_gcc'    # N=12625,  E=20362,   MAX_CORE=23
    # file_name       = 'email_enron_gcc'       # N=33696,  E=180811,  MAX_CORE=43
    # file_name       = 'jazz_musicians_gcc'    #
    #
    # file_name       = 'celegansneural_gcc'    #
    # file_name       = 'dolphins_gcc'          #
    # file_name       = 'lesmis_gcc'            #
    # file_name       = 'netscience_gcc'        # N=379,    E=914,     MAX_CORE=8
    # file_name       = 'polblogs_gcc'          # N=1222,   E=16714,   MAX_CORE=36

    print('1.Read network attributes from the file: *.pickle file.')
    start_time   = total_time
    network_attr = pkrw.read_pickle_file(folder_file+file_name+'-attr.pickle')
    print(' -', round(time.time() - start_time, 4), 'seconds')

    print("2.Draw and save network attribute scatter.")
    start_time = time.time()
    attr_list = [('node_k-core-entropy', 'node_k-core'),            # Ei vs k-core
                 ('node_k-core-entropy', 'node_closeness'),         # Ei vs closeness
                 ('node_neighbor-degree', 'node_closeness'),        # Li vs closeness
                 ('node_neighbor-degree', 'node_neighbor-core'),    # Li vs coreness
                 ('node_k-core-entropy', 'node_neighbor-degree')]   # Ei vs Li
    plot_title = 'Analysis of node attributes:'
    image_name = folder_image+'network_attribute_scatter_net='+file_name+'.png'
    draw_attribute_scatter(network_attr, attr_list, plot_title, image_name, image_save=True, image_show=False)
    print(' -', round(time.time() - start_time, 4), 'seconds')
    print('Done., total of run time:', round(time.time() - total_time, 4), 'seconds')

# ###
# 5.Run main function for testing or useing
# ###
if __name__ == '__main__': main_function()
