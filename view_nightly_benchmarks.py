import json
import pandas as pd
import matplotlib.pyplot as plt
import glob
from pathlib import Path
import argparse


def json_to_dataframe(filepath):
    """Loads a JSON file from the specified path and returns a dataframe
    with the benchmark information.

    Parameters
    ----------
    filepath : str
        path to the benchmark file

    Returns
    -------
    data : DataFrame
        DataFrame containing all the required plotting data from the
        benchmark file.

    """

    with open(filepath) as f:
        data_json = json.load(f)

        # Create dataframe
        data = pd.json_normalize(data_json["benchmarks"], sep="_")

        # Set operation from group name
        data["params_operation"] = data.group.str.split('-')
        data.params_operation = [d[0] for d in data.params_operation]

        # Add time and cpu to dataframe
        data['cpu'] = data_json['machine_info']["cpu"]["brand_raw"]
        data['datetime'] = data_json['datetime']
        data['datetime'] = pd.to_datetime(data['datetime'])

        # drop unused columns
        unused = [
            'options_disable_gc', 'options_timer', 'options_min_rounds',
            'options_max_time', 'options_min_time', 'options_warmup',
            'stats_min', 'stats_max', 'stats_median', 'stats_iqr', 'stats_q1',
            'stats_q3', 'stats_iqr_outliers', 'stats_stddev_outliers',
            'stats_outliers', 'stats_ld15iqr', 'stats_hd15iqr', 'stats_ops',
            'stats_total', 'stats_iterations', 'stats_rounds'
            ]
        data = data.drop(unused, axis="columns")

        return data


def get_paths(folder):
    """Returns a list of paths to all benchmark runs

    Parameters
    ----------
    folder : str
        path to the benchmarks folder

    Returns
    -------
    Paths : list
        list of the paths to each benchmark file

    """

    benchmark_paths = glob.glob(f"{folder}/*/*.json")
    dates = [''.join(_b.split("/")[-1].split('_')[2:4])
             for _b in benchmark_paths]
    zipped = zip(dates, benchmark_paths)
    tmp = sorted(zipped, key=lambda x: x[0])
    paths = list(zip(*tmp))

    return paths[1]


def create_dataframe(paths):
    """ fetch all required data

    Parameters
    ----------
    paths : list
        List containing all the paths to the benchmark files.

    Returns
    -------
    data : DataFrame
        Pandas dataframe containing all the required plotting data
        from all the benchmarks.

    """

    dfs = []
    for path in paths:
        df = json_to_dataframe(path)
        dfs.append(df)
    data = pd.concat(dfs)

    return data


def filter_ops(df, filter=None):
    """Filters the input dataframe by operation

    Parameters
    ----------
    df : DataFrame
        Dataframe containing data to be filtered.

    filter : list
        list of desired operation names in the output,
        if None the function will output all operations in
        the dataframe.

    Returns
    -------
    data : dict
        Dictionnary of the form {"operation": dataframe}.

    """

    if filter:
        ops = filter
    else:
        ops = list(df['params_operation'].unique())

    data = {}
    for op in ops:
        data[op] = df[df["params_operation"] == op]

        # drop columns that only exist for other operations
        data[op] = data[op].dropna(axis=1, how='all')

    return data


def filter_params(df, line_sep=None):
    """Filters the input dataframe by parameters used
    to separate each plot

    Parameters
    ----------
    df : DataFrame
        Dataframe containing data to be filtered.

    line_sep : list
        specifies which paramters should be used as line separators
        rather than plot separators. These need to be a substring contained
        in the parameter name. e.g: "type" will apply to both "params_coeftype"
        and "params_dtype".

    Returns
    -------
    data : dict
        Nested Dictionnary of the form {"operation-param_1-param_2-...":
        {data: dataframe; line_sep: str}}. line_sep = None if the parameter
        wasn't specified.

    separators : list
        List of the exact parameter names used as line separators.
    """

    # TODO add filter paramter to include only specfic filtering params
    data = {}
    for op in df:
        # get names of parameter columns and drop the one containing operations
        params = [
            param for param in list(df[op].columns)
            if "params_" in param and "operation" not in param
            ]

        separator = None

        # drop parameters that will be used as line separators
        if line_sep:
            # find the full param name from the initial substrings
            for sep in line_sep:
                for param in params:
                    if sep in param:
                        separator = param
                # remove separator prameter from parameter list
                if separator in params:
                    params.remove(separator)

        # create dataframe grouped by the remaining params
        for plot_params, plot_df in df[op].groupby(params):

            # handle cases for multiple and single parameters
            if type(plot_params) is tuple:
                key = [op]
                for i in plot_params:
                    key.append(i)
            else:
                key = [op, plot_params]

            # Creat key string id
            key = "-".join([str(item) for item in key])

            # Create sub dict
            tmp_dict = {}
            tmp_dict["data"] = plot_df
            tmp_dict["line_sep"] = separator

            # Append sub dict to main dict
            data[key] = tmp_dict
    return data


def plot_data(data, path):

    # create storage folder
    folder = Path(f"{path}")
    folder.mkdir(parents=True, exist_ok=True)

    # Set colors and markers for legend
    colors = [
        "blue", "orange", "green",
        "red", "black", "gray",
        "pink", "purple", "cyan"]
    markers = ['o--', 'x-', 'v:', "1-.", "*:"]

    for plot in data:
        line_sep = data[plot]["line_sep"]
        df = data[plot]["data"]

        # Create figure
        fig, ax = plt.subplots(1, 1)

        fig.suptitle(plot, fontsize=20)
        fig.set_size_inches(9, 9)

        # Separation by cpu andd line_sep
        if line_sep:
            labels = list(df[line_sep].unique())
            # separate by line_sep
            for sep, g in df.groupby(line_sep):
                count = 0
                cpus = []
                # Separate by CPU
                for cpu, gr in g.groupby('cpu'):
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

        # Only CPU line separation
        else:
            labels = list(df["cpu"].unique())
            # Separate by CPU
            for cpu, gr in df.groupby('cpu'):
                for i, label in enumerate(labels):
                    if cpu == label:
                        ax.plot(
                            gr.datetime, gr.stats_mean,
                            color=colors[i]
                            )

            # Generate legend
            def f(m, c):
                return plt.plot([], [], m, color=c)[0]
            handles = [f("s", colors[i]) for i in range(len(labels))]
            ax.legend(handles, labels)

        ax.set_xlabel("date")
        ax.set_ylabel("time (s)")
        ax.set_yscale('log')

        fig.tight_layout()
        plt.gcf().autofmt_xdate()
        plt.savefig(f"{folder}/{plot}.png", bbox_inches='tight')
        plt.close()


def main(args=[]):
    parser = argparse.ArgumentParser(description="""Choose what to plot and
                    where to store it, by default all benchmarks will be
                    plotted using default size and dimensions""")
    parser.add_argument('--plotpath', default="./images", type=Path,
                        help="""Path to folder in which the plots will be
                        stored""")
    parser.add_argument('--benchpath', default="./.benchmarks", type=Path,
                        help="""Path to folder in which the benchmarks are
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
    paths = get_paths(args.benchpath)
    data = create_dataframe(paths)
    data = filter_ops(data)
    data = filter_params(data, line_sep=['type', 'model'])
    # data = filter_params(data)
    plot_data(data, args.plotpath)


if __name__ == '__main__':
    main()
