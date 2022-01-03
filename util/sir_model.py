"""
SIR model
Crate on 2014/03/16
@auth: Yu-Hsiang Fu
"""
# ###
# 1.Import packages
# ###
import numpy  as np
import random as r
import sys

# ###
# 2.Define functions
# ###
def convert_susceptible_to_infected(G, node_susceptible, node_infected, rate_infection):
    target_list   = set(node_susceptible)
    infected_list = []
    for ni in node_infected:
        # Shuffle neighbor_list
        neighbor_list = G.neighbors(ni)
        np.random.shuffle(neighbor_list)

        # If neighbor is susceptible, then interact with it
        for nb in neighbor_list:
            if (nb in target_list) and (r.random() < rate_infection):
                infected_list.append(nb)
    return infected_list

def convert_infected_to_recovered(node_infected, rate_recovery):
    recovery_list = []
    if rate_recovery is 1: # Case 1: all infected nodes are recovered
        recovery_list = list(node_infected)
    else:                  # Case 2: recover infected nodes by rate_recovery
        for ni in node_infected:
            if (r.random() < rate_recovery):
                recovery_list.append(ni)
    return recovery_list

def propagation(G, initial_nodes, num_round=1000, num_time_step=100, rate_infection=0.1, rate_recovery=1, progress=False):
    # Check parameters of propagation fuction
    if not initial_nodes:                            return
    if num_round < 1:                                return
    if num_time_step < 1:                            return
    if (rate_infection < 0) or (rate_infection > 1): return
    if (rate_recovery < 0)  or (rate_recovery > 1):  return

    # Compute proportion of infected nodes of each by num_round
    num_time_step +=1
    round_density = [0] * num_time_step
    for i in range(0, num_round):
        node_susceptible = list(G.nodes()) # S
        node_infected    = []              # I
        node_recovered   = []              # R
        for t in range(0, num_time_step):
            current_infected = []
            current_recovery = []
            if t is 0: # Case 1: I = I + Initial nodes
                node_infected.extend(list(initial_nodes))
                node_susceptible = list(set(node_susceptible) - set(node_infected)) # S = S - I
            else:      # Case 2: S -> I by rate_infection, I -> R by rate_recovery
                current_infected = convert_susceptible_to_infected(G, node_susceptible, node_infected, rate_infection) # S -> I
                current_recovery = convert_infected_to_recovered(node_infected, rate_recovery)                         # I -> R

                # Modify lists of node_susceptible (S), node_infected (I) and node_recovered (R)
                node_recovered.extend(current_recovery)                                # R = R + current_recovery
                node_infected.extend(current_infected)                                 # I = I + current_infected
                node_infected    = list(set(node_infected) - set(current_recovery))    # I = I - current_recovery
                node_susceptible = list(set(node_susceptible) - set(current_infected)) # S = S - current_infected

            # Add recovery (or infected) nodes of each time t: p(t) += R(t)
            round_density[t] += len(node_recovered)

        # Show progress
        progress_interval = int(num_round/10) if num_round > 10 else 1
        if progress and i is 0: sys.stdout.write('  -Infection rate = {0:<4}'.format(rate_infection)+', Round: '+str(i+1))
        if progress and (int((i+1) % progress_interval) is 0) and (i is not 0): sys.stdout.write(','+str(i+1))
        if progress: sys.stdout.flush()
    if progress: print('.')

    # Compute average infected nodes: I/N, R/N or (I+R)/N
    round_density = list(np.divide(round_density, np.multiply(num_round, len(G.nodes()))))
    return round_density
