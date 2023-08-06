import argparse
from pynextgen.basics_counts import clean_feature_counts
from pynextgen.utils import simplify_outpath
from pynextgen.version import __version__


def parse_arguments():
    parser = argparse.ArgumentParser(
        description=f"""{'='*60}
Clean FeatureCounts table (pynextgen {__version__}).
{'='*60}

Simplify the table created by featureCount to use it in downstream analysis (DESEQ2,...).
Create a "*_clean.csv" table.
""",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "counts", help="A count table obtained from subread featureCounts."
    )
    parser.add_argument(
        "--extra_name_rm",
        nargs="+",
        default=[],
        help="A string of character to remove from the library names (in column names in the featureCounts table)",
    )

    return parser.parse_args()


def main():
    args = parse_arguments()

    df = clean_feature_counts(args.counts, extra_name_rm=args.extra_name_rm)
    outfile = simplify_outpath(args.counts, suffix="_clean.csv", keep_path=True)
    df.to_csv(outfile)


if __name__ == "__main__":
    main()
