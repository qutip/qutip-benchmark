#
# qutip benchmark: expect
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
    expectation values
    """
    N=25
    alpha=3j
    a=destroy(N)
    coh=coherent_dm(N,alpha)
    coh_dm=coherent_dm(N,alpha)
    n=num(N)

    tot_elapsed = 0
    for m in range(runs):
        tic = time.time()
        expect(n,coh)
        expect(n,coh_dm)
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

