'''

script for deploying job on perlmutter


'''
import os, sys


def spender(imodel): 
    cntnt = '\n'.join([
        "#!/bin/bash",
        "#SBATCH -A desi", 
        "#SBATCH -C gpu",
        "#SBATCH -q shared",
        "#SBATCH -t 00:59:59",
        "#SBATCH -n 1",
        '#SBATCH --gpus-per-task=1', 
        "#SBATCH -J qso%i" % imodel,  
        "#SBATCH -o o/qso%i.o" % imodel, 
        "",
        'now=$(date +"%T")',
        'echo "start time ... $now"',
        "",
        "module load cudatoolkit/12.2", 
        "module load cudnn/8.9.3_cuda12",
        "module load python", 
        "conda activate gqp",
        "",
        "python /global/homes/c/chahah/projects/spender/bin/train_desiqso.py /global/cfs/projectdirs/desi/users/chahah/spender_qso /global/cfs/projectdirs/desi/users/chahah/spender_qso/models/model%i.pt -n 12 -b 256 -l 50 -zmax 4.0 -v" % imodel, 
        'now=$(date +"%T")',
        'echo "end time ... $now"',
        ""])

    # create the slurm script execute it and remove it
    f = open('_train.slurm','w')
    f.write(cntnt)
    f.close()
    os.system('sbatch _train.slurm')
    os.system('rm _train.slurm')
    return None


# run 2024.05.13
spender(2)
