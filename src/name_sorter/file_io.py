from collections.abc import Iterable
from pathlib import Path

from name_sorter.names import PersonName, parse_name


def read_names(path: Path) -> list[PersonName]:
    """Read names from a UTF-8 file, reporting invalid names by line number."""
    names = []

    #utf-8-sig also accepts files with a byte-order mark from windows editors
    with path.open("r", encoding="utf-8-sig") as source:
        for line_number, line in enumerate(source, start=1):
            #blank lines are not names, but still count toward error line numbers
            if not line.strip():
                continue

            try:
                names.append(parse_name(line))
            except ValueError as error:
                #include the file and line so the user can locate the problem
                raise ValueError(
                    f"{path}: invalid name on line {line_number}: {error}"
                ) from error

    return names


def write_names(path: Path, names: Iterable[PersonName]) -> None:
    """Write names to a UTF-8 file, replacing any existing contents."""

    #use consistent line endings so output is the same on windows and linux
    with path.open("w", encoding="utf-8", newline="\n") as destination:
        for name in names:
            destination.write(f"{name.full_name}\n")