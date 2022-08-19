import json
import pandas as pd
import matplotlib.pyplot as plt
import glob
from pathlib import Path
import argparse


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


def prep_data(df, separators):
    """creates a list of dicts of the form 
    [(plot1),{line1:values;line2:values...},(plot2),{line1:values; ...}...}]
    with values stored as dataframes"""
    res = []
    for plot_separators in separators:
        for line_separators in plot_separators[1]:
            plot_id = {
                    plot: {
                        line: line_data for line, line_data
                        in plot_data.groupby(line_separators)
                        }
                    for plot, plot_data in df.groupby(plot_separators[0])
                    }

            # delete empty entries caused by plots with same
            # plot separators but different line separators
            tmp = {key: data for key, data in plot_id.items() if data}
            res += tmp.items()
    return res



def plot_data(df, line_sep, labels, fig_title, fig_path, restrict_cpu):
    """Uses the line_sep (dtype,coeftype,model) to plot differnt lines,
    assigns them a different color and assigns different line markers
    for each cpu"""

    # Create figure
    fig, ax = plt.subplots(1, 1)

    fig.suptitle(fig_title, fontsize=20)
    fig.set_size_inches(9, 9)

    # Set colors and markers for legend
    colors = [
        "blue", "orange", "green",
        "red", "black", "gray",
        "pink", "purple", "cyan"]
    markers = ['o--', 'x-', 'v:', "1-.", "*:"]

    # Separate using line separator
    for sep, g in df.groupby(line_sep):
        count = 0
        cpus = []
        # Separate by CPU
        for cpu, gr in g.groupby('cpu'):
            if restrict_cpu:
                if restrict_cpu in cpu:
                    cpus.append(cpu)
                    for i, label in enumerate(labels):
                        if sep == label:
                            ax.plot(
                                gr.datetime, gr.stats_mean,
                                markers[count], color=colors[i]
                                )
                    count = count+1
            else:
                cpus.append(cpu)
                for i, label in enumerate(labels):
                    if sep == label:
                        ax.plot(
                            gr.datetime, gr.stats_mean,
                            markers[count], color=colors[i]
                            )
                count = count+1

    # Generate legend
    def f(m, c):
        return plt.plot([], [], m, color=c)[0]
    handles = [f("s", colors[i]) for i in range(len(labels))]
    handles += [f(markers[i], "k") for i in range(len(cpus))]
    labels += cpus
    ax.legend(handles, labels)

    ax.set_xlabel("date")
    ax.set_ylabel("time (s)")
    ax.set_yscale('log')

    fig.tight_layout()
    plt.gcf().autofmt_xdate()
    plt.savefig(fig_path, bbox_inches='tight')
    plt.close()


def separate_plots(df, plot_sep, path, size, restrict_cpu=None):
    """Plots the evolution over time of the add and matmul operation
    benchmarks for a specified matrix size"""
    res = []
    # Create storage folder
    folder = Path(f"{path}/nightly")
    folder.mkdir(parents=True, exist_ok=True)

    # Group group based onn plot_sep parameters
    grouped = df.groupby(plot_sep)

    for param, group in grouped:

        op_title = params[0].replace("_", " ")

        # Determine whether it is a solver or a matrix operation
        # based on amount of parameters (3 = operations; 2 = solvers)
        if len(param) == 3:
            fig_title = f"""Operation:{op_title}
            Matrix density: {param[2]} Matrix Size: {param[1]}x{param[1]}"""

            fig_path = f"{path}/nightly/{param[0]}_{param[2]}_{param[1]}.png"

            if 'QobjEvo' in param[0]:
                line_sep = 'params_coeftype'
            else:
                line_sep = 'params_dtype'

        elif len(param) == 2:
            fig_title = f"""Solver: {op_title}
            Hilbert Space Dimension: {param[1]}"""

            fig_path = f"{path}/nightly/{param[0]}_{param[1]}.png"

            if 'steadystate' in param[0]:
                line_sep = 'params_model_steady'
            else:
                line_sep = 'params_model_solve'

        # Create labels for each line
        labels = group[line_sep].unique().tolist()

        # Plot data if size equals parameters
        if param[1] in size:
            res.append(
                (group, line_sep, labels,
                 fig_title, fig_path, restrict_cpu)
                )
    return res


def get_paths():
    """Returns the path to the latest benchmark run from `./.benchmarks/`"""

    benchmark_paths = glob.glob("./.benchmarks/*/*.json")
    dates = [''.join(_b.split("/")[-1].split('_')[2:4])
             for _b in benchmark_paths]
    zipped = zip(dates, benchmark_paths)
    tmp = sorted(zipped, key=lambda x: x[0])
    res = list(zip(*tmp))

    return res[1]


def create_dataframe(paths):
    df = pd.DataFrame()

    for path in paths:
        data = json_to_dataframe(path)
        df = pd.concat([df, data])

    return pd.DataFrame(df)


def main(args=[]):
    parser = argparse.ArgumentParser(description="""Choose what to plot and
                    where to store it, by default all benchmarks will be
                    plotted using default size and dimensions""")
    parser.add_argument('--path', default="./images", type=Path,
                        help="""Path to folder in which the plots will be
                        stored""")
    parser.add_argument('--size', nargs="+", default=[64, 256], type=int,
                        help="""Size of the matrices on which the operations
                        will be performed in the history benchmarks, has to be
                        a power of 2, max=256, min=4, default=[64,256], """)
    parser.add_argument('--dimension', nargs="+", default=[32, 128], type=int,
                        help="""Size of the matrices on which the operations
                        will be performed in the history benchmarks, has to be
                        a power of 2, max=256, min=4, default[32,128]""")
    parser.add_argument('--solve', action='store_true',
                        help="""Only plot solvers""")
    parser.add_argument('--operations', action='store_true',
                        help="""Only plot operations""")

    args = parser.parse_args()

    # fetch data
    paths = get_paths()
    data = create_dataframe(paths)

    ###                  ###
    ###     Method 1     ###
    ###                  ###

    # data separators
    # lin_alg_plot_sep = ['params_operation', 'params_size', 'params_density']
    # solver_plot_sep = ['params_operation', 'params_dimension']

    # # Separate data
    # if args.operations and not args.solve:
    #     plots = separate_plots(
    #                         data, lin_alg_plot_sep,
    #                         args.path, args.size
    #                         )

    # elif args.solve and not args.operation:
    #     plots = separate_plots(
    #                         data, solver_plot_sep,
    #                         args.path, args.dimension
    #                         )

    # else:
    #     plots = separate_plots(
    #                         data, lin_alg_plot_sep,
    #                         args.path, args.size
    #                         )
    #     plots += separate_plots(
    #                         data, solver_plot_sep,
    #                         args.path, args.dimension
    #                         )

    # # Plot data
    # for plot in plots:
    #     plot_data(*plot)


    ###                  ###
    ###     Method 2     ###
    ###                  ###

    separators = [
        [['params_operation', 'params_size', 'params_density'],
            ['params_coeftype','params_dtype']],
        [['params_operation', 'params_dimension'],
            ['params_model_steady','params_model_solve']]
        ]
    prep_data(data,separators)

if __name__ == '__main__':
    main()
