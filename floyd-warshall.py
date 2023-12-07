import argparse
from pprint import pprint
from xlngraph.graph import Graph


def main():
    args = parse_args()

    G = Graph.from_csv(
        filename=args.input,
        source_column="source",
        destination_column="destination",
        weight_column="weight",
    )

    distances, parent_matrix = G.floyd_warshall()
    print_path(distances, parent_matrix)


def print_path(distances, parent_matrix: dict):
    def recursive(source, val):
        if val is None:
            return val

        recursive(source, parent_matrix[source][val])

        if parent_matrix[source][val] is not None:
            print(" -> ", end="")

        print(val, end="")

    for source, children in parent_matrix.items():
        print("source:", source)

        for child in children:
            recursive(source, child)
            print(f" ({distances[source][child]})")

        print()


def parse_args():
    parser = argparse.ArgumentParser(
        prog="floyd-warshall",
        description="Calculate the shortest path from a source vertex S to every other, in a directed graph G",
        epilog="Thank you!",
    )

    parser.add_argument(
        "input",
        help="CSV file containing [source destination weight] columns",
        type=str,
    )

    return parser.parse_args()


if __name__ == "__main__":
    main()
