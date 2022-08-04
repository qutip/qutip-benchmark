import time

try:
    from numpy import *
    from qutip import *
except:
    print("nan")
    import sys
    sys.exit(1)

def benchmark(runs=1):
    """
    Cavity+qubit wigner function
    """
    kappa = 2; gamma = 0.2; g = 1;
    wc = 0; w0 = 0; wl = 0; E = 0.5;
    N = 20
    tlist = linspace(0,10,200);
    ida    = qeye(N)
    idatom = qeye(2)
    a  = tensor(destroy(N),idatom)
    sm = tensor(ida,sigmam())
    H = (w0-wl)*sm.dag()*sm + (wc-wl)*a.dag()*a + 1j*g*(a.dag()*sm - sm.dag()*a) + E*(a.dag()+a)
    C1=sqrt(2*kappa)*a
    C2=sqrt(gamma)*sm
    psi0 = tensor(basis(N,0),basis(2,1))
    rho0 = psi0.dag() * psi0
    out=mesolve(H, psi0, tlist, [C1, C2], [])
    rho_cavity=ptrace(out.states[-1],0)
    xvec=linspace(-10,10,200)

    tot_elapsed = 0
    for n in range(runs):
        tic = time.time()
        W = wigner(rho_cavity,xvec,xvec)
        toc = time.time()
        tot_elapsed += toc - tic
    
    return tot_elapsed / runs
 

if __name__ == "__main__":

    try:
        import argparse
        parser = argparse.ArgumentParser()
        parser.add_argument("-r", "--number-of-runs",
                            help="number of times to run the benchmark",
                            default=1, type=int)
        args = parser.parse_args()

        print(benchmark(args.number_of_runs))
    except Exception as e:
        print("nan")

