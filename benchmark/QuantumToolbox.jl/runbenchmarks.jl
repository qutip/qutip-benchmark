using BenchmarkTools
using QuantumToolbox

QuantumToolbox.about()

const GROUP = get(ENV, "GROUP", "CPU")

include("setup.jl")
include("mesolve.jl")
