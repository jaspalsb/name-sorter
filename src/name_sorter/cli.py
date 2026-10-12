import argparse
import sys
from collections.abc import Sequence
from pathlib import Path

from name_sorter.file_io import read_names, write_names
from name_sorter.names import sort_names


OUTPUT_FILENAME = "sorted-names-list.txt"


def main(argv: Sequence[str] | None = None) -> int:
    """Run the name sorter, returning zero on success and one on failure."""
    parser = argparse.ArgumentParser(
        description="Sort names by last name, then given names."
    )
    parser.add_argument(
        "input_file",
        type=Path,
        help="path to a UTF-8 file containing one name per line",
    )
    args = parser.parse_args(argv)

    #the assessment requires output in the working directory, not the input folder
    output_path = Path.cwd() / OUTPUT_FILENAME

    try:
        #finish reading and validating before opening the output file
        names = read_names(args.input_file)
        sorted_names = sort_names(names)
        write_names(output_path, sorted_names)
    except UnicodeDecodeError:
        print(
            f"Error: '{args.input_file}' is not a valid UTF-8 text file.",
            file=sys.stderr,
        )
        return 1
    except ValueError as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    except OSError as error:
        #include the affected path for both input and output file errors
        affected_path = error.filename or str(args.input_file)
        print(
            f"Error: could not access '{affected_path}': {error.strerror}",
            file=sys.stderr,
        )
        return 1

    #print results only after the output file has been written successfully
    for name in sorted_names:
        print(name.full_name)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())