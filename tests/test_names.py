import pytest

from name_sorter.names import PersonName, parse_name, sort_names


@pytest.mark.parametrize(
    ("text", "given_names", "last_name"),
    [
        ("Janet Parsons", ("Janet",), "Parsons"),
        ("Adonis Julius Archer", ("Adonis", "Julius"), "Archer"),
        (
            "Hunter Uriah Mathew Clarke",
            ("Hunter", "Uriah", "Mathew"),
            "Clarke",
        ),
    ],
)
def test_parse_name_supports_one_to_three_given_names(
    text, given_names, last_name
):
    name = parse_name(text)

    assert name.given_names == given_names
    assert name.last_name == last_name
    assert name.full_name == text


def test_parse_name_normalizes_extra_whitespace():
    name = parse_name("  Adonis\t Julius   Archer  ")

    assert name.full_name == "Adonis Julius Archer"


def test_parse_name_preserves_capitalization_accents_and_punctuation():
    name = parse_name("Élodie Anne-Marie O'Neill")

    assert name.full_name == "Élodie Anne-Marie O'Neill"


@pytest.mark.parametrize(
    "text",
    [
        "",
        "   ",
        "Janet",
        "One Two Three Four Five",
    ],
)
def test_parse_name_rejects_invalid_number_of_name_parts(text):
    with pytest.raises(
        ValueError,
        match="expected 1–3 given names and a last name",
    ):
        parse_name(text)


@pytest.mark.parametrize(
    "given_names",
    [
        (),
        ("One", "Two", "Three", "Four"),
    ],
)
def test_person_name_rejects_invalid_given_name_count(given_names):
    with pytest.raises(ValueError, match="expected 1–3 given names"):
        PersonName(given_names=given_names, last_name="Smith")


@pytest.mark.parametrize(
    ("given_names", "last_name"),
    [
        (("",), "Smith"),
        (("Mary Jane",), "Smith"),
        (("Janet",), ""),
        (("Janet",), "Van Dyke"),
    ],
)
def test_person_name_rejects_empty_or_whitespace_containing_parts(
    given_names, last_name
):
    with pytest.raises(ValueError, match="each name part"):
        PersonName(given_names=given_names, last_name=last_name)

def test_names_are_sorted_by_last_name_before_given_names():
    names = [
        parse_name("Amy Zane"),
        parse_name("Zoe Adams"),
        parse_name("Ben Miller"),
    ]

    result = sort_names(names)

    assert [name.full_name for name in result] == [
        "Zoe Adams",
        "Ben Miller",
        "Amy Zane",
    ]


def test_names_with_same_last_name_are_sorted_by_given_names():
    names = [
        parse_name("Zoe Smith"),
        parse_name("Amy Zoe Smith"),
        parse_name("Amy Beth Smith"),
        parse_name("Amy Smith"),
    ]

    result = sort_names(names)

    assert [name.full_name for name in result] == [
        "Amy Smith",
        "Amy Beth Smith",
        "Amy Zoe Smith",
        "Zoe Smith",
    ]


def test_sorting_compares_all_three_given_names():
    names = [
        parse_name("Amy Beth Zoe Smith"),
        parse_name("Amy Beth Anne Smith"),
    ]

    result = sort_names(names)

    assert [name.full_name for name in result] == [
        "Amy Beth Anne Smith",
        "Amy Beth Zoe Smith",
    ]


def test_sorting_ignores_case_and_preserves_original_capitalization():
    names = [
        parse_name("bob smith"),
        parse_name("Zoe adams"),
        parse_name("Alice SMITH"),
    ]

    result = sort_names(names)

    assert [name.full_name for name in result] == [
        "Zoe adams",
        "Alice SMITH",
        "bob smith",
    ]


def test_names_with_equal_sorting_keys_keep_their_input_order():
    names = [
        parse_name("amy Smith"),
        parse_name("Amy SMITH"),
    ]

    result = sort_names(names)

    assert [name.full_name for name in result] == [
        "amy Smith",
        "Amy SMITH",
    ]


def test_sorting_preserves_duplicate_names():
    names = [
        parse_name("Janet Parsons"),
        parse_name("Marin Alvarez"),
        parse_name("Janet Parsons"),
    ]

    result = sort_names(names)

    assert [name.full_name for name in result] == [
        "Marin Alvarez",
        "Janet Parsons",
        "Janet Parsons",
    ]


def test_sorting_does_not_change_the_original_list():
    names = [
        parse_name("Janet Parsons"),
        parse_name("Marin Alvarez"),
    ]
    original_names = names.copy()

    result = sort_names(names)

    assert names == original_names
    assert result is not names
    assert result == [
        parse_name("Marin Alvarez"),
        parse_name("Janet Parsons"),
    ]


def test_sorting_an_empty_list_returns_an_empty_list():
    assert sort_names([]) == []


def test_sorting_accepts_a_generator():
    names = (
        parse_name(text)
        for text in ["Janet Parsons", "Marin Alvarez"]
    )

    result = sort_names(names)

    assert [name.full_name for name in result] == [
        "Marin Alvarez",
        "Janet Parsons",
    ]