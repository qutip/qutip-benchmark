# Write the benchmarking functions here.
# See "Writing benchmarks" in the asv docs for more information.

from qutip import *
from numpy import pi, sqrt, linspace

try:
    import cvxpy
except:
    cvxpy = None

class QobjTimeSuite:
    """
    Tests basic operations on Qobj instances.
    """

    def setup(self):
        self.ptrace_example = tensor([sigmax(), sigmay(), sigmaz(), sigmay(), sigmaz(), sigmax()])
        self.big_dms = [rand_dm_ginibre(N=32), rand_dm_ginibre(N=32)]
        self.big_unitary = rand_unitary_haar(N=32)
     
    def time_tensor(self):
        """
        Tensor 6 spin operators.
        """
        tensor(sigmax(), sigmay(), sigmaz(), sigmay(), sigmaz(), sigmax())

    def time_ptrace(self):
        """
        Partial trace of a six-spin operator.
        """
        ptrace(self.ptrace_example, [1, 3, 4])

    def time_expm_dispsque(self, N=20, alpha=2+2j, sp=1.25j):
        """
        Expm w/ displacement and squeezing.
        """
        coherent(N, alpha)
        squeeze(N, sp)

    def time_add(self):
        qobj = self.big_dms[0] + self.big_dms[1]

    def time_mul(self):
        qobj = self.big_unitary * self.big_dms[0]


class SuperopTimeSuite:
    """
    Tests superoperator manipulations.
    """

    def setup(self, dim=8):
        self.U = rand_unitary_haar(N=dim)
        # We also make a copy of to_super(U)
        # so that we can check to_choi, to_kraus, etc.
        # without including the cost of to_super itself.
        self.S = to_super(self.U)

        # Make superoperators corresponding to two
        # smaller unitaries.
        self.small_superunis = [to_super(rand_unitary_haar(N=3)), to_super(rand_unitary_haar(N=3))]

    def time_oper_to_super(self):
        S = to_super(self.U)

    def time_super_to_choi(self):
        J = to_choi(self.S)

    def time_super_to_chi(self):
        C = to_chi(self.S)

    def time_super_to_kraus(self):
        K = to_kraus(self.S)

    def time_super_to_stinespring(self):
        A, B = to_stinespring(self.S)

    def time_super_tensor(self):
        super_tensor(self.S, self.S)


    if cvxpy:
        def time_dnorm_diff_unitaries(self):
            self.small_superunis[0].dnorm(self.small_superunis[1])

    
class JaynesCummingTimeSuite:
    """
    Tests more sophisticated examples based on the Jaynes-Cumming model.
    """

    def time_jc_hamiltonian(self):
        """
        Construct Jaynes-Cumming Hamiltonian with Nc=10, Na=2.
        """
        wc = 1.0 * 2 * pi  
        wa = 1.0 * 2 * pi
        g  = 0.05 * 2 * pi
        Nc = 10
        a = tensor(destroy(Nc), qeye(2))
        sm = tensor(qeye(Nc), sigmam())
        H = wc * a.dag() * a + wa * sm.dag() * sm + g * (a.dag() + a) * (sm.dag() + sm)


    def time_steady_state(self, 
            kappa=2, gamma=0.2, g=1, wc=0,
            w0=0, N=10, E=0.5, wl=0
        ):
        """
        Cavity+qubit steady state
        """
        ida=qeye(N)
        idatom=qeye(2)
        a=tensor(destroy(N),idatom)
        sm=tensor(ida,sigmam())
        H=(w0-wl)*sm.dag()*sm+(wc-wl)*a.dag()*a+1j*g*(a.dag()*sm-sm.dag()*a)+E*(a.dag()+a)
        C1=sqrt(2*kappa)*a
        C2=sqrt(gamma)*sm
        C1dC1=C1.dag() * C1
        C2dC2=C2.dag() * C2
        rhoss = steadystate(H, [C1, C2])
    
    def time_cavity_me(self,
            kappa = 2, gamma = 0.2, g = 1,
            wc = 0, w0 = 0, wl = 0, E = 0.5,
            N = 10
        ):
        """
        Cavity+qubit master equation
        """

        tlist = linspace(0,10,200)
        ida    = qeye(N)
        idatom = qeye(2)
        a  = tensor(destroy(N),idatom)
        sm = tensor(ida,sigmam())
        H = (w0-wl)*sm.dag()*sm + (wc-wl)*a.dag()*a + 1j*g*(a.dag()*sm - sm.dag()*a) + E*(a.dag()+a)
        C1=sqrt(2*kappa)*a
        C2=sqrt(gamma)*sm
        C1dC1=C1.dag()*C1
        C2dC2=C2.dag()*C2
        psi0 = tensor(basis(N,0),basis(2,1))
        rho0 = psi0.dag() * psi0
        mesolve(H, psi0, tlist, [C1, C2], [C1dC1, C2dC2, a])
    
    def time_cavity_mc(self,
            kappa = 2, gamma = 0.2, g = 1,
            wc = 0, w0 = 0, wl = 0, E = 0.5,
            N = 10
        ):
        """
        Cavity+qubit monte carlo equation
        """

        tlist = linspace(0,10,200);

        ida = qeye(N)
        idatom = qeye(2)
        a  = tensor(destroy(N),idatom)
        sm = tensor(ida,sigmam())
        H = (w0-wl)*sm.dag()*sm + (wc-wl)*a.dag()*a + 1j*g*(a.dag()*sm - sm.dag()*a) + E*(a.dag()+a)
        C1=sqrt(2*kappa)*a
        C2=sqrt(gamma)*sm
        C1dC1=C1.dag()*C1
        C2dC2=C2.dag()*C2
        psi0 = tensor(basis(N,0),basis(2,1))
        mcsolve(H, psi0, tlist, [C1, C2], [C1dC1, C2dC2, a],options=Odeoptions(gui=False))
