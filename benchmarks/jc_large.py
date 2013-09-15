#
# qutip benchmark: solve for the dynamics of the jaynes-cummings model
#

try:
    from numpy import *
    from qutip import *
except:
    print("nan")
    import sys
    sys.exit(1)

def jc_integrate(N, wc, wa, g, kappa, gamma,    tlist):

    # initial state
    psi0 = tensor(basis(N,N-1),    basis(2,0))    # start with an excited atom 

    # Hamiltonian
    idc = qeye(N)
    ida = qeye(2)

    a  = tensor(destroy(N), ida)
    sm = tensor(idc, destroy(2))

    H = wc * a.dag() * a + wa * sm.dag() * sm + g * (a.dag() * sm + a * sm.dag())
        
    # collapse operators
    c_op_list = []

    n_th_a = 0.0 # zero temperature

    rate = kappa * (1 + n_th_a)
    if rate > 0.0:
        c_op_list.append(sqrt(rate) * a)

    rate = kappa * n_th_a
    if rate > 0.0:
        c_op_list.append(sqrt(rate) * a.dag())

    rate = gamma
    if rate > 0.0:
        c_op_list.append(sqrt(rate) * sm)

    # evolve and calculate expectation values
    output = mesolve(H, psi0, tlist, c_op_list, [a.dag() * a, sm.dag() * sm])  

    # or use the MC solver
    #output = mcsolve(H, psi0, tlist, c_op_list, [a.dag() * a, sm.dag() * sm])

    return output.expect[0], output.expect[1]


def benchmark(N=1):

    import time

    wc = 1.0 * 2 * pi   # cavity frequency
    wa = 1.0 * 2 * pi   # atom frequency
    g  = 0.25 * 2 * pi  # coupling strength

    kappa = 0.015       # cavity dissipation rate
    gamma = 0.15        # atom dissipation rate

    NN = 20              # number of cavity fock states

    tlist = linspace(0,25,100)

    total_elased_time = 0
    for r in range(N):
        start_time = time.time()
        for n in range(20):
            nc, na = jc_integrate(NN, wc, wa, g, kappa, gamma, tlist)
        total_elased_time += (time.time() - start_time)

    return (total_elased_time / N)


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

