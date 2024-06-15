class Treatments:
    doctor_list: list[str] = [
        "Akupunktur", "Allgemeinmedizin", "Apotheker", "Bademeister", "Chiropraktiker",
        "Endokrinologie", "Geistheiler", "Dermatologie", "Hypnotiseur", "Pädiatrie",
        "Krankenschwester", "Masseur", "Naturheilkundler", "Neurologie", "Onkologie",
        "Proktologie", "Psychiatrie", "Psychotherapie", "Rheumatologie", "Urologie",
        "Allergologie", "Anästhesiologie", "Ophthalmologie", "Kardiologie", "Chirurgie",
        "Gynäkologie", "HNO-Heilkunde", "Heilpraktiker", "Internist", "Physiotherapeut",
        "Pulmologie", "MKG-Chirurgie", "Nervenarzt", "Neurochirurgie", "Orthopädie",
        "Priester", "Dipl.-Psychologe", "Radiologie", "Schmerztherapie", "Zahnheilkunde"
    ]

    medical_idx: list[int] = [1, 2, 5, 7, 9, 10, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 28, 30, 31, 32,
                              33, 34, 36, 37, 38, 39]

    alt_medicine_idx: list[int] = [0, 3, 4, 6, 8, 12, 27, 35]

    def __init__(self, doctors, alternatives, physio):
        self.doctors: str = doctors
        self.alternatives: str = alternatives
        self.physio: str = physio

    @classmethod
    def build(cls, choices: list[bool]):
        if len(choices) != len(cls.doctor_list):
            return cls("", "", "")

        return cls(
            "Die bisherige Behandlung erfolgte bei Ärzten mit der Fach- bzw. Zusatzbezeichnung "
            + ", ".join([cls.doctor_list[idx] for idx in cls.medical_idx if choices[idx]]),

            "Alternativmedizinische Behandlungsversuche umfassten "
            + ", ".join([cls.doctor_list[idx] for idx in cls.alt_medicine_idx if choices[idx]]),

            "{pat_nom} erhielt " + "und ".join([cls.doctor_list[idx] for idx in (29, 11) if choices[idx]])
            if choices[11] or choices[29] else ""
        )