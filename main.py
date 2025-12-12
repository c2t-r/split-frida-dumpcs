import sys

from src.dumpcs import Dumpcs


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: uv run main.py <dump.cs> [output_dir]")
        sys.exit(1)

    path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "dump"

    print(f"Loading: {path}")
    dcs = Dumpcs(path)

    print(f"Splitting to: {output_dir}/")
    dcs.split(output_dir)


if __name__ == "__main__":
    main()
