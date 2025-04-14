import numpy as np
import matplotlib

import matplotlib.pyplot as plt
plt.style.use('seaborn-v0_8')


def plot_analysis(data):
    """plot the dynamic key factors that changes with time"""
    fig, axs = plt.subplots(2, 2, figsize=(8, 6))
    
    
    ### diameter comparision
    proximal_um = np.array(data['proximal_diameter']) * 1e5
    distal_um = np.array(data['distal_diameter']) * 1e5
    
    axs[0,1].plot(data['time'], proximal_um, label='Proximal', lw=2)
    axs[0,1].plot(data['time'], distal_um, label='Distal', lw=2)
    axs[0,1].set_title('Diameter Comparison')
    axs[0,1].set_xlabel('Time (steps)')
    axs[0,1].set_ylabel('Diameter (μm)')
    axs[0,1].set_ylim(0.0, 5.0)
    axs[0,1].set_yticks(np.arange(0, 5.1, 1))
    axs[0,1].legend()
    
    # branch probability (BR5)
    if 'branch_prob' in data and data['branch_prob']:
        prob = np.array(data['branch_prob'])
        axs[0,0].plot(data['time'], prob[:,0], label='P(Proximal)', color='blue', ls='--')
        axs[0,0].plot(data['time'], prob[:,1], label='P(Distal)', color='red', ls='--')
        axs[0,0].set_title('Branch Selection Probability')
        axs[0,0].set_ylabel('Probability')
        axs[0,0].set_xlabel('Time (steps)')
        axs[0,0].set_ylim(0.0, 1.0)
        axs[0,0].legend()
        

        ### proximal and distal tau~num
        ax1 = axs[1,0]
        color = 'tab:red'
        ax1.set_xlabel('Time Step')
        ax1.set_ylabel('Shear Stress (Pa)', color=color)
        ax1.plot(data['time'], data['proximal_tau'], color=color, lw=2, label='Proximal Tau')
        ax1.tick_params(axis='y', labelcolor=color)
        ax1_r = ax1.twinx()  
        color = 'tab:blue'
        ax1_r.set_ylabel('Cell Count', color=color)
        ax1_r.plot(data['time'], data['proximal_cells'], color=color, lw=2, linestyle='--', label='Proximal Cells')
        ax1_r.tick_params(axis='y', labelcolor=color)
        ax1.set_title('Proximal Branch: Shear Stress vs Cell Count')
        ax1.grid(True)

        ### distal 
        ax2 = axs[1,1]
        color = 'tab:green'
        ax2.set_xlabel('Time Step')
        ax2.set_ylabel('Shear Stress (Pa)', color=color)
        ax2.plot(data['time'], data['distal_tau'], color=color, lw=2, label='Distal Tau')
        ax2.tick_params(axis='y', labelcolor=color)
        
        ax2_r = ax2.twinx()
        color = 'tab:blue'
        ax2_r.set_ylabel('Cell Count', color=color) 
        ax2_r.plot(data['time'], data['distal_cells'], color=color, lw=2, linestyle='--', label='Distal Cells')
        ax2_r.tick_params(axis='y', labelcolor=color)
        
        ax2.set_title('Distal Branch: Shear Stress vs Cell Count')
        ax2.grid(True)

    else:
        ### tau comparision 
        axs[1,0].plot(data['time'], data['proximal_tau'], label='Proximal', lw=2)
        axs[1,0].plot(data['time'], data['distal_tau'], label='Distal', lw=2)
        axs[1,0].set_title('Shear Stress Comparison')
        axs[1,0].set_xlabel('Time (steps)')
        axs[1,0].set_ylabel('Shear Stress (Pa)')
        axs[1,0].legend()
        
        ### cell num
        axs[1,1].plot(data['time'], data['proximal_cells'], label='Proximal', lw=2)
        axs[1,1].plot(data['time'], data['distal_cells'], label='Distal', lw=2)
        axs[1,1].set_title('Cell Number Comparison')
        axs[1,1].set_ylabel('Cell Count')
        axs[1,1].legend()
    
    plt.subplots_adjust(wspace=0.35, hspace=0.4)  ### set the formation of the graph

    plt.tight_layout()
    plt.show(block=True)


if __name__ == "__main__":
    ### test case
    test_data = {
        'time': range(40),
        'proximal_flow': np.random.rand(40),
        'distal_flow': np.random.rand(40),
        'proximal_diameter': np.linspace(5, 20, 40),
        'distal_diameter': np.linspace(20, 5, 40),
        'proximal_tau': np.abs(np.random.normal(1, 0.2, 40)),
        'distal_tau': np.abs(np.random.normal(0.8, 0.3, 40)),
        'proximal_cells': np.random.randint(5, 15, 40),
        'distal_cells': np.random.randint(5, 15, 40)
    }
    plot_analysis(test_data) 
    print("version", matplotlib.__version__)