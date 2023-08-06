import argparse
import sys
from pynextgen.divtrans import DivTransFromBam
from pynextgen.version import __version__


def parse_arguments():
    parser = argparse.ArgumentParser(
        description=f"""
{'='*60}
Divergent Transcription (pynextgen {__version__}).
{'='*60}

Detect divergent transcription events from rf-stranded, paired-end RNA-seq alignments.

Create a bed file with the divergent transcription events annotated as bed intervals.
""",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "bam", help="A coordinate sorted bam to detect divergent transcription from."
    )
    parser.add_argument(
        "-d",
        "--distance",
        type=int,
        default=100,
        help="The maximum distance between two divergent reads to take into account a divergent transcription event.",
    )
    parser.add_argument(
        "--max_template_size",
        type=int,
        default=500,
        help="The maximum template size for a pair of reads.",
    )
    parser.add_argument(
        "--include_overlaps",
        action="store_true",
        default=False,
        help="Include events where divergent reads are overlapping. Excluded by default.",
    )
    parser.add_argument(
        "--include_gl_contigs",
        action="store_true",
        default=False,
        help="Include the 'GL_contigs' found sometimes in assemblies in the analysis. Excluded by default.",
    )
    parser.add_argument(
        "-f",
        "--filter_by_counts",
        action="store_true",
        default=False,
        help="Create an additional bed file with the intervals filtered according to surrounding read coverage",
    )
    parser.add_argument(
        "-c",
        "--chro_sizes",
        help="Path to chromosome sizes file for bedtools flank",
        required=any(arg in sys.argv for arg in ["-f", "--filter_by_counts"]),
    )
    parser.add_argument(
        "--flank",
        type=int,
        default=500,
        help="The number of bases to consider upstream and downstream of a divergent transcription event for count calculations (filtering option).",
    )
    parser.add_argument(
        "--count_thres",
        type=int,
        default=5,
        help="The minimum counts which has to be observed upstream and downstream of divergent transcription events to be considered (filtering option).",
    )
    parser.add_argument(
        "--count_ratio_thres",
        type=float,
        default=1,
        help="The minimum ratio for both transcription ratios: -/+ upstream and +/- downstream (filtering option).",
    )
    parser.add_argument(
        "-t",
        "--threads",
        type=int,
        default=1,
        help="Number of threads to use for count based filtering (filtering option).",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"pynextgen {__version__}",
        help="Display current version.",
    )

    return parser.parse_args()


def main():

    args = parse_arguments()

    divtrans = DivTransFromBam(
        args.bam,
        distance=args.distance,
        no_overlap=args.include_overlaps,
        remove_GL_contigs=args.include_gl_contigs,
    )
    divtrans.run()

    if args.filter_by_counts:
        divtrans.filter_by_counts(
            args.chro_sizes,
            flank=args.flank,
            count_thres=args.count_thres,
            count_ratio_thres=args.count_ratio_thres,
            threads=args.threads,
        )


if __name__ == "__main__":
    main()
