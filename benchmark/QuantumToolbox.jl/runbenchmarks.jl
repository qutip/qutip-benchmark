using BenchmarkTools
using QuantumToolbox

QuantumToolbox.versioninfo()

const GROUP = get(ENV, "GROUP", "CPU")

include("setup.jl")
include("mesolve.jl")