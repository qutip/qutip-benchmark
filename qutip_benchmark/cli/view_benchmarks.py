import argparse
from qutip_benchmark.view_utilities import default_nightly_plots, default_scaling_plots


def main():
    """View historical performance of nightly benchmarks"""
    parser = argparse.ArgumentParser(
        description="""Choose what to plot and
                    where to store it, by default all benchmarks will be
                    plotted using default size and dimensions"""
    )
    parser.add_argument(
        "--plotpath",
        default=None,
        type=str,
        help="""Path to folder in which the plots will be
                        stored.
                        By default separates nightly and scaling into
                        './images/plots/scaling' and './images/plots/nightly'
                        if you want them to be separated with a custom path
                        you will need to run this file twice using the
                        --scaling and --nightly flags and the desired path""",
    )
    parser.add_argument(
        "--benchpath",
        default="./.benchmarks",
        type=str,
        help="""Path to folder in which the benchmarks are
                        stored""",
    )
    parser.add_argument(
        "--scaling",
        action="store_true",
        help="""Run only scaling benchmarks.""",
    )
    parser.add_argument(
        "--nightly",
        action="store_true",
        help="""Run only nightly benchmarks.""",
    )

    args = parser.parse_args()

    if args.plotpath:
        scaling_path = nightly_path = args.plotpath
    else:
        scaling_path = "./images/plots/scaling"
        nightly_path = "./images/plots/nightly"

    if (args.scaling and args.nightly) or not (args.scaling or args.nightly):
        default_scaling_plots(scaling_path, args.benchpath)
        default_nightly_plots(nightly_path, args.benchpath)
    elif args.scaling:
        default_scaling_plots(scaling_path, args.benchpath)
    else:
        default_nightly_plots(nightly_path, args.benchpath)


if __name__ == "__main__":
    main()
