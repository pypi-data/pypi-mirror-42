from __future__ import division
from __future__ import absolute_import

import mpi4py
mpi4py.rc.recv_mprobe = False # Disable matching probes
from mpi4py import MPI
import sys, os        
import numpy as np

USE_BALSAM = False

from forces_simf import run_forces # From current dir

# Import libEnsemble modules
from libensemble.libE import libE
from libensemble.gen_funcs.uniform_sampling import uniform_random_sample

# Get this script name (for output at end)
script_name = os.path.splitext(os.path.basename(__file__))[0]

sim_app = os.path.join(os.getcwd(),'forces.x')
#print('sim_app is ',sim_app)

# Normally would be pre-compiled
if not os.path.isfile('forces.x'):
    if os.path.isfile('build_forces.sh'):
        import subprocess
        subprocess.check_call(['./build_forces.sh'])
        
# Normally the sim_dir will exist with common input which is copied for each worker. Here it starts empty.
# Create if no ./sim dir. See sim_specs['sim_dir']
if not os.path.isdir('./sim'):
    os.mkdir('./sim')

#Create job_controller and register sim to it.
if USE_BALSAM:
    from libensemble.balsam_controller import BalsamJobController
    jobctrl = BalsamJobController()    
else:
    from libensemble.mpi_controller import MPIJobController
    jobctrl = MPIJobController()
jobctrl.register_calc(full_path=sim_app, calc_type='sim')


#todo - clarify difference sim 'in' and 'keys'

#State the objective function, its arguments, output, and necessary parameters (and their sizes)
sim_specs = {'sim_f': run_forces,           # This is the function whose output is being minimized (sim func)
             'in': ['x'],                   # Name of input data structure for sim func
             'out': [                       # Output from sim func
                     ('energy',float), 
                    ],
             'keys': ['seed'],              # Key/keys for input data
             'sim_dir': './sim',            # Simulation input dir to be copied for each worker (*currently empty)
             'simdir_basename': 'forces',   # User attribute to name sim directories (forces_***)
             'cores': 2,                    # User attribute to set number of cores for sim func runs (optional)
             'sim_particles': 1e3,          # User attribute for number of particles in simulations
             'sim_timesteps': 5,            # User attribute for number of timesteps in simulations             
             'sim_kill_minutes': 10.0       # User attribute for max time for simulations
             }
             
# State the generating function, its arguments, output, and necessary parameters.
gen_specs = {'gen_f': uniform_random_sample,# Generator function
             'in': ['sim_id'],              # Generator input
             'out': [('x',float,(1,))],     # Name, type and size of data produced (must match sim_specs 'in')
             'lb': np.array([0]),           # List of lower bounds for random sample array (1D)
             'ub': np.array([32767]),       # List of upper bounds for random sample array (1D) 
             'gen_batch_size': 1000,        # How many random samples to generate in one call
             'batch_mode': True,            # If true wait for sims to process before generate more
             'num_active_gens':1,           # Only one active generator at a time.
             'save_every_k': 1000           # Save every K steps
             }

# Maximum number of simulations
sim_max = 5
exit_criteria = {'sim_max': sim_max}

# Create a different random number stream for each worker (used by uniform_random_sample)
np.random.seed(1)
persis_info = {}
for i in range(MPI.COMM_WORLD.Get_size()):
    persis_info[i] = {'rand_stream': np.random.RandomState(i)}

H, persis_info, flag = libE(sim_specs, gen_specs, exit_criteria, persis_info=persis_info)

#Save results to numpy file
if MPI.COMM_WORLD.Get_rank() == 0:
    short_name = script_name.split("test_", 1).pop()
    filename = short_name + '_results_History_length=' + str(len(H)) + '_evals=' + str(sum(H['returned']))
    print("\n\nRun completed.\nSaving results to file: " + filename)
    np.save(filename, H)

