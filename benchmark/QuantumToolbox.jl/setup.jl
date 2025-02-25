if GROUP == "CUDA"
    using CUDA
    CUDA.allowscalar(false)
    CUDA.versioninfo()
end