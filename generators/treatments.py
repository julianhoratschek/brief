from loaders.patient import Patient


class Treatments:
    """
    Generates list of doctors and other specialist a patient has frequented. This class is meant to be used
    to ease transfer from an analog paper questionnaire.
    """

    # List of all specialists in order of analog questionnaire. The following elements will be omitted:
    #   - Krankenschwester
    doctor_list: list[str] = [
        "Akupunktur", "Allgemeinmedizin", "Apotheker", "Versorgung durch Bademeister", "Chiropraxie",
        "Endokrinologie", "Besuche beim Geistheiler", "Dermatologie", "Hypnosen", "Pädiatrie",
        "Krankenschwester", "Massagen", "naturheilkundliche Behandlungen", "Neurologie", "Onkologie",
        "Proktologie", "Psychiatrie", "Psychotherapie", "Rheumatologie", "Urologie",
        "Allergologie", "Anästhesiologie", "Ophthalmologie", "Kardiologie", "Chirurgie",
        "Gynäkologie", "HNO-Heilkunde", "Besuche beim Heilpraktiker", "Internist", "Physiotherapie",
        "Pulmologie", "MKG-Chirurgie", "Nervenarzt", "Neurochirurgie", "Orthopädie",
        "Priesterkonsultation", "Dipl.-Psychologe", "Radiologie", "Schmerztherapie", "Zahnheilkunde"
    ]

    # List of indices of medical professions in doctor_list
    medical_idx: list[int] = [1, 2, 5, 7, 9, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 28, 30, 31, 32,
                              33, 34, 36, 37, 38, 39]

    # List of indices of non medical professions in doctor_list
    alt_medicine_idx: list[int] = [0, 3, 4, 6, 8, 12, 27, 35]

    def __init__(self, choices: list[bool]):
        """Translates checklist choices into text to insert into finished letter."""

        # Only assign if a valid list was submitted
        if len(choices) != len(Treatments.doctor_list):
            doctors = ""
            alternatives = ""
            physio = ""

        else:
            doctors = ("Die bisherige Behandlung erfolgte bei Ärzten mit der Fach- bzw. Zusatzbezeichnung "
                       + ", ".join([Treatments.doctor_list[idx]
                                    for idx in Treatments.medical_idx if choices[idx]]))

            alternatives = ("Alternativmedizinische Behandlungsversuche umfassten "
                            + ", ".join([Treatments.doctor_list[idx]
                                         for idx in Treatments.alt_medicine_idx if choices[idx]]))

            physio = ("Zudem betätigte {pat_nom} sich regelmäßig sportlich, erhielt "
                      + " und ".join([Treatments.doctor_list[idx]
                                      for idx in (29, 11) if choices[idx]])) if choices[11] or choices[29] else ""

        self.doctors: str = doctors
        self.alternatives: str = alternatives
        self.physio: str = physio

        self.acute_medication: str = ""
        self.basis_medication: str = ""

    def set_medication(self, patient: Patient):
        """Generate insert text from medication loaded by patient."""

        self.basis_medication = ("Versuche einer Kopfschmerzprophylaxe waren leitliniengerecht mit "
                                 + ", ".join(patient.former_basis_medication)
                                 + " unternommen worden")

        self.acute_medication = ("Zur Akutschmerzmedikation kamen "
                                 + ", ".join(patient.former_acute_medication)
                                 + " zum Einsatz")

    def valid(self) -> bool:
        """Simple helper function to increase readability"""

        return self.doctors != ""

    def __str__(self):
        return f"{self.doctors}. {self.basis_medication}. {self.acute_medication}. {self.alternatives}. {self.physio}."

