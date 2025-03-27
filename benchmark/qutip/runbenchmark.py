import sys
import pytest
from importlib.metadata import version, PackageNotFoundError

def pkg_version(package):
    try:
        return version(package)
    except PackageNotFoundError:
        return None

@pytest.hookimpl()
def pytest_benchmark_update_json(config, benchmarks, output_json):
    output_json["package_versions"]["scipy"] = pkg_version("scipy")
    output_json["package_versions"]["numpy"] = pkg_version("numpy")
    output_json["package_versions"]["cython"] = pkg_version("cython")
    output_json["package_versions"]["qutip"] = pkg_version("qutip")
    output_json["package_versions"]["pytest"] = pkg_version("pytest")

def run_benchmarks():
    return pytest.main(
        [
            "benchmark/qutip/scripts",
            "--benchmark-only",
            "--benchmark-columns=Mean,StdDev,rounds,Iterations",
            "--benchmark-sort=name",
            "--benchmark-autosave",
            "--benchmark-storage=./benchmark/results/qutip/",
            "--durations=0",
            "--durations-min=1.0",
        ]
    )

def main():
    return run_benchmarks()


if __name__ == "__main__":
    sys.exit(main())