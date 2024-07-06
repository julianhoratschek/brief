import re


class Medication:
    def __init__(self, name: str, amount: str = "", unit: str = "", taken: list[str] | None = None):
        self.name: str = name
        self.amount: str = amount
        self.unit: str = unit
        self.taken: list[str] | None = taken

    def destructure_taken(self) -> tuple[str, str, str, str]:
        if self.taken is None:
            return '', '', '', ''

        for _ in range(len(self.taken), 4):
            self.taken.append('0')

        return self.taken[0], self.taken[1], self.taken[2], self.taken[3]

    def times(self) -> dict[str, str]:
        return dict(zip(["morning", "noon", "evening", "night"], self.destructure_taken()))

    def __str__(self):
        # For debugging purposes
        return f"{self.name} {self.amount}[{self.unit}]\t{'\t-\t'.join(self.taken) if self.taken else ''}"


def extract_medication_strings(pre_match: str) -> list[str]:
    """Finds a comma separated list in lines of pre_match, ignores first line."""

    return [medication.strip()
            for meds in pre_match.splitlines()[1:]
            for medication in meds.split(",")]


def extract_medication_objects(pre_match: str) -> list[Medication]:
    """
    Finds medication notation in each line of pre_match searching for
        <name> <dosage> <unit> <0-1-1(-0)>
    If no match for the pattern could be matched, the whole string is saved as the name property of Medication.
    """

    medication_pattern: re.Pattern = re.compile(
        r"([a-zA-Z)(\d\s\-]*?)\s+([\d,./]+)\s*(.*?)\s+([\d\s,./]+(?:-[\d\s,./]+)+)")
    medication: list[Medication] = []

    for line in pre_match.splitlines()[1:]:
        if meds := medication_pattern.search(line):
            medication.append(Medication(meds.group(1), meds.group(2), meds.group(3),
                                         list(map(lambda s: s.strip(), meds.group(4).split("-")))))
            continue

        medication.append(Medication(line))

    return medication

