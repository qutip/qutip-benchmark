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
            "--benchmark-storage=./benchmark/results/"
        ]
    )


def main():
    exit_code = run_benchmarks()
    return exit_code


if __name__ == "__main__":
    sys.exit(main())