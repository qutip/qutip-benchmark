import json
import pytest
import argparse
import glob
from importlib.metadata import version, PackageNotFoundError


def pkg_version(package):
    try:
        return version(package)
    except PackageNotFoundError:
        return None



def get_latest_benchmark():
    """Returns the path to the latest benchmark run from `./.benchmarks/`"""

    benchmark_paths = glob.glob("./.benchmarks/*/*.json")
    dates = [''.join(_b.split("/")[-1].split('_')[2:4])
             for _b in benchmark_paths]
    benchmarks = {date: value for date, value in zip(dates, benchmark_paths)}

    dates.sort()
    latest = dates[-1]
    benchmark_latest = benchmarks[latest]

    return benchmark_latest


def add_packages_to_json(filepath):
    """Loads the created JSON file and adds package versions"""
    with open(filepath, "r") as f:
        data = json.load(f)
        data['package_versions'] = {}
        data['package_versions']['scipy'] = pkg_version('scipy')
        data['package_versions']['numpy'] = pkg_version('numpy')
        data['package_versions']['cython'] = pkg_version('cython')
        data['package_versions']['qutip'] = pkg_version('qutip')
        data['package_versions']['pytest'] = pkg_version('pytest')
    with open(filepath, "w") as f:
        json.dump(data, f, indent=4, separators=(',', ': '))
    return data


def run_benchmarks(args):
    "Run pytest benchmark with sensible defaults."
    pytest.main(["--benchmark-only",
                 "--benchmark-columns=Mean,StdDev,rounds,Iterations",
                 "--benchmark-sort=name",
                 "--benchmark-autosave",
                 "-Wdefault"] +
                args)


def main(args=[]):
    parser = argparse.ArgumentParser(description="""Run and plot the benchmarks.
                                     The script also accepts the same
                                     arguments as pytest/pytest-benchmark. The
                                     script must be run from the root of the
                                     repository.""")

    args, other_args = parser.parse_known_args()

    run_benchmarks(other_args)
    benchmark_latest = get_latest_benchmark()
    add_packages_to_json(benchmark_latest)


if __name__ == '__main__':
    main()
