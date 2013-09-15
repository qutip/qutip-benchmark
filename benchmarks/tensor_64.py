try:
    from numpy import *
    from qutip import *
except:
    print("nan")
    import sys
    sys.exit(1)

def benchmark(runs=1):
    """
    Tensor 6 spin operators.
    """
    tot_elapsed = 0
    for n in range(runs):
        tic = time.time()
        tensor(sigmax(),sigmay(),sigmaz(),sigmay(),sigmaz(),sigmax())
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

