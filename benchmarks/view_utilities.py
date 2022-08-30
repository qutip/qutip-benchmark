import json
import pandas as pd
import matplotlib.pyplot as plt
import glob
from pathlib import Path
import warnings


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

    with open(filepath, encoding='utf-8') as f:
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


def sort_ops(df, filters=None):
    """Filters the input dataframe by operation

    Parameters
    ----------
    df : DataFrame
        Dataframe containing data to be filtered.

    filters : list
        list of desired operation names in the output,
        if None the function will output all operations in
        the dataframe. Not case sensitive and Name can be
        substring of the full name. e.g: filter=[matmul], will
        produce plots for 'Matmul_QobjEvo_op@ket', 'Matmul_op@op'
        and 'Matmul_op@ket'.

    Returns
    -------
    data : dict
        Dictionnary of the form {"operation": dataframe}.

    """

    if filters:
        old_ops = list(df['params_operation'].unique())
        ops = []
        for param in filters:
            for op in old_ops:
                if param.lower() in op.lower():
                    ops.append(op)
    else:
        ops = list(df['params_operation'].unique())

    data = {}
    for op in ops:
        data[op] = df[df["params_operation"] == op]

        # drop columns that only exist for other operations
        data[op] = data[op].dropna(axis=1, how='all')
    return data


def param_filtering(filters, dict_params, key):
    """Filters the input dataframe by parameters used
    to separate each plot

    Parameters
    ----------
    filters : dict
        dict of the form {param_name: [accepted_values]}, filters the data by
        the given values for each parameter. Won't filter if the parameter
        doesn't apply to a give operation
        e.g: {param_size: [16,128]; param_density: [sparse]} will filter by
        size and density for operations but only by size for solvers,
        as solver benchmarks do not have a density parameter.

    params_dict : dict
        dict of the form {param_name: value}

    key : str
        name of the plot to which the filtering is applied

    Returns
    -------
    res : Bool
        True if the params correspond to the filter, False otherwise
    """
    if filters:
        tmp_filters = {}
        params = list(dict_params.keys())
        # create dict with correct keys from substring
        for param in params:
            for f_key, f_item in filters.items():
                if f_key.lower() in param.lower():
                    tmp_filters[param] = f_item

        # if no dict was created raise warning but proceed anyway
        if not tmp_filters:
            warning = "Filters don't apply to "
            warning += key
            warning += ", the plot will be made anyway \n"
            warning += "applied filters: "
            warning += ", ".join(list(filters.keys()))
            warning += "; available filters: " + ", ".join(params)
            warnings.warn(warning)
        else:
            # if a plot parameter doesn't match the corresponding
            # filter do not add data to output
            for f_key, f_item in tmp_filters.items():
                if dict_params[f_key] not in f_item:
                    return False
    return True


def column_filtering(df, filters, key):
    """deletes rows that contain specified values of a column columns

    Parameters
    ----------
    filters : dict
        dict of the form {column_name: [deleted_values]}, filters the data by
        the given values for each columns, the name is can be a substring of
        the column and is not case sensitive.
        e.g: {'CPU': ["Platinum"], "Size":[32,128]} will delete all rows that
        contain "Platinum" in the 'cpu' column or 32 or 128 in the
        'param_size' column.

    params_dict : dict
        dict of the form {param_name: value}

    Returns
    -------
    df : Dataframe
        filtered dataframe
    """
    if filters:
        columns = list(df.columns)
        tmp_filters = {}

        # create dict with correct keys from substring
        for col in columns:
            for f_key, f_item in filters.items():
                if f_key.lower() in col.lower():
                    tmp_filters[col] = f_item

        if tmp_filters:
            # Filter data
            for tmp_key, tmp_item in tmp_filters.items():
                for item in tmp_item:
                    if df[tmp_key].dtype == 'object':
                        df = df[~df[tmp_key].str.contains(item)]
                    else:
                        df = df[~(df[tmp_key] == item)]
        else:
            warning = "filter doesn correspond to any column for"
            warning += key
            warning += ", plotting anyway"
            warnings.warn(warning)

    return df


def sort_params(
     df, line_sep=None, filters=None,
     col_filters=None, exclude=None):
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

    filters : dict
        dict of the form {param_name: [values]}, filters the data by the
        given values for each parameter. Won't filter if the parameter doesn't
        apply to a give operation
        e.g: {param_size: [16,128]; param_density: [sparse]} will filter by
        size and density for operations but only by size for solvers,
        as solver benchmarks do not have a density parameter.

    col_filters : dict
        dict of the form {column_name: [deleted_values]}, filters the data by
        the given values for each columns, the name is can be a substring of
        the column and is not case sensitive.
        e.g: {'CPU': ["Platinum"], "Size":[32,128]} will delete all rows that
        contain "Platinum" in the 'cpu' column or 32 or 128 in the
        'param_size' column.

    exclude : list
        List of params not to be used as plot separators, by default will use
        all, of them except those specified in line_sep.

    Returns
    -------
    data : dict
        Nested Dictionnary of the form {"operation-param_1-param_2-...":
        {data: dataframe; line_sep: str}}. line_sep = None if the parameter
        wasn't specified.

    separators : list
        List of the exact parameter names used as line separators.
    """

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
                    if sep.lower() in param.lower():
                        separator = param
                # remove separator parameter from parameter list
                if separator in params:
                    params.remove(separator)

        # drop excluded parameters
        if exclude:
            # find the full param name from the initial substrings
            for ex in exclude:
                for param in params:
                    if ex.lower() in param.lower():
                        excluded = param
                # remove excluded parameter from parameter list
                if excluded in params:
                    params.remove(excluded)

        if params:
            # create dataframe grouped by the remaining params
            for plot_params, plot_df in df[op].groupby(params):
                # handle single parameter case
                if type(plot_params) is not tuple:
                    plot_params = (plot_params,)

                # create dict of parameters and their value
                # in this iteration
                dict_params = dict(zip(params, plot_params))

                key = [op] + list(dict_params.values())
                key = "-".join([str(item) for item in key])

                # add data to output only if param value exists
                #  in the filter
                if param_filtering(filters, dict_params, key):
                    plot_df = column_filtering(plot_df, col_filters, key)
                    data[key] = {
                        "data": plot_df,
                        "line_sep": separator
                    }
        else:
            key = [op]
            key = "-".join([str(item) for item in key])
            if filters:
                warning = "no parameter to apply filters to"
                warning += key
                warning += ", plotting anyway"
                warnings.warn(warning)
            plot_df = column_filtering(df[op], col_filters, key)
            data[key] = {
                "data": plot_df,
                "line_sep": separator
            }

    return data


def get_x_y_axes(cols, x_axis, y_axis):
    """Replaces given x and y axes substrings with the exact name of the
    corresponding column

    Parameters
    ----------
    cols : list
        lsit of all available column names

    x_axis : str
        substring contained in the column name to be used as the
        x axis

    y_axis : str
        substring contained in the column name to be used as the
        y axis

    Returns
    -------
    x_axis : str
        Exact column name to be used as the x axis

    y_axis : str
        Exact column name to be used as the y axis

    """
    x_matching = [col for col in cols if x_axis.lower() in col.lower()]
    if len(x_matching) > 1:
        raise Exception("Given x_axis corresponds to more than 1 column")
    if len(x_matching) == 0:
        raise Exception("Given x_axis doesn correspond to any columns ")
    x_axis = "".join(x_matching)

    y_matching = [col for col in cols if y_axis.lower() in col.lower()]
    if len(y_matching) > 1:
        raise Exception("Given x_axis corresponds to more than 1 column")
    if len(y_matching) == 0:
        raise Exception("Given x_axis doesn correspond to any columns ")
    y_axis = "".join(y_matching)

    return x_axis, y_axis


def plot_data(data, x_axis, y_axis, x_log, y_log, path):
    """Plots the contents of the input dict, based on the given line_separators

    Parameters
    ----------
    data : dict
        Nested Dictionnary of the form {"operation-param_1-param_2-...":
        {data: dataframe; line_sep: str/None}}.

    path : str
        location to store the plot folders.

    """
    # create storage folder
    folder = Path(f"{path}")
    folder.mkdir(parents=True, exist_ok=True)

    # Set colors and markers for legend
    colors = [
        "blue", "orange", "green",
        "red", "black", "gray",
        "pink", "purple", "cyan"]
    markers = ['o--', 'x-', 'v:', "1-.", "*:"]
    i = 0
    for plot in data:

        line_sep = data[plot]["line_sep"]
        df = data[plot]["data"]
        cols = list(df.columns)
        x_axis, y_axis = get_x_y_axes(cols, x_axis, y_axis)

        # Create figure
        fig, ax = plt.subplots(1, 1)

        fig.suptitle(plot, fontsize=20)
        fig.set_size_inches(9, 9)

        # Separation by cpu and line_sep
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
                                gr[x_axis], gr[y_axis],
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
                            gr[x_axis], gr[y_axis],
                            'o--', color=colors[i]
                            )

            # Generate legend
            def f(m, c):
                return plt.plot([], [], m, color=c)[0]
            handles = [f("s", colors[i]) for i in range(len(labels))]
            ax.legend(handles, labels)

        ax.set_xlabel(x_axis)
        ax.set_ylabel("time (s)")
        if y_log:
            ax.set_yscale('log')
        if x_log:
            ax.set_xscale('log')

        fig.tight_layout()
        if x_axis == "datetime":
            plt.gcf().autofmt_xdate()
        plt.savefig(f"{folder}/{plot}.png", bbox_inches='tight')
        plt.close()


def default_nightly_plots(plot_path, bench_path):
    """Function to plot nightly benchmarks for all operation with
    default settings"""
    plot_path = Path(plot_path)
    bench_path = Path(bench_path)
    line_sep = ["type", "model"]
    param_sep = {"size" : [32,128,512]}

    paths = get_paths(bench_path)
    data = create_dataframe(paths)
    data = sort_ops(data)
    data = sort_params(
        data, line_sep,
        param_sep,
        col_filters={'cpu': ["E5"]}
        )
    plot_data(
        data, "datetime", "stats_mean",
        False, True, plot_path)


def default_scaling_plots(plot_path, bench_path):
    """Function to plot scaling benchmarks for all operation with
    default settings"""
    plot_path = Path(plot_path)
    bench_path = Path(bench_path)
    line_sep = ["type", "model"]

    path = get_paths(bench_path)[-1]
    data = json_to_dataframe(path)
    data = sort_ops(data)
    data = sort_params(
        data, line_sep,
        exclude=["size"]
    )
    plot_data(
        data, 'size', 'stats_mean',
        True, True, plot_path)
