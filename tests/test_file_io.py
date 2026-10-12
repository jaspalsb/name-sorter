import pytest

from name_sorter.file_io import read_names, write_names
from name_sorter.names import parse_name


def test_read_names_preserves_the_order_in_the_file(tmp_path):
    source = tmp_path / "names.txt"
    source.write_text(
        "Janet Parsons\nAdonis Julius Archer\n",
        encoding="utf-8",
    )

    result = read_names(source)

    assert result == [
        parse_name("Janet Parsons"),
        parse_name("Adonis Julius Archer"),
    ]


def test_read_names_skips_blank_lines_and_normalizes_whitespace(tmp_path):
    source = tmp_path / "names.txt"
    source.write_text(
        "\n  Janet   Parsons  \n \t \nMarin Alvarez\n",
        encoding="utf-8",
    )

    result = read_names(source)

    assert result == [
        parse_name("Janet Parsons"),
        parse_name("Marin Alvarez"),
    ]


def test_read_names_reports_the_file_and_original_line_number(tmp_path):
    source = tmp_path / "names.txt"
    source.write_text(
        "Janet Parsons\n\nInvalid\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError) as raised:
        read_names(source)

    assert str(raised.value) == (
        f"{source}: invalid name on line 3: "
        "expected 1–3 given names and a last name"
    )


def test_read_names_accepts_a_utf8_byte_order_mark(tmp_path):
    source = tmp_path / "names.txt"
    source.write_text("Élodie O'Neill\n", encoding="utf-8-sig")

    result = read_names(source)

    assert result == [parse_name("Élodie O'Neill")]


def test_read_names_accepts_a_final_line_without_a_newline(tmp_path):
    source = tmp_path / "names.txt"
    source.write_text("Janet Parsons", encoding="utf-8")

    assert read_names(source) == [parse_name("Janet Parsons")]


def test_read_names_returns_an_empty_list_for_an_empty_file(tmp_path):
    source = tmp_path / "names.txt"
    source.write_text("", encoding="utf-8")

    assert read_names(source) == []


def test_read_names_reports_a_missing_file(tmp_path):
    with pytest.raises(FileNotFoundError):
        read_names(tmp_path / "missing.txt")


def test_read_names_reports_invalid_utf8(tmp_path):
    source = tmp_path / "names.txt"
    source.write_bytes(b"\xff\xfe")

    with pytest.raises(UnicodeDecodeError):
        read_names(source)


def test_write_names_writes_utf8_with_one_name_per_line(tmp_path):
    destination = tmp_path / "sorted-names-list.txt"
    names = [
        parse_name("Marin Alvarez"),
        parse_name("Élodie O'Neill"),
    ]

    write_names(destination, names)

    assert destination.read_bytes() == (
        "Marin Alvarez\nÉlodie O'Neill\n".encode("utf-8")
    )


def test_write_names_replaces_existing_contents(tmp_path):
    destination = tmp_path / "sorted-names-list.txt"
    destination.write_text(
        "old contents that should be removed\n",
        encoding="utf-8",
    )

    write_names(destination, [parse_name("Janet Parsons")])

    assert destination.read_bytes() == b"Janet Parsons\n"


def test_write_names_creates_an_empty_file_for_no_names(tmp_path):
    destination = tmp_path / "sorted-names-list.txt"

    write_names(destination, [])

    assert destination.read_bytes() == b""


def test_write_names_accepts_a_generator(tmp_path):
    destination = tmp_path / "sorted-names-list.txt"
    names = (
        parse_name(text)
        for text in ["Marin Alvarez", "Janet Parsons"]
    )

    write_names(destination, names)

    assert destination.read_bytes() == (
        b"Marin Alvarez\nJanet Parsons\n"
    )