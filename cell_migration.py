import numpy as np

def cell_mig(seg, cell_idx, new_seg_cells, target_seg, polar_vect):
    """the logic of migration of single cell"""
    new_seg_cells[target_seg]['num'] += 1
    new_seg_cells[seg]['num'] -= 1  
    new_seg_cells[target_seg]['polarity'].append(polar_vect)
    new_seg_cells[seg]['polarity'].pop(cell_idx)
    return new_seg_cells

def cell_migration(seg, seg_cells, new_seg_cells, Q, branch_rule, branch_alpha=None, tau=None, P1_dict=None):
    """Agent model for cell migration in a segment"""
    cell_size = 10e-6  
    mchance = 1        

    if seg_cells[seg]['num'] == 0:
        return seg_cells, new_seg_cells

    ### reverse loop cells in seg
    for cell_idx in reversed(range(int(seg_cells[seg]['num']))):
        if np.random.rand() > mchance:
            continue

        polar_vect = seg_cells[seg]['polarity'][cell_idx]
        migrate_vect = cell_size * polar_vect
        target_seg = None

        ### migration condition base on segidx
        
        ### sepecific 0, 20, 19, 39
        if seg == 0:
            if migrate_vect[1] >= cell_size / 2:
                target_seg = seg + 1
            elif migrate_vect[1] <= -cell_size / 2:
                target_seg = 19

        elif seg == 20:
            if migrate_vect[1] >= cell_size / 2:
                target_seg = seg + 1
            elif migrate_vect[1] <= -cell_size / 2:
                target_seg = 4

        elif seg == 19:
            if migrate_vect[1] >= cell_size / 2:
                target_seg = seg - 1
            elif migrate_vect[1] <= -cell_size / 2:
                target_seg = 0

        elif seg == 39:
            if migrate_vect[1] >= cell_size / 2:
                target_seg = seg - 1
            elif migrate_vect[1] <= -cell_size / 2:
                target_seg = 15
        ### vertical segment1
        elif 1 <= seg <= 4 or 21 <= seg <= 24:
            if migrate_vect[1] >= cell_size / 2:
                target_seg = seg + 1
            elif migrate_vect[1] <= -cell_size / 2:
                target_seg = seg - 1
        ### horizontal
        elif 5 <= seg <= 14 or 25 <= seg <= 34:
            if migrate_vect[0] >= cell_size / 2:
                target_seg = seg + 1
            elif migrate_vect[0] <= -cell_size / 2:
                target_seg = seg - 1
        ### vertical section 2
        elif 16 <= seg <= 18 or 35 <= seg <= 38:
            if migrate_vect[1] >= cell_size / 2:
                target_seg = seg - 1
            elif migrate_vect[1] <= -cell_size / 2:
                target_seg = seg + 1

        ### bifuration: seg 15, 
        elif seg == 15:
            if migrate_vect[1] <= -cell_size / 2:
                target_seg = 16
            elif migrate_vect[1] >= cell_size / 2:
                
                ### branch decision rules match
                if branch_rule == 1: ### BR1: base on tau
                    target_seg = 14 if tau[14] >= tau[39] else 39
                elif branch_rule == 2: # BR2: bas on angle
                    target_seg = 39  # simplified, just move upward
                elif branch_rule == 3: ### BR3: same prob
                    target_seg = 14 if np.random.rand() < 0.5 else 39
                elif branch_rule == 4: ### BR4: 0.7 & 0.3
                    target_seg = 14 if np.random.rand() < 0.7 else 39
                
                elif branch_rule == 5: ### BR5: a combination of tau and flow
                    ### take the value
                    tau1 = tau[14]
                    tau2 = tau[39]
                    n1 = seg_cells[14].get('num', 0)  
                    n2 = seg_cells[39].get('num', 0)                   
                    ### calculation
                    tau_sum = tau1 + tau2
                    tau_ratio = tau1 / tau_sum if tau_sum != 0 else 0.5
                    n_sum = n1 + n2
                    n_ratio = n1 / n_sum if n_sum != 0 else 0.5
                    ### probability with weight
                    P1 = branch_alpha * tau_ratio + (1 - branch_alpha) * n_ratio
                    target_seg = 14 if np.random.rand() < P1 else 39
                
                ### conduct the migration base on target_seg
                new_seg_cells = cell_mig(seg, cell_idx, new_seg_cells, target_seg, polar_vect)
                continue  

        # conduct the migration base on target_seg
        if target_seg is not None:
            new_seg_cells = cell_mig(seg, cell_idx, new_seg_cells, target_seg, polar_vect)

    return seg_cells, new_seg_cells