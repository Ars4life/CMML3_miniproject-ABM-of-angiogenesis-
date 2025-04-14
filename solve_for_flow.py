import numpy as np

def solve_for_flow(G, Pin, Pout, H=None):
    """Solve for flow in the bifurcating vessel network."""
    Nn = 40  # Number of nodes
    Nseg = 40  # Number of segments

    # Set very small values for zero conductance to avoid singular matrix errors
    G[G == 0] = 1e-25
    
    # Initialize matrices
    P = np.zeros(Nn)  # Nodal pressure array (Pa)
    Q = np.zeros(Nseg)  # Segment flow array (m^3/s)
    C = np.zeros((Nn, Nn))  # Conductance matrix
    B = np.zeros(Nn)  # Solution vector
    
    
    ## Set equations for internal nodes
    for seg in range(Nn):
        if seg == 0:
            C[seg, seg] = G[0] * 1
            B[seg] = G[0] * Pin
        if 1 <= seg <= 19 or 22 <= seg <= 38:
            C[seg, seg - 1] = -G[seg - 1]
            C[seg, seg] = G[seg - 1] + G[seg]
            C[seg, seg + 1] = -G[seg]
        if seg == 20:
        # Set equation for last node
            C[20, 20] = G[19] * 1
            B[20] = G[19] * Pout
        if seg == 21:
            C[21, 5] = -G[20]
            C[21, 21] = G[20] + G[21]
            C[21, 22] = -G[21]
        if seg == 39:
            C[39, 38] = -G[38]
            C[39, 39] = G[38] + G[39]
            C[39, 15] = -G[39]
    
    # Solve for pressure
    P = np.linalg.solve(C, B)
    
    for seg in range(Nseg):
        if seg <= 19 or 21 <= seg <= 38:  
            Q[seg] = -G[seg] * (P[seg + 1] - P[seg])
        elif seg == 20:
            Q[seg] = -G[seg] * (P[seg + 1] - P[4])
        elif seg == 39:
            Q[seg] = -G[seg] * (P[15] - P[seg])
        
    

    # Compute shear stress if H is provided
    if H is not None:
        tau = H * Q
        return P, Q, tau
    else:
        return P, Q

