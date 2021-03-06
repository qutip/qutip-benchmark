from qutip import *
from numpy import sqrt
from time import time

def test_16(runs=1):
    """
    optomechanical steady state
    """
    test_name='opto steady [180]'
    Nc=4						#Number of cavity states
    Nm=45						#Number of mechanical states
    alpha=0.311					#Coherent state amplitude
    g0=0.36						#Coupling strength
    kappa=0.3					#Cavity damping rate
    gamma=0.00147				#Mech damping rate
    delta=-kappa				#detuning

    #operators
    idc=qeye(Nc)
    idm=qeye(Nm)
    a=tensor(destroy(Nc),idm)
    b=tensor(idc,destroy(Nm))
    #collapse operators
    cc=sqrt(kappa)*a
    cm=sqrt(gamma)*b
    c_op_list=[cc,cm]
    #construct Hamiltonian
    H=(-delta+g0*(b.dag()+b))*(a.dag()*a)+b.dag()*b+alpha*(a.dag()+a)
    #find steady state
    tot_elapsed = 0
    for n in range(runs):
        tic=time()
        steadystate(H,c_op_list, method='iterative-gmres',tol=1e-15, 
                    drop_tol=1e-3,use_precond=True,use_rcm=True)
        toc=time()
        tot_elapsed += toc - tic

    return [test_name], [tot_elapsed / runs]
 

if __name__=='__main__':
    print(test_16())
