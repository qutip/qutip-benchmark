from importlib.metadata import version, PackageNotFoundError

def pkg_version(package):
    try:
        return version(package)
    except PackageNotFoundError:
        return None

def pytest_benchmark_update_json(config, benchmarks, output_json):
    output_json["package_versions"] = {}
    output_json["package_versions"]["scipy"] = pkg_version("scipy")
    output_json["package_versions"]["numpy"] = pkg_version("numpy")
    output_json["package_versions"]["cython"] = pkg_version("cython")
    output_json["package_versions"]["qutip"] = pkg_version("qutip")
    output_json["package_versions"]["qutip-jax"] = pkg_version("qutip-jax")
    output_json["package_versions"]["jax"] = pkg_version("jax")
    output_json["package_versions"]["pytest"] = pkg_version("pytest")
