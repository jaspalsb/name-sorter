from collections.abc import Iterable
from dataclasses import dataclass


#keep names immutable so their values cannot change between parsing and sorting
@dataclass(frozen=True)
class PersonName:
    """A name containing one to three given names and a last name."""

    given_names: tuple[str, ...]
    last_name: str

    def __post_init__(self) -> None:
        #validate here too because callers can create PersonName without parsing
        if not 1 <= len(self.given_names) <= 3:
            raise ValueError(
                "expected 1–3 given names and a last name"
            )

        #each field represents one word; parsing handles whitespace between words
        for part in (*self.given_names, self.last_name):
            if not part or any(character.isspace() for character in part):
                raise ValueError(
                    "each name part must be nonempty and contain no whitespace"
                )

    @property
    def full_name(self) -> str:
        """Return the name with single spaces between its parts."""
        return " ".join((*self.given_names, self.last_name))


def parse_name(text: str) -> PersonName:
    """Parse a full name, raising ValueError if it has fewer than two or more than four parts."""

    #split handles repeated spaces and tabs while preserving spelling and case
    parts = text.split()

    if not 2 <= len(parts) <= 4:
        raise ValueError(
            "expected 1–3 given names and a last name"
        )

    #the assessment treats the final word as the last name
    return PersonName(
        given_names=tuple(parts[:-1]),
        last_name=parts[-1],
    )
def sort_names(names: Iterable[PersonName]) -> list[PersonName]:
    """Return a new list sorted by last name, then given names."""

    #casefold allows case-insensitive comparison without changing displayed names
    #compare given names separately so shorter matching names come first
    return sorted(
        names,
        key=lambda name: (
            name.last_name.casefold(),
            tuple(part.casefold() for part in name.given_names),
        ),
    )