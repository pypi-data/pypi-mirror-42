from __future__ import division
from __future__ import absolute_import

from mpi4py import MPI # for libE communicator
import sys, os             # for adding to path
import numpy as np

# Import libEnsemble modules
from libensemble.libE import libE
from libensemble.sim_funcs.job_control_hworld import job_control_hworld
from libensemble.gen_funcs.uniform_sampling import uniform_random_sample
from libensemble.controller import JobController
from libensemble.calc_info import CalcInfo
from libensemble.resources import Resources
from libensemble.message_numbers import *

USE_BALSAM = False

def build_simfunc():
    import subprocess

    #Build simfunc
    #buildstring='mpif90 -o my_simjob.x my_simjob.f90' # On cray need to use ftn
    buildstring='mpicc -o my_simjob.x ../unit_tests/simdir/my_simjob.c'
    #subprocess.run(buildstring.split(),check=True) #Python3.5+
    subprocess.check_call(buildstring.split())

script_name = os.path.splitext(os.path.basename(__file__))[0]
short_name = script_name.split("test_", 1).pop()

NCORES = 1
sim_app = './my_simjob.x'
if not os.path.isfile(sim_app):
    build_simfunc()

if USE_BALSAM:
    from libensemble.balsam_controller import BalsamJobController
    jobctrl = BalsamJobController(auto_resources = True)
else:
    from libensemble.mpi_controller import MPIJobController
    jobctrl = MPIJobController(auto_resources = False)
jobctrl.register_calc(full_path=sim_app, calc_type='sim')

summary_file_name = short_name + '.libe_summary.txt'
CalcInfo.set_statfile_name(summary_file_name)
if MPI.COMM_WORLD.Get_size() == 4:
    CalcInfo.keep_worker_stat_files = True # Testing this functionality
else:
    CalcInfo.keep_worker_stat_files = False # Testing this functionality

num_workers = Resources.get_num_workers()

#State the objective function, its arguments, output, and necessary parameters (and their sizes)
sim_specs = {'sim_f': job_control_hworld, # This is the function whose output is being minimized
             'in': ['x'], # These keys will be given to the above function
             'out': [('f',float), # This is the output from the function being minimized
                     ('cstat',int),
                    ],
             'cores': NCORES,
             'save_every_k': 400
             }

# State the generating function, its arguments, output, and necessary parameters.
gen_specs = {'gen_f': uniform_random_sample,
             'in': ['sim_id'],
             'out': [('x',float,2),
                    ],
             'lb': np.array([-3,-2]),
             'ub': np.array([ 3, 2]),
             'gen_batch_size': 5*num_workers,
             'batch_mode': True,
             'num_active_gens':1,
             'save_every_k': 20
             }

# Tell libEnsemble when to stop
exit_criteria = {'elapsed_wallclock_time': 15}

np.random.seed(1)
persis_info = {}
for i in range(MPI.COMM_WORLD.Get_size()):
    persis_info[i] = {'rand_stream': np.random.RandomState(i)}

# Perform the run
H, persis_info, flag = libE(sim_specs, gen_specs, exit_criteria, persis_info)

if MPI.COMM_WORLD.Get_rank() == 0:
    print('\nChecking expected job status against Workers ...\n')

    #Expected list: Last is zero as will not be entered into H array on manager kill - but should show in the summary file.
    #Repeat expected lists num_workers times and compare with list of status's received from workers
    calc_status_list_in = np.asarray([WORKER_DONE,WORKER_KILL_ON_ERR,WORKER_KILL_ON_TIMEOUT, JOB_FAILED, 0])
    calc_status_list = np.repeat(calc_status_list_in,num_workers)

    #For debug
    print("Expecting: {}".format(calc_status_list))
    print("Received:  {}\n".format(H['cstat']))

    assert np.array_equal(H['cstat'], calc_status_list), "Error - unexpected calc status. Received: " + str(H['cstat'])

    #Check summary file:
    print('Checking expected job status against job summary file ...\n')

    calc_desc_list_in = ['Completed','Worker killed job on Error','Worker killed job on Timeout', 'Job Failed', 'Manager killed on finish']
    #Repeat N times for N workers and insert Completed at start for generator
    calc_desc_list = ['Completed'] + calc_desc_list_in * num_workers
    with open(summary_file_name,'r') as f:
        i=0
        for line in f:
            if "Status:" in line:
                _, file_status = line.partition("Status:")[::2]
                print("Expected: {}   Filestatus: {}".format(calc_desc_list[i], file_status.strip()))
                assert calc_desc_list[i] == file_status.strip(), "Status does not match file"
                i+=1

    print("\n\n\nRun completed.")
