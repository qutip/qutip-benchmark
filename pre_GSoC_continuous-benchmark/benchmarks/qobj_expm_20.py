import time

try:
    from numpy import *
    from qutip import *
except:
    print("nan")
    import sys
    sys.exit(1)


def benchmark_qobj_expm(runs=1):
    """
    Test expm with displacement and squeezing operators.
    """
    alpha = 2+2j
    sp = 1.25j
    tot_elapsed = 0
    for n in range(runs):
        tic=time.time()
        coherent(20, alpha)
        squeeze(20, sp)
        toc=time.time()
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

        print(benchmark_qobj_expm(args.number_of_runs))
    except Exception as e:
        #print(e)
        print("nan")
