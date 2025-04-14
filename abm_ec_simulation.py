import numpy as np
import matplotlib.pyplot as plt
from solve_for_flow import solve_for_flow
from cell_migration import cell_migration
from realign_polarity import realign_polarity
from plot_network import plot_network
from plot_time import plot_analysis
from make_segments import make_segments
import copy

# Set random seed for reproducibility
np.random.seed(123)

# Input parameters
Nt = 80  # Number of time steps
Pin = 2 * 98  # Inlet pressure (Pa)
Pout = 0 * 98  # Outlet pressure (Pa)

mu = 3.5e-3  # Dynamic viscosity of blood (Pa-s)
Nn = 40  # Number of nodes
Nseg = 40  # Number of segments
num_cell = 10  # Initial number of cells per segment
cell_size = 5e-6  # Size of each cell (m)

branch_rule = 5  # Branching rule - new
branch_alpha = 0.45  # Branching parameter

# Polarization re-alignment weights
w2 = 0.5  # Flow component weight
w3 = 0.1  # Neighbor re-alignment weight
w4 = 0.1  # Random re-alignment weight
w1 = 1 - w2 - w3 - w4  # Persistence component

# Initialize segment properties
L = np.ones(Nseg) * 10e-6  # Segment lengths (m)
Ncell = np.ones(Nseg) * num_cell  # Segment cell number array
D = np.zeros(Nseg)  # Segment diameters (m)
G = np.zeros(Nseg)  # Segment conductance array (m^4/Pa-s-m)
H = np.zeros(Nseg)  # Shear stress calculation factor



tau = np.zeros(Nseg)  # Shear stress array
segments = make_segments(L)  # Generate segment structure

### data storage for ploting 
analysis_data = {
    'time': [],
    'proximal_flow': [],
    'distal_flow': [],
    'proximal_diameter': [],
    'distal_diameter': [],
    'proximal_tau': [],
    'distal_tau': [],
    'proximal_cells': [],
    'distal_cells': [],
    'branch_prob': [],
}

# Initialize segment cell structures
def initialize_segments(Nseg, num_cell):
    seg_cells = [{} for _ in range(Nseg)]
    for seg in range(Nseg):
        seg_cells[seg]['num'] = int(num_cell)  # Number of cells
        seg_cells[seg]['polarity'] = [np.random.randn(2) for _ in range(num_cell)]  # Random polarity vectors
        for v in seg_cells[seg]['polarity']:
            v /= np.linalg.norm(v)  # Normalize to unit vectors
        seg_cells[seg]['migration'] = np.zeros(num_cell)  # Migration indicator
    return seg_cells

seg_cells = initialize_segments(Nseg, num_cell)

# Compute initial segment conductance and shear stress
def compute_conductance(Nseg, Ncell, cell_size, mu, L):
    D = np.zeros(Nseg)
    G = np.zeros(Nseg)
    H = np.zeros(Nseg)
    for seg in range(Nseg):
        if Ncell[seg] >= 1:
            D[seg] = Ncell[seg] * cell_size / np.pi
        else:
            D[seg] = 0
        G[seg] = (np.pi * D[seg]**4) / (128 * mu * L[seg])
        if D[seg] != 0:
            H[seg] = (32 * mu) / (np.pi * D[seg]**3)
    return D, G, H




D, G, H = compute_conductance(Nseg, Ncell, cell_size, mu, L)

# Solve for initial flow
P, Q, tau = solve_for_flow(G, Pin, Pout, H)
### print (tau)
# plot_network(segments, D, P, Q, seg_cells, tau)

# Time stepping for migration process
# P1_dict = []
for t in range(Nt):
    if (t + 1) % 20 == 0:
        print(f'Time step {t+1}/{Nt}')
    
    migrate = np.zeros(Nseg)
    
    new_seg_cells = copy.deepcopy(seg_cells)
    
    for seg in range(Nseg):
        seg_cells, new_seg_cells = realign_polarity(seg, Q, seg_cells, new_seg_cells, w1, w2, w3, w4)
        seg_cells, new_seg_cells = cell_migration(seg, seg_cells, new_seg_cells, Q, branch_rule, branch_alpha, tau)
    
    seg_cells = copy.deepcopy(new_seg_cells)
    
    ### Update Ncell
    for seg in range(Nseg):
        Ncell[seg] = seg_cells[seg]['num']
    
    # Update conductance and shear stress
    D, G, H = compute_conductance(Nseg, Ncell, cell_size, mu, L)
    
    # Solve for flow with updated parameters
    P, Q, tau = solve_for_flow(G, Pin, Pout, H)

    ### data collection
    analysis_data['time'].append(t)
    ### set the range of proximal and distal vessels
    proximal_segs = range(5, 15)
    distal_segs = range(25, 35)
    analysis_data['proximal_flow'].append(np.mean(Q[proximal_segs]))
    analysis_data['distal_flow'].append(np.mean(Q[distal_segs]))
    analysis_data['proximal_diameter'].append(np.mean(D[proximal_segs]))
    analysis_data['distal_diameter'].append(np.mean(D[distal_segs]))
    analysis_data['proximal_tau'].append(np.mean(tau[proximal_segs]))
    analysis_data['distal_tau'].append(np.mean(tau[distal_segs]))
    analysis_data['proximal_cells'].append(np.mean(Ncell[proximal_segs]))
    analysis_data['distal_cells'].append(np.mean(Ncell[distal_segs]))

    ### record the prob at bifur, BR5
    if branch_rule == 5:
        seg1, seg2 = 0, 20  #
        P1 = branch_alpha * (tau[seg1]/(tau[seg1]+tau[seg2])) + (1-branch_alpha)*(Ncell[seg1]/(Ncell[seg1]+Ncell[seg2]))
        analysis_data['branch_prob'].append((P1, 1-P1))

    # Plot only every 20 time steps
    if (t + 1) % 20 == 0:
        plot_network(segments, D, P, Q, seg_cells, tau)

### plot the time dynamics after loop
plot_analysis(analysis_data)

#### option save the data
# np.savez('simulation_data.npz', **analysis_data)
