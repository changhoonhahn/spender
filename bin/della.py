'''

python script for deploying job on adroit 

'''
import os, sys
import time 


def spender(study, tag, zmin, zmax, debug=False):
    ''' deploy ANPE training 
    '''
    cntnt = '\n'.join([
        "#!/bin/bash", 
        "#SBATCH -J %s" % study,
        ["#SBATCH --time=11:59:59", "#SBATCH --time=00:29:59"][debug], 
        "#SBATCH --export=ALL", 
        "#SBATCH -o o/%s.o" % study, 
        "#SBATCH --mail-type=all", 
        "#SBATCH --mail-user=chhahn@princeton.edu", 
        "#SBATCH --gres=gpu:1", 
        "#SBATCH --constraint=gpu80", 
        "#SBATCH --mem-per-cpu=8G", 
        "", 
        'now=$(date +"%T")', 
        'echo "start time ... $now"', 
        "", 
        "source ~/.bashrc", 
        "conda activate gqp", 
        "",
        "python /home/chhahn/projects/spender_qso/bin/train_desiqso.py /tigress/chhahn/spender_qso/train /tigress/chhahn/spender_qso/models/%s.pt -t %s -n 10 -zmin %f -zmax %f -v" % (study, tag, zmin, zmax),
        "",
        'now=$(date +"%T")', 
        'echo "end time ... $now"', 
        ""]) 

    # create the slurm script execute it and remove it
    f = open('_spender.slurm','w')
    f.write(cntnt)
    f.close()
    os.system('sbatch _spender.slurm')
    os.system('rm _spender.slurm')
    return None 

#spender('model0', 'qso_lowz', 0., 2.1, debug=False) 

# 2024.06.05
spender('qso.z_2p1_3p5', 'qso_highz', 2.1, 3.5, debug=False) 
