"""
Experiment1: draw plot only
Crate: 2014/03/29
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
# import util.sir_model            as sir
# import util.read_write_edgelist  as elrw
# import util.read_write_pickle    as pkrw

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
PLOT_X_SIZE = 2.5
PLOT_Y_SIZE = 2.5
PLOT_DPI    = 1200
# PLOT_FORMAT = 'png'
PLOT_FORMAT = 'eps'

# ###
# 3.Define functions
# ###
def read_propagation_result(filename=''):
    if filename is '': return

    # Read file
    propagation_result = {}
    with open(filename, mode="r") as f:
        for line in f:
            # Split string
            content = line.strip().split(' ')
            key     = content[0]
            value   = content[1:len(content)]
            # Add to dict
            propagation_result[key] = value
        f.close()
    return propagation_result

def draw_propagation_result(propagation_result, title, image_name='', image_show=False, image_save=False):
    if np.multiply(3, 3) < len(propagation_result.keys()): return # Return when plot size < length of propagation_result

    # Plot setting: position, size, title and so on
    # fig, = plt.figure(figsize=(PLOT_X_SIZE, PLOT_Y_SIZE), facecolor='w')
    # fig.canvas.set_window_title(title)
    # ax_cols = 1
    # ax_rows = 1
    # ax_main = plt.subplot2grid((ax_rows,ax_cols), (0,0),  colspan=1, rowspan=1)
    fig, ax_main = plt.subplots(figsize=(PLOT_X_SIZE, PLOT_Y_SIZE), facecolor='w')
    fig.canvas.set_window_title(title)

    # Setting of main plot and sub-plots
    ax_main.grid()
    ax_main.set_title(title,               fontdict={'fontsize': 8})
    ax_main.set_xlabel('time-step',        fontdict={'fontsize': 8})
    ax_main.set_ylabel('% infected-nodes', fontdict={'fontsize': 8})
    ax_main.tick_params(axis='both', which='major', labelsize=8)
    ax_main.tick_params(axis='both', which='minor', labelsize=8)

    # Draw plots of propagation result:
    cm_index = 0
    legen_text  = []
    for i in sorted(propagation_result.keys()):
        # Draw main plot: avg_infected
        ax_main.plot(propagation_result[i], color=COLOR_LIST[cm_index], linewidth=2) #, marker=MARKER_LIST[cm_index], markersize=8, fillstyle='none')

        if i == 'node_mv17':
            method = 'proposed'
        else:
            method = i.split('_')[1]
        legen_text.append(method)
        cm_index += 1

    # Draw legend of main plot: loc=1 (ur), loc=2 (ul), loc=4 (lr), fontsize: medium, small, x-small
    # ax_main.legend(legen_text, loc=4, fontsize='medium', prop={'size':6}) # fig size = 2.5, it's doesn't need legend

    # Save and show the plot
    plt.tight_layout()
    # if image_save: plt.savefig(image_name, dpi=PLOT_DPI)
    if image_save: plt.savefig(image_name, dpi=PLOT_DPI, format=PLOT_FORMAT, bbox_inches='tight', pad_inches=0.02)
    if image_show: plt.show()
    plt.close(fig)

# ###
# 4.Main function
# ###
def main_function():
    total_time   = time.time()
    folder_file  = 'file/'
    folder_image = 'image/'
    # file_name    = 'propagation_result,net=ca_astroph_gcc,round=1000,t=50,topk=1,b=0.03,r=1'
    # file_name    = 'propagation_result,net=ca_condmat_gcc,round=1000,t=50,topk=1,b=0.05,r=1'
    # file_name    = 'propagation_result,net=ca_grqc_gcc,round=1000,t=50,topk=1,b=0.15,r=1'
    # file_name    = 'propagation_result,net=ca_hepph_gcc,round=1000,t=50,topk=1,b=0.05,r=1'
    # file_name    = 'propagation_result,net=ca_hepth_gcc,round=1000,t=50,topk=1,b=0.12,r=1'
    # file_name    = 'propagation_result,net=celegansneural_gcc,round=1000,t=50,topk=1,b=0.06,r=1'
    # file_name    = 'propagation_result,net=dolphins_gcc,round=1000,t=50,topk=1,b=0.15,r=1'
    # file_name    = 'propagation_result,net=email_contacts_gcc,round=1000,t=50,topk=1,b=0.05,r=1'
    # file_name    = 'propagation_result,net=email_enron_gcc,round=1000,t=50,topk=1,b=0.05,r=1'
    # file_name    = 'propagation_result,net=jazz_musicians_gcc,round=1000,t=50,topk=1,b=0.04,r=1'
    # file_name    = 'propagation_result,net=lesmis_gcc,round=1000,t=50,topk=1,b=0.08,r=1'
    # file_name    = 'propagation_result,net=netscience_gcc,round=1000,t=50,topk=1,b=0.2,r=1'
    file_name    = 'propagation_result,net=polblogs_gcc,round=1000,t=50,topk=1,b=0.02,r=1'

    print('1.Read propagation result from file.')
    start_time = time.time()
    propagation_result = read_propagation_result(folder_image+file_name+'.txt')
    print(' -', round(time.time() - start_time, 4), 'seconds')

    print("2.Draw and save figure of propagation result.")
    start_time = time.time()
    plot_title = '' # 'Result of network propagation: '+str(file_name)+'.'
    image_name = folder_image+file_name+'.'+PLOT_FORMAT
    draw_propagation_result(propagation_result, plot_title, image_name, image_save=False, image_show=True)
    print(' -', round(time.time() - start_time, 4), 'seconds')
    print('Done., total of run time:', round(time.time() - total_time, 4), 'seconds')

# ###
# 5.Run main function
# ###
if __name__ == '__main__': main_function()
