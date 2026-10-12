from name_sorter.cli import main


def test_cli_prints_sorted_names_and_writes_them_in_working_directory(
    tmp_path, monkeypatch, capsys
):
    input_folder = tmp_path / "input"
    input_folder.mkdir()
    source = input_folder / "names.txt"
    source.write_text(
        "Janet Parsons\nMarin Alvarez\nAdonis Julius Archer\n",
        encoding="utf-8",
    )
    monkeypatch.chdir(tmp_path)

    exit_code = main([str(source)])

    captured = capsys.readouterr()
    expected = (
        "Marin Alvarez\n"
        "Adonis Julius Archer\n"
        "Janet Parsons\n"
    )

    assert exit_code == 0
    assert captured.out == expected
    assert captured.err == ""
    assert (tmp_path / "sorted-names-list.txt").read_bytes() == (
        expected.encode("utf-8")
    )
    assert not (input_folder / "sorted-names-list.txt").exists()


def test_cli_overwrites_an_existing_output_file(
    tmp_path, monkeypatch, capsys
):
    source = tmp_path / "names.txt"
    source.write_text("Janet Parsons\n", encoding="utf-8")
    destination = tmp_path / "sorted-names-list.txt"
    destination.write_text("previous results\n", encoding="utf-8")
    monkeypatch.chdir(tmp_path)

    exit_code = main([str(source)])

    assert exit_code == 0
    assert destination.read_bytes() == b"Janet Parsons\n"
    assert capsys.readouterr().out == "Janet Parsons\n"


def test_cli_reports_invalid_input_without_overwriting_previous_results(
    tmp_path, monkeypatch, capsys
):
    source = tmp_path / "names.txt"
    source.write_text("Janet Parsons\nInvalid\n", encoding="utf-8")
    destination = tmp_path / "sorted-names-list.txt"
    destination.write_text("previous results\n", encoding="utf-8")

    #compare the original bytes so this checks preservation on any platform
    original_contents = destination.read_bytes()
    monkeypatch.chdir(tmp_path)

    exit_code = main([str(source)])

    captured = capsys.readouterr()

    assert exit_code == 1
    assert captured.out == ""
    assert "invalid name on line 2" in captured.err
    assert destination.read_bytes() == original_contents


def test_cli_reports_a_missing_input_file(
    tmp_path, monkeypatch, capsys
):
    source = tmp_path / "missing.txt"
    monkeypatch.chdir(tmp_path)

    exit_code = main([str(source)])

    captured = capsys.readouterr()

    assert exit_code == 1
    assert captured.out == ""
    assert "could not access" in captured.err
    assert str(source) in captured.err
    assert not (tmp_path / "sorted-names-list.txt").exists()


def test_cli_reports_invalid_utf8(
    tmp_path, monkeypatch, capsys
):
    source = tmp_path / "names.txt"
    source.write_bytes(b"\xff\xfe")
    monkeypatch.chdir(tmp_path)

    exit_code = main([str(source)])

    captured = capsys.readouterr()

    assert exit_code == 1
    assert captured.out == ""
    assert "not a valid UTF-8 text file" in captured.err
    assert not (tmp_path / "sorted-names-list.txt").exists()


def test_cli_reports_an_output_file_error(
    tmp_path, monkeypatch, capsys
):
    source = tmp_path / "names.txt"
    source.write_text("Janet Parsons\n", encoding="utf-8")

    #a directory at the output path reliably causes a write error on both platforms
    (tmp_path / "sorted-names-list.txt").mkdir()
    monkeypatch.chdir(tmp_path)

    exit_code = main([str(source)])

    captured = capsys.readouterr()

    assert exit_code == 1
    assert captured.out == ""
    assert "could not access" in captured.err
    assert "sorted-names-list.txt" in captured.err


def test_cli_handles_an_empty_input_file(
    tmp_path, monkeypatch, capsys
):
    source = tmp_path / "names.txt"
    source.write_text("", encoding="utf-8")
    monkeypatch.chdir(tmp_path)

    exit_code = main([str(source)])

    captured = capsys.readouterr()

    assert exit_code == 0
    assert captured.out == ""
    assert captured.err == ""
    assert (tmp_path / "sorted-names-list.txt").read_bytes() == b""