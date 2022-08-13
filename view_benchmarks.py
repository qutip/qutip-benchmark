from cmath import nan
import json
from tkinter.ttk import Separator
import pandas as pd
import matplotlib.pyplot as plt
import glob
from pathlib import Path



def unravel(data, key):
    """Transforms {key:{another_key: values, another_key2: value2}} into
    {key_another_key:value, key_another_key2:value}"""
    for d in data:
        values = d.pop(key)
        for k, v in values.items():
            d[key+'_'+k] = v
    return data


def json_to_dataframe(filepath):
    """Loads a JSON file where the benchmark is stored and returns a dataframe
    with the benchmar information."""
    with open(filepath) as f:
        data_json = json.load(f)
        cpu = data_json['machine_info']["cpu"]["brand_raw"]
        time = data_json['datetime']

        data = data_json['benchmarks']
        data = unravel(data, 'options')
        data = unravel(data, 'stats')
        data = unravel(data, 'params')
        data = unravel(data, 'extra_info')

        # Create dataframe
        data = pd.DataFrame(data)

        # Set operation from group name
        data["params_operation"] = data.group.str.split('-')
        data.params_operation = [d[0] for d in data.params_operation]

        # Add time and cpu to dataframe
        data['cpu'] = cpu
        data['datetime'] = time
        data['datetime'] = pd.to_datetime(data['datetime'])
        return data


def plot_data(df, separator, sep_labels, ax, restrict_cpu=False):
    """Uses the separator(dtype,coeftype,model) to plot differnt lines,
    assigns them a different color and assigns different line markers
    for each cpu"""

    # Separate using seperator
    for sep, g in df.groupby(separator):
        colors = [
            "blue", "orange", "green",
            "red", "black", "gray",
            "pink", "purple", "cyan"]
        markers = ['o--', 'x-', 'v:', "1-.", "*:"]
        count = 0
        cpus = []

        # Seperate by CPU
        for cpu, gr in g.groupby('cpu'):
            if restrict_cpu:
                if 'Platinum' in cpu:
                    cpus.append(cpu)
                    for i, label in enumerate(sep_labels):
                        if sep == label:
                            ax.plot(
                                gr.datetime, gr.stats_mean,
                                markers[count], color=colors[i]
                                )
                    count = count+1
            else:
                cpus.append(cpu)
                for i, label in enumerate(sep_labels):
                    if sep == label:
                        ax.plot(
                            gr.datetime, gr.stats_mean,
                            markers[count], color=colors[i]
                            )
                count = count+1

    # Generate legend
    def f(m, c):
        return plt.plot([], [], m, color=c)[0]
    handles = [f("s", colors[i]) for i in range(len(sep_labels))]
    handles += [f(markers[i], "k") for i in range(len(cpus))]
    sep_labels += cpus
    ax.legend(handles, sep_labels)

    ax.set_xlabel("date")
    ax.set_ylabel("time (s)")
    ax.set_yscale('log')


def plot_operations(df, matrix_size=[64, 256]):
    """Plots the evolution over time of the add and matmul operation
    benchmarks for a specified matrix size"""

    # Create storage folder
    folder = Path("images/plots")
    folder.mkdir(parents=True, exist_ok=True)

    # Group by operation, density and size
    grouped = df.groupby(['params_operation', 'params_density', 'params_size'])
    for (operation, density, size), group in grouped:
        if size in matrix_size:
            size = int(size)

            # Create Figure
            fig, ax = plt.subplots(1, 1)
            fig.suptitle(
                f'Matrix density: {density}  Matrix Size: {size}x{size}',
                fontsize=20
                )
            fig.set_size_inches(9, 9)

            # Plot data and create legend
            if 'QobjEvo' in operation:
                labels = ['function', 'array', 'string']
                plot_data(group, 'params_coeftype', labels, ax)
            else:
                labels = ['numpy', 'qutip_dense', 'qutip_csr', 'scipy_csr']
                plot_data(group, 'params_dtype', labels, ax)

            # Save figure
            fig.tight_layout()
            fig.subplots_adjust(top=0.95)
            plt.gcf().autofmt_xdate()
            plt.savefig(
                f"./images/plots/{operation}_{density}_{size}.png",
                bbox_inches='tight'
                )
            plt.close()


def plot_solvers(df, dimension_size=[32, 128]):
    """Plots the evolution over time of solver
    benchmarks for a specified Hilbert Dimension"""

    # Create storage folder
    folder = Path("images/plots")
    folder.mkdir(parents=True, exist_ok=True)

    # Groub by solver type and Hibert space dimension
    grouped = df.groupby(['params_operation', 'params_dimension'])
    for (operation, dimension), group in grouped:
        if (dimension in dimension_size):

            # Create figure
            dimension = int(dimension)
            fig, ax = plt.subplots(1, 1)
            fig.suptitle(
                f'Solver: {operation}  Hilbert Space Dimension: {dimension}',
                fontsize=20
                )
            fig.set_size_inches(9, 9)

            # Plot data
            if operation == 'steadystate':
                labels = ["Jaynes Cummings", "Cavity"]
                plot_data(group, 'params_model_steady', labels, ax)
            else:
                labels = ["Jaynes Cummings", "Cavity", "Qubit Spin Chain"]
                plot_data(group, 'params_model_solve', labels, ax)

            # Save figure
            fig.tight_layout()
            fig.subplots_adjust(top=0.95)
            plt.gcf().autofmt_xdate()
            plt.savefig(
                f"./images/plots/{operation}_{dimension}.png",
                bbox_inches='tight'
                )
            plt.close()


def compare_operations(df):
    """Plots comaprison results using matplotlib. It iterates params_operation
    and params_density and plots time vs N (for NxN matrices)"""

    # Create storage folder
    folder = Path("images/compare")
    folder.mkdir(parents=True, exist_ok=True)

    grouped = df.groupby(['params_operation', 'params_density'])
    cpu = df["cpu"]
    for (operation, density), group in grouped:
        if "QobjEvo" not in operation:
            for dtype, g in group.groupby('params_dtype'):
                plt.errorbar(
                    g.params_size, g.stats_mean, g.stats_stddev,
                    fmt='.-', label=dtype
                    )
        else:
            for coeftype, g in group.groupby('params_coeftype'):
                plt.errorbar(
                    g.params_size, g.stats_mean, g.stats_stddev,
                    fmt='.-', label=coeftype
                    )

        plt.title(f"{operation} {density} {cpu}")
        plt.legend()
        plt.yscale('log')

        plt.xlabel("N")
        plt.ylabel("time (s)")
        plt.savefig(f"./images/compare/{operation}_{density}.png")
        plt.close()


def plot_compare_solvers(df, separator):
    grouped = df.groupby(separator)
    for (model), group in grouped:
        if model != nan:
            for solver, g in group.groupby('params_operation'):
                plt.errorbar(
                    g.params_dimension, g.stats_mean,
                    g.stats_stddev, fmt='.-', label=solver
                    )

            plt.title(f"{model}")
            plt.legend()
            plt.yscale('log')
            plt.xlabel("N")
            plt.ylabel("time (s)")
            plt.savefig(f"./images/compare/{separator[13:]}_{model}.png")
            plt.close()

def compare_solvers(df):
    """Plots comparison of solver performance for inreasing Hilbert Space
    dimensions using Matplotlib"""

    # Create storage folder
    folder = Path("images/compare")
    folder.mkdir(parents=True, exist_ok=True)

    # plot mcsolve and mesolve
    plot_compare_solvers(df, "params_model_solve")
    
    # plot steadystate
    plot_compare_solvers(df, "params_model_steady")


def get_paths():
    """Returns the path to the latest benchmark run from `./.benchmarks/`"""

    benchmark_paths = glob.glob("./.benchmarks/*/*.json")
    dates = [''.join(_b.split("/")[-1].split('_')[2:4])
             for _b in benchmark_paths]
    zipped = zip(dates, benchmark_paths)
    tmp = sorted(zipped, key=lambda x: x[0])
    res = list(zip(*tmp))

    return res[1]


def get_latest_benchmark_path():
    """Returns the path to the latest benchmark run from `./.benchmarks/`"""

    benchmark_paths = glob.glob("./.benchmarks/*/*.json")
    dates = [''.join(_b.split("/")[-1].split('_')[2:4])
             for _b in benchmark_paths]
    benchmarks = {date: value for date, value in zip(dates, benchmark_paths)}

    dates.sort()
    latest = dates[-1]
    benchmark_latest = benchmarks[latest]

    return benchmark_latest


def create_dataframe(paths):
    df = pd.DataFrame()

    for path in paths:
        data = json_to_dataframe(path)
        df = pd.concat([df, data])

    return df


def main(args=[]):
    folder = Path("images")
    paths = get_paths()
    latest_path = get_latest_benchmark_path()
    data = create_dataframe(paths)
    latest_data = json_to_dataframe(latest_path)

    # plot_operations(data)
    # plot_solvers(data)
    # compare_operations(latest_data)
    compare_solvers(latest_data)


if __name__ == '__main__':
    main()