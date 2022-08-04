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
    Cavity+qubit steady state
    """
    kappa = 1
    gamma = 0.01
    g = 1
    wc = w0 = wl = 0
    N = 20
    E = 1.5

    a = tensor(destroy(N), qeye(2))
    sm = tensor(qeye(N), sigmam())
    H = (w0-wl)*sm.dag()*sm+(wc-wl)*a.dag()*a+1j*g*(a.dag()*sm-sm.dag()*a)+E*(a.dag()+a)
    c_ops = [sqrt(2*kappa)*a, sqrt(gamma)*sm]

    tot_elapsed = 0
    for n in range(runs):
        tic = time.time()
        rhoss = steadystate(H, c_ops, use_umfpack=True)
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

