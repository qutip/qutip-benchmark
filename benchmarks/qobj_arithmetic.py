#
# qutip benchmark: Qobj arithmetic
#

try:
    from numpy import *
    from qutip import *
except:
    print("nan")
    import sys
    sys.exit(1)

def benchmark(runs=1):
    """
    Construct Jaynes-Cumming Hamiltonian with Nc=10, Na=2.
    """
    wc = 1.0 * 2 * pi  
    wa = 1.0 * 2 * pi
    g  = 0.05 * 2 * pi
    Nc=10
    tot_elapsed = 0
    for n in range(runs):
        tic = time.time()
        a = tensor(destroy(Nc),qeye(2))
        sm = tensor(qeye(Nc),sigmam())
        H = wc*a.dag()*a+wa*sm.dag()*sm+g*(a.dag()+a)*(sm.dag()+sm)
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
        #print(e)
        print("nan")
