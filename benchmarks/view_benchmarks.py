from pathlib import Path
import argparse
import view_funcs

def main():
    """View historical performance of nightly benchmarks"""
    parser = argparse.ArgumentParser(description="""Choose what to plot and
                    where to store it, by default all benchmarks will be
                    plotted using default size and dimensions""")
    parser.add_argument('--plotpath', default="./images", type=Path,
                        help="""Path to folder in which the plots will be
                        stored""")
    parser.add_argument('--benchpath', default="./.benchmarks", type=Path,
                        help="""Path to folder in which the benchmarks are
                        stored""")
    parser.add_argument('--size', nargs="*", default=None, type=int,
                        help="""Size of the matrices on which the
                        operations will be performed in the history benchmarks,
                        has to be a power of 2, max=256, min=4,
                        default=None, [32,128] if nothing specified
                        WARNING: If a parameter is used as line_sep it cannot
                        be used as a filter""")
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
    parser.add_argument('--scaling', action='store_true',
                        help="""Run scaling benchmarks instead of history
                        benchmarks.
                        WARNING:cannot filter by size if used""")

    args = parser.parse_args()
    param_filters = None
    line_sep = None

    # because const isn't available for nargs="*"
    if args.size is not None and not args.size:
        args.size = [32, 128]
    if args.line_sep is not None and not args.line_sep:
        args.line_sep = ['type', 'model']

    # create param_filter dict if called
    if (args.density or args.size or args.model
       or args.dtype or args.coeftype):
        param_filters = {}
        if args.density:
            param_filters["density"] = args.density
        if args.size:
            param_filters["size"] = args.size
        if args.dtype:
            param_filters["dtype"] = args.dtype
        if args.model:
            param_filters["model"] = args.model
        if args.coeftype:
            param_filters["coeftype"] = args.coeftype

    if args.line_sep:
        line_sep = args.line_sep

    if not args.scaling:
        if args.plotpath == Path('images'):
            args.plotpath = args.plotpath / 'nightly'
        paths = view_funcs.get_paths(args.benchpath)
        data = view_funcs.create_dataframe(paths)
        data = view_funcs.sort_ops(data, args.operations)
        data = view_funcs.sort_params(
            data, line_sep,
            filters=param_filters,
            col_filters={'cpu': ["E5"]}
            )
        view_funcs.plot_data(data, "datetime", "stats_mean", False, True, args.plotpath)
    else:
        if args.plotpath == Path('images'):
            args.plotpath = args.plotpath / 'scaling'
        path = view_funcs.get_latest_benchmark_path(args.benchpath)
        data = view_funcs.json_to_dataframe(path)
        data = view_funcs.sort_ops(data, args.operations)
        data = view_funcs.sort_params(
            data, line_sep,
            filters=param_filters,
            exclude=["size"]
        )
        view_funcs.plot_data(data, 'size', 'stats_mean', True, True, args.plotpath)


if __name__ == '__main__':
    main()
