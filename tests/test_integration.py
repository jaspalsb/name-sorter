import shutil
import subprocess
import sysconfig
from name_sorter.cli import main


def test_assessment_example_matches_expected_output(
    tmp_path, monkeypatch, capsys
):
    source = tmp_path / "unsorted-names-list.txt"
    source.write_text(
        "Janet Parsons\n"
        "Vaugh Lewis\n"
        "Adonis Julius Archer\n"
        "Shelby Nathan Yoder\n"
        "Marin Alvarez\n"
        "London Lindsey\n"
        "Beau Tristan Bentley\n"
        "Leo Gardner\n"
        "Hunter Uriah Mathew Clarke\n"
        "Mikayla Lopez\n"
        "Frankie Conner Ritter\n",
        encoding="utf-8",
    )
    monkeypatch.chdir(tmp_path)

    exit_code = main([str(source)])

    #preserve Vaugh from the input; the assessment output appears to contain a typo
    expected = (
        "Marin Alvarez\n"
        "Adonis Julius Archer\n"
        "Beau Tristan Bentley\n"
        "Hunter Uriah Mathew Clarke\n"
        "Leo Gardner\n"
        "Vaugh Lewis\n"
        "London Lindsey\n"
        "Mikayla Lopez\n"
        "Janet Parsons\n"
        "Frankie Conner Ritter\n"
        "Shelby Nathan Yoder\n"
    )
    captured = capsys.readouterr()

    assert exit_code == 0
    assert captured.out == expected
    assert captured.err == ""
    assert (tmp_path / "sorted-names-list.txt").read_bytes() == (
        expected.encode("utf-8")
    )


def test_installed_command_sorts_one_thousand_names(tmp_path):
    #ask python where commands are installed because the layout varies by environment
    scripts_directory = sysconfig.get_path("scripts")
    command = shutil.which("name-sorter", path=scripts_directory)

    assert command is not None, (
        f"name-sorter was not found in {scripts_directory}. "
        'Install the project first with: python -m pip install -e ".[dev]"'
    )

    #fixed-width numbers give us a predictable order without calling our sorter
    expected_names = [
        f"Given{given:03d} Family{family:03d}"
        for family in range(20)
        for given in range(50)
    ]
    source = tmp_path / "thousand-names.txt"
    source.write_text(
        "\n".join(reversed(expected_names)) + "\n",
        encoding="utf-8",
    )

    result = subprocess.run(
        [command, str(source)],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=15,
        check=False,
    )

    expected = "\n".join(expected_names) + "\n"

    assert result.returncode == 0, result.stderr
    assert result.stderr == ""
    assert result.stdout == expected
    assert (tmp_path / "sorted-names-list.txt").read_bytes() == (
        expected.encode("utf-8")
    )