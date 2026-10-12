# Name Sorter

A Python command-line application that sorts names by last name, then by
given names. It prints the results and writes them to
`sorted-names-list.txt` in the current working directory.

Requires Python 3.12 or newer. The application has no runtime dependencies.

## Setup

Run these commands from the repository root.

### Windows PowerShell

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
.\.venv\Scripts\name-sorter.exe .\unsorted-names-list.txt
```

These commands use the virtual environment directly, so activation is
not required.

### Linux or macOS

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -e ".[dev]"
.venv/bin/name-sorter ./unsorted-names-list.txt
```

With the virtual environment activated, the command is:

```bash
name-sorter ./unsorted-names-list.txt
```

## Input and sorting rules

- Each nonblank line contains one name.
- A name has one to three given names followed by a last name.
- The final whitespace-separated word is treated as the last name.
- Blank lines are ignored, and extra whitespace is normalized.
- Names are compared case-insensitively using Unicode case folding.
- Given names are compared individually, in their original sequence.
- Names with equal sorting keys retain their input order.
- Duplicates, spelling, capitalization, accents, and punctuation are preserved.
- Input must be UTF-8; a UTF-8 byte-order mark is also supported.

Sorting is deterministic and does not use language-specific collation.
Compound last names containing spaces are outside the assumed input format.

The assessment input contains `Vaugh Lewis`, while its example output
contains `Vaughn Lewis`. This application preserves `Vaugh Lewis`.

## Output and errors

Successful runs print only the sorted names and overwrite
`sorted-names-list.txt` in the current working directory.

The output uses UTF-8 and LF line endings. Empty input creates an empty
output file.

Errors go to standard error. Invalid names include the input path and
original line number. All input is validated before writing, so invalid
input leaves an existing output file unchanged.

Exit codes:

- `0`: success
- `1`: input validation, encoding, or file access error
- `2`: invalid command-line arguments

## Design

- `names.py` contains the immutable name model, validation, and sorting.
- `file_io.py` handles reading and writing files.
- `cli.py` handles arguments, coordinates operations, and reports errors.

Separating these responsibilities keeps sorting independent of file
handling and makes each part easier to understand and test. The CLI
depends on small functions with explicit inputs and outputs.

Comments explain decisions and assumptions. Tests describe expected
behavior through their names and assertions. Additional abstractions
are avoided where they would add complexity without helping this task.

Sorting uses Python's stable built-in sort, with O(n log n) time
complexity and O(n) memory for the bounded-length names in this assessment.

## Tests

On Windows:

```powershell
.\.venv\Scripts\python.exe -m pytest -v
```

On Linux or macOS:

```bash
.venv/bin/python -m pytest -v
```

Tests cover parsing, sorting, file handling, CLI errors, the assessment
example, and the installed command with 1,000 names.

File tests use temporary directories so they do not modify project files.
The 1,000-name test constructs its expected order independently of the
application's sorting function.

## Build and continuous integration

Build the wheel and source archive on Windows:

```powershell
.\.venv\Scripts\python.exe -m build
```

On Linux or macOS:

```bash
.venv/bin/python -m build
```

Packages are created in `dist/`.

The GitHub Actions workflow runs tests and builds distribution packages
on Windows and Linux for pushes and pull requests. It can also be
started manually from the Actions tab.