import sys
import pytest

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