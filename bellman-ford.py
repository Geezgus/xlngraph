import argparse
from xlngraph.graph import Graph


def main():
    args = parse_args()

    G = Graph.from_csv(
        filename=args.input,
        source_column="source",
        destination_column="destination",
        weight_column="weight",
    )

    distance = G.bellman_ford(args.S)

    for k, v in distance.items():
        print(f"{k}: {v}")


def parse_args():
    parser = argparse.ArgumentParser(
        prog="bellman-ford",
        description="Calculate the shortest path from a source vertex S to every other, in a directed graph G",
        epilog="Thank you!",
    )

    parser.add_argument(
        "input",
        help="CSV file containing [source destination weight] columns",
        type=str,
    )

    parser.add_argument(
        "S",
        help="Source vertex",
        type=str,
    )

    return parser.parse_args()


if __name__ == "__main__":
    main()
