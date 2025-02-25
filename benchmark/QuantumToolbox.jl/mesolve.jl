N = 20  # cutoff of the Hilbert space dimension
ω = 1.0 # frequency of the harmonic oscillator
γ = 0.1 # damping rate

tlist = range(0, 10, 100) # time list

# annihilation operator and initial state
if GROUP == "CPU"
    a = destroy(N) 
    ψ0 = fock(N, 3)
elseif GROUP == "CUDA"
    a = cu(destroy(N))
    ψ0 = cu(fock(N, 3))
end

H = ω * a' * a
c_ops = [sqrt(γ) * a]
e_ops = [a' * a]

@benchmark mesolve($H, $ψ0, $tlist, $c_ops, e_ops = $e_ops, progress_bar = Val(false))