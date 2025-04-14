# Agent-Based Model of Flow-Mediated Angiogenic Bifurcation Remodeling

This mini-project implements an agent-based model (ABM) to simulate endothelial cell (EC) migration and vascular network remodeling during angiogenesis, focusing on bifurcation stability under hemodynamic forces. The model replicates key findings from Edgar et al. (2021), exploring how shear stress and cell collective behavior influence vascular hierarchy.

---

## Code Structure
### Core Modules:
1. **`abm_ec_simulation.py`**  
   - Main driver script  
   - Initializes parameters, runs simulation loop, and coordinates data collection  
   - Calls visualization and physics modules  

2. **`cell_migration.py`**  
   - Implements cell migration logic across vessel segments  
   - Handles 5 bifurcation rules (BR1–BR5):  
     - **BR1**: Shear stress-based selection  
     - **BR2**: Minimal directional change  
     - **BR3**: Random selection (50/50)  
     - **BR4**: Probabilistic bias (70/30)  
     - **BR5**: Hybrid mechanism (α-weighted shear stress + cell count)  

3. **`make_segments.py`**  
   - Generates bifurcated vascular network geometry  
   - Defines coordinates for feeding/draining vessels and branches  

4. **`plot_network.py`**  
   - Visualizes vessel network with:  
     - Diameter-scaled segments  
     - Flow direction (red/blue)  
     - Cell polarity vectors  

5. **`plot_time.py`**  
   - Plots dynamic metrics:  
     - Proximal vs. distal diameter/shear stress/cell count  
     - Branch selection probability (BR5)  

6. **`realign_polarity.py`**  
   - Updates EC polarity vectors using:  
     - Flow alignment (w₂)  
     - Neighbor alignment (w₃)  
     - Random component (w₄)  

7. **`solve_for_flow.py`**  
   - Solves pressure/flow using Hagen-Poiseuille equation  
   - Computes shear stress (τ) via nodal balance equations  

---

## Key Features
- **Dynamic Coupling**: Cell migration directly impacts lumen diameter, which feeds back into hemodynamic calculations.
- **Agent-based**
- **Branch Stability Analysis**: BR5 reveals competitive oscillations between shear stress and collective cues.  
- **Visualization Suite**: Network topology + time-series metrics (20-step intervals).  

---

## Simulation Parameters
### BR 1-4
| Parameter          | Value               | Description                          |
|---------------------|---------------------|--------------------------------------|
| `Nt`               | 80                  | Total simulation steps               |
| `Pin`              | 196 Pa              | Inlet pressure                       |
| `Pout`             | 0 Pa                | Outlet pressure                      |
| `mu`               | 3.5e-3 Pa·s         | Blood viscosity                      |
| `cell_size`        | 5e-6 m              | EC width                             |
| `branch_rule`      | 1~4                 | Active bifurcation rule (1–5)        |
| `branch_alpha`     | 0.45                | Shear stress weight in BR5           |
| `w1/w2/w3/w4`      | 0/1/0/0             | Polarity alignment weights           |
### BR5
| Parameter          | Value               | Description                          |
|---------------------|---------------------|--------------------------------------|
| `Nt`               | 80                  | Total simulation steps               |
| `Pin`              | 196 Pa              | Inlet pressure                       |
| `Pout`             | 0 Pa                | Outlet pressure                      |
| `mu`               | 3.5e-3 Pa·s         | Blood viscosity                      |
| `cell_size`        | 5e-6 m              | EC width                             |
| `branch_rule`      | 5                   | Active bifurcation rule (1–5)        |
| `branch_alpha`     | 0.45                | Shear stress weight in BR5           |
| `w1/w2/w3/w4`      | 0.3/0.5/0.1/0.1     | Polarity alignment weights           |

- **Random Seed**: `np.random.seed(123)` ensures reproducibility.  

## Requirements  
- Python 3.8+  
- NumPy, Matplotlib  

Run:  
```bash
python abm_ec_simulation.py
