"""Report GC content for each record in a FASTA file."""

import argparse
import sys


def read_fasta_records(path):
    """Yield each FASTA header and its assembled sequence."""
    header = None
    sequence = []

    with open(path, encoding="utf-8") as fasta:
        for line in fasta:
            line = line.strip()
            if not line:
                continue
            if line.startswith(">"):
                if header is not None:
                    yield header, "".join(sequence)
                header = line
                sequence = []
            elif header is None:
                raise ValueError("Sequence data encountered before a FASTA header")
            else:
                sequence.append(line)

    if header is not None:
        yield header, "".join(sequence)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("fasta_file", help="path to a FASTA file")
    parser.add_argument(
        "--min-gc",
        type=float,
        help="only print records with GC content above this percentage",
    )
    args = parser.parse_args()

    for header, sequence in read_fasta_records(args.fasta_file):
        if not sequence:
            print(f"Warning: skipping empty sequence for {header}", file=sys.stderr)
            continue
        gc_percent = (sequence.upper().count("G") + sequence.upper().count("C")) / len(
            sequence
        ) * 100
        if args.min_gc is not None and gc_percent <= args.min_gc:
            continue
        print(f"{header}\t{gc_percent:.2f}%")


if __name__ == "__main__":
    main()
