import sys
import argparse
import pytest

def run_benchmarks(args):
    """Run pytest benchmarks with defaults and optional additional args."""

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
            "-Wdefault",
        ]
        + args
    )

def main():
    pars = argparse.ArgumentParser(
        description="""
            Run the benchmarks for QuTiP. The script als accepts the same
            arguments as pytest/pytest-benchmark. Run the script from the
            root directory of the repository.
        """
    )
    _, other_args = pars.parse_known_args()
    return run_benchmarks(other_args)

if __name__ == "__main__":
    sys.exit(main())