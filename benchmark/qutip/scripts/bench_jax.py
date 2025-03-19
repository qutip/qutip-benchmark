import pytest
import jax
import jax.numpy as jnp
import qutip_jax as qj
from qutip import mesolve, basis, sigmax, sigmaz, CoreOptions

@pytest.mark.jax
def bench_jax_mesolve(benchmark):
    benchmark.group = "jax:mesolve"
    qj.set_as_default()

    with jax.default_device(jax.devices("gpu")[0]):
        opt = { "method": "diffrax", "normalize_output": False }

        with CoreOptions(default_dtype="jax"):
            delta = jnp.pi
            g = 0.2
            H = delta/2.0 * sigmax()
            c_ops = [jnp.sqrt(g) * sigmaz()]
            e_ops = [sigmaz()]
            psi0 = basis(2, 0)
            tlist = jnp.linspace(0, 10, 100)
            benchmark(mesolve, H, psi0, tlist, c_ops, e_ops=e_ops, options=opt)
