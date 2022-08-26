import json
import pandas as pd
import matplotlib.pyplot as plt
import glob
from pathlib import Path
import argparse
from view_nightly_benchmarks import (json_to_dataframe,
                                     sort_ops,
                                     sort_params,
                                     plot_data, sort_ops)


def get_latest_benchmark_path(folder):
    """Returns a list of paths to all benchmark runs

    Parameters
    ----------
    folder : str
        path to the benchmarks folder

    Returns
    -------
    Paths : Path
        Path to the latest bencchmark
    """

    benchmark_paths = glob.glob(f"{folder}/*/*.json")
    dates = [''.join(_b.split("/")[-1].split('_')[2:4])
             for _b in benchmark_paths]
    benchmarks = {date: value for date, value in zip(dates, benchmark_paths)}

    dates.sort()
    latest = dates[-1]
    benchmark_latest = benchmarks[latest]

    return benchmark_latest


def main(args=[]):
    parser = argparse.ArgumentParser(description="""Choose what to plot and
                    where to store it, by default all benchmarks will be
                    plotted using default size and dimensions""")
    parser.add_argument('--plotpath', default="./images/scaling", type=Path,
                        help="""Path to folder in which the plots will be
                        stored""")
    parser.add_argument('--benchpath', default="./.benchmarks", type=Path,
                        help="""Path to folder in which the benchmarks are
                        stored""")
    parser.add_argument('--density', nargs="?", default=None, type=str,
                        help="""Density the matrices on which the
                        operations will be performed in the history benchmarks,
                        values: 'sparse' or 'dense'
                        WARNING: If a parameter is used as line_sep it cannot
                        be used as a filter""")
    parser.add_argument('--operations', nargs="+", default=None, type=str,
                        help="""Specify which operations to plot, plots all by
                        default or if nothing specified""")
    parser.add_argument('--line_sep', nargs="*", default=None, type=str,
                        help="""Specify which parameter should be used
                        to separate line on the plot instead of separating the
                        plots. default=None, ['type', 'model'] if nothing
                        specified
                        WARNING: If a parameter is used as line_sep it cannot
                        be used as a filter""")
    parser.add_argument('--dtype', nargs="+", default=None, type=str,
                        help="""Specify which dtypes to plot, plots all by
                        default or if nothing specified
                        Only applies to linear algebra benchmarks
                        WARNING: If a parameter is used as line_sep it cannot
                        be used as a filter""")
    parser.add_argument('--model', nargs="+", default=None, type=str,
                        help="""Specify which models to plot, plots all by
                        default or if nothing specified
                        Only applies to solver benchmarks
                        WARNING: If a parameter is used as line_sep it cannot
                        be used as a filter""")
    parser.add_argument('--coeftype', nargs="+", default=None, type=str,
                        help="""Specify which coefficient types to plot, plots
                        all by default or if nothing specified
                        Only applies to QobjEvo benchmarks
                        WARNING: If a parameter is used as line_sep it cannot
                        be used as a filter""")

    args = parser.parse_args()
    param_filters = None
    line_sep = None

    # because const isn't available for nargs="*"
    if args.line_sep is not None and not args.line_sep:
        args.line_sep = ['type', 'model']

    # create param_filter dict if called
    if (args.density or args.model
       or args.dtype or args.coeftype):
        param_filters = {}
        if args.density:
            param_filters["density"] = args.density
        if args.dtype:
            param_filters["dtype"] = args.dtype
        if args.model:
            param_filters["model"] = args.model
        if args.coeftype:
            param_filters["coeftype"] = args.coeftype

    if args.line_sep:
        line_sep = args.line_sep

    # fetch data
    path = get_latest_benchmark_path(args.benchpath)
    data = json_to_dataframe(path)
    data = sort_ops(data, args.operations)
    data = sort_params(
        data, line_sep=line_sep,
        filters=param_filters, exclude=["size"]
        )
    plot_data(data, 'size', args.plotpath)


if __name__ == '__main__':
    main()
